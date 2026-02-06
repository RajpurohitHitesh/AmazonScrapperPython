# 🚀 Quick Start Guide - Amazon Scraper API

## Get started in 5 minutes!

### Step 1: Download

**Option A: Git Clone (Recommended)**
```bash
git clone https://github.com/RajpurohitHitesh/AmazonScrapperPython.git
cd AmazonScrapperPython
```

**Option B: ZIP Download**
1. Go to GitHub and click "Code" → "Download ZIP"
2. Extract the ZIP
3. Navigate to the folder

---

### Step 2: Install

**On Windows:**
```bash
# Double-click:
start.bat

# or in Command Prompt:
pip install -r requirements.txt
python -m playwright install chromium
```

**On Linux/Mac:**
```bash
# In Terminal:
chmod +x start.sh
./start.sh

# or manually:
pip3 install -r requirements.txt
python3 -m playwright install chromium
```

**Run with Docker (optional):**
```bash
docker build -t amazon-scraper-api .
docker run -p 5000:5000 --env-file .env amazon-scraper-api
# or
docker-compose up --build
```

---

### Step 3: Configure

**1. Create environment file:**
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

**2. Edit `.env` file:**
```bash
# Change only this line:
API_KEY=your_secure_api_key_here
```

**💡 Generate a secure API Key:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output and paste it in `.env`.

---

### Step 4: Run

```bash
python api_server.py
```

**You'll see:**
JSON logs in console and api.log

✅ **Server is running!**
- **Local:** http://127.0.0.1:5000
- **Production:** https://your-domain.com (if configured)
- **Docs:** http://127.0.0.1:5000/docs
- **Metrics:** http://127.0.0.1:5000/metrics

---

### Step 5: Test

**Option 1: Browser**
```
# Local
http://127.0.0.1:5000/api/health

# Production
https://your-domain.com/api/health
```

**Option 2: cURL**
```bash
# Local
curl http://127.0.0.1:5000/api/health

# Production
curl https://your-domain.com/api/health
```

**Option 3: Python**
```python
import requests

# Change base_url based on your setup
base_url = "http://127.0.0.1:5000"  # Local
# base_url = "https://your-domain.com"  # Production

# Scrape a product
url = f"{base_url}/api/scrape"
headers = {"X-API-Key": "your_api_key_here"}
data = {"url": "https://www.amazon.in/dp/B0FMDNZ61S"}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

---

## 📋 Common Commands

### Server Start/Stop

**Start:**
```bash
python api_server.py
```

**Stop:**
```
Ctrl + C
```

### Check Status
```bash
# Local
curl http://127.0.0.1:5000/api/health

# Production
curl https://your-domain.com/api/health
```

### View Logs
```bash
# View log file
cat api.log           # Linux/Mac
type api.log          # Windows
```

---

## 🔥 Usage Examples

**Note:** Replace URL based on your setup:
- **Local:** `http://127.0.0.1:5000`
- **Production:** `https://your-domain.com`

### 1. Health Check
```bash
curl http://127.0.0.1:5000/api/health  # Local
```

### 2. Scrape Indian Product
```bash
# Local
curl -X POST http://127.0.0.1:5000/api/scrape \
  -H "X-API-Key: your_key" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.amazon.in/dp/B0FMDNZ61S"}'
```

### 3. Scrape US Product
```bash
# Local
curl -X POST http://127.0.0.1:5000/api/scrape \
  -H "X-API-Key: your_key" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.amazon.com/dp/B08N5WRWNW"}'
```

### 4. Get Supported Countries
```bash
curl http://127.0.0.1:5000/api/countries  # Local
```

---

## 🐛 Troubleshooting

### Error: "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Error: "Port already in use"
```bash
# Change port in .env
API_PORT=5001
```

### Error: "Invalid API Key"
```bash
# Check API_KEY in .env
# and use the same key in requests
```

### Playwright Browser Issues
```bash
# Reinstall browser binaries
python -m playwright install chromium
```

---

## 🎯 Next Steps

1. ✅ Read the [Full Documentation](README.md)
2. ✅ See the [VPS Deployment Guide](INSTALL.txt)
3. ✅ Check [Contributing Guidelines](CONTRIBUTING.md)
4. ✅ Integrate into your application

---

## 💡 Pro Tips

- **Development:** Keep `DEBUG_MODE=True` in `.env`
- **Production:** Set `DEBUG_MODE=False` and use a strong API key
- **Logs:** Regularly check logs to monitor issues
- **Updates:** Pull the repository regularly for new features

---

## 📞 Need Help?

- 📖 [Full Documentation](README.md)
- 🐛 [Report Issues](https://github.com/RajpurohitHitesh/AmazonScrapperPython/issues)
- 💬 [Discussions](https://github.com/RajpurohitHitesh/AmazonScrapperPython/discussions)

---

<div align="center">

**Happy Scraping! 🎉**

</div>
