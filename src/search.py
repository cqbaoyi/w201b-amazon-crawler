"""
Amazon product search functionality.
Handles keyword-based product searches and result parsing.
"""

from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import logging

logger = logging.getLogger(__name__)


class AmazonSearcher:
    """Handles Amazon product searches."""
    
    def __init__(self, session: requests.Session):
        self.session = session
        self.base_url = "https://www.amazon.com"
        
    def search_products(self, keyword: str, max_results: int = 3) -> List[Dict]:
        """
        Search for products by keyword and return top results.
        
        Args:
            keyword: Search term
            max_results: Maximum number of results to return
            
        Returns:
            List of product dictionaries
        """
        logger.info(f"Searching Amazon for: {keyword}")
        
        try:
            # Construct Amazon search URL
            search_url = f"{self.base_url}/s?k={keyword.replace(' ', '+')}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            
            # Add a small delay to be respectful
            time.sleep(1)
            
            response = self.session.get(search_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            return self._parse_search_results(soup, max_results)
            
        except requests.RequestException as e:
            logger.error(f"Error searching Amazon: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error during search: {e}")
            return []
    
    def _parse_search_results(self, soup: BeautifulSoup, max_results: int) -> List[Dict]:
        """Parse Amazon search results from HTML."""
        products = []
        
        # Find product containers - Amazon uses different selectors
        product_selectors = [
            'div[data-component-type="s-search-result"]',
            '.s-result-item',
            '[data-asin]'
        ]
        
        product_elements = []
        for selector in product_selectors:
            elements = soup.select(selector)
            if elements:
                product_elements = elements
                break
        
        logger.info(f"Found {len(product_elements)} product elements")
        
        for element in product_elements[:max_results]:
            try:
                product = self._extract_product_info(element)
                if product:
                    products.append(product)
            except Exception as e:
                logger.warning(f"Error parsing product element: {e}")
                continue
        
        return products
    
    def _extract_product_info(self, element) -> Optional[Dict]:
        """Extract product information from a single product element."""
        try:
            # Extract title
            title_selectors = [
                'h2 a span',
                '.s-size-mini .s-color-base',
                '[data-cy="title-recipe-title"]',
                'h2 span'
            ]
            title = self._extract_text_by_selectors(element, title_selectors)
            
            # Extract price
            price_selectors = [
                '.a-price-whole',
                '.a-price .a-offscreen',
                '.a-price-range',
                '.a-price-symbol'
            ]
            price = self._extract_text_by_selectors(element, price_selectors)
            
            # Extract rating
            rating_selectors = [
                '.a-icon-alt',
                '.a-icon-star-small .a-icon-alt',
                '[aria-label*="stars"]'
            ]
            rating_text = self._extract_text_by_selectors(element, rating_selectors)
            rating = self._parse_rating(rating_text)
            
            # Extract review count
            review_selectors = [
                '.a-size-base',
                '[aria-label*="ratings"]',
                '.a-link-normal'
            ]
            review_count = self._extract_review_count(element, review_selectors)
            
            # Extract URL
            url_element = element.find('a', href=True)
            url = urljoin(self.base_url, url_element['href']) if url_element else None
            
            # Only return if we have at least a title
            if title:
                return {
                    'title': title.strip(),
                    'price': price.strip() if price else 'N/A',
                    'rating': rating,
                    'reviews_count': review_count,
                    'url': url
                }
            
        except Exception as e:
            logger.warning(f"Error extracting product info: {e}")
        
        return None
    
    def _extract_text_by_selectors(self, element, selectors: List[str]) -> str:
        """Try multiple selectors to extract text."""
        for selector in selectors:
            try:
                found = element.select_one(selector)
                if found and found.get_text(strip=True):
                    return found.get_text(strip=True)
            except:
                continue
        return ""
    
    def _parse_rating(self, rating_text: str) -> float:
        """Parse rating from text like '4.5 out of 5 stars'."""
        if not rating_text:
            return 0.0
        
        try:
            # Extract number from text like "4.5 out of 5 stars"
            import re
            numbers = re.findall(r'\d+\.?\d*', rating_text)
            if numbers:
                return float(numbers[0])
        except:
            pass
        return 0.0
    
    def _extract_review_count(self, element, selectors: List[str]) -> int:
        """Extract review count from element."""
        for selector in selectors:
            try:
                found = element.select_one(selector)
                if found:
                    text = found.get_text(strip=True)
                    # Extract number from text like "1,234 ratings"
                    import re
                    numbers = re.findall(r'[\d,]+', text)
                    if numbers:
                        return int(numbers[0].replace(',', ''))
            except:
                continue
        return 0
