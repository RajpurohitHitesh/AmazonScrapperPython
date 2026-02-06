import time
from threading import Lock


class TTLCache:
    def __init__(self, ttl_seconds: int = 300, max_items: int = 1000):
        self.ttl_seconds = ttl_seconds
        self.max_items = max_items
        self._store = {}
        self._lock = Lock()

    def _purge(self):
        now = time.time()
        keys_to_delete = [k for k, v in self._store.items() if v[1] < now]
        for k in keys_to_delete:
            del self._store[k]

        if len(self._store) > self.max_items:
            # Remove oldest items
            sorted_items = sorted(self._store.items(), key=lambda item: item[1][1])
            for k, _ in sorted_items[: len(self._store) - self.max_items]:
                del self._store[k]

    def get(self, key):
        with self._lock:
            self._purge()
            if key in self._store:
                value, expiry = self._store[key]
                if expiry >= time.time():
                    return value
                del self._store[key]
        return None

    def set(self, key, value):
        with self._lock:
            self._purge()
            self._store[key] = (value, time.time() + self.ttl_seconds)

    def size(self):
        with self._lock:
            self._purge()
            return len(self._store)
