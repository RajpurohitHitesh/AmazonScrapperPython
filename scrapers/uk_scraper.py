"""
UK Amazon Scraper (amazon.co.uk)
Country-specific scraping logic for United Kingdom
"""

import logging
import time
import random
import re
from bs4 import BeautifulSoup
from .base_scraper import BaseAmazonScraper

class UKScraper(BaseAmazonScraper):
    """Amazon UK (amazon.co.uk) specific scraper"""
    
    def scrape_product(self, url):
        """Scrape product from Amazon UK"""
        try:
            asin = self.extract_asin(url)
            if not asin:
                return {'error': 'Invalid Amazon URL - ASIN not found'}
            
            logging.info(f"📦 Scraping ASIN: {asin} from Amazon UK")
            
            if not self.init_browser():
                return {'error': 'Browser initialization failed'}
            
            self.driver.get(url)
            time.sleep(random.uniform(3, 5))
            
            soup = BeautifulSoup(self.driver.page_source, 'html5lib')
            
            product = {
                'asin': asin,
                'merchant': 'Amazon UK',
                'name': self._extract_title(soup),
                'category': self._extract_category(soup),
                'subcategory': self._extract_subcategory(soup),
                'brand': self._extract_brand(soup),
                'current_price': self._extract_price(soup),
                'original_price': self._extract_original_price(soup),
                'stock_status': self._extract_stock_status(soup),
                'image_path': self._extract_image(soup),
                'rating': self._extract_rating(soup),
                'review_count': self._extract_review_count(soup)
            }
            
            self.close_browser()
            logging.info(f"✅ Successfully scraped: {product['name']}")
            return product
            
        except Exception as e:
            logging.error(f"❌ Scraping error: {e}")
            self.close_browser()
            return {'error': str(e)}
    
    # Use same extraction methods as USA (inherit or reuse logic)
    _extract_title = lambda self, soup: IndiaScraper._extract_title(self, soup)
    _extract_price = lambda self, soup: IndiaScraper._extract_price(self, soup)
    _extract_original_price = lambda self, soup: IndiaScraper._extract_original_price(self, soup)
    _extract_brand = lambda self, soup: IndiaScraper._extract_brand(self, soup)
    _extract_category = lambda self, soup: IndiaScraper._extract_category(self, soup)
    _extract_subcategory = lambda self, soup: IndiaScraper._extract_subcategory(self, soup)
    _extract_stock_status = lambda self, soup: IndiaScraper._extract_stock_status(self, soup)
    _extract_image = lambda self, soup: IndiaScraper._extract_image(self, soup)
    _extract_rating = lambda self, soup: IndiaScraper._extract_rating(self, soup)
    _extract_review_count = lambda self, soup: IndiaScraper._extract_review_count(self, soup)
    _extract_description = lambda self, soup: IndiaScraper._extract_description(self, soup)
    _extract_specifications = lambda self, soup: IndiaScraper._extract_specifications(self, soup)
    _extract_all_images = lambda self, soup: IndiaScraper._extract_all_images(self, soup)
    _extract_seller_info = lambda self, soup: IndiaScraper._extract_seller_info(self, soup)

from .india_scraper import IndiaScraper
