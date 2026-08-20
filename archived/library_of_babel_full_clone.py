#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import os
import random
import sys
from dataclasses import dataclass

# =====================
# CONFIG
# =====================
ALPHABET = "abcdefghijklmnopqrstuvwxyz, ."
PAGE_LEN = 3200
HEXAGONS = 1_000_000
WALLS = 4
SHELVES = 5
VOLUMES = 32
PAGES = 410
OUTPUT_FILE = "library_page.txt"
# =====================

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


def format_page_from_text(text: str) -> str:
    return pad_page(text)


def search_by_content(text: str) -> Address:
    page = format_page_from_text(text)
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


def save_page(address: str, page_text: str, filename: str = OUTPUT_FILE) -> str:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Address: {address}\n\n")
        f.write(page_text)
    return filename


def print_config() -> None:
    print("Current config:")
    print(f"  ALPHABET  = {ALPHABET!r}")
    print(f"  PAGE_LEN  = {PAGE_LEN}")
    print(f"  HEXAGONS  = {HEXAGONS}")
    print(f"  WALLS     = {WALLS}")
    print(f"  SHELVES   = {SHELVES}")
    print(f"  VOLUMES   = {VOLUMES}")
    print(f"  PAGES     = {PAGES}")
    print(f"  OUTPUT    = {OUTPUT_FILE}")


def menu() -> None:
    print("\nLibrary of Babel Clone")
    print("1) Search by text")
    print("2) Browse by address")
    print("3) Snippet search")
    print("4) Generate random page")
    print("5) Show config")
    print("6) Exit")


def cli() -> None:
    parser = argparse.ArgumentParser(description="Library of Babel-style clone")
    sub = parser.add_subparsers(dest="cmd")

    p1 = sub.add_parser("search", help="search by text and return address")
    p1.add_argument("text", nargs=argparse.REMAINDER)

    p2 = sub.add_parser("browse", help="browse by address and return page text")
    p2.add_argument("address")

    p3 = sub.add_parser("snippet", help="snippet search")
    p3.add_argument("text", nargs=argparse.REMAINDER)

    p4 = sub.add_parser("random", help="generate a deterministic random page from a seed")
    p4.add_argument("seed")

    p5 = sub.add_parser("save", help="search by text and save page to file")
    p5.add_argument("text", nargs=argparse.REMAINDER)
    p5.add_argument("--file", default=OUTPUT_FILE)

    p6 = sub.add_parser("config", help="show config")

    args = parser.parse_args()
    if not args.cmd:
        return

    if args.cmd == "search":
        text = " ".join(args.text)
        print(search_by_content(text))
    elif args.cmd == "browse":
        print(browse_by_address(args.address))
    elif args.cmd == "snippet":
        text = " ".join(args.text)
        addr, page = search_snippet(text)
        print(f"Address: {addr}")
        print(page)
    elif args.cmd == "random":
        seed_value = stable_seed("random", args.seed)
        print(random_page_from_seed(seed_value))
    elif args.cmd == "save":
        text = " ".join(args.text)
        addr = search_by_content(text)
        page = browse_by_address(str(addr))
        fn = save_page(str(addr), page, args.file)
        print(f"Saved {fn}")
    elif args.cmd == "config":
        print_config()


def interactive() -> None:
    while True:
        menu()
        choice = input("> ").strip()
        try:
            if choice == "1":
                text = input("Enter text: ")
                addr = search_by_content(text)
                print("Address:", addr)
            elif choice == "2":
                addr = input("Enter address hexagon:wall:shelf:volume:page: ")
                page = browse_by_address(addr)
                print("\nPage:\n")
                print(page)
                if input("Save to file? (y/n): ").strip().lower() == "y":
                    fn = save_page(addr, page)
                    print("Saved to", fn)
            elif choice == "3":
                text = input("Enter snippet: ")
                addr, page = search_snippet(text)
                print("Address:", addr)
                print("\nPage:\n")
                print(page)
                if input("Save to file? (y/n): ").strip().lower() == "y":
                    fn = save_page(str(addr), page)
                    print("Saved to", fn)
            elif choice == "4":
                seed = input("Seed: ")
                seed_value = stable_seed("random", seed)
                print(random_page_from_seed(seed_value))
            elif choice == "5":
                print_config()
            elif choice == "6":
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print("Error:", e)


def main() -> None:
    if len(sys.argv) > 1:
        cli()
    else:
        interactive()


if __name__ == "__main__":
    main()
