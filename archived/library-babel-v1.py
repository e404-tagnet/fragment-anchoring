#!/usr/bin/env python3
import sys

# === CONFIG ===
ALPHABET = "abcdefghijklmnopqrstuvwxyz, ."
PAGE_LEN = 3200
ROOMS = 1
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


def address_to_index(room, wall, shelf, volume, page):
    room = int(room)
    wall = int(wall)
    shelf = int(shelf)
    volume = int(volume)
    page = int(page)
    return (((((room - 1) * WALLS + (wall - 1)) * SHELVES + (shelf - 1)) * VOLUMES + (volume - 1)) * PAGES + (page - 1))


def index_to_address(index):
    page = (index % PAGES) + 1
    index //= PAGES
    volume = (index % VOLUMES) + 1
    index //= VOLUMES
    shelf = (index % SHELVES) + 1
    index //= SHELVES
    wall = (index % WALLS) + 1
    index //= WALLS
    room = index + 1
    return room, wall, shelf, volume, page


def search_by_content(text):
    page = pad_page(text)
    n = text_to_int(page)
    return index_to_address(n)


def search_by_address(address):
    parts = address.replace(".", ":").split(":")
    if len(parts) == 5:
        room, wall, shelf, volume, page = parts
    elif len(parts) == 4:
        room = 1
        wall, shelf, volume, page = parts
    else:
        raise ValueError("Address must be room:wall:shelf:volume:page or wall:shelf:volume:page")
    idx = address_to_index(room, wall, shelf, volume, page)
    return int_to_text(idx, PAGE_LEN)


def format_address(addr):
    return f"{addr[0]}:{addr[1]}:{addr[2]}:{addr[3]}:{addr[4]}"


def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python library_of_babel_clone.py search <text>")
        print("  python library_of_babel_clone.py browse <room:wall:shelf:volume:page>")
        sys.exit(1)

    mode = sys.argv[1].lower()
    arg = " ".join(sys.argv[2:])

    if mode == "search":
        addr = search_by_content(arg)
        print(format_address(addr))
    elif mode == "browse":
        page = search_by_address(arg)
        print(page)
    else:
        raise SystemExit("Unknown mode. Use search or browse.")


if __name__ == "__main__":
    main()