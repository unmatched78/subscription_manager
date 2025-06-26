import hashlib
from typing import Dict

def fingerprint_from_headers(headers: Dict[str, str], ip: str) -> str:
    """
    Generate a simple device/IP fingerprint from headers and IP.
    """
    seed = ip + "::" + headers.get("User-Agent", "")
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()
