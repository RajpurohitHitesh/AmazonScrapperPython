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

# Get base URL for API
def get_base_url():
    """Get the base URL for the API (domain or localhost)"""
    if API_DOMAIN:
        return API_DOMAIN.rstrip('/')
    return f'http://127.0.0.1:{API_PORT}'

# Security
API_KEY = os.getenv('API_KEY', 'your-secret-api-key-here')  # Change this in .env file
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*').split(',')

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
