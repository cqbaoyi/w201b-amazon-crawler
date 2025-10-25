"""
Robots.txt compliance checker.
Ensures crawler respects website robots.txt rules.
"""

import requests
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse
import logging

logger = logging.getLogger(__name__)


class RobotsChecker:
    """Checks robots.txt compliance before crawling."""
    
    def __init__(self, base_url: str = "https://www.amazon.com"):
        self.base_url = base_url
        self.robot_parser = RobotFileParser()
        
    def can_crawl(self, path: str, user_agent: str = "*") -> bool:
        """
        Check if crawling a specific path is allowed.
        
        Args:
            path: URL path to check
            user_agent: User agent string
            
        Returns:
            True if crawling is allowed
        """
        try:
            robots_url = urljoin(self.base_url, "/robots.txt")
            self.robot_parser.set_url(robots_url)
            self.robot_parser.read()
            return self.robot_parser.can_fetch(user_agent, path)
        except Exception as e:
            logger.warning(f"Could not check robots.txt: {e}")
            return True  # Default to allowing if check fails
