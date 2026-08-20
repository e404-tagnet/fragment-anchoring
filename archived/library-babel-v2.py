#!/usr/bin/env python3
import sys

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


def menu():
    print("Library of Babel Clone")
    print("1) Search by text")
    print("2) Browse by address")
    print("3) Exit")


def main():
    if len(sys.argv) >= 3:
        mode = sys.argv[1].lower()
        arg = " ".join(sys.argv[2:])
        if mode == "search":
            print(format_address(search_by_content(arg)))
        elif mode == "browse":
            print(search_by_address(arg))
        else:
            raise SystemExit("Use: search <text> or browse <hexagon:wall:shelf:volume:page>")
        return

    while True:
        menu()
        choice = input("> ").strip()
        if choice == "1":
            text = input("Enter text: ")
            print("Address:", format_address(search_by_content(text)))
        elif choice == "2":
            addr = input("Enter address hexagon:wall:shelf:volume:page: ")
            print("Page:\n")
            print(search_by_address(addr))
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()