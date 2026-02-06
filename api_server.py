"""
AmazonScraper Flask API
Main API server to handle scraping requests from clients.
"""

import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from datetime import datetime
from functools import wraps
from uuid import uuid4

import jwt
from flask import Flask, request, jsonify, g, Response
from flask_cors import CORS
from flasgger import Swagger
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from services.browser_manager import BrowserManager
from services.cache import TTLCache
from services.circuit_breaker import CircuitBreaker
from services.metrics import REQUESTS_TOTAL, SCRAPE_TOTAL, CAPTCHA_TOTAL, SCRAPE_DURATION, QUEUE_DEPTH, CACHE_SIZE
from services.rate_limit import RateLimiter
from utils.logging_config import configure_logging
from utils.validators import validate_amazon_url

# Import configurations
from api_config import (
    API_HOST,
    API_PORT,
    DEBUG_MODE,
    API_KEY,
    API_KEYS,
    ENABLE_JWT,
    JWT_SECRET,
    ALLOWED_ORIGINS,
    AMAZON_COUNTRIES,
    get_country_from_url,
    get_allowed_domains,
    LOG_LEVEL,
    RATE_LIMIT_PER_MINUTE_KEY,
    RATE_LIMIT_PER_MINUTE_IP,
    MAX_CONTENT_LENGTH_MB,
    HEADLESS_MODE,
    SCRAPE_TIMEOUT_SECONDS,
    SCRAPE_MAX_RETRIES,
    MAX_CONCURRENCY,
    PROXY_URLS,
    CACHE_TTL_SECONDS,
    CACHE_MAX_ITEMS,
    READY_CHECK_ASIN,
    READY_CHECK_COUNTRY,
    READY_CHECK_INTERVAL_SECONDS,
    STRICT_ENV_VALIDATE,
    validate_config,
)
from scrapers.india_scraper import IndiaScraper
from scrapers.usa_scraper import USAScraper
from scrapers.uk_scraper import UKScraper
from scrapers.generic_scraper import GenericScraper

# Initialize Flask app
logger = configure_logging(LOG_LEVEL)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH_MB * 1024 * 1024
CORS(app, origins=ALLOWED_ORIGINS)

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "AmazonScraper API",
        "version": "2.0.0",
    },
    "securityDefinitions": {
        "ApiKeyAuth": {
            "type": "apiKey",
            "name": "X-API-Key",
            "in": "header",
        }
    },
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/openapi.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs",
}
Swagger(app, config=swagger_config, template=swagger_template)

browser_manager = BrowserManager(headless=HEADLESS_MODE)
browser_manager.start()

cache = TTLCache(ttl_seconds=CACHE_TTL_SECONDS, max_items=CACHE_MAX_ITEMS)
circuit_breaker = CircuitBreaker()
rate_limiter_key = RateLimiter(RATE_LIMIT_PER_MINUTE_KEY)
rate_limiter_ip = RateLimiter(RATE_LIMIT_PER_MINUTE_IP)

executor = ThreadPoolExecutor(max_workers=MAX_CONCURRENCY)
queue_lock = threading.Lock()
queue_depth = 0

ready_state = {
    "ready": True,
    "last_check": None,
    "error": None,
}

allowed_domains = get_allowed_domains()

# API Key Authentication Decorator
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        provided_key = request.headers.get('X-API-Key') or request.args.get('api_key')

        if ENABLE_JWT:
            auth_header = request.headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ', 1)[1].strip()
                try:
                    jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
                    return f(*args, **kwargs)
                except Exception:
                    pass

        if not provided_key:
            return jsonify({
                'success': False,
                'error': 'API key is required',
                'message': 'Please provide API key in X-API-Key header or api_key parameter'
            }), 401

        valid_keys = set([API_KEY] + API_KEYS)
        if provided_key not in valid_keys:
            return jsonify({
                'success': False,
                'error': 'Invalid API key',
                'message': 'The provided API key is incorrect'
            }), 403

        return f(*args, **kwargs)
    
    return decorated_function


@app.before_request
def assign_request_id():
    g.request_id = str(uuid4())


@app.after_request
def track_metrics(response):
    try:
        REQUESTS_TOTAL.labels(endpoint=request.path, status=str(response.status_code)).inc()
    except Exception:
        pass
    response.headers["X-Request-Id"] = g.get("request_id", "")
    return response


