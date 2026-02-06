"""
USA Amazon Scraper (amazon.com)
Country-specific scraping logic for United States
"""

import logging
import time
import random
import re
from bs4 import BeautifulSoup
from .base_scraper import BaseAmazonScraper

class USAScraper(BaseAmazonScraper):
    """Amazon USA (amazon.com) specific scraper"""
    
    def scrape_product(self, url):
        """Scrape product from Amazon USA"""
        try:
            asin = self.extract_asin(url)
            if not asin:
                return {'error': 'Invalid Amazon URL - ASIN not found'}
            
            logging.info(f"📦 Scraping ASIN: {asin} from Amazon USA")
            
            if not self.init_browser():
                return {'error': 'Browser initialization failed'}
            
            self.driver.get(url)
            time.sleep(random.uniform(3, 5))
            
            soup = BeautifulSoup(self.driver.page_source, 'html5lib')
            
            product = {
                'asin': asin,
                'merchant': 'Amazon USA',
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
    
    def _extract_title(self, soup):
        """Extract product title"""
        title_elem = soup.select_one('#productTitle')
        if title_elem:
            title = self._clean_text(title_elem.get_text())
            if title:
                return title[:500]
        return 'Unknown Product'
    
    def _extract_price(self, soup):
        """Extract current price (USA uses dollar format)"""
        selectors = [
            '.a-price-whole',
            'span.a-price span.a-offscreen',
            '#priceblock_ourprice',
            '#priceblock_dealprice'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                price = self._extract_price_value(element.get_text())
                if price:
                    logging.info(f"💰 Price: ${price}")
                    return price
        return None
    
    def _extract_original_price(self, soup):
        """Extract original price"""
        selectors = [
            '.a-price.a-text-price .a-offscreen',
            '.a-text-strike'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                price = self._extract_price_value(element.get_text())
                if price:
                    return price
        return None
    
    def _extract_brand(self, soup):
        """Extract brand name"""
        brand_elem = soup.select_one('a#bylineInfo')
        if brand_elem:
            brand = self._clean_text(brand_elem.get_text())
            brand = brand.replace('Visit the', '').replace('Store', '').replace('Brand:', '').strip()
            if brand:
                return brand[:100]
        return 'Generic'
    
    def _extract_category(self, soup):
        """Extract main category"""
        breadcrumbs = soup.select('#wayfinding-breadcrumbs_container li a')
        if breadcrumbs:
            return self._clean_text(breadcrumbs[0].get_text())[:100]
        return 'General'
    
    def _extract_subcategory(self, soup):
        """Extract subcategory"""
        breadcrumbs = soup.select('#wayfinding-breadcrumbs_container li a')
        if len(breadcrumbs) > 1:
            return self._clean_text(breadcrumbs[1].get_text())[:100]
        return 'General'
    
    def _extract_stock_status(self, soup):
        """Extract stock status"""
        availability = soup.select_one('#availability span')
        if availability:
            text = availability.get_text().lower()
            if 'out of stock' in text or 'unavailable' in text:
                return 'out_of_stock'
        return 'in_stock'
    
    def _extract_image(self, soup):
        """Extract main product image"""
        img = soup.select_one('#landingImage')
        if not img:
            img = soup.select_one('.a-dynamic-image')
        if img:
            src = img.get('src') or img.get('data-old-hires')
            if src:
                return src[:500]
        return None
    
    def _extract_rating(self, soup):
        """Extract product rating"""
        rating_elem = soup.select_one('span[data-hook="rating-out-of-text"]')
        if rating_elem:
            match = re.search(r'([\d.]+)', rating_elem.get_text())
            if match:
                return float(match.group(1))
        return None
    
    def _extract_review_count(self, soup):
        """Extract review count"""
        review_elem = soup.select_one('#acrCustomerReviewText')
        if review_elem:
            match = re.search(r'([\d,]+)', review_elem.get_text())
            if match:
                return int(match.group(1).replace(',', ''))
        return 0
    
    def _extract_description(self, soup):
        """Extract product description"""
        desc_elem = soup.select_one('#feature-bullets ul')
        if desc_elem:
            points = [self._clean_text(li.get_text()) for li in desc_elem.select('li')]
            return ' | '.join(points)[:2000]
        return None
    
    def _extract_specifications(self, soup):
        """Extract specifications"""
        specs = {}
        for row in soup.select('#productDetails_techSpec_section_1 tr, #prodDetails tr'):
            header = row.select_one('th')
            value = row.select_one('td')
            if header and value:
                key = self._clean_text(header.get_text())
                val = self._clean_text(value.get_text())
                if key and val:
                    specs[key] = val
        return specs if specs else None
    
    def _extract_all_images(self, soup):
        """Extract all product images"""
        images = []
        for img in soup.select('#altImages img'):
            src = img.get('src')
            if src and 'http' in src:
                full_size = src.replace('_SS40_', '_SX679_')
                if full_size not in images:
                    images.append(full_size)
        return images[:10]
    
    def _extract_seller_info(self, soup):
        """Extract seller info"""
        seller = {}
        seller_elem = soup.select_one('#sellerProfileTriggerId')
        if seller_elem:
            seller['name'] = self._clean_text(seller_elem.get_text())
        fulfillment = soup.select_one('#fulfillerInfoFeature_feature_div')
        if fulfillment:
            seller['fulfilled_by_amazon'] = 'amazon' in fulfillment.get_text().lower()
        return seller if seller else None
