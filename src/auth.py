"""
Authentication and session management for Amazon.
Handles login, cookie management, and persistent sessions.
"""

from typing import Optional, Dict
import requests
from playwright.sync_api import sync_playwright
import json
import os
import logging

logger = logging.getLogger(__name__)


class AmazonAuth:
    """Handles Amazon authentication and session management."""
    
    def __init__(self):
        self.session = requests.Session()
        self.cookies_file = "cookies.json"
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def authenticate(self) -> bool:
        """Authenticate with Amazon using Playwright."""
        print("\n🔐 Amazon Authentication")
        print("Choose authentication method:")
        print("1. Automatic")
        print("2. Manual (for the first time)")
        
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == "2":
            return self._manual_authenticate()
        
        try:
            email = input("Enter Amazon email: ").strip()
            password = input("Enter Amazon password: ").strip()
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()
                
                # Navigate to Amazon homepage first
                page.goto("https://www.amazon.com")
                page.wait_for_load_state("networkidle")
                
                # Navigate to sign in
                try:
                    page.click("a[data-nav-role='signin']")
                    page.wait_for_load_state("networkidle")
                except:
                    page.goto("https://www.amazon.com/ap/signin")
                    page.wait_for_load_state("networkidle")
                
                # Wait for email field and fill it
                try:
                    page.wait_for_selector("#ap_email", timeout=10000)
                    page.fill("#ap_email", email)
                    page.click("#continue")
                    page.wait_for_load_state("networkidle")
                except Exception as e:
                    print(f"Error with email field: {e}")
                    print(f"Current URL: {page.url}")
                    browser.close()
                    return False
                
                # Wait for password field and fill it
                try:
                    page.wait_for_selector("#ap_password", timeout=10000)
                    page.fill("#ap_password", password)
                    page.click("#signInSubmit")
                    page.wait_for_load_state("networkidle")
                except Exception as e:
                    print(f"Error with password field: {e}")
                    print(f"Current URL: {page.url}")
                    browser.close()
                    return False
                
                # Wait a bit for redirect
                page.wait_for_timeout(3000)
                
                # Check if login successful - look for Amazon homepage or account indicators
                current_url = page.url
                print(f"Current URL: {current_url}")
                
                # Check for successful login indicators
                login_indicators = [
                    "amazon.com" in current_url and "ap/signin" not in current_url,
                    "amazon.com" in current_url and "signin" not in current_url,
                    "amazon.com" in current_url and "ap/" not in current_url,
                    page.locator("#nav-link-accountList").count() > 0,
                    page.locator("a[data-nav-role='signin']").count() == 0
                ]
                
                if any(login_indicators):
                    # Save cookies
                    cookies = context.cookies()
                    self._save_cookies(cookies)
                    browser.close()
                    print("✅ Authentication successful!")
                    return True
                else:
                    print("❌ Authentication failed. Please check credentials.")
                    print(f"URL: {current_url}")
                    browser.close()
                    return False
                    
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            print(f"❌ Authentication error: {e}")
            return False
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        if not os.path.exists(self.cookies_file):
            return False
            
        try:
            self._load_cookies()
            # Test with a simple request
            response = self.session.get("https://www.amazon.com", timeout=10)
            if response.status_code == 200:
                # Check if we're not on a signin page
                return "ap/signin" not in response.url and "signin" not in response.url
            return False
        except:
            return False
    
    def _save_cookies(self, cookies: list) -> None:
        """Save cookies to file."""
        with open(self.cookies_file, 'w') as f:
            json.dump(cookies, f)
    
    def _manual_authenticate(self) -> bool:
        """Manual authentication where user handles login in browser."""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()
                
                print("\n🌐 Opening Amazon login page...")
                page.goto("https://www.amazon.com")
                page.wait_for_load_state("networkidle")
                
                print("\n📝 Please log in to Amazon in the browser window.")
                print("   - Click 'Sign in' or 'Hello, Sign in'")
                print("   - Enter your email and password")
                print("   - Complete any 2FA if required")
                print("   - Wait until you see the Amazon homepage")
                
                input("\nPress Enter when you have successfully logged in...")
                
                # Check if login successful - look for Amazon homepage or account indicators
                current_url = page.url
                print(f"Current URL: {current_url}")
                
                # Check for successful login indicators
                login_indicators = [
                    "amazon.com" in current_url and "ap/signin" not in current_url,
                    "amazon.com" in current_url and "signin" not in current_url,
                    "amazon.com" in current_url and "ap/" not in current_url,
                    page.locator("#nav-link-accountList").count() > 0,
                    page.locator("a[data-nav-role='signin']").count() == 0
                ]
                
                if any(login_indicators):
                    # Save cookies
                    cookies = context.cookies()
                    self._save_cookies(cookies)
                    browser.close()
                    print("✅ Authentication successful!")
                    return True
                else:
                    print("❌ Authentication failed. Please try again.")
                    print(f"URL: {current_url}")
                    browser.close()
                    return False
                    
        except Exception as e:
            logger.error(f"Manual authentication failed: {e}")
            print(f"❌ Authentication error: {e}")
            return False
    
    def _load_cookies(self) -> None:
        """Load cookies from file."""
        if os.path.exists(self.cookies_file):
            with open(self.cookies_file, 'r') as f:
                cookies = json.load(f)
                for cookie in cookies:
                    self.session.cookies.set(cookie['name'], cookie['value'], domain=cookie.get('domain'))
    
