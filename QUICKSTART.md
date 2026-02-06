# 🚀 Quick Start Guide - Amazon Scraper API

## 5 मिनट में Setup करें!

### Step 1: Download करें

**Option A: Git Clone (Recommended)**
```bash
git clone https://github.com/yourusername/AmazonScrapperPython.git
cd AmazonScrapperPython
```

**Option B: ZIP Download**
1. GitHub पर जाएं और "Code" → "Download ZIP" click करें
2. ZIP extract करें
3. Folder में navigate करें

---

### Step 2: Install करें

**Windows पर:**
```bash
# Double-click करें:
start.bat

# या Command Prompt में:
pip install -r requirements.txt
```

**Linux/Mac पर:**
```bash
# Terminal में:
chmod +x start.sh
./start.sh

# या manually:
pip3 install -r requirements.txt
```

---

### Step 3: Configure करें

**1. Environment file बनाएं:**
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

**2. `.env` file edit करें:**
```bash
# सिर्फ ये line change करें:
API_KEY=your_secure_api_key_here
```

**💡 Secure API Key generate करें:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Output को copy करके `.env` में paste कर दें।

---

### Step 4: Run करें

```bash
python api_server.py
```

**Output दिखेगा:**
```
============================================================
🚀 AmazonScraper API Server
============================================================
📅 Started: 2026-02-06 10:30:45
🌐 Host: 0.0.0.0:5000
🔐 API Key Authentication: Enabled
🌍 Supported Countries: 15
============================================================
```

✅ **Server चालू है!** http://127.0.0.1:5000

---

### Step 5: Test करें

**Option 1: Browser से**
```
http://127.0.0.1:5000/health
```

**Option 2: cURL से**
```bash
curl http://127.0.0.1:5000/health
```

**Option 3: Python से**
```python
import requests

# Product scrape करें
url = "http://127.0.0.1:5000/api/scrape"
headers = {"X-API-Key": "your_api_key_here"}
data = {"product_url": "https://www.amazon.in/dp/B0FMDNZ61S"}

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
curl http://127.0.0.1:5000/health
```

### View Logs
```bash
# Log file देखें
cat api.log           # Linux/Mac
type api.log          # Windows
```

---

## 🔥 Usage Examples

### 1. Health Check
```bash
curl http://127.0.0.1:5000/health
```

### 2. Scrape Indian Product
```bash
curl -X POST http://127.0.0.1:5000/api/scrape \
  -H "X-API-Key: your_key" \
  -H "Content-Type: application/json" \
  -d '{"product_url": "https://www.amazon.in/dp/B0FMDNZ61S"}'
```

### 3. Scrape US Product
```bash
curl -X POST http://127.0.0.1:5000/api/scrape \
  -H "X-API-Key: your_key" \
  -H "Content-Type: application/json" \
  -d '{"product_url": "https://www.amazon.com/dp/B08N5WRWNW"}'
```

### 4. Get Supported Countries
```bash
curl http://127.0.0.1:5000/api/countries
```

---

## 🐛 Troubleshooting

### Error: "Module not found"
```bash
# Dependencies फिर से install करें
pip install -r requirements.txt --force-reinstall
```

### Error: "Port already in use"
```bash
# .env में port change करें
API_PORT=5001
```

### Error: "Invalid API Key"
```bash
# .env में API_KEY check करें
# और request में same key use करें
```

### Browser/WebDriver Issues
```bash
# Internet connection check करें
# First run पर WebDriver auto-download होगा
```

---

## 🎯 Next Steps

1. ✅ [Full Documentation](README.md) पढ़ें
2. ✅ [VPS Deployment Guide](INSTALL.txt) देखें
3. ✅ [Contributing Guidelines](CONTRIBUTING.md) देखें
4. ✅ अपनी application में integrate करें

---

## 💡 Pro Tips

- **Development:** `DEBUG_MODE=True` रखें `.env` में
- **Production:** `DEBUG_MODE=False` करें और proper API key use करें
- **Logs:** Regular logs check करें issues देखने के लिए
- **Updates:** Repository regularly pull करें नए features के लिए

---

## 📞 Need Help?

- 📖 [Full Documentation](README.md)
- 🐛 [Report Issues](https://github.com/yourusername/AmazonScrapperPython/issues)
- 💬 [Discussions](https://github.com/yourusername/AmazonScrapperPython/discussions)

---

<div align="center">

**Happy Scraping! 🎉**

</div>
