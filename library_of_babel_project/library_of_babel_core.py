from __future__ import annotations
import hashlib, random
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
    def __str__(self): return f"{self.hexagon}:{self.wall}:{self.shelf}:{self.volume}:{self.page}"
def normalize(text): return "".join(c for c in text.lower() if c in ALPHABET)
def pad_page(text):
    text = normalize(text)
    return text[:PAGE_LEN].ljust(PAGE_LEN, " ")
def text_to_int(text):
    n=0
    for c in text: n = n * BASE + CHAR_TO_DIGIT[c]
    return n
def int_to_text(n, length=PAGE_LEN):
    chars=[" "]*length
    for i in range(length-1,-1,-1):
        n,r=divmod(n,BASE)
        chars[i]=DIGIT_TO_CHAR[r]
    return "".join(chars)
def stable_seed(*parts):
    h=hashlib.sha256()
    for p in parts:
        h.update(str(p).encode()); h.update(b"|")
    return int.from_bytes(h.digest(), "big")
def random_page_from_seed(seed_value):
    rng=random.Random(seed_value)
    return "".join(rng.choice(ALPHABET) for _ in range(PAGE_LEN))
def validate_ranges(addr):
    if not (1 <= addr.hexagon <= HEXAGONS): raise ValueError(f"hexagon must be 1..{HEXAGONS}")
    if not (1 <= addr.wall <= WALLS): raise ValueError(f"wall must be 1..{WALLS}")
    if not (1 <= addr.shelf <= SHELVES): raise ValueError(f"shelf must be 1..{SHELVES}")
    if not (1 <= addr.volume <= VOLUMES): raise ValueError(f"volume must be 1..{VOLUMES}")
    if not (1 <= addr.page <= PAGES): raise ValueError(f"page must be 1..{PAGES}")
def address_to_index(addr):
    validate_ranges(addr)
    return (((((addr.hexagon - 1) * WALLS + (addr.wall - 1)) * SHELVES + (addr.shelf - 1)) * VOLUMES + (addr.volume - 1)) * PAGES + (addr.page - 1))
def index_to_address(index):
    page=(index % PAGES)+1; index//=PAGES
    volume=(index % VOLUMES)+1; index//=VOLUMES
    shelf=(index % SHELVES)+1; index//=SHELVES
    wall=(index % WALLS)+1; index//=WALLS
    hexagon=(index % HEXAGONS)+1
    return Address(hexagon, wall, shelf, volume, page)
def parse_address(text):
    parts=text.replace(".",":").split(":")
    if len(parts)!=5: raise ValueError("Address must be hexagon:wall:shelf:volume:page")
    return Address(*(int(p) for p in parts))
def search_by_content(text): return index_to_address(text_to_int(pad_page(text)))
def browse_by_address(address): return int_to_text(address_to_index(parse_address(address)), PAGE_LEN)
def search_snippet(text):
    hexagon = (text_to_int(normalize(text)) % HEXAGONS) + 1
    addr = Address(hexagon, 1, 1, 1, 1)
    return addr, random_page_from_seed(stable_seed("snippet", text, str(addr)))
def save_page(address, page_text, filename=OUTPUT_FILE):
    path=Path(filename)
    path.write_text(f"Address: {address}

{page_text}", encoding="utf-8")
    return path
