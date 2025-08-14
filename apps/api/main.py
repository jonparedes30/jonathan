from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hashlib
import time
import os
from datetime import datetime, timedelta
from typing import Optional, List
import secrets
import sys
sys.path.append('../../packages')
from connectors.skimlinks_connector import SkimlinksConnector

app = FastAPI(title="La Ventanita API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3100"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBasic()

def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, os.getenv("ADMIN_USERNAME", "admin"))
    correct_password = secrets.compare_digest(credentials.password, os.getenv("ADMIN_PASSWORD", "admin123"))
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Models
class ClickIn(BaseModel):
    product_id: int
    session_id: str

class SearchStats(BaseModel):
    total_searches: int
    total_clicks: int
    total_products: int
    ctr: float
    estimated_earnings: float

# Initialize Skimlinks connector
skimlinks = SkimlinksConnector(
    site_id=os.getenv("SKIMLINKS_SITE_ID", "123456"),
    pub_code=os.getenv("SKIMLINKS_PUB_CODE", "789012")
)

# Mock data storage (replace with real DB)
mock_data = {
    "searches": [],
    "clicks": [],
    "products": [],
    "stores": skimlinks.get_supported_stores()
}

@app.get("/api/health")
def health():
    return {"status": "ok", "uptime": int(time.time())}

@app.get("/api/search")
def search(q: str = "", cat: Optional[str] = None, page: int = 1, page_size: int = 24):
    if not q.strip():
        return {"page": page, "page_size": page_size, "total": 0, "items": []}
    
    # Get results from Skimlinks
    results = skimlinks.search(q, cat, page, page_size)
    
    # Log search
    mock_data["searches"].append({
        "query": q,
        "category": cat,
        "timestamp": datetime.now(),
        "results_count": len(results)
    })
    
    # Store products for click tracking
    items = []
    for i, result in enumerate(results):
        product_id = len(mock_data["products"]) + i + 1
        mock_data["products"].append({
            "id": product_id,
            "title": result.title,
            "price": result.price_amount,
            "merchant": result.merchant_name,
            "source_url": result.source_url,
            "image": result.image,
            "rating": result.rating,
            "shipping": result.shipping_text
        })
        
        items.append({
            "id": product_id,
            "title": result.title,
            "image": result.image,
            "price": {"amount": result.price_amount, "currency": result.currency},
            "merchant": {"name": result.merchant_name},
            "rating": result.rating,
            "shipping": result.shipping_text,
            "affiliate_preview": True
        })
    
    return {
        "page": page,
        "page_size": page_size,
        "total": len(results),
        "items": items
    }

@app.get("/api/product/{pid}")
def product(pid: int):
    product = next((p for p in mock_data["products"] if p["id"] == pid), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/api/click")
def click(c: ClickIn, request: Request):
    ip = request.client.host or "0.0.0.0"
    ip_hash = hashlib.sha256(ip.encode()).hexdigest()
    
    # Find product
    product = next((p for p in mock_data["products"] if p["id"] == c.product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Generate affiliate URL
    affiliate_url = skimlinks.to_affiliate(product["source_url"])
    
    # Log click
    mock_data["clicks"].append({
        "product_id": c.product_id,
        "session_id": c.session_id,
        "ip_hash": ip_hash,
        "merchant": product["merchant"],
        "price": product["price"],
        "timestamp": datetime.now()
    })
    
    return {"redirect_url": affiliate_url}

# Admin Panel Endpoints
@app.get("/api/admin/stats")
def get_stats(admin: str = Depends(verify_admin)):
    total_searches = len(mock_data["searches"])
    total_clicks = len(mock_data["clicks"])
    total_products = len(mock_data["products"])
    ctr = (total_clicks / total_searches * 100) if total_searches > 0 else 0
    
    # Estimate earnings based on actual click data
    estimated_earnings = 0
    for click in mock_data["clicks"]:
        price = click.get("price", 50.0)
        commission_rate = 0.05  # 5% average
        estimated_earnings += price * commission_rate * 0.15  # 15% conversion rate
    
    return SearchStats(
        total_searches=total_searches,
        total_clicks=total_clicks,
        total_products=total_products,
        ctr=round(ctr, 2),
        estimated_earnings=round(estimated_earnings, 2)
    )

@app.get("/api/admin/recent-activity")
def get_recent_activity(admin: str = Depends(verify_admin)):
    recent_searches = sorted(mock_data["searches"], key=lambda x: x["timestamp"], reverse=True)[:10]
    recent_clicks = sorted(mock_data["clicks"], key=lambda x: x["timestamp"], reverse=True)[:10]
    
    return {
        "recent_searches": recent_searches,
        "recent_clicks": recent_clicks
    }

@app.get("/api/admin/daily-stats")
def get_daily_stats(admin: str = Depends(verify_admin)):
    # Mock daily data for the last 7 days
    today = datetime.now().date()
    daily_stats = []
    
    for i in range(7):
        date = today - timedelta(days=i)
        # Mock data - replace with real DB queries
        daily_stats.append({
            "date": date.isoformat(),
            "searches": max(0, 50 - i * 5),
            "clicks": max(0, 15 - i * 2),
            "estimated_earnings": max(0, 25.50 - i * 3.2)
        })
    
    return {"daily_stats": list(reversed(daily_stats))}

@app.get("/api/admin/stores")
def get_stores(admin: str = Depends(verify_admin)):
    """Get supported stores information"""
    return {
        "network": "Skimlinks",
        "total_stores": len(mock_data["stores"]),
        "stores": mock_data["stores"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8090)