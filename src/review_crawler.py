"""
Review crawling functionality with pagination support.
Handles crawling reviews from Amazon product pages.
"""

from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
import time
import logging
from urllib.parse import urljoin, urlparse, parse_qs
import re

logger = logging.getLogger(__name__)


class ReviewCrawler:
    """Handles crawling of Amazon product reviews with pagination."""
    
    def __init__(self, session: requests.Session):
        self.session = session
        self.base_url = "https://www.amazon.com"
        
    def crawl_product_reviews(self, product_url: str, max_pages: int = 2, 
                            max_reviews_per_page: int = 10) -> List[Dict]:
        """
        Crawl reviews for a specific product with pagination support.
        
        Args:
            product_url: URL of the Amazon product
            max_pages: Maximum number of review pages to crawl
            max_reviews_per_page: Maximum reviews per page
            
        Returns:
            List of review dictionaries
        """
        logger.info(f"Starting review crawl for product: {product_url}")
        
        all_reviews = []
        current_page = 1
        
        try:
            # Get the reviews URL for the product
            reviews_url = self._get_reviews_url(product_url)
            if not reviews_url:
                return []
            
            while current_page <= max_pages:
                # Construct paginated URL
                page_url = self._add_pagination_to_url(reviews_url, current_page)
                
                # Make request to reviews page
                reviews = self._crawl_reviews_page(page_url, max_reviews_per_page)
                
                if not reviews:
                    break
                
                all_reviews.extend(reviews)
                time.sleep(1)  # Delay between pages
                current_page += 1
                
        except Exception as e:
            logger.error(f"Error crawling reviews: {e}")
        
        return all_reviews
    
    def _get_reviews_url(self, product_url: str) -> Optional[str]:
        """Extract or construct the reviews URL from product URL."""
        asin = self._extract_asin_from_url(product_url)
        if asin:
            return f"{self.base_url}/product-reviews/{asin}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
        return None
    
    def _extract_asin_from_url(self, url: str) -> Optional[str]:
        """Extract ASIN from Amazon product URL."""
        patterns = [
            r'%2Fdp%2F([A-Z0-9]{10})',  # URL encoded (most common)
            r'/dp/([A-Z0-9]{10})',
            r'/product/([A-Z0-9]{10})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def _add_pagination_to_url(self, reviews_url: str, page: int) -> str:
        """Add pagination parameter to reviews URL."""
        if page <= 1:
            return reviews_url
        
        separator = '&' if '?' in reviews_url else '?'
        return f"{reviews_url}{separator}pageNumber={page}"
    
    def _crawl_reviews_page(self, reviews_url: str, max_reviews: int) -> List[Dict]:
        """Crawl reviews from a single reviews page."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            
            response = self.session.get(reviews_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            from src.parser import AmazonParser
            reviews = AmazonParser.parse_reviews(soup)
            
            return reviews[:max_reviews]
            
        except Exception as e:
            logger.error(f"Error crawling reviews page: {e}")
            return []
    
    
