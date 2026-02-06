import logging
import random
from threading import Lock
from typing import Optional
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


DEVICE_PROFILES = [
    {
        "name": "Desktop Chrome",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "viewport": {"width": 1366, "height": 768},
    },
    {
        "name": "Desktop Edge",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
        "viewport": {"width": 1536, "height": 864},
    },
    {
        "name": "Desktop Firefox",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        "viewport": {"width": 1440, "height": 900},
    },
    {
        "name": "Mobile Android",
        "user_agent": "Mozilla/5.0 (Linux; Android 12; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
        "viewport": {"width": 393, "height": 851},
    },
]


class BrowserManager:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self._playwright = None
        self._browser = None
        self._current_proxy = None
        self._lock = Lock()

    def start(self):
        with self._lock:
            if self._playwright is None:
                self._playwright = sync_playwright().start()
            if self._browser is None:
                self._browser = self._playwright.chromium.launch(headless=self.headless)
                logging.info("Browser started")

    def stop(self):
        with self._lock:
            if self._browser:
                self._browser.close()
                self._browser = None
            if self._playwright:
                self._playwright.stop()
                self._playwright = None
                logging.info("Browser stopped")

    def _ensure_browser(self, headless: bool, proxy_url: Optional[str]):
        if self._playwright is None:
            self._playwright = sync_playwright().start()
        if self._browser is None or self.headless != headless or self._current_proxy != proxy_url:
            if self._browser:
                try:
                    self._browser.close()
                except Exception:
                    pass
            self.headless = headless
            launch_args = {"headless": headless}
            if proxy_url:
                launch_args["proxy"] = {"server": proxy_url}
            self._browser = self._playwright.chromium.launch(**launch_args)
            self._current_proxy = proxy_url
            logging.info("Browser (re)started")

    def get_context(self, headless: bool, proxy_url: Optional[str]):
        with self._lock:
            self._ensure_browser(headless=headless, proxy_url=proxy_url)
            profile = random.choice(DEVICE_PROFILES)
            viewport = profile["viewport"].copy()
            viewport["width"] += random.randint(-40, 40)
            viewport["height"] += random.randint(-40, 40)
            try:
                context = self._browser.new_context(
                    user_agent=profile["user_agent"],
                    viewport=viewport,
                )
            except Exception:
                if self._browser:
                    try:
                        self._browser.close()
                    except Exception:
                        pass
                launch_args = {"headless": headless}
                if proxy_url:
                    launch_args["proxy"] = {"server": proxy_url}
                self._browser = self._playwright.chromium.launch(**launch_args)
                self._current_proxy = proxy_url
                context = self._browser.new_context(
                    user_agent=profile["user_agent"],
                    viewport=viewport,
                )
            context.add_init_script(
                """
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                window.chrome = { runtime: {} };
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                """
            )
            return context

    def is_running(self) -> bool:
        return self._browser is not None


__all__ = ["BrowserManager", "PlaywrightTimeoutError"]
