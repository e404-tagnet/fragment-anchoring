#!/usr/bin/env python3
import sys
import hashlib
import random

# === CONFIG ===
ALPHABET = "abcdefghijklmnopqrstuvwxyz, ."
PAGE_LEN = 3200
HEXAGONS = 1_000_000
WALLS = 4
SHELVES = 5
VOLUMES = 32
PAGES = 410
# =============

BASE = len(ALPHABET)
CHAR_TO_DIGIT = {c: i for i, c in enumerate(ALPHABET)}
DIGIT_TO_CHAR = {i: c for i, c in enumerate(ALPHABET)}


def normalize(text):
    text = text.lower()
    return "".join(c for c in text if c in ALPHABET)


def text_to_int(text):
    n = 0
    for c in text:
        n = n * BASE + CHAR_TO_DIGIT[c]
    return n


def int_to_text(n, length=PAGE_LEN):
    chars = [" "] * length
    for i in range(length - 1, -1, -1):
        n, r = divmod(n, BASE)
        chars[i] = DIGIT_TO_CHAR[r]
    return "".join(chars)


def pad_page(text):
    text = normalize(text)
    if len(text) > PAGE_LEN:
        return text[:PAGE_LEN]
    return text.ljust(PAGE_LEN, " ")


def stable_seed(*parts):
    h = hashlib.sha256()
    for p in parts:
        h.update(str(p).encode("utf-8"))
        h.update(b"|")
    return int.from_bytes(h.digest(), "big")


def random_page_from_seed(seed_value):
    rng = random.Random(seed_value)
    return "".join(rng.choice(ALPHABET) for _ in range(PAGE_LEN))


def hash_text_to_hexagon(text):
    return text_to_int(normalize(text)) % HEXAGONS + 1


def address_to_index(hexagon, wall, shelf, volume, page):
    hexagon = int(hexagon)
    wall = int(wall)
    shelf = int(shelf)
    volume = int(volume)
    page = int(page)
    return (((((hexagon - 1) * WALLS + (wall - 1)) * SHELVES + (shelf - 1)) * VOLUMES + (volume - 1)) * PAGES + (page - 1))


def index_to_address(index):
    page = (index % PAGES) + 1
    index //= PAGES
    volume = (index % VOLUMES) + 1
    index //= VOLUMES
    shelf = (index % SHELVES) + 1
    index //= SHELVES
    wall = (index % WALLS) + 1
    index //= WALLS
    hexagon = (index % HEXAGONS) + 1
    return hexagon, wall, shelf, volume, page


def search_by_content(text):
    page = pad_page(text)
    n = text_to_int(page)
    return index_to_address(n)


def search_snippet(text):
    hexagon = hash_text_to_hexagon(text)
    seed_value = stable_seed("snippet", text, hexagon)
    page = random_page_from_seed(seed_value)
    return format_address((hexagon, 1, 1, 1, 1)), page


def search_by_address(address):
    parts = address.replace(".", ":").split(":")
    if len(parts) == 5:
        hexagon, wall, shelf, volume, page = parts
    else:
        raise ValueError("Address must be hexagon:wall:shelf:volume:page")
    idx = address_to_index(hexagon, wall, shelf, volume, page)
    return int_to_text(idx, PAGE_LEN)


def format_address(addr):
    return f"{addr[0]}:{addr[1]}:{addr[2]}:{addr[3]}:{addr[4]}"


def save_page_to_file(address, page_text, filename="library_page.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Address: {address}\n\n")
        f.write(page_text)
    return filename


def menu():
    print("Library of Babel Clone")
    print("1) Search by text")
    print("2) Browse by address")
    print("3) Snippet search")
    print("4) Exit")


def main():
    if len(sys.argv) >= 3:
        mode = sys.argv[1].lower()
        arg = " ".join(sys.argv[2:])
        if mode == "search":
            print(format_address(search_by_content(arg)))
        elif mode == "browse":
            print(search_by_address(arg))
        elif mode == "snippet":
            addr, page = search_snippet(arg)
            print("Address:", addr)
            print(page)
        else:
            raise SystemExit("Use: search <text> | browse <hexagon:wall:shelf:volume:page> | snippet <text>")
        return

    while True:
        menu()
        choice = input("> ").strip()
        if choice == "1":
            text = input("Enter text: ")
            addr = format_address(search_by_content(text))
            print("Address:", addr)
        elif choice == "2":
            addr = input("Enter address hexagon:wall:shelf:volume:page: ")
            page = search_by_address(addr)
            print("Page:\n")
            print(page)
            if input("Save to file? (y/n): ").strip().lower() == "y":
                fn = save_page_to_file(addr, page)
                print("Saved to", fn)
        elif choice == "3":
            text = input("Enter snippet: ")
            addr, page = search_snippet(text)
            print("Address:", addr)
            print("Page:\n")
            print(page)
            if input("Save to file? (y/n): ").strip().lower() == "y":
                fn = save_page_to_file(addr, page)
                print("Saved to", fn)
        elif choice == "4":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()