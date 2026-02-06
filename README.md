# Amazon Scraper API - Multi-Country Product Scraping

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Selenium](https://img.shields.io/badge/Selenium-4.15-red.svg)

**A powerful REST API service for scraping product data from 15+ Amazon marketplaces worldwide**

[Features](#-features) • [Installation](#-installation) • [Quick Start](QUICKSTART.md) • [Usage](#-api-usage) • [Contributing](CONTRIBUTING.md)

</div>

---

## 🎯 Overview

REST API service for scraping Amazon product data across 15 countries. Built with Flask, Selenium, and BeautifulSoup for reliable data extraction. 

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
- ✅ **Anti-Detection** - Built-in browser fingerprinting prevention
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
- Microsoft Edge browser
- Internet connection

### Quick Setup

**1. Clone the repository:**
```bash
git clone https://github.com/RajpurohitHitesh/AmazonScrapperPython.git
cd AmazonScrapperPython
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
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

## 📡 API Usage

**Base URL:**
- **Local Development:** `http://127.0.0.1:5000`
- **Production:** `https://your-domain.com` (configure in `.env`)

### Health Check
Check if API is running:

```bash
# Local
curl http://127.0.0.1:5000/health

# Production
curl https://your-domain.com/health
```

Response:
```json
{
  "status": "healthy",
  "supported_countries": 15
}
```

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
  "product_url": "https://www.amazon.in/dp/B0FMDNZ61S"
}
```

**Example with cURL:**
```bash
# Local
curl -X POST http://127.0.0.1:5000/api/scrape \
  -H "X-API-Key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"product_url": "https://www.amazon.in/dp/B0FMDNZ61S"}'

# Production
curl -X POST https://your-domain.com/api/scrape \
  -H "X-API-Key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"product_url": "https://www.amazon.in/dp/B0FMDNZ61S"}'
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
    "product_url": "https://www.amazon.in/dp/B0FMDNZ61S"
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

**Success Response:**
```json
{
  "success": true,
  "data": {
    "asin": "B0FMDNZ61S",
    "merchant": "Amazon India",
    "name": "Product Name",
    "category": "Electronics",
    "subcategory": "Smartphones",
    "brand": "Samsung",
    "current_price": 1299.00,
    "original_price": 1999.00,
    "stock_status": "In Stock",
    "image_path": "https://m.media-amazon.com/images/I/...",
    "rating": 4.2,
    "review_count": 1850
  },
  "country": "India",
  "scrape_time": "2.45s"
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
  "message": "Please provide a valid Amazon product URL"
}
```

## 📦 Response Fields

API returns 12 essential fields:

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
| `stock_status` | string | "In Stock" or "Out of Stock" |
| `image_path` | string | Main product image URL |
| `rating` | float | Average rating (0-5) |
| `review_count` | int | Number of reviews |

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

# Application
DEBUG_MODE=True           # Enable debug logging
HEADLESS_MODE=False       # Run browser without GUI
BROWSER_TIMEOUT=30        # Browser timeout in seconds

# CORS
ALLOWED_ORIGINS=http://localhost:8000,https://yourdomain.com
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

## 📦 Response Fields

API returns 12 essential fields:

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
| `stock_status` | string | "In Stock" or "Out of Stock" |
| `image_path` | string | Main product image URL |
| `rating` | float | Average rating (0-5) |
| `review_count` | int | Number of reviews |

## 🏗️ Architecture

### Base Scraper Class
All country scrapers inherit from `BaseAmazonScraper`:
- Browser initialization with anti-detection
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

1. Create new scraper file:
```python
# scrapers/germany_scraper.py
from scrapers.base_scraper import BaseAmazonScraper

class GermanyScraper(BaseAmazonScraper):
    def scrape_product(self, url):
        # Implement Germany-specific scraping
        pass
```

2. Add to `api_config.py`:
```python
AMAZON_COUNTRIES = {
    'DE': {
        'name': 'Germany',
        'domain': 'amazon.de',
        'currency': 'EUR',
        'scraper': 'germany_scraper.GermanyScraper'
    }
}
```

3. Import in `api_server.py`:
```python
from scrapers.germany_scraper import GermanyScraper
```

## 📊 Logging

### Development
- Console output with DEBUG_MODE=True
- Real-time scraping progress

### Production
- Output log: `/home/amazonscraper/app/logs/output.log`
- Error log: `/home/amazonscraper/app/logs/error.log`
- Systemd journal: `sudo journalctl -u amazon-scraper-api`

## 🐛 Troubleshooting

### WebDriver Issues
```bash
# Auto-download on first run
# Requires internet connection
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
# Check statussudo systemctl status amazon-scraper-api

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