from typing import List, Tuple
from urllib.parse import urlparse


def validate_amazon_url(url: str, allowed_domains: List[str]) -> Tuple[bool, str]:
    if not url or not isinstance(url, str):
        return False, "URL is required"

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False, "URL must start with http or https"

    host = (parsed.netloc or "").lower()
    if host.startswith("www."):
        host = host[4:]

    if not host:
        return False, "URL host is invalid"

    if not any(host == d or host.endswith("." + d) for d in allowed_domains):
        return False, "URL must be an Amazon domain"

    return True, ""
