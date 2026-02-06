# Contributing to Amazon Scraper API

Welcome! Your contributions are appreciated! 🎉

## How to Contribute

### Reporting Bugs

If you find a bug:

1. Check [GitHub Issues](https://github.com/yourusername/AmazonScrapperPython/issues) to see if the bug has already been reported
2. If not, create a new issue:
   - Provide a clear title
   - Describe steps to reproduce
   - Explain expected vs actual behavior
   - Attach screenshots if possible
   - Include environment details (Python version, OS, etc.)

### Suggesting Features

To suggest new features:

1. Create an issue with tag `enhancement`
2. Explain the feature in detail
3. Describe the use case and why it would be useful
4. Share implementation ideas (optional)

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
   - Keep code clean and readable
   - Add comments where necessary
   - Follow existing code style

4. **Test your changes**
   ```bash
   python api_server.py
   # Test the API
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
   - Go to your fork on GitHub
   - Click "New Pull Request" button
   - Write a clear description of your changes

## Development Guidelines

### Code Style

- Follow Python PEP 8 guidelines
- Use descriptive variable names
- Document functions properly
- Implement error handling

### Adding New Country Scraper

To add a new country scraper:

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
   - Test with multiple products
   - Check different categories
   - Handle edge cases

### Testing

Before committing changes:

- Run the API locally
- Test all endpoints
- Verify error cases
- Test with different products

## Questions?

If you have questions:

- Ask in [GitHub Discussions](https://github.com/yourusername/AmazonScrapperPython/discussions)
- Create an issue
- Email: your.email@example.com

## Code of Conduct

- Be respectful
- Give constructive feedback
- Help others
- Maintain an inclusive environment

## License

Contributions will be distributed under the MIT License (same as the project).

Thank you! 🙏
