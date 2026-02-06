from bs4 import BeautifulSoup

from scrapers.base_scraper import BaseAmazonScraper


class DummyBrowserManager:
    def get_context(self, headless, proxy_url):
        raise RuntimeError("Not used in parsing tests")


def test_basic_parsing():
    with open("tests/fixtures/amazon_sample.html", "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html5lib")
    scraper = BaseAmazonScraper("US", {"name": "United States", "currency": "$", "currency_code": "USD"}, DummyBrowserManager())

    assert scraper._extract_title(soup) == "Sample Product Title"
    assert scraper._extract_price(soup) == 19.99
    assert scraper._extract_stock_status(soup) == "in_stock"
    assert scraper._extract_category(soup) == "Electronics"
    assert scraper._extract_subcategory(soup) == "Accessories"
    assert scraper._extract_brand(soup) == "SampleBrand"
    assert scraper._extract_bullet_points(soup) == ["Bullet 1", "Bullet 2"]
