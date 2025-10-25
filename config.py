"""
Configuration settings for the Amazon crawler.
"""

# Crawler settings
CRAWL_DELAY = 2.0  # Seconds between requests
MAX_RETRIES = 3
TIMEOUT = 30

# User agent for requests
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# File paths
DATA_DIR = "data"
COOKIES_FILE = "cookies.json"
LOG_FILE = "crawler.log"

# Amazon URLs
AMAZON_BASE_URL = "https://www.amazon.com"
AMAZON_LOGIN_URL = "https://www.amazon.com/ap/signin"

# Rate limiting
REQUESTS_PER_MINUTE = 30
