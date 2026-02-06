"""
Base Amazon Scraper
Common scraping logic shared across all countries
"""

import re
import time
import random
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from fake_useragent import UserAgent

class BaseAmazonScraper:
    """Base class for Amazon scrapers"""
    
    def __init__(self, country_code, country_config):
        self.country_code = country_code
        self.country_config = country_config
        self.driver = None
        
    def extract_asin(self, url):
        """Extract ASIN from Amazon URL"""
        # Pattern 1: /dp/ASIN
        match = re.search(r'/dp/([A-Z0-9]{10})', url)
        if match:
            return match.group(1)
        
        # Pattern 2: /gp/product/ASIN
        match = re.search(r'/gp/product/([A-Z0-9]{10})', url)
        if match:
            return match.group(1)
        
        # Pattern 3: /gp/aw/d/ASIN (mobile URL)
        match = re.search(r'/gp/aw/d/([A-Z0-9]{10})', url)
        if match:
            return match.group(1)
        
        # Pattern 4: ASIN in query parameters
        from urllib.parse import parse_qs
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        if 'ASIN' in params:
            return params['ASIN'][0]
        
        return None
    
    def init_browser(self):
        """Initialize Edge browser with anti-detection"""
        try:
            logging.info(f"🌐 Initializing browser for {self.country_config['name']}...")
            
            ua = UserAgent()
            user_agent = ua.random
            
            options = EdgeOptions()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument(f'user-agent={user_agent}')
            
            try:
                self.driver = webdriver.Edge(options=options)
            except:
                service = EdgeService(EdgeChromiumDriverManager().install())
                self.driver = webdriver.Edge(service=service, options=options)
            
            # Random window size
            widths = [1366, 1440, 1536, 1920]
            heights = [768, 900, 864, 1080]
            self.driver.set_window_size(random.choice(widths), random.choice(heights))
            
            # Execute stealth scripts
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})
            
            logging.info("✅ Browser initialized")
            return True
            
        except Exception as e:
            logging.error(f"❌ Browser initialization failed: {e}")
            return False
    
    def close_browser(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logging.info("🔒 Browser closed")
    
    def scrape_product(self, url):
        """Scrape product - to be implemented by country-specific scrapers"""
        raise NotImplementedError("Country-specific scraper must implement scrape_product()")
    
    def _clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return None
        return ' '.join(text.split()).strip()
    
    def _extract_price_value(self, price_text):
        """Extract numeric price from text"""
        if not price_text:
            return None
        
        # Remove all non-numeric characters except dot and comma
        price = re.sub(r'[^\d.,]', '', price_text)
        
        # Handle different decimal separators
        if ',' in price and '.' in price:
            # Format like 1,234.56 or 1.234,56
            if price.index(',') < price.index('.'):
                price = price.replace(',', '')  # 1,234.56 -> 1234.56
            else:
                price = price.replace('.', '').replace(',', '.')  # 1.234,56 -> 1234.56
        elif ',' in price:
            # Could be thousands separator or decimal
            if price.count(',') == 1 and len(price.split(',')[1]) <= 2:
                price = price.replace(',', '.')  # Decimal comma
            else:
                price = price.replace(',', '')  # Thousands separator
        
        try:
            return float(price)
        except:
            return None
    
    def _generate_affiliate_link(self, url, asin):
        """Generate Amazon affiliate link"""
        from config import AMAZON_AFFILIATE
        
        if AMAZON_AFFILIATE.get('enable'):
            tag = AMAZON_AFFILIATE.get('associate_tag', '')
            base_url = f"https://www.{self.country_config['domain']}"
            return f"{base_url}/dp/{asin}?tag={tag}"
        
        return f"https://www.{self.country_config['domain']}/dp/{asin}"
