# Contributing to Amazon Scraper API

आपका योगदान स्वागत है! 🎉

## How to Contribute

### Reporting Bugs

अगर आपको कोई bug मिलता है:

1. [GitHub Issues](https://github.com/yourusername/AmazonScrapperPython/issues) पर check करें कि वो bug पहले report हुआ है या नहीं
2. अगर नहीं, तो नया issue create करें:
   - Clear title दें
   - Steps to reproduce बताएं
   - Expected vs actual behavior explain करें
   - Screenshots attach करें (अगर possible हो)
   - Environment details दें (Python version, OS, etc.)

### Suggesting Features

नई features suggest करने के लिए:

1. Issue create करें with tag `enhancement`
2. Feature को detail में explain करें
3. Use case बताएं कि ये feature क्यों useful होगा
4. Implementation के ideas share करें (optional)

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/AmazonScrapperPython.git
   cd AmazonScrapperPython
   ```

2. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Code clean और readable रखें
   - Comments add करें जहां जरूरी हो
   - Existing code style follow करें

4. **Test your changes**
   ```bash
   python api_server.py
   # API test करें
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: feature description"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request**
   - GitHub पर अपनी fork में जाएं
   - "New Pull Request" button click करें
   - Clear description लिखें कि आपने क्या changes किए हैं

## Development Guidelines

### Code Style

- Python PEP 8 guidelines follow करें
- Variable names descriptive रखें
- Functions को properly document करें
- Error handling implement करें

### Adding New Country Scraper

नया country scraper add करने के लिए:

1. **Create scraper file:**
   ```python
   # scrapers/your_country_scraper.py
   from scrapers.base_scraper import BaseAmazonScraper
   
   class YourCountryScraper(BaseAmazonScraper):
       def scrape_product(self, url):
           # Implementation
           pass
   ```

2. **Update api_config.py:**
   ```python
   AMAZON_COUNTRIES = {
       'XX': {
           'name': 'Your Country',
           'domain': 'amazon.xx',
           'currency': 'XXX',
           'scraper': 'your_country_scraper.YourCountryScraper'
       }
   }
   ```

3. **Test thoroughly:**
   - Multiple products test करें
   - Different categories check करें
   - Edge cases handle करें

### Testing

Changes commit करने से पहले:

- API को locally run करें
- सभी endpoints test करें
- Error cases verify करें
- Different products के साथ test करें

## Questions?

अगर कोई सवाल हो तो:

- [GitHub Discussions](https://github.com/yourusername/AmazonScrapperPython/discussions) में पूछें
- Issue create करें
- Email करें: your.email@example.com

## Code of Conduct

- Respectful रहें
- Constructive feedback दें
- दूसरों की मदद करें
- Inclusive environment बनाए रखें

## License

Contributions को MIT License के under distribute किया जाएगा (same as the project).

धन्यवाद! 🙏
