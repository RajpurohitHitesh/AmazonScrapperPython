"""
Base Amazon Scraper
Common scraping logic shared across all countries
"""

import logging
import random
import re
import time
from typing import Optional, List
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from services.browser_manager import PlaywrightTimeoutError

class BaseAmazonScraper:
    """Base class for Amazon scrapers"""

    def __init__(self, country_code, country_config, browser_manager, timeout_seconds: int = 30, max_retries: int = 2, proxy_urls: Optional[List[str]] = None, headless_default: bool = True):
        self.country_code = country_code
        self.country_config = country_config
        self.browser_manager = browser_manager
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.proxy_urls = proxy_urls or []
        self.headless_default = headless_default
        
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
    
    def _pick_proxy(self, requested_proxy: Optional[str] = None) -> Optional[str]:
        if requested_proxy:
            return requested_proxy
        if not self.proxy_urls:
            return None
        return random.choice(self.proxy_urls)

    def scrape_product(self, url, headless: Optional[bool] = None, proxy: Optional[str] = None):
        """Scrape product data using Playwright"""
        asin = self.extract_asin(url)
        if not asin:
            return {"error": "Invalid Amazon URL - ASIN not found"}

        attempt = 0
        last_error = None
        while attempt <= self.max_retries:
            attempt += 1
            try:
                use_headless = self.headless_default if headless is None else headless
                proxy_url = self._pick_proxy(proxy)
                context = self.browser_manager.get_context(headless=use_headless, proxy_url=proxy_url)
                page = context.new_page()
                page.set_default_timeout(self.timeout_seconds * 1000)

                logging.info(f"🌍 Visiting {url} (attempt {attempt})")
                page.goto(url, wait_until="domcontentloaded")
                try:
                    page.wait_for_selector("#productTitle", timeout=self.timeout_seconds * 1000)
                except PlaywrightTimeoutError:
                    pass

                content = page.content()
                if self._detect_captcha(content):
                    context.close()
                    return {"error": "CAPTCHA_REQUIRED", "error_code": "captcha"}

                soup = BeautifulSoup(content, "html5lib")
                product = {
                    "asin": asin,
                    "merchant": f"Amazon {self.country_config['name']}",
                    "name": self._extract_title(soup),
                    "category": self._extract_category(soup),
                    "subcategory": self._extract_subcategory(soup),
                    "brand": self._extract_brand(soup),
                    "current_price": self._extract_price(soup),
                    "original_price": self._extract_original_price(soup),
                    "currency": self.country_config.get("currency"),
                    "currency_code": self.country_config.get("currency_code"),
                    "stock_status": self._extract_stock_status(soup),
                    "image_path": self._extract_image(soup),
                    "images": self._extract_all_images(soup),
                    "rating": self._extract_rating(soup),
                    "review_count": self._extract_review_count(soup),
                    "bullet_points": self._extract_bullet_points(soup),
                    "variations": self._extract_variations(soup),
                    "delivery_eta": self._extract_delivery_eta(soup),
                    "seller": self._extract_seller_info(soup),
                    "offers_count": self._extract_offers_count(soup),
                    "buy_box_winner": self._extract_buy_box_winner(soup),
                    "seller_type": self._extract_seller_type(soup),
                    "description": self._extract_description(soup),
                    "specifications": self._extract_specifications(soup),
                }

                context.close()
                return product

            except Exception as e:
                last_error = str(e)
                logging.error(f"Scrape error: {e}")
                try:
                    if 'context' in locals() and context:
                        context.close()
                except Exception:
                    pass
                time.sleep(min(2 ** (attempt - 1), 10))
        return {"error": last_error or "Unknown error"}
    
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
        except (ValueError, TypeError):
            return None
    
    def _detect_captcha(self, html: str) -> bool:
        if not html:
            return False
        lower = html.lower()
        # Be more specific to avoid false positives in product descriptions
        markers = [
            "enter the characters you see",
            "type the characters",
            "sorry, we just need to make sure",
            "validatecaptcha",
            "<title>robot check</title>"
        ]
        return any(m in lower for m in markers)

    def _extract_title(self, soup):
        title_elem = soup.select_one("#productTitle")
        if title_elem:
            title = self._clean_text(title_elem.get_text())
            if title:
                return title[:500]
        return "Unknown Product"

    def _extract_price(self, soup):
        """Extract current price with detailed logging"""
        selectors = [
            ".a-price-whole",
            "span.a-price.a-text-price.a-size-medium span.a-offscreen",
            "#priceblock_ourprice",
            "#priceblock_dealprice",
            ".a-price .a-offscreen",
        ]
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                price = self._extract_price_value(element.get_text())
                if price is not None:
                    logging.info(f"💰 Price found: {price}")
                    return price
        return None

    def _extract_original_price(self, soup):
        """Extract original/MRP price"""
        selectors = [
            ".a-price.a-text-price .a-offscreen",
            "span.a-price.a-text-price span.a-offscreen",
            "span.a-text-strike",
            ".a-text-price .a-offscreen",
        ]
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                price = self._extract_price_value(element.get_text())
                if price is not None:
                    return price
        return None

    def _extract_brand(self, soup):
        """Extract brand name with fallback to product details"""
        brand_elem = soup.select_one("a#bylineInfo")
        if brand_elem:
            brand = self._clean_text(brand_elem.get_text())
            brand = brand.replace("Visit the", "").replace("Store", "").replace("Brand:", "").strip()
            if brand:
                logging.info(f"🏷️  Brand: {brand}")
                return brand[:100]
        
        # Try product details table
        for row in soup.select("tr"):
            header = row.select_one("th")
            if header and "Brand" in header.get_text():
                value = row.select_one("td")
                if value:
                    brand = self._clean_text(value.get_text())
                    if brand:
                        logging.info(f"🏷️  Brand from table: {brand}")
                        return brand[:100]
        
        return "Generic"

    def _extract_category(self, soup):
        """Extract main category (first breadcrumb)"""
        # Try multiple breadcrumb selectors
        breadcrumb_selectors = [
            "#wayfinding-breadcrumbs_container li a",
            "#wayfinding-breadcrumbs_feature_div ul li a",
            "ul.a-unordered-list.a-horizontal.a-size-small li a",
            "div[data-feature-name='breadcrumbs'] a",
            "#wayfinding-breadcrumbs_container",
            "#wayfinding-breadcrumbs_feature_div",
        ]
        
        for selector in breadcrumb_selectors:
            breadcrumbs = soup.select(selector)
            if breadcrumbs and len(breadcrumbs) > 0:
                # Try link-based extraction first
                if breadcrumbs[0].name == 'a':
                    category = self._clean_text(breadcrumbs[0].get_text())
                    if category and category.lower() != "back to results":
                        logging.info(f"📁 Category found: {category}")
                        return category[:100]
                else:
                    # Try text-based extraction with separator
                    text = self._clean_text(breadcrumbs[0].get_text())
                    if '›' in text:
                        parts = [p.strip() for p in text.split('›')]
                        if parts and parts[0] and parts[0].lower() != "back to results":
                            logging.info(f"📁 Category found: {parts[0]}")
                            return parts[0][:100]
        
        logging.warning("⚠️ Category not found, using General")
        return "General"

    def _extract_subcategory(self, soup):
        """Extract subcategory (last meaningful breadcrumb, ignore duplicates)"""
        # Try multiple breadcrumb selectors
        breadcrumb_selectors = [
            "#wayfinding-breadcrumbs_container li a",
            "#wayfinding-breadcrumbs_feature_div ul li a",
            "ul.a-unordered-list.a-horizontal.a-size-small li a",
            "div[data-feature-name='breadcrumbs'] a",
            "#wayfinding-breadcrumbs_container",
            "#wayfinding-breadcrumbs_feature_div",
        ]
        
        for selector in breadcrumb_selectors:
            breadcrumbs = soup.select(selector)
            if len(breadcrumbs) > 0:
                # Check if it's a container with › separator
                if breadcrumbs[0].name != 'a':
                    text = self._clean_text(breadcrumbs[0].get_text())
                    if '›' in text:
                        parts = [p.strip() for p in text.split('›')]
                        parts = [p for p in parts if p and p.lower() != "back to results"]
                        if len(parts) > 0:
                            # Last part is subcategory
                            subcategory = parts[-1]
                            logging.info(f"📂 Subcategory found: {subcategory}")
                            return subcategory[:100]
                    continue
                
                # Link-based extraction
                if len(breadcrumbs) > 1:
                    # Get all breadcrumb texts
                    crumbs = [self._clean_text(b.get_text()) for b in breadcrumbs]
                    crumbs = [c for c in crumbs if c and c.lower() != "back to results"]  # Remove empty and "Back to results"
                
                if len(crumbs) > 1:
                    # Get last breadcrumb
                    last_crumb = crumbs[-1]
                    
                    # If last is duplicate of second-to-last, use second-to-last
                    if len(crumbs) > 2 and last_crumb == crumbs[-2]:
                        logging.info(f"📂 Subcategory found: {crumbs[-2]}")
                        return crumbs[-2][:100]
                    
                    logging.info(f"📂 Subcategory found: {last_crumb}")
                    return last_crumb[:100]
        
        logging.warning("⚠️ Subcategory not found, using General")
        return "General"

    def _extract_stock_status(self, soup):
        availability = soup.select_one("#availability span")
        if availability:
            text = availability.get_text().lower()
            if "out of stock" in text or "unavailable" in text:
                return "out_of_stock"
        return "in_stock"

    def _extract_image(self, soup):
        img = soup.select_one("#landingImage")
        if not img:
            img = soup.select_one(".a-dynamic-image")
        if img:
            src = img.get("src") or img.get("data-old-hires")
            if src:
                return src[:500]
        return None

    def _extract_all_images(self, soup):
        """Extract all product images"""
        images = []
        for img in soup.select("#altImages img"):
            src = img.get("src")
            if src and "http" in src:
                full_size = src.replace("_SS40_", "_SX679_").replace("_AC_US40_", "_SX679_")
                if full_size not in images:
                    images.append(full_size)
        if images:
            logging.info(f"🖼️  Found {len(images)} images")
        return images[:10]

    def _extract_rating(self, soup):
        """Extract product rating"""
        rating_elem = soup.select_one('span[data-hook="rating-out-of-text"]')
        if rating_elem:
            rating_text = rating_elem.get_text()
            match = re.search(r"([\d.]+)", rating_text)
            if match:
                try:
                    rating = float(match.group(1))
                    logging.info(f"⭐ Rating: {rating}")
                    return rating
                except Exception:
                    return None
        return None

    def _extract_review_count(self, soup):
        """Extract number of reviews"""
        review_elem = soup.select_one("#acrCustomerReviewText")
        if review_elem:
            review_text = review_elem.get_text()
            match = re.search(r"([\d.,]+)", review_text)
            if match:
                try:
                    count = int(re.sub(r'[^\d]', '', match.group(1)))
                    logging.info(f"💬 Reviews: {count}")
                    return count
                except Exception:
                    return 0
        return 0

    def _extract_description(self, soup):
        """Extract product description from bullet points"""
        desc_elem = soup.select_one("#feature-bullets ul")
        if desc_elem:
            points = [self._clean_text(li.get_text()) for li in desc_elem.select("li")]
            points = [p for p in points if p]
            if points:
                logging.info(f"📝 Found {len(points)} description points")
            return " | ".join(points)[:2000]
        return None

    def _extract_bullet_points(self, soup):
        """Extract bullet points list"""
        desc_elem = soup.select_one("#feature-bullets ul")
        if desc_elem:
            points = [self._clean_text(li.get_text()) for li in desc_elem.select("li")]
            filtered_points = [p for p in points if p][:10]
            if filtered_points:
                logging.info(f"📌 Found {len(filtered_points)} bullet points")
            return filtered_points
        return []

    def _extract_specifications(self, soup):
        """Extract product specifications from details table"""
        specs = {}
        # Product details table
        for row in soup.select("#productDetails_techSpec_section_1 tr, #prodDetails tr, #productDetails_detailBullets_sections1 tr"):
            header = row.select_one("th")
            value = row.select_one("td")
            if header and value:
                key = self._clean_text(header.get_text())
                val = self._clean_text(value.get_text())
                if key and val:
                    specs[key] = val
        
        if specs:
            logging.info(f"📋 Found {len(specs)} specifications")
        return specs if specs else None

    def _extract_variations(self, soup):
        """Extract product variations"""
        variations = []
        for label in soup.select("#twister .a-form-label"):
            text = self._clean_text(label.get_text())
            if text and text not in variations:
                variations.append(text)
        if variations:
            logging.info(f"🔄 Found {len(variations)} variations")
        return variations[:10]

    def _extract_delivery_eta(self, soup):
        """Extract delivery estimate"""
        selectors = [
            "#mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_LARGE",
            "#deliveryMessageMirId",
            "#mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_MEDIUM",
        ]
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                eta = self._clean_text(elem.get_text())
                if eta:
                    logging.info(f"🚚 Delivery: {eta[:50]}...")
                return eta
        return None

    def _extract_seller_info(self, soup):
        """Extract seller information"""
        seller = {}
        seller_elem = soup.select_one("#sellerProfileTriggerId")
        if seller_elem:
            seller["name"] = self._clean_text(seller_elem.get_text())
            logging.info(f"🏪 Seller: {seller['name']}")
        fulfillment = soup.select_one("#fulfillerInfoFeature_feature_div")
        if fulfillment:
            seller["fulfilled_by_amazon"] = "amazon" in fulfillment.get_text().lower()
        return seller if seller else None

    def _extract_seller_type(self, soup):
        seller = self._extract_seller_info(soup) or {}
        name = (seller.get("name") or "").lower()
        if "amazon" in name:
            return "amazon"
        if name:
            return "marketplace"
        return None

    def _extract_buy_box_winner(self, soup):
        seller = self._extract_seller_info(soup)
        if seller and seller.get("name"):
            return seller.get("name")
        return None

    def _extract_offers_count(self, soup):
        elem = soup.select_one("#olpLinkWidget a, #olp_feature_div a")
        if elem:
            text = elem.get_text()
            match = re.search(r"([\d.,]+)", text)
            if match:
                try:
                    return int(re.sub(r'[^\d]', '', match.group(1)))
                except Exception:
                    return None
        return None
