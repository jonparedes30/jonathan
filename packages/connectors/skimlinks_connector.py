import requests
from typing import List, Optional
from .base import BaseConnector, SearchResult
import os
import random

class SkimlinksConnector(BaseConnector):
    """Skimlinks universal affiliate connector"""
    
    def __init__(self, site_id: str, pub_code: str):
        super().__init__("Skimlinks Network", 0.05)
        self.site_id = site_id
        self.pub_code = pub_code
        self.base_url = "https://go.skimresources.com"
        
        # Mock stores data
        self.mock_stores = [
            {"name": "Best Buy", "domain": "bestbuy.com", "commission": 0.04},
            {"name": "Target", "domain": "target.com", "commission": 0.03},
            {"name": "Walmart", "domain": "walmart.com", "commission": 0.025},
            {"name": "Home Depot", "domain": "homedepot.com", "commission": 0.035},
            {"name": "Macy's", "domain": "macys.com", "commission": 0.06},
            {"name": "Nike", "domain": "nike.com", "commission": 0.08},
            {"name": "Adidas", "domain": "adidas.com", "commission": 0.07},
            {"name": "Samsung", "domain": "samsung.com", "commission": 0.045}
        ]
    
    def search(self, q: str, cat: Optional[str], page: int, page_size: int) -> List[SearchResult]:
        """Search across Skimlinks network stores"""
        results = []
        
        # Generate mock results from different stores
        for i in range(min(page_size, 12)):
            store = random.choice(self.mock_stores)
            price = round(random.uniform(19.99, 299.99), 2)
            rating = round(random.uniform(3.5, 5.0), 1)
            
            result = self.build_search_result(
                title=f"{q} - {store['name']} Edition {i+1}",
                image=f"https://picsum.photos/300/300?random={i}",
                price_amount=price,
                currency="USD",
                source_url=f"https://{store['domain']}/product/{q.replace(' ', '-').lower()}-{i+1}",
                shipping_text="Free shipping on orders $35+" if price > 35 else "Standard shipping",
                rating=rating,
                merchant_name=store['name'],
                source_sku=f"skim-{store['domain']}-{i+1}",
                return_policy_url=f"https://{store['domain']}/returns"
            )
            results.append(result)
        
        return results
    
    def product(self, source_id: str) -> SearchResult:
        """Get single product from Skimlinks network"""
        store = random.choice(self.mock_stores)
        
        return self.build_search_result(
            title=f"Premium Product - {source_id}",
            image="https://picsum.photos/600/600?random=999",
            price_amount=89.99,
            currency="USD",
            source_url=f"https://{store['domain']}/product/{source_id}",
            shipping_text="Free 2-day shipping",
            rating=4.7,
            merchant_name=store['name'],
            source_sku=source_id,
            return_policy_url=f"https://{store['domain']}/returns"
        )
    
    def to_affiliate(self, source_url: str) -> str:
        """Convert to Skimlinks affiliate URL"""
        return f"{self.base_url}/?id={self.site_id}&url={source_url}"
    
    def get_supported_stores(self) -> List[dict]:
        """Get list of supported stores"""
        return self.mock_stores