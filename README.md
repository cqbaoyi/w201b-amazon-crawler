# Amazon Product Crawler

A lightweight Python web crawler for Amazon product data extraction.

## Quick Start

```bash
pip install -r requirements.txt
playwright install
python main.py
```

## Features

- Search Amazon products by keywords
- Extract product details and customer reviews
- Authentication support for review access
- Save results to JSON files

## Project Structure

```
├── src/
│   ├── crawler.py      # Main crawler class
│   ├── search.py       # Product search functionality
│   ├── parser.py       # HTML parsing utilities
│   ├── auth.py         # Authentication and session management
│   ├── review_crawler.py # Review crawling
│   ├── robots.py       # Robots.txt compliance
│   └── storage.py      # Data storage utilities
├── data/               # Output data directory
├── main.py             # Entry point
└── requirements.txt    # Dependencies
```

## Usage

Follow the prompts to:
1. Enter search keyword
2. Set minimum rating filter
3. Choose number of results
4. Enable review crawling (requires authentication)
5. Set max review pages per product

Results are saved to `data/products_YYYYMMDD_HHMMSS.json`.