"""
Test script for Amazon India scraper
Run with: python -m pytest tests/test_india.py -v
Or directly: python tests/test_india.py
"""
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scrapers.india_scraper import IndiaScraper
from services.browser_manager import BrowserManager
from api_config import AMAZON_COUNTRIES, HEADLESS_MODE, SCRAPE_TIMEOUT_SECONDS, SCRAPE_MAX_RETRIES, PROXY_URLS


def test_india_scraper():
    """Test Amazon India product scraping"""
    print("\n" + "="*80)
    print("🇮🇳 TESTING AMAZON INDIA SCRAPER")
    print("="*80 + "\n")
    
    # Initialize browser and scraper
    browser_manager = BrowserManager(headless=HEADLESS_MODE)
    browser_manager.start()
    
    country_config = AMAZON_COUNTRIES['IN']
    scraper = IndiaScraper(
        'IN',
        country_config,
        browser_manager,
        timeout_seconds=SCRAPE_TIMEOUT_SECONDS,
        max_retries=SCRAPE_MAX_RETRIES,
        proxy_urls=PROXY_URLS,
        headless_default=HEADLESS_MODE,
    )
    
    # Test URL
    test_url = "https://www.amazon.in/iQOO-Snapdragon-Processor-SuperComputing-Smartphone/dp/B0F83HTPM2"
    
    print(f"🔍 Testing URL: {test_url}\n")
    
    # Scrape product
    result = scraper.scrape_product(test_url)
    
    # Stop browser
    browser_manager.stop()
    
    # Verify results
    print("\n" + "="*80)
    print("📊 TEST RESULTS")
    print("="*80 + "\n")
    
    if 'error' in result:
        print(f"❌ FAILED: {result['error']}")
        return False
    
    # Check essential fields
    essential_fields = ['asin', 'name', 'brand', 'current_price', 'category']
    missing_fields = []
    
    for field in essential_fields:
        if not result.get(field):
            missing_fields.append(field)
    
    if missing_fields:
        print(f"⚠️  WARNING: Missing fields: {', '.join(missing_fields)}\n")
    
    # Display results
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Summary
    print("\n" + "="*80)
    print("📋 SUMMARY")
    print("="*80)
    print(f"✅ Product: {result.get('name', 'N/A')}")
    print(f"✅ Brand: {result.get('brand', 'N/A')}")
    print(f"✅ Price: ₹{result.get('current_price', 'N/A')}")
    print(f"✅ Category: {result.get('category', 'N/A')} > {result.get('subcategory', 'N/A')}")
    print(f"✅ Rating: {result.get('rating', 'N/A')} ({result.get('review_count', 0)} reviews)")
    print(f"✅ Stock: {result.get('stock_status', 'N/A')}")
    print("="*80 + "\n")
    
    return True


if __name__ == "__main__":
    try:
        success = test_india_scraper()
        if success:
            print("✅ TEST PASSED!\n")
            sys.exit(0)
        else:
            print("❌ TEST FAILED!\n")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ TEST ERROR: {str(e)}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
