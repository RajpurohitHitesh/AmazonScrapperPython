import requests
import time


class AmazonScraperClient:
    def __init__(self, base_url: str, api_key: str, timeout: int = 30, retries: int = 2):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.retries = retries

    def scrape(self, url: str):
        headers = {"X-API-Key": self.api_key}
        payload = {"url": url}
        for attempt in range(self.retries + 1):
            try:
                resp = requests.post(
                    f"{self.base_url}/api/scrape",
                    json=payload,
                    headers=headers,
                    timeout=self.timeout,
                )
                resp.raise_for_status()
                return resp.json()
            except Exception:
                if attempt >= self.retries:
                    raise
                time.sleep(2 ** attempt)


if __name__ == "__main__":
    client = AmazonScraperClient("http://127.0.0.1:5000", "your_api_key_here")
    print(client.scrape("https://www.amazon.com/dp/B0FMDNZ61S"))
