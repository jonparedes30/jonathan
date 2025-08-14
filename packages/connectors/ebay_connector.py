import requests
from typing import List, Optional
from .base import BaseConnector, SearchResult
import os

class EbayConnector(BaseConnector):
    """eBay Browse API connector"""
    
    def __init__(self, app_id: str, affiliate_tag: Optional[str] = None):
        super().__init__("eBay", 0.03)  # 3% commission rate
        self.app_id = app_id
        self.affiliate_tag = affiliate_tag
        self.base_url = "https://api.ebay.com/buy/browse/v1"
        self.access_token = None
    
    def _get_access_token(self) -> str:
        """Get OAuth token for eBay API"""
        if self.access_token:
            return self.access_token
            
        # Mock token for development
        self.access_token = "mock_token_" + self.app_id
        return self.access_token
    
    def search(self, q: str, cat: Optional[str], page: int, page_size: int) -> List[SearchResult]:
        """Search eBay products"""
        # Mock implementation - replace with real API calls
        mock_results = [
            self.build_search_result(
                title=f"eBay Product: {q} - Item {i}",
                image="https://via.placeholder.com/300x300",
                price_amount=29.99 + i * 10,
                currency="USD",
                source_url=f"https://ebay.com/itm/mock-{i}",
                shipping_text="Free shipping",
                rating=4.2 + (i * 0.1),
                source_sku=f"ebay-{i}"
            ) for i in range(1, min(page_size + 1, 6))
        ]
        return mock_results
    
    def product(self, source_id: str) -> SearchResult:
        """Get single eBay product"""
        return self.build_search_result(
            title=f"eBay Product Details - {source_id}",
            image="https://via.placeholder.com/600x600",
            price_amount=49.99,
            currency="USD",
            source_url=f"https://ebay.com/itm/{source_id}",
            shipping_text="Free shipping",
            rating=4.5,
            source_sku=source_id,
            return_policy_url="https://ebay.com/help/policies/returns"
        )
    
    def to_affiliate(self, source_url: str) -> str:
        """Convert to eBay affiliate URL"""
        if self.affiliate_tag:
            # Direct eBay affiliate link
            return f"{source_url}?mkcid=1&mkrid=711-53200-19255-0&siteid=0&campid={self.affiliate_tag}"
        else:
            # Use aggregator (Skimlinks/Sovrn)
            return f"https://go.skimresources.com/?id={os.getenv('SKIMLINKS_SITE_ID')}&url={source_url}"