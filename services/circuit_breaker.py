import time
from threading import Lock


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, reset_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures = {}
        self.open_until = {}
        self.lock = Lock()

    def is_open(self, key: str) -> bool:
        with self.lock:
            until = self.open_until.get(key)
            if until and time.time() < until:
                return True
            if until and time.time() >= until:
                self.open_until.pop(key, None)
                self.failures.pop(key, None)
            return False

    def record_success(self, key: str):
        with self.lock:
            self.failures.pop(key, None)
            self.open_until.pop(key, None)

    def record_failure(self, key: str):
        with self.lock:
            count = self.failures.get(key, 0) + 1
            self.failures[key] = count
            if count >= self.failure_threshold:
                self.open_until[key] = time.time() + self.reset_timeout
