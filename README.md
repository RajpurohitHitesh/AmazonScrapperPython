# Amazon Scraper API - Multi-Country Product Scraping

## 🎯 Overview

REST API service for scraping Amazon product data across 15 countries. Built with Flask, Selenium, and BeautifulSoup for reliable data extraction.

## 📁 Project Structure

```
AmazonScraper/
├── api_server.py           # Flask API server
├── api_config.py           # Country configurations
├── .env                    # Environment configuration
├── .env.example            # Example environment file
├── requirements.txt        # Python dependencies
├── INSTALL.txt             # Complete installation & VPS deployment guide
├── README.md               # This file
└── scrapers/
    ├── base_scraper.py     # Base scraper class
    ├── india_scraper.py    # Amazon India
    ├── usa_scraper.py      # Amazon USA
    └── uk_scraper.py       # Amazon UK
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Microsoft Edge browser
- Internet connection

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure environment:**
```bash
copy .env.example .env
```

Edit `.env` and set your API key:
```
API_KEY=your_secret_api_key_here
```

3. **Run the server:**
```bash
python api_server.py
```

Server starts at: http://127.0.0.1:5000

## 📡 API Endpoints

### Health Check
```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "supported_countries": 15
}
```

### Scrape Product
```bash
POST /api/scrape
Headers: X-API-Key: your_api_key_here
         Content-Type: application/json

Body:
{
  "product_url": "https://www.amazon.in/dp/B0FMDNZ61S"
}
```

Response (12 essential fields):
```json
{
  "success": true,
  "data": {
    "asin": "B0FMDNZ61S",
    "merchant": "Amazon",
    "name": "Product Name",
    "category": "Category",
    "subcategory": "Subcategory",
    "brand": "Brand Name",
    "current_price": 1299.00,
    "original_price": 1999.00,
    "stock_status": "In Stock",
    "image_path": "https://...",
    "rating": 4.2,
    "review_count": 1850
  }
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

## 📦 Response Fields

The API returns only 12 essential fields (no bloat):

1. **asin** - Amazon Standard Identification Number
2. **merchant** - Seller name (Amazon, Cloudtail, etc.)
3. **name** - Product title
4. **category** - Main category
5. **subcategory** - Subcategory
6. **brand** - Brand name
7. **current_price** - Current price (numeric)
8. **original_price** - Original/MRP price (numeric)
9. **stock_status** - "In Stock" or "Out of Stock"
10. **image_path** - Main product image URL
11. **rating** - Average rating (0-5)
12. **review_count** - Number of reviews

## 🔗 Laravel Integration

### Service Class
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
    'url' => env('AMAZON_SCRAPER_URL', 'http://127.0.0.1:5000'),
    'api_key' => env('AMAZON_SCRAPER_API_KEY'),
    'timeout' => env('AMAZON_SCRAPER_TIMEOUT', 60),
],
```

### Environment (.env)
```bash
AMAZON_SCRAPER_URL=http://127.0.0.1:5000
AMAZON_SCRAPER_API_KEY=1AqqRHyRhnlWzvljsvjD011dROrTeS3jqVxmqZHUFDqnbe1zLZ5bqxE5wVMVXgwF
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
# Check status
