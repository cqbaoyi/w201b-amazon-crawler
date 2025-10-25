"""
HTML parsing utilities for Amazon pages.
Handles product details, reviews, and rating extraction.
"""

from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import re
import logging

logger = logging.getLogger(__name__)


class AmazonParser:
    """Parses Amazon HTML content for product information."""
    
    @staticmethod
    def parse_product_details(soup: BeautifulSoup) -> Dict:
        """Extract product details from product page."""
        # Implementation will go here
        pass
    
    @staticmethod
    def parse_reviews(soup: BeautifulSoup) -> List[Dict]:
        """Extract review information from reviews section."""
        reviews = []
        
        # Find review containers - Amazon uses different selectors for reviews
        review_selectors = [
            '[data-hook="review"]',
            'div[data-hook="review"]',
            '.a-section[data-hook="review"]',
            '.cr-original-review-item',
            '.a-section.cr-original-review-item',
            '.a-section.a-spacing-small.review',
            '.a-section.review',
            '.review',
            '[id*="customer-review"]',
            '.a-section.a-spacing-none.review'
        ]
        
        review_elements = []
        for selector in review_selectors:
            elements = soup.select(selector)
            if elements:
                review_elements = elements
                break
        
        logger.info(f"Found {len(review_elements)} review elements")
        
        
        for element in review_elements:
            try:
                review = AmazonParser._extract_single_review(element)
                if review:
                    reviews.append(review)
            except Exception as e:
                logger.warning(f"Error parsing review element: {e}")
                continue
        
        return reviews
    
    @staticmethod
    def _extract_single_review(element) -> Optional[Dict]:
        """Extract information from a single review element."""
        try:
            # Extract reviewer name
            name_selectors = [
                '.a-profile-name',
                '[data-hook="review-author"]',
                '.review-byline .author'
            ]
            reviewer_name = AmazonParser._extract_text_by_selectors(element, name_selectors)
            
            # Extract rating
            rating_selectors = [
                '.a-icon-alt',
                '[data-hook="review-star-rating"] .a-icon-alt',
                '.a-star-rating .a-icon-alt'
            ]
            rating_text = AmazonParser._extract_text_by_selectors(element, rating_selectors)
            rating = AmazonParser._parse_rating_from_text(rating_text)
            
            # Extract review title
            title_selectors = [
                '[data-hook="review-title"]',
                '.review-title',
                'h3'
            ]
            review_title = AmazonParser._extract_text_by_selectors(element, title_selectors)
            
            # Extract review text
            text_selectors = [
                '[data-hook="review-body"]',
                '.review-text',
                '.a-expander-content'
            ]
            review_text = AmazonParser._extract_text_by_selectors(element, text_selectors)
            
            # Extract date
            date_selectors = [
                '[data-hook="review-date"]',
                '.review-date',
                '.a-size-base.a-color-secondary'
            ]
            review_date = AmazonParser._extract_text_by_selectors(element, date_selectors)
            
            # Extract helpful votes
            helpful_selectors = [
                '[data-hook="helpful-vote-statement"]',
                '.a-size-base.a-color-tertiary'
            ]
            helpful_text = AmazonParser._extract_text_by_selectors(element, helpful_selectors)
            helpful_votes = AmazonParser._parse_helpful_votes(helpful_text)
            
            if review_text:  # Only return if we have review text
                return {
                    'reviewer_name': reviewer_name.strip() if reviewer_name else 'Anonymous',
                    'rating': rating,
                    'title': review_title.strip() if review_title else '',
                    'text': review_text.strip(),
                    'date': review_date.strip() if review_date else '',
                    'helpful_votes': helpful_votes
                }
                
        except Exception as e:
            logger.warning(f"Error extracting review: {e}")
        
        return None
    
    @staticmethod
    def _extract_text_by_selectors(element, selectors: List[str]) -> str:
        """Try multiple selectors to extract text."""
        for selector in selectors:
            try:
                found = element.select_one(selector)
                if found and found.get_text(strip=True):
                    return found.get_text(strip=True)
            except:
                continue
        return ""
    
    @staticmethod
    def _parse_rating_from_text(rating_text: str) -> float:
        """Parse rating from text like '4.0 out of 5 stars'."""
        if not rating_text:
            return 0.0
        
        try:
            import re
            numbers = re.findall(r'\d+\.?\d*', rating_text)
            if numbers:
                return float(numbers[0])
        except:
            pass
        return 0.0
    
    @staticmethod
    def _parse_helpful_votes(helpful_text: str) -> int:
        """Parse helpful votes from text like '15 people found this helpful'."""
        if not helpful_text:
            return 0
        
        try:
            import re
            numbers = re.findall(r'\d+', helpful_text)
            if numbers:
                return int(numbers[0])
        except:
            pass
        return 0
    
    @staticmethod
    def filter_by_rating(products: List[Dict], min_rating: float) -> List[Dict]:
        """Filter products by minimum rating."""
        filtered = []
        for product in products:
            if product.get('rating', 0) >= min_rating:
                filtered.append(product)
        return filtered
