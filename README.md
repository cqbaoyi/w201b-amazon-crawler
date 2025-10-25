# Amazon Crawler

A lightweight Python web crawler for learning Amazon data extraction.

## Features

- Search Amazon products by keywords
- Extract top product details (title, price, rating, reviews)
- Filter products by rating
- Crawl review content
- Handle authentication and maintain persistent login
- Respect robots.txt compliance
- Rate limiting and ethical crawling practices

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install
```

## Usage

```python
from src.crawler import AmazonCrawler

# Initialize crawler
crawler = AmazonCrawler(delay=2.0)

# Search for products
products = crawler.crawl_products(
    keyword="wireless headphones",
    min_rating=4.0,
    max_results=3
)

# Save results
crawler.storage.save_products(products)
```

## Project Structure

```
├── src/
│   ├── __init__.py
│   ├── crawler.py      # Main crawler class
│   ├── search.py       # Product search functionality
│   ├── parser.py       # HTML parsing utilities
│   ├── auth.py         # Authentication and session management
│   ├── robots.py       # Robots.txt compliance
│   └── storage.py      # Data storage utilities
├── data/               # Output data directory
├── main.py             # Example usage
├── config.py           # Configuration settings
└── requirements.txt    # Dependencies
```

## Ethical Considerations

- Always respects robots.txt
- Implements rate limiting (2+ second delays)
- Uses proper User-Agent headers
- Handles errors gracefully
- For educational purposes only