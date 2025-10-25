"""
Main crawler class that orchestrates the entire crawling process.
Combines search, parsing, authentication, and storage functionality.
"""

from typing import List, Dict, Optional
import time
import logging
from src.search import AmazonSearcher
from src.parser import AmazonParser
from src.auth import AmazonAuth
from src.robots import RobotsChecker
from src.storage import DataStorage

logger = logging.getLogger(__name__)


class AmazonCrawler:
    """Main crawler class for Amazon data extraction."""
    
    def __init__(self, delay: float = 2.0):
        self.delay = delay
        self.auth = AmazonAuth()
        self.robots_checker = RobotsChecker()
        self.storage = DataStorage()
        self.parser = AmazonParser()
        
        # Initialize session with authentication
        self.searcher = AmazonSearcher(self.auth.session)
    
    def crawl_products(self, keyword: str, min_rating: float = 0.0, 
                      max_results: int = 3) -> List[Dict]:
        """
        Main crawling method that searches and extracts product data.
        
        Args:
            keyword: Search term
            min_rating: Minimum rating filter
            max_results: Maximum number of products to return
            
        Returns:
            List of product dictionaries with details
        """
        logger.info(f"Starting crawl for keyword: {keyword}")
        
        # Check robots.txt compliance
        if not self.robots_checker.can_crawl("/s"):
            logger.warning("Robots.txt disallows crawling search results")
            return []
        
        # Search for products
        products = self.searcher.search_products(keyword, max_results)
        
        # Filter by rating if specified
        if min_rating > 0:
            products = self.parser.filter_by_rating(products, min_rating)
        
        # Add delay between requests
        time.sleep(self.delay)
        
        logger.info(f"Found {len(products)} products")
        return products
    
    def crawl_reviews(self, product_url: str, max_reviews: int = 50) -> List[Dict]:
        """
        Crawl reviews for a specific product.
        
        Args:
            product_url: URL of the product
            max_reviews: Maximum number of reviews to crawl
            
        Returns:
            List of review dictionaries
        """
        # Implementation will go here
        pass
