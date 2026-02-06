import os
import requests

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5000")
API_KEY = os.getenv("API_KEY", "your_api_key_here")
TEST_URL = os.getenv("TEST_URL", "https://www.amazon.com/dp/B0FMDNZ61S")


def main():
    headers = {"X-API-Key": API_KEY}
    resp = requests.post(f"{BASE_URL}/api/scrape", json={"url": TEST_URL}, headers=headers, timeout=60)
    print(resp.status_code)
    print(resp.json())


if __name__ == "__main__":
    main()
