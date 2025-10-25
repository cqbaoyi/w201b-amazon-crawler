"""
Main entry point for the Amazon crawler.
Example usage and demonstration of the crawler functionality.
"""

import logging
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.crawler import AmazonCrawler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Main function demonstrating crawler usage."""
    
    # Get user input for search keyword
    print("Amazon Product Crawler")
    print("=" * 30)
    keyword = input("Enter search keyword: ").strip()
    
    if not keyword:
        print("No keyword provided. Exiting.")
        return
    
    # Get additional parameters from user
    try:
        min_rating = float(input("Enter minimum rating (0-5, default 4.0): ") or "4.0")
        max_results = int(input("Enter max results (default 3): ") or "3")
    except ValueError:
        print("Invalid input. Using defaults: min_rating=4.0, max_results=3")
        min_rating = 4.0
        max_results = 3
    
    print(f"\nSearching for: '{keyword}'")
    print(f"Minimum rating: {min_rating}")
    print(f"Max results: {max_results}")
    print("-" * 30)
    
    # Initialize crawler
    crawler = AmazonCrawler(delay=2.0)
    
    # Search for products
    products = crawler.crawl_products(
        keyword=keyword,
        min_rating=min_rating,
        max_results=max_results
    )
    
    # Save results
    if products:
        crawler.storage.save_products(products)
        print(f"Found {len(products)} products for '{keyword}'")
        
        # Display results
        for i, product in enumerate(products, 1):
            print(f"{i}. {product.get('title', 'N/A')}")
            print(f"   Rating: {product.get('rating', 'N/A')}")
            print(f"   Price: {product.get('price', 'N/A')}")
            print()

if __name__ == "__main__":
    main()