@app.route('/', methods=['GET'])
def index():
    """API information endpoint"""
    html = """
    <html>
      <head><title>AmazonScraper API</title></head>
      <body>
        <h1>AmazonScraper API</h1>
        <p>Status: running</p>
        <ul>
          <li><a href="/docs">Swagger UI</a></li>
          <li><a href="/api/health">/api/health</a></li>
          <li><a href="/api/ready">/api/ready</a></li>
          <li><a href="/metrics">/metrics</a></li>
        </ul>
      </body>
    </html>
    """
    return Response(html, mimetype='text/html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint
    ---
    tags:
        - Health
    responses:
        200:
            description: Service health status
    """
    return jsonify({
        'status': 'healthy',
        'service': 'AmazonScraper API',
        'timestamp': datetime.now().isoformat(),
        'browser_running': browser_manager.is_running(),
        'queue_depth': get_queue_depth(),
        'cache_size': cache.size()
    })


@app.route('/api/ready', methods=['GET'])
def ready_check():
    """Readiness probe for deployment/containers
    ---
    tags:
        - Health
    responses:
        200:
            description: Readiness status
    """
    return jsonify({
        'ready': ready_state["ready"],
        'service': 'AmazonScraper API',
        'supported_countries': len(AMAZON_COUNTRIES),
        'auth': 'api-key',
        'timestamp': datetime.now().isoformat(),
        'last_check': ready_state["last_check"],
        'error': ready_state["error"],
    })


@app.route('/api/countries', methods=['GET'])
@require_api_key
def get_countries():
    """Get list of supported countries
    ---
    tags:
        - Countries
    security:
        - ApiKeyAuth: []
    responses:
        200:
            description: Countries list
    """
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
    ---
    tags:
        - Scrape
    security:
        - ApiKeyAuth: []
    parameters:
        - in: body
          name: body
          required: true
          schema:
            type: object
            properties:
                url:
                    type: string
                headless:
                    type: boolean
                proxy:
                    type: string
    responses:
        200:
            description: Scrape result
    """
    try:
        data = request.get_json()

        if not data or ('url' not in data and 'product_url' not in data):
            return jsonify({
                'success': False,
                'error': 'Missing required field: url',
                'message': 'Please provide Amazon product URL in request body'
            }), 400

        product_url = data.get('url') or data.get('product_url')
        headless = data.get('headless')
        proxy = data.get('proxy')

        is_valid, error_msg = validate_amazon_url(product_url, allowed_domains)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': 'Invalid URL',
                'message': error_msg
            }), 400

        api_key_for_limit = request.headers.get('X-API-Key') or request.args.get('api_key') or ''
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr or '')
        if not rate_limiter_key.is_allowed(api_key_for_limit):
            return jsonify({
                'success': False,
                'error': 'Rate limit exceeded',
                'message': 'API key rate limit exceeded'
            }), 429
        if not rate_limiter_ip.is_allowed(client_ip):
            return jsonify({
                'success': False,
                'error': 'Rate limit exceeded',
                'message': 'IP rate limit exceeded'
            }), 429
        
        # Detect country from URL
        country_code = get_country_from_url(product_url)
        
        if not country_code:
            return jsonify({
                'success': False,
                'error': 'Unsupported Amazon domain',
                'message': f'Could not detect country from URL. Supported domains: {", ".join([c["domain"] for c in AMAZON_COUNTRIES.values()])}'
            }), 400
        
        country_config = AMAZON_COUNTRIES[country_code]
        
        logger.info(f"Scraping request for {country_config['name']} ({country_code})")
        
        # Select appropriate scraper based on country
        if circuit_breaker.is_open(country_code):
            return jsonify({
                'success': False,
                'error': 'Service temporarily unavailable',
                'message': 'Circuit breaker open for this country'
            }), 503

        scraper = get_scraper_for_country(country_code, country_config)
        
        if not scraper:
            return jsonify({
                'success': False,
                'error': 'Scraper not available',
                'message': f'Scraper for {country_config["name"]} is not yet implemented'
            }), 501
        
        # Scrape the product
        cache_key = f"{country_code}:{scraper.extract_asin(product_url)}"
        cached = cache.get(cache_key)
        if cached:
            CACHE_SIZE.set(cache.size())
            return jsonify({
                'success': True,
                'country': country_config['name'],
                'country_code': country_code,
                'detected_country': country_code,
                'cached': True,
                'data': cached
            })

        start_time = time.time()
        future = submit_scrape(lambda: scraper.scrape_product(product_url, headless=headless, proxy=proxy))
        try:
            result = future.result(timeout=SCRAPE_TIMEOUT_SECONDS + 10)
        except FuturesTimeoutError:
            circuit_breaker.record_failure(country_code)
            SCRAPE_TOTAL.labels(status="timeout", country=country_code).inc()
            return jsonify({
                'success': False,
                'error': 'Timeout',
                'message': 'Scrape timed out'
            }), 504
        finally:
            duration = time.time() - start_time
            SCRAPE_DURATION.labels(country=country_code).observe(duration)
        
        # Check if scraping was successful
        if 'error' in result:
            if result.get('error_code') == 'captcha':
                CAPTCHA_TOTAL.labels(country=country_code).inc()
            circuit_breaker.record_failure(country_code)
            SCRAPE_TOTAL.labels(status="failure", country=country_code).inc()
            return jsonify({
                'success': False,
                'error': result['error'],
                'country': country_config['name'],
                'country_code': country_code
            }), 500

        circuit_breaker.record_success(country_code)
        SCRAPE_TOTAL.labels(status="success", country=country_code).inc()
        cache.set(cache_key, result)
        CACHE_SIZE.set(cache.size())
        
        # Return successful result
        return jsonify({
            'success': True,
            'country': country_config['name'],
            'country_code': country_code,
            'detected_country': country_code,
            'data': result
        })
    
    except Exception as e:
        logger.error(f"API Error: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500


def get_scraper_for_country(country_code, country_config):
    """Get the appropriate scraper instance for a country"""
    scrapers = {
        'IN': IndiaScraper,
        'US': USAScraper,
        'UK': UKScraper,
    }

    scraper_class = scrapers.get(country_code, GenericScraper)
    return scraper_class(
        country_code,
        country_config,
        browser_manager,
        timeout_seconds=SCRAPE_TIMEOUT_SECONDS,
        max_retries=SCRAPE_MAX_RETRIES,
        proxy_urls=PROXY_URLS,
        headless_default=HEADLESS_MODE,
    )


def submit_scrape(task):
    global queue_depth
    with queue_lock:
        queue_depth += 1
        QUEUE_DEPTH.set(queue_depth)

    def wrapped():
        try:
            return task()
        finally:
            global queue_depth
            with queue_lock:
                queue_depth -= 1
                QUEUE_DEPTH.set(queue_depth)

    return executor.submit(wrapped)


def get_queue_depth():
    with queue_lock:
        return queue_depth


def readiness_worker():
    if not READY_CHECK_ASIN:
        return
    while True:
        try:
            country = READY_CHECK_COUNTRY.upper()
            cfg = AMAZON_COUNTRIES.get(country)
            if not cfg:
                ready_state["ready"] = False
                ready_state["error"] = "Invalid READY_CHECK_COUNTRY"
                time.sleep(READY_CHECK_INTERVAL_SECONDS)
                continue
            url = f"https://www.{cfg['domain']}/dp/{READY_CHECK_ASIN}"
            scraper = get_scraper_for_country(country, cfg)
            result = scraper.scrape_product(url, headless=True)
            ready_state["ready"] = "error" not in result
            ready_state["error"] = result.get("error") if isinstance(result, dict) else None
        except Exception as e:
            ready_state["ready"] = False
            ready_state["error"] = str(e)
        finally:
            ready_state["last_check"] = datetime.now().isoformat()
            time.sleep(READY_CHECK_INTERVAL_SECONDS)


@app.route('/metrics', methods=['GET'])
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    config_errors = validate_config()
    if config_errors:
        logger.error("Config validation errors: " + "; ".join(config_errors))
        if STRICT_ENV_VALIDATE:
            raise SystemExit(1)

    threading.Thread(target=readiness_worker, daemon=True).start()

    app.run(host=API_HOST, port=API_PORT, debug=DEBUG_MODE)

def main():
    """Entry point for console script"""
    if __name__ == '__main__':
        return
    app.run(host=API_HOST, port=API_PORT, debug=DEBUG_MODE)
