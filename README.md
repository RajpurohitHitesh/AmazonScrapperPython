# Amazon Scraper API - Multi-Country Product Scraping

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Playwright](https://img.shields.io/badge/Playwright-1.41-purple.svg)

**A powerful REST API service for scraping product data from 15+ Amazon marketplaces worldwide**

[Features](#-features) • [Installation](#-installation) • [Quick Start](QUICKSTART.md) • [Usage](#-api-usage) • [Contributing](CONTRIBUTING.md)

</div>

---

## 🎯 Overview

REST API service for scraping Amazon product data across 15 countries. Built with Flask, Playwright, and BeautifulSoup for reliable data extraction. 

**Perfect for:**
- E-commerce price monitoring
- Product research & analytics
- Inventory management systems
- Market research applications

## ✨ Features

- ✅ **15+ Amazon Marketplaces** - Support for US, UK, India, Japan, and more
- ✅ **Auto Country Detection** - Automatically detects country from URL
- ✅ **12 Essential Fields** - Clean, structured product data
- ✅ **API Authentication** - Secure API key-based access
- ✅ **Anti-Detection** - Playwright with stealth scripts + device profiles
- ✅ **Rate Limiting** - Per API key/IP throttling
- ✅ **Metrics** - Prometheus-ready /metrics endpoint
- ✅ **Swagger UI** - Interactive API docs at /docs
- ✅ **Caching** - Short TTL cache by ASIN + country
- ✅ **Easy Deployment** - One-command setup for VPS
- ✅ **CORS Support** - Ready for web applications
- ✅ **Production Ready** - Systemd service, logging, error handling

## 📁 Project Structure

```
AmazonScrapperPython/
├── api_server.py           # Flask API server
├── api_config.py           # Country configurations
├── .env.example            # Example environment file
├── .gitignore              # Git ignore rules
├── requirements.txt        # Python dependencies
├── setup.py                # Package installation
├── LICENSE                 # MIT License
├── INSTALL.txt             # Detailed installation guide
├── CONTRIBUTING.md         # Contribution guidelines
├── README.md               # This file
├── start.bat               # Quick start (Windows)
├── start.sh                # Quick start (Linux/Mac)
└── scrapers/
    ├── __init__.py
    ├── base_scraper.py     # Base scraper class
    ├── india_scraper.py    # Amazon India
    ├── usa_scraper.py      # Amazon USA
    └── uk_scraper.py       # Amazon UK
```

## 🚀 Installation

### Method 1: Quick Start (Recommended)

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

Script automatically:
- ✅ Checks Python installation
- ✅ Installs dependencies
- ✅ Creates .env file
- ✅ Starts the server

### Method 2: Manual Installation

### Prerequisites
- Python 3.7 or higher
- Internet connection (for Playwright browser downloads)

### Quick Setup

**1. Clone the repository:**
```bash
git clone https://github.com/RajpurohitHitesh/AmazonScrapperPython.git
cd AmazonScrapperPython
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
python -m playwright install chromium
```

**3. Configure environment:**
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

**4. Edit `.env` and set your API key:**
```bash
API_KEY=your_secure_api_key_here
```

**💡 Tip:** Generate a secure API key with:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**5. Run the server:**
```bash
python api_server.py
```

Server will start at: http://127.0.0.1:5000

✅ **Installation complete!** You can now use the API.

### Method 3: Docker (Recommended for server/deployment)

**Build and run:**
```bash
docker build -t amazon-scraper-api .
docker run -p 5000:5000 --env-file .env amazon-scraper-api
```

**Or with docker-compose:**
```bash
docker-compose up --build
```

Configure your domain in `.env`:
```dotenv
API_DOMAIN=https://api.yourdomain.com
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

## 📡 API Usage

**Base URL:**
- **Local Development:** `http://127.0.0.1:5000`
- **Production:** `https://your-domain.com` (configure in `.env`)

### Health Check
Check if API is running:

```bash
# Local
curl http://127.0.0.1:5000/api/health

# Production
curl https://your-domain.com/api/health
```

### Readiness (for load balancers/containers)
```bash
# Local
curl http://127.0.0.1:5000/api/ready

# Production
curl https://your-domain.com/api/ready
```

### Swagger UI
Open interactive docs at:
- Local: http://127.0.0.1:5000/docs
- Production: https://your-domain.com/docs

### Metrics
Prometheus endpoint:
- Local: http://127.0.0.1:5000/metrics
- Production: https://your-domain.com/metrics

Response includes queue depth and cache size.

### Scrape Product

**Endpoint:** `POST /api/scrape`

**Headers:**
```
X-API-Key: your_api_key_here
Content-Type: application/json
```

**Request Body:**
```json
{
  "url": "https://www.amazon.in/dp/B0FMDNZ61S",
  "headless": true,
  "proxy": "http://user:pass@host:port"
}
```

**Example with cURL:**
```bash
# Local
curl -X POST http://127.0.0.1:5000/api/scrape \
  -H "X-API-Key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.amazon.in/dp/B0FMDNZ61S"}'

# Production
curl -X POST https://your-domain.com/api/scrape \
  -H "X-API-Key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.amazon.in/dp/B0FMDNZ61S"}'
```

**Example with Python:**
```python
import requests

# Change base_url based on your setup
base_url = "http://127.0.0.1:5000"  # Local
# base_url = "https://your-domain.com"  # Production

url = f"{base_url}/api/scrape"
headers = {
    "X-API-Key": "your_api_key_here",
    "Content-Type": "application/json"
}
data = {
    "url": "https://www.amazon.in/dp/B0FMDNZ61S"
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

**Success Response:**
```json
{
  "success": true,
  "cached": false,
  "country": "India",
  "country_code": "IN",
  "detected_country": "IN",
  "data": {
    "asin": "B0FMDNZ61S",
    "merchant": "Amazon India",
    "name": "Product Name",
    "category": "Electronics",
    "subcategory": "Smartphones",
    "brand": "Samsung",
    "current_price": 1299.00,
    "original_price": 1999.00,
    "currency": "₹",
    "currency_code": "INR",
    "stock_status": "in_stock",
    "image_path": "https://m.media-amazon.com/images/I/...",
    "images": ["https://m.media-amazon.com/images/I/..."],
    "rating": 4.2,
    "review_count": 1850,
    "bullet_points": ["..."],
    "variations": ["Color", "Size"],
    "delivery_eta": "Tomorrow",
    "seller": {
      "name": "Amazon",
      "fulfilled_by_amazon": true
    },
    "offers_count": 5,
    "buy_box_winner": "Amazon",
    "seller_type": "amazon",
    "description": "...",
    "specifications": {
      "Brand": "Samsung"
    }
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Invalid URL",
  "message": "Please provide a valid Amazon product URL"
}
```

## 📦 Response Fields

API returns these fields (when available):

| Field | Type | Description |
|-------|------|-------------|
| `asin` | string | Amazon Standard Identification Number |
| `merchant` | string | Country-specific Amazon (e.g., Amazon India, Amazon USA) |
| `name` | string | Product title |
| `category` | string | Main category |
| `subcategory` | string | Subcategory |
| `brand` | string | Brand name |
| `current_price` | float | Current price (numeric) |
| `original_price` | float | Original/MRP price (numeric) |
| `currency` | string | Currency symbol |
| `currency_code` | string | Currency code |
| `stock_status` | string | `in_stock` or `out_of_stock` |
| `image_path` | string | Main product image URL |
| `images` | array | Additional image URLs |
| `rating` | float | Average rating (0-5) |
| `review_count` | int | Number of reviews |
| `bullet_points` | array | Key feature bullets |
| `variations` | array | Variation labels (e.g., size/color) |
| `delivery_eta` | string | Delivery estimate (if shown) |
| `seller` | object | Seller info (name, FBA) |
| `offers_count` | int | Offers count (if shown) |
| `buy_box_winner` | string | Buy box seller (if shown) |
| `seller_type` | string | `amazon` or `marketplace` |
| `description` | string | Description text |
| `specifications` | object | Key-value specs |

## 🌍 Supported Countries (15 Amazon Marketplaces)

| Country | Domain | Currency |
|---------|--------|----------|
| 🇺🇸 United States | amazon.com | USD |
| 🇨🇦 Canada | amazon.ca | CAD |
| 🇲🇽 Mexico | amazon.com.mx | MXN |
| 🇧🇷 Brazil | amazon.com.br | BRL |
| 🇬🇧 United Kingdom | amazon.co.uk | GBP |
| 🇩🇪 Germany | amazon.de | EUR |
| 🇫🇷 France | amazon.fr | EUR |
| 🇮🇹 Italy | amazon.it | EUR |
| 🇪🇸 Spain | amazon.es | EUR |
| 🇳🇱 Netherlands | amazon.nl | EUR |
| 🇦🇪 UAE | amazon.ae | AED |
| 🇮🇳 India | amazon.in | INR |
| 🇯🇵 Japan | amazon.co.jp | JPY |
| 🇦🇺 Australia | amazon.com.au | AUD |
| 🇸🇬 Singapore | amazon.sg | SGD |

## 🔧 Configuration

### Environment Variables (.env)

```bash
# API Server
API_HOST=0.0.0.0          # 0.0.0.0 for public, 127.0.0.1 for local
API_PORT=5000             # Server port
API_KEY=your_key_here     # Authentication key
API_KEYS=key1,key2        # Optional rotated keys
ENABLE_JWT=False          # Optional JWT auth
JWT_SECRET=your_secret

# Application
DEBUG_MODE=True           # Enable debug logging
HEADLESS_MODE=True        # Run browser without GUI
SCRAPE_TIMEOUT_SECONDS=30 # Scrape timeout
SCRAPE_MAX_RETRIES=2      # Retry attempts
MAX_CONCURRENCY=3         # Max concurrent scrapes
PROXY_URLS=               # Optional proxy list (comma-separated)

# CORS
ALLOWED_ORIGINS=http://localhost:8000,https://yourdomain.com

# Rate limiting
RATE_LIMIT_PER_MINUTE_KEY=60
RATE_LIMIT_PER_MINUTE_IP=120

# Cache
CACHE_TTL_SECONDS=300
CACHE_MAX_ITEMS=1000

# Readiness checks
READY_CHECK_ASIN=
READY_CHECK_COUNTRY=US
READY_CHECK_INTERVAL_SECONDS=900
```

## 🔐 Authentication

All API requests require authentication via API key:

**Method 1: Header (Recommended)**
```bash
X-API-Key: your_api_key_here
```

**Method 2: Query Parameter**
```bash
?api_key=your_api_key_here
```

**Optional JWT:**
```bash
Authorization: Bearer <jwt>
```

## 🏗️ Architecture

### Base Scraper Class
All country scrapers inherit from `BaseAmazonScraper`:
- Playwright browser contexts with stealth scripts
- ASIN extraction from URLs
- Common scraping methods
- Error handling

### Country-Specific Scrapers
Each country has its own scraper module:
- `india_scraper.py` - Amazon India
- `usa_scraper.py` - Amazon USA
- `uk_scraper.py` - Amazon UK
- More countries coming soon...

### Automatic Country Detection
API automatically detects country from product URL:
```python
amazon.in → India Scraper
amazon.com → USA Scraper
amazon.co.uk → UK Scraper
```

## 🔗 Integration Examples

### Laravel (PHP)
```php
use App\Services\AmazonScraperService;

$scraper = new AmazonScraperService();
$result = $scraper->scrapeProduct('https://www.amazon.in/dp/B0FMDNZ61S');

if ($result['success']) {
    $data = $result['data'];
    // Use data...
}
```

### Configuration (config/services.php)
```php
'amazon_scraper' => [
    'url' => env('AMAZON_SCRAPER_URL', 'http://127.0.0.1:5000'),  // Local or production URL
    'api_key' => env('AMAZON_SCRAPER_API_KEY'),
    'timeout' => env('AMAZON_SCRAPER_TIMEOUT', 60),
],
```

### Environment (.env)
```bash
# Local Development
AMAZON_SCRAPER_URL=http://127.0.0.1:5000

# Production
# AMAZON_SCRAPER_URL=https://your-domain.com

AMAZON_SCRAPER_API_KEY=your_api_key_here
AMAZON_SCRAPER_TIMEOUT=60
```

## 🖥️ VPS Deployment (Always Running)

For production deployment on VPS with systemd service (24/7 operation):

**See INSTALL.txt for complete guide including:**
- Ubuntu/Debian setup
- Systemd service configuration
- Nginx reverse proxy
- SSL certificate setup
- Firewall configuration
- Always-running configuration
- Monitoring and logs

Quick command to make it always run:
```bash
sudo systemctl enable amazon-scraper-api
sudo systemctl start amazon-scraper-api
```

## 🛠️ Development

### Adding New Country Scraper

1. Add country in `api_config.py`:
```python
AMAZON_COUNTRIES = {
    'DE': {
        'name': 'Germany',
        'domain': 'amazon.de',
        'currency': 'EUR',
    'currency_code': 'EUR'
    }
}
```

2. (Optional) Add a custom scraper if needed and register in `get_scraper_for_country`.

## 📊 Logging

### Development
- JSON logs to console with DEBUG_MODE=True
- Request IDs in logs

### Production
- File log: `api.log`
- Systemd journal: `sudo journalctl -u amazon-scraper-api`

## 🐛 Troubleshooting

### Playwright Browser Issues
```bash
# Reinstall browser binaries
python -m playwright install chromium
```

### Port Already in Use
```bash
# Change API_PORT in .env
API_PORT=5001
```

### CORS Errors
```bash
# Add your domain to ALLOWED_ORIGINS
ALLOWED_ORIGINS=https://yourdomain.com,http://localhost:8000
```

### Service Not Starting (VPS)
```bash
# Check status
sudo systemctl status amazon-scraper-api

# View logs
sudo journalctl -u amazon-scraper-api -f
```

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Ways to contribute:**
- 🐛 Report bugs
- 💡 Suggest features
- 🌍 Add new country scrapers
- 📝 Improve documentation
- ⚡ Optimize performance

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

**Disclaimer:** This software is for educational purposes only. Users are responsible for complying with Amazon's Terms of Service.

## 🙏 Support

If you find this project helpful:

- ⭐ Star the repository
- 🐛 Report issues
- 🔀 Submit pull requests
- 📢 Share with others

## 📞 Contact

- **Issues:** [GitHub Issues](https://github.com/RajpurohitHitesh/AmazonScrapperPython/issues)
- **Discussions:** [GitHub Discussions](https://github.com/RajpurohitHitesh/AmazonScrapperPython/discussions)
- **Email:** your.email@example.com

---

<div align="center">

Made with ❤️ for the developer community

**[⬆ Back to Top](#amazon-scraper-api---multi-country-product-scraping)**

</div>