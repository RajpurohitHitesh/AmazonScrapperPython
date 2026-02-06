from prometheus_client import Counter, Histogram, Gauge

REQUESTS_TOTAL = Counter("api_requests_total", "Total API requests", ["endpoint", "status"])
SCRAPE_TOTAL = Counter("scrape_total", "Total scrape attempts", ["status", "country"])
CAPTCHA_TOTAL = Counter("captcha_total", "Captcha detections", ["country"])
SCRAPE_DURATION = Histogram("scrape_duration_seconds", "Scrape duration in seconds", ["country"])
QUEUE_DEPTH = Gauge("scrape_queue_depth", "Current scrape queue depth")
CACHE_SIZE = Gauge("cache_size", "Current cache size")
