"""
Amazon Scraper API - Setup Script
Install with: pip install -e .
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="amazon-scraper-api",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="REST API service for scraping Amazon product data across 15+ countries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RajpurohitHitesh/AmazonScrapperPython",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "amazon-scraper=api_server:main",
        ],
    },
    include_package_data=True,
    keywords="amazon scraper api flask selenium web-scraping ecommerce",
    project_urls={
        "Bug Reports": "https://github.com/RajpurohitHitesh/AmazonScrapperPython/issues",
        "Source": "https://github.com/RajpurohitHitesh/AmazonScrapperPython",
        "Documentation": "https://github.com/RajpurohitHitesh/AmazonScrapperPython#readme",
    },
)
