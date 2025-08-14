#!/usr/bin/env python3
import requests
import json
import time
import os
from datetime import datetime

# Configuration
QUERIES = [
    "iPhone 15 Pro Max",
    "Samsung Galaxy S24",
    "MacBook Air M3",
    "AirPods Pro",
    "Nintendo Switch",
    "Sony WH-1000XM5",
    "iPad Pro",
    "Apple Watch Series 9",
    "Dell XPS 13",
    "Nike Air Max"
]

PER_QUERY_LIMIT = 6
GLOBAL_MAX = 50
EBAY_SITE = os.getenv('EBAY_SITE', 'EBAY_US')

def get_ebay_token():
    """Get eBay OAuth token"""
    client_id = os.getenv('EBAY_CLIENT_ID')
    client_secret = os.getenv('EBAY_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        raise ValueError("eBay credentials not found in environment variables")
    
    url = "https://api.ebay.com/identity/v1/oauth2/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {requests.auth._basic_auth_str(client_id, client_secret)}'
    }
    data = {
        'grant_type': 'client_credentials',
        'scope': 'https://api.ebayapis.com/oauth/api_scope'
    }
    
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()['access_token']

def search_ebay_products(token, query, limit=6, ship_to="EC"):
    """Search eBay for products that ship to Ecuador"""
    url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
    headers = {
        'Authorization': f'Bearer {token}',
        'X-EBAY-C-MARKETPLACE-ID': EBAY_SITE,
        'X-EBAY-C-ENDUSERCTX': 'contextualLocation=country%3DEC'
    }
    params = {
        'q': query,
        'limit': limit,
        'sort': 'price',
        'filter': f'conditionIds:{{1000|1500|2000|2500|3000|4000|5000}},deliveryCountry:{ship_to}',
        'fieldgroups': 'MATCHING_ITEMS,EXTENDED'
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def normalize_product(item, category="Electronics"):
    """Normalize eBay item to our format"""
    try:
        # Get price
        price = 0
        if 'price' in item and 'value' in item['price']:
            price = float(item['price']['value'])
        
        # Get image
        image = "https://via.placeholder.com/400x400?text=Product"
        if 'image' in item:
            image = item['image']['imageUrl']
        elif 'thumbnailImages' in item and item['thumbnailImages']:
            image = item['thumbnailImages'][0]['imageUrl']
        
        # Get shipping info for Ecuador
        shipping = "Envía a Ecuador"
        shipping_cost = None
        eta = None
        
        if 'shippingOptions' in item and item['shippingOptions']:
            shipping_option = item['shippingOptions'][0]
            
            # Get shipping cost
            if 'shippingCost' in shipping_option and shipping_option['shippingCost']:
                cost_value = shipping_option['shippingCost'].get('value', '0')
                if float(cost_value) == 0:
                    shipping = "Envío gratis a Ecuador"
                else:
                    shipping_cost = float(cost_value)
                    shipping = f"Envío a Ecuador: ${shipping_cost:.2f}"
            
            # Get delivery estimate
            if 'minEstimatedDeliveryDate' in shipping_option and 'maxEstimatedDeliveryDate' in shipping_option:
                from datetime import datetime
                min_date = datetime.fromisoformat(shipping_option['minEstimatedDeliveryDate'].replace('Z', '+00:00'))
                max_date = datetime.fromisoformat(shipping_option['maxEstimatedDeliveryDate'].replace('Z', '+00:00'))
                eta = f"ETA: {min_date.strftime('%d/%m')}-{max_date.strftime('%d/%m')}"
                shipping += f" | {eta}"
        
        return {
            "id": item.get('itemId', ''),
            "title": item.get('title', 'Product'),
            "price": price,
            "merchant": "eBay",
            "category": category,
            "image": image,
            "rating": 4.5,  # Default rating
            "shipping": shipping,
            "url": item.get('itemWebUrl', ''),
            "location": item.get('itemLocation', {}).get('country', 'US'),
            "ships_to_ecuador": True,
            "shipping_cost": shipping_cost,
            "eta": eta
        }
    except Exception as e:
        print(f"Error normalizing product: {e}")
        return None

def build_catalog():
    """Build product catalog from eBay"""
    print("🔄 Building product catalog...")
    
    try:
        token = get_ebay_token()
        print("✅ eBay token obtained")
    except Exception as e:
        print(f"❌ Error getting eBay token: {e}")
        return False
    
    all_products = []
    
    for i, query in enumerate(QUERIES):
        if len(all_products) >= GLOBAL_MAX:
            break
            
        print(f"🔍 Searching: {query} ({i+1}/{len(QUERIES)})")
        
        try:
            results = search_ebay_products(token, query, PER_QUERY_LIMIT)
            
            if 'itemSummaries' in results:
                for item in results['itemSummaries']:
                    if len(all_products) >= GLOBAL_MAX:
                        break
                        
                    product = normalize_product(item)
                    if product and product['price'] > 0:
                        all_products.append(product)
            
            # Rate limiting
            time.sleep(1)
            
        except Exception as e:
            print(f"⚠️ Error searching {query}: {e}")
            continue
    
    # Save to JSON
    catalog_data = {
        "products": all_products,
        "generated_at": datetime.now().isoformat(),
        "total_products": len(all_products),
        "source": "eBay API"
    }
    
    os.makedirs('data', exist_ok=True)
    with open('data/products.json', 'w', encoding='utf-8') as f:
        json.dump(all_products, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Catalog built: {len(all_products)} products saved")
    return True

if __name__ == "__main__":
    success = build_catalog()
    exit(0 if success else 1)