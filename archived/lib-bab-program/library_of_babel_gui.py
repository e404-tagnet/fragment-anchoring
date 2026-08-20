#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import random
import tkinter as tk
from dataclasses import dataclass
from tkinter import filedialog, messagebox, ttk

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


def save_page(address: str, page_text: str, filename: str = OUTPUT_FILE) -> str:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Address: {address}\n\n")
        f.write(page_text)
    return filename


class BabelGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Library of Babel Clone")
        self.root.geometry("1100x800")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self._build_search_tab()
        self._build_browse_tab()
        self._build_snippet_tab()
        self._build_random_tab()
        self._build_config_tab()
        self._build_status_bar()

    def _build_status_bar(self):
        self.status = tk.StringVar(value="Ready")
        bar = ttk.Label(self.root, textvariable=self.status, anchor="w")
        bar.pack(fill="x", side="bottom")

    def _tab(self, title: str):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        return frame

    def _build_search_tab(self):
        frame = self._tab("Search")
        ttk.Label(frame, text="Enter text:").pack(anchor="w", padx=10, pady=(10, 0))
        self.search_input = tk.Text(frame, height=8, wrap="word")
        self.search_input.pack(fill="x", padx=10, pady=8)
        ttk.Button(frame, text="Search", command=self.do_search).pack(padx=10, pady=5, anchor="w")
        ttk.Label(frame, text="Address:").pack(anchor="w", padx=10, pady=(15, 0))
        self.search_result = tk.StringVar()
        ttk.Entry(frame, textvariable=self.search_result, width=60).pack(fill="x", padx=10, pady=5)

    def _build_browse_tab(self):
        frame = self._tab("Browse")
        ttk.Label(frame, text="Address (hexagon:wall:shelf:volume:page):").pack(anchor="w", padx=10, pady=(10, 0))
        self.browse_addr = tk.StringVar()
        ttk.Entry(frame, textvariable=self.browse_addr).pack(fill="x", padx=10, pady=5)
        ttk.Button(frame, text="Browse", command=self.do_browse).pack(padx=10, pady=5, anchor="w")
        ttk.Button(frame, text="Save page to file", command=self.do_save_browse).pack(padx=10, pady=5, anchor="w")
        ttk.Label(frame, text="Page:").pack(anchor="w", padx=10, pady=(15, 0))
        self.browse_output = tk.Text(frame, height=25, wrap="word")
        self.browse_output.pack(fill="both", expand=True, padx=10, pady=8)

    def _build_snippet_tab(self):
        frame = self._tab("Snippet")
        ttk.Label(frame, text="Enter snippet:").pack(anchor="w", padx=10, pady=(10, 0))
        self.snippet_input = tk.Text(frame, height=8, wrap="word")
        self.snippet_input.pack(fill="x", padx=10, pady=8)
        ttk.Button(frame, text="Find snippet", command=self.do_snippet).pack(padx=10, pady=5, anchor="w")
        ttk.Button(frame, text="Save snippet page", command=self.do_save_snippet).pack(padx=10, pady=5, anchor="w")
        ttk.Label(frame, text="Address:").pack(anchor="w", padx=10, pady=(10, 0))
        self.snippet_addr = tk.StringVar()
        ttk.Entry(frame, textvariable=self.snippet_addr).pack(fill="x", padx=10, pady=5)
        ttk.Label(frame, text="Page:").pack(anchor="w", padx=10, pady=(10, 0))
        self.snippet_output = tk.Text(frame, height=18, wrap="word")
        self.snippet_output.pack(fill="both", expand=True, padx=10, pady=8)

    def _build_random_tab(self):
        frame = self._tab("Random")
        ttk.Label(frame, text="Seed:").pack(anchor="w", padx=10, pady=(10, 0))
        self.random_seed = tk.StringVar()
        ttk.Entry(frame, textvariable=self.random_seed).pack(fill="x", padx=10, pady=5)
        ttk.Button(frame, text="Generate page", command=self.do_random).pack(padx=10, pady=5, anchor="w")
        ttk.Button(frame, text="Save random page", command=self.do_save_random).pack(padx=10, pady=5, anchor="w")
        ttk.Label(frame, text="Page:").pack(anchor="w", padx=10, pady=(10, 0))
        self.random_output = tk.Text(frame, height=24, wrap="word")
        self.random_output.pack(fill="both", expand=True, padx=10, pady=8)

    def _build_config_tab(self):
        frame = self._tab("Config")
        info = (
            f"ALPHABET = {ALPHABET!r}\n"
            f"PAGE_LEN = {PAGE_LEN}\n"
            f"HEXAGONS = {HEXAGONS}\n"
            f"WALLS = {WALLS}\n"
            f"SHELVES = {SHELVES}\n"
            f"VOLUMES = {VOLUMES}\n"
            f"PAGES = {PAGES}\n"
            f"OUTPUT_FILE = {OUTPUT_FILE}\n"
        )
        self.config_box = tk.Text(frame, height=20, wrap="word")
        self.config_box.pack(fill="both", expand=True, padx=10, pady=10)
        self.config_box.insert("1.0", info)
        self.config_box.configure(state="disabled")

    def _set_text(self, widget: tk.Text, text: str):
        widget.delete("1.0", "end")
        widget.insert("1.0", text)

    def do_search(self):
        try:
            text = self.search_input.get("1.0", "end").strip()
            addr = search_by_content(text)
            self.search_result.set(str(addr))
            self.status.set("Search complete")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.set("Search failed")

    def do_browse(self):
        try:
            addr = self.browse_addr.get().strip()
            page = browse_by_address(addr)
            self._set_text(self.browse_output, page)
            self.status.set("Browse complete")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.set("Browse failed")

    def do_save_browse(self):
        try:
            addr = self.browse_addr.get().strip()
            page = browse_by_address(addr)
            filename = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=OUTPUT_FILE, filetypes=[("Text files", "*.txt"), ("All files", "*")])
            if filename:
                save_page(addr, page, filename)
                self.status.set(f"Saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.set("Save failed")

    def do_snippet(self):
        try:
            text = self.snippet_input.get("1.0", "end").strip()
            addr, page = search_snippet(text)
            self.snippet_addr.set(str(addr))
            self._set_text(self.snippet_output, page)
            self.status.set("Snippet search complete")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.set("Snippet search failed")

    def do_save_snippet(self):
        try:
            addr = self.snippet_addr.get().strip()
            page = self.snippet_output.get("1.0", "end").rstrip("\n")
            if not addr.strip() or not page.strip():
                raise ValueError("Run a snippet search first")
            filename = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=OUTPUT_FILE, filetypes=[("Text files", "*.txt"), ("All files", "*")])
            if filename:
                save_page(addr, page, filename)
                self.status.set(f"Saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.set("Save failed")

    def do_random(self):
        try:
            seed = self.random_seed.get().strip()
            seed_value = stable_seed("random", seed)
            page = random_page_from_seed(seed_value)
            self._set_text(self.random_output, page)
            self.status.set("Random page generated")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.set("Random generation failed")

    def do_save_random(self):
        try:
            seed = self.random_seed.get().strip()
            seed_value = stable_seed("random", seed)
            page = random_page_from_seed(seed_value)
            filename = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=OUTPUT_FILE, filetypes=[("Text files", "*.txt"), ("All files", "*")])
            if filename:
                save_page(f"seed:{seed}", page, filename)
                self.status.set(f"Saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.set("Save failed")


def main():
    root = tk.Tk()
    app = BabelGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
