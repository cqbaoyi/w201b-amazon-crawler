"""
Data storage utilities.
Handles saving and loading of crawled data.
"""

import json
import csv
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)


class DataStorage:
    """Handles data storage and retrieval."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def save_products(self, products: List[Dict], filename: Optional[str] = None) -> str:
        """Save products to JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"products_{timestamp}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(products)} products to {filepath}")
        return filepath
    
    def save_reviews(self, reviews: List[Dict], filename: Optional[str] = None) -> str:
        """Save reviews to JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reviews_{timestamp}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(reviews, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(reviews)} reviews to {filepath}")
        return filepath
    
    def export_to_csv(self, data: List[Dict], filename: str) -> str:
        """Export data to CSV format."""
        if not data:
            return ""
        
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        
        logger.info(f"Exported data to {filepath}")
        return filepath
