from typing import Protocol, NamedTuple, Optional, List
from abc import ABC, abstractmethod

class SearchResult(NamedTuple):
    title: str
    image: str
    price_amount: float
    currency: str
    source_url: str
    shipping_text: Optional[str]
    rating: Optional[float]
    merchant_name: str
    return_policy_url: Optional[str]
    source_sku: Optional[str]

class Connector(Protocol):
    """Base interface for all affiliate connectors"""
    
    @abstractmethod
    def search(self, q: str, cat: Optional[str], page: int, page_size: int) -> List[SearchResult]:
        """Search for products"""
        pass
    
    @abstractmethod
    def product(self, source_id: str) -> SearchResult:
        """Get single product details"""
        pass
    
    @abstractmethod
    def to_affiliate(self, source_url: str) -> str:
        """Convert source URL to affiliate URL"""
        pass

class BaseConnector(ABC):
    """Base implementation with common functionality"""
    
    def __init__(self, merchant_name: str, commission_rate: float = 0.05):
        self.merchant_name = merchant_name
        self.commission_rate = commission_rate
    
    def normalize_price(self, price_str: str) -> float:
        """Extract numeric price from string"""
        import re
        price_match = re.search(r'[\d,]+\.?\d*', price_str.replace(',', ''))
        return float(price_match.group()) if price_match else 0.0
    
    def build_search_result(self, **kwargs) -> SearchResult:
        """Helper to build SearchResult with defaults"""
        return SearchResult(
            title=kwargs.get('title', ''),
            image=kwargs.get('image', ''),
            price_amount=kwargs.get('price_amount', 0.0),
            currency=kwargs.get('currency', 'USD'),
            source_url=kwargs.get('source_url', ''),
            shipping_text=kwargs.get('shipping_text'),
            rating=kwargs.get('rating'),
            merchant_name=self.merchant_name,
            return_policy_url=kwargs.get('return_policy_url'),
            source_sku=kwargs.get('source_sku')
        )