from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass
from pathlib import Path

ALPHABET = "abcdefghijklmnopqrstuvwxyz, ."
PAGE_LEN = 3200
HEXAGONS = 1_000_000
WALLS = 4
SHELVES = 5
VOLUMES = 32
PAGES = 410
OUTPUT_FILE = "library_page.txt"

BASE = len(ALPHABET)
CHAR_TO_DIGIT = {c: i for i, c in enumerate(ALPHABET)}
DIGIT_TO_CHAR = {i: c for i, c in enumerate(ALPHABET)}


@dataclass(frozen=True)
class Address:
    hexagon: int
    wall: int
    shelf: int
    volume: int
    page: int

    def __str__(self) -> str:
        return f"{self.hexagon}:{self.wall}:{self.shelf}:{self.volume}:{self.page}"


def normalize(text: str) -> str:
    text = text.lower()
    return "".join(c for c in text if c in ALPHABET)


def pad_page(text: str) -> str:
    text = normalize(text)
    if len(text) > PAGE_LEN:
        return text[:PAGE_LEN]
    return text.ljust(PAGE_LEN, " ")


def text_to_int(text: str) -> int:
    n = 0
    for c in text:
        n = n * BASE + CHAR_TO_DIGIT[c]
    return n


def int_to_text(n: int, length: int = PAGE_LEN) -> str:
    chars = [" "] * length
    for i in range(length - 1, -1, -1):
        n, r = divmod(n, BASE)
        chars[i] = DIGIT_TO_CHAR[r]
    return "".join(chars)


def stable_seed(*parts) -> int:
    h = hashlib.sha256()
    for p in parts:
        h.update(str(p).encode("utf-8"))
        h.update(b"|")
    return int.from_bytes(h.digest(), "big")


def random_page_from_seed(seed_value: int) -> str:
    rng = random.Random(seed_value)
    return "".join(rng.choice(ALPHABET) for _ in range(PAGE_LEN))


def validate_ranges(addr: Address) -> None:
    if not (1 <= addr.hexagon <= HEXAGONS):
        raise ValueError(f"hexagon must be 1..{HEXAGONS}")
    if not (1 <= addr.wall <= WALLS):
        raise ValueError(f"wall must be 1..{WALLS}")
    if not (1 <= addr.shelf <= SHELVES):
        raise ValueError(f"shelf must be 1..{SHELVES}")
    if not (1 <= addr.volume <= VOLUMES):
        raise ValueError(f"volume must be 1..{VOLUMES}")
    if not (1 <= addr.page <= PAGES):
        raise ValueError(f"page must be 1..{PAGES}")


def address_to_index(addr: Address) -> int:
    validate_ranges(addr)
    return (((((addr.hexagon - 1) * WALLS + (addr.wall - 1)) * SHELVES + (addr.shelf - 1)) * VOLUMES + (addr.volume - 1)) * PAGES + (addr.page - 1))


def index_to_address(index: int) -> Address:
    page = (index % PAGES) + 1
    index //= PAGES
    volume = (index % VOLUMES) + 1
    index //= VOLUMES
    shelf = (index % SHELVES) + 1
    index //= SHELVES
    wall = (index % WALLS) + 1
    index //= WALLS
    hexagon = (index % HEXAGONS) + 1
    return Address(hexagon, wall, shelf, volume, page)


def parse_address(text: str) -> Address:
    parts = text.replace(".", ":").split(":")
    if len(parts) != 5:
        raise ValueError("Address must be hexagon:wall:shelf:volume:page")
    return Address(*(int(p) for p in parts))


def search_by_content(text: str) -> Address:
    page = pad_page(text)
    n = text_to_int(page)
    return index_to_address(n)


def browse_by_address(address: str) -> str:
    addr = parse_address(address)
    idx = address_to_index(addr)
    return int_to_text(idx, PAGE_LEN)


def search_snippet(text: str) -> tuple[Address, str]:
    hexagon = (text_to_int(normalize(text)) % HEXAGONS) + 1
    addr = Address(hexagon, 1, 1, 1, 1)
    seed_value = stable_seed("snippet", text, str(addr))
    page = random_page_from_seed(seed_value)
    return addr, page


def save_page(address: str, page_text: str, filename: str = OUTPUT_FILE) -> Path:
    path = Path(filename)
    path.write_text(f"Address: {address}\n\n{page_text}", encoding="utf-8")
    return path
