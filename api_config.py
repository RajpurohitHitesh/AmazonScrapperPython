"""
AmazonScraper API Configuration
Dynamic domain and API key settings
"""

import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_HOST = os.getenv('API_HOST', '0.0.0.0')  # Listen on all interfaces
API_PORT = int(os.getenv('API_PORT', '5000'))
API_DOMAIN = os.getenv('API_DOMAIN', '')  # Optional: Your domain (e.g., https://api.yourdomain.com)
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Get base URL for API
def get_base_url():
    """Get the base URL for the API (domain or localhost)"""
    if API_DOMAIN:
        return API_DOMAIN.rstrip('/')
    return f'http://127.0.0.1:{API_PORT}'

if API_DOMAIN and AUTO_ORIGIN_FROM_DOMAIN and (not ALLOWED_ORIGINS or ALLOWED_ORIGINS == ['*']):
    root_domain = API_DOMAIN.replace('https://', '').replace('http://', '')
    if root_domain.startswith('api.'):
        root_domain = root_domain[4:]
    ALLOWED_ORIGINS = [API_DOMAIN, f"https://{root_domain}", f"http://{root_domain}"]

# Security
API_KEY = os.getenv('API_KEY', 'your-secret-api-key-here')  # Change this in .env file
API_KEYS = [k.strip() for k in os.getenv('API_KEYS', '').split(',') if k.strip()]
ENABLE_JWT = os.getenv('ENABLE_JWT', 'False').lower() == 'true'
JWT_SECRET = os.getenv('JWT_SECRET', '')
ALLOWED_ORIGINS = [o.strip() for o in os.getenv('ALLOWED_ORIGINS', '*').split(',') if o.strip()]
AUTO_ORIGIN_FROM_DOMAIN = os.getenv('AUTO_ORIGIN_FROM_DOMAIN', 'True').lower() == 'true'

# Rate limiting
RATE_LIMIT_PER_MINUTE_KEY = int(os.getenv('RATE_LIMIT_PER_MINUTE_KEY', '60'))
RATE_LIMIT_PER_MINUTE_IP = int(os.getenv('RATE_LIMIT_PER_MINUTE_IP', '120'))

# Request limits
MAX_CONTENT_LENGTH_MB = int(os.getenv('MAX_CONTENT_LENGTH_MB', '1'))

# Scrape behavior
HEADLESS_MODE = os.getenv('HEADLESS_MODE', 'True').lower() == 'true'
SCRAPE_TIMEOUT_SECONDS = int(os.getenv('SCRAPE_TIMEOUT_SECONDS', '30'))
SCRAPE_MAX_RETRIES = int(os.getenv('SCRAPE_MAX_RETRIES', '2'))
MAX_CONCURRENCY = int(os.getenv('MAX_CONCURRENCY', '3'))

# Proxy support
PROXY_URLS = [p.strip() for p in os.getenv('PROXY_URLS', '').split(',') if p.strip()]

# Cache
CACHE_TTL_SECONDS = int(os.getenv('CACHE_TTL_SECONDS', '300'))
CACHE_MAX_ITEMS = int(os.getenv('CACHE_MAX_ITEMS', '1000'))

# Readiness checks
READY_CHECK_ASIN = os.getenv('READY_CHECK_ASIN', '')
READY_CHECK_COUNTRY = os.getenv('READY_CHECK_COUNTRY', 'US')
READY_CHECK_INTERVAL_SECONDS = int(os.getenv('READY_CHECK_INTERVAL_SECONDS', '900'))

# Config validation
STRICT_ENV_VALIDATE = os.getenv('STRICT_ENV_VALIDATE', 'False').lower() == 'true'

# Supported Amazon Countries
AMAZON_COUNTRIES = {
    'US': {
        'name': 'United States',
        'domain': 'amazon.com',
        'currency': '$',
        'currency_code': 'USD'
    },
    'CA': {
        'name': 'Canada',
        'domain': 'amazon.ca',
        'currency': 'C$',
        'currency_code': 'CAD'
    },
    'MX': {
        'name': 'Mexico',
        'domain': 'amazon.com.mx',
        'currency': 'MX$',
        'currency_code': 'MXN'
    },
    'BR': {
        'name': 'Brazil',
        'domain': 'amazon.com.br',
        'currency': 'R$',
        'currency_code': 'BRL'
    },
    'UK': {
        'name': 'United Kingdom',
        'domain': 'amazon.co.uk',
        'currency': '£',
        'currency_code': 'GBP'
    },
    'DE': {
        'name': 'Germany',
        'domain': 'amazon.de',
        'currency': '€',
        'currency_code': 'EUR'
    },
    'FR': {
        'name': 'France',
        'domain': 'amazon.fr',
        'currency': '€',
        'currency_code': 'EUR'
    },
    'IT': {
        'name': 'Italy',
        'domain': 'amazon.it',
        'currency': '€',
        'currency_code': 'EUR'
    },
    'ES': {
        'name': 'Spain',
        'domain': 'amazon.es',
        'currency': '€',
        'currency_code': 'EUR'
    },
    'NL': {
        'name': 'Netherlands',
        'domain': 'amazon.nl',
        'currency': '€',
        'currency_code': 'EUR'
    },
    'AE': {
        'name': 'UAE',
        'domain': 'amazon.ae',
        'currency': 'AED',
        'currency_code': 'AED'
    },
    'IN': {
        'name': 'India',
        'domain': 'amazon.in',
        'currency': '₹',
        'currency_code': 'INR'
    },
    'JP': {
        'name': 'Japan',
        'domain': 'amazon.co.jp',
        'currency': '¥',
        'currency_code': 'JPY'
    },
    'AU': {
        'name': 'Australia',
        'domain': 'amazon.com.au',
        'currency': 'A$',
        'currency_code': 'AUD'
    },
    'SG': {
        'name': 'Singapore',
        'domain': 'amazon.sg',
        'currency': 'S$',
        'currency_code': 'SGD'
    }
}

def get_country_from_url(url):
    """Detect country code from Amazon URL"""
    url_lower = url.lower()

    for country_code, config in AMAZON_COUNTRIES.items():
        if config['domain'] in url_lower:
            return country_code

    return None


def get_allowed_domains():
    return [cfg['domain'] for cfg in AMAZON_COUNTRIES.values()]


def validate_config():
    errors = []
    if API_KEY == 'your-secret-api-key-here' and not API_KEYS:
        errors.append('API_KEY is not set to a secure value')
    if ENABLE_JWT and not JWT_SECRET:
        errors.append('JWT_SECRET is required when ENABLE_JWT is true')
    if MAX_CONCURRENCY < 1:
        errors.append('MAX_CONCURRENCY must be at least 1')
    return errors
