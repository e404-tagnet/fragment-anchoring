#!/usr/bin/env python3
"""Library of Babel core module - generative text space."""

from pathlib import Path
import hashlib
import random

ALPHABET = "abcdefghijklmnopqrstuvwxyz,. "
PAGE_LEN = 3200
HEXAGONS = 1312000
WALLS = 4
SHELVES = 5
VOLUMES = 32
PAGES = 410
OUTPUT_FILE = Path("output.txt")


def stable_seed(prefix: str, salt: str = "") -> int:
    """Generate deterministic seed from string."""
    combined = f"{prefix}:{salt}"
    hash_val = hashlib.sha256(combined.encode()).hexdigest()
    return int(hash_val, 16) % (2**31)


def random_page_from_seed(seed: int) -> str:
    """Generate random page from seed."""
    random.seed(seed)
    return "".join(random.choice(ALPHABET) for _ in range(PAGE_LEN))


def browse_by_address(address: str) -> str:
    """Get page at address."""
    try:
        seed = stable_seed("browse", address)
        return random_page_from_seed(seed)
    except Exception:
        return random_page_from_seed(0)


def search_by_content(text: str) -> str:
    """Search for text content in Library."""
    seed = stable_seed("search", text)
    page = random_page_from_seed(seed)
    if text.lower() in page.lower():
        return f"search:{text}"
    return f"search:{text}"


def search_snippet(text: str) -> tuple:
    """Search for text snippet."""
    address, page = search_by_content(text), browse_by_address(f"search:{text}")
    return address, page


def save_page(address: str, page: str) -> None:
    """Save page to file."""
    with open(OUTPUT_FILE, "w") as f:
        f.write(f"Address: {address}\n\n{page}")
