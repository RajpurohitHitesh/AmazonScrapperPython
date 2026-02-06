import time
from threading import Lock
from typing import Optional


class TokenBucket:
    def __init__(self, rate_per_minute: int, burst: Optional[int] = None):
        self.capacity = burst if burst is not None else rate_per_minute
        self.tokens = self.capacity
        self.rate_per_sec = rate_per_minute / 60.0
        self.last_refill = time.time()
        self.lock = Lock()

    def allow(self) -> bool:
        with self.lock:
            now = time.time()
            elapsed = now - self.last_refill
            self.last_refill = now
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate_per_sec)
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False


class RateLimiter:
    def __init__(self, rate_per_minute: int, burst: Optional[int] = None):
        self.rate_per_minute = rate_per_minute
        self.burst = burst
        self.buckets = {}
        self.lock = Lock()

    def is_allowed(self, key: str) -> bool:
        if not key:
            return True
        with self.lock:
            if key not in self.buckets:
                self.buckets[key] = TokenBucket(self.rate_per_minute, self.burst)
            bucket = self.buckets[key]
        return bucket.allow()
