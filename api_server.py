"""
AmazonScraper Flask API
Main API server to handle scraping requests from clients.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import logging
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Import configurations
from api_config import API_HOST, API_PORT, DEBUG_MODE, API_KEY, ALLOWED_ORIGINS, AMAZON_COUNTRIES, get_country_from_url
from scrapers.india_scraper import IndiaScraper

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=ALLOWED_ORIGINS)

# API Key Authentication Decorator
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        provided_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        if not provided_key:
            return jsonify({
                'success': False,
                'error': 'API key is required',
                'message': 'Please provide API key in X-API-Key header or api_key parameter'
            }), 401
        
        if provided_key != API_KEY:
            return jsonify({
                'success': False,
                'error': 'Invalid API key',
                'message': 'The provided API key is incorrect'
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


@app.route('/', methods=['GET'])
def index():
    """API information endpoint"""
    return jsonify({
        'service': 'AmazonScraper API',
        'version': '2.0.0',
        'status': 'running',
        'supported_countries': len(AMAZON_COUNTRIES),
        'endpoints': {
            'scrape': '/api/scrape',
            'countries': '/api/countries',
            'health': '/api/health'
        },
        'documentation': 'Provide product URL and API key to scrape Amazon products'
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'AmazonScraper API',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/countries', methods=['GET'])
@require_api_key
def get_countries():
    """Get list of supported countries"""
    countries = []
    for code, config in AMAZON_COUNTRIES.items():
        countries.append({
            'code': code,
            'name': config['name'],
            'domain': config['domain'],
            'currency': config['currency'],
            'currency_code': config['currency_code']
        })
    
    return jsonify({
        'success': True,
        'count': len(countries),
        'countries': countries
    })


@app.route('/api/scrape', methods=['POST'])
@require_api_key
def scrape_product():
    """
    Main scraping endpoint
    Expected JSON body:
    {
        "url": "https://www.amazon.in/dp/B0XXXXXX"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: url',
                'message': 'Please provide Amazon product URL in request body'
            }), 400
        
        product_url = data['url']
        
        # Detect country from URL
        country_code = get_country_from_url(product_url)
        
        if not country_code:
            return jsonify({
                'success': False,
                'error': 'Unsupported Amazon domain',
                'message': f'Could not detect country from URL. Supported domains: {", ".join([c["domain"] for c in AMAZON_COUNTRIES.values()])}'
            }), 400
        
        country_config = AMAZON_COUNTRIES[country_code]
        
        logging.info(f"🌍 Scraping request for {country_config['name']} ({country_code})")
        logging.info(f"🔗 URL: {product_url}")
        
        # Select appropriate scraper based on country
        scraper = get_scraper_for_country(country_code, country_config)
        
        if not scraper:
            return jsonify({
                'success': False,
                'error': 'Scraper not available',
                'message': f'Scraper for {country_config["name"]} is not yet implemented'
            }), 501
        
        # Scrape the product
        result = scraper.scrape_product(product_url)
        
        # Check if scraping was successful
        if 'error' in result:
            return jsonify({
                'success': False,
                'error': result['error'],
                'country': country_config['name'],
                'country_code': country_code
            }), 500
        
        # Return successful result
        return jsonify({
            'success': True,
            'country': country_config['name'],
            'country_code': country_code,
            'data': result
        })
    
    except Exception as e:
        logging.error(f"❌ API Error: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500


def get_scraper_for_country(country_code, country_config):
    """Get the appropriate scraper instance for a country"""
    scrapers = {
        'IN': IndiaScraper,
        # 'US': USAScraper,
        # 'UK': UKScraper,
        # Add more as they are implemented
    }
    
    scraper_class = scrapers.get(country_code)
    if scraper_class:
        return scraper_class(country_code, country_config)
    
    return None


if __name__ == '__main__':
    from datetime import datetime
    
    print("=" * 60)
    print("🚀 AmazonScraper API Server")
    print("=" * 60)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Host: {API_HOST}:{API_PORT}")
    print(f"🔐 API Key Authentication: Enabled")
    print(f"🌍 Supported Countries: {len(AMAZON_COUNTRIES)}")
    print(f"🔧 Debug Mode: {DEBUG_MODE}")
    print("=" * 60)
    print(f"📡 API Endpoints:")
    print(f"   - GET  /              - API Info")
    print(f"   - GET  /api/health    - Health Check")
    print(f"   - GET  /api/countries - Supported Countries")
    print(f"   - POST /api/scrape    - Scrape Product (Requires API Key)")
    print("=" * 60)
    print(f"💡 Use X-API-Key header or api_key parameter for authentication")
    print("=" * 60)
    
    app.run(host=API_HOST, port=API_PORT, debug=DEBUG_MODE)

def main():
    """Entry point for console script"""
    if __name__ == '__main__':
        pass
    else:
        # When called via console script
        import sys
        sys.exit(app.run(host=API_HOST, port=API_PORT, debug=DEBUG_MODE))

if __name__ == '__main__':
    main()
