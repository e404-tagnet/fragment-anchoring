#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import random
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, send_file, url_for

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
SECRET_KEY = "library-of-babel-secret-change-me"
# =====================

BASE = len(ALPHABET)
CHAR_TO_DIGIT = {c: i for i, c in enumerate(ALPHABET)}
DIGIT_TO_CHAR = {i: c for i, c in enumerate(ALPHABET)}

app = Flask(__name__)
app.secret_key = SECRET_KEY


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


def validate_ranges(hexagon: int, wall: int, shelf: int, volume: int, page: int) -> None:
    if not (1 <= hexagon <= HEXAGONS):
        raise ValueError(f"hexagon must be 1..{HEXAGONS}")
    if not (1 <= wall <= WALLS):
        raise ValueError(f"wall must be 1..{WALLS}")
    if not (1 <= shelf <= SHELVES):
        raise ValueError(f"shelf must be 1..{SHELVES}")
    if not (1 <= volume <= VOLUMES):
        raise ValueError(f"volume must be 1..{VOLUMES}")
    if not (1 <= page <= PAGES):
        raise ValueError(f"page must be 1..{PAGES}")


def address_to_index(hexagon: int, wall: int, shelf: int, volume: int, page: int) -> int:
    validate_ranges(hexagon, wall, shelf, volume, page)
    return (((((hexagon - 1) * WALLS + (wall - 1)) * SHELVES + (shelf - 1)) * VOLUMES + (volume - 1)) * PAGES + (page - 1))


def index_to_address(index: int) -> tuple[int, int, int, int, int]:
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


def parse_address(text: str) -> tuple[int, int, int, int, int]:
    parts = text.replace(".", ":").split(":")
    if len(parts) != 5:
        raise ValueError("Address must be hexagon:wall:shelf:volume:page")
    return tuple(int(p) for p in parts)


def search_by_content(text: str) -> str:
    page = pad_page(text)
    n = text_to_int(page)
    addr = index_to_address(n)
    return f"{addr[0]}:{addr[1]}:{addr[2]}:{addr[3]}:{addr[4]}"


def browse_by_address(address: str) -> str:
    hexagon, wall, shelf, volume, page = parse_address(address)
    idx = address_to_index(hexagon, wall, shelf, volume, page)
    return int_to_text(idx, PAGE_LEN)


def search_snippet(text: str) -> tuple[str, str]:
    hexagon = (text_to_int(normalize(text)) % HEXAGONS) + 1
    address = f"{hexagon}:1:1:1:1"
    seed_value = stable_seed("snippet", text, address)
    page = random_page_from_seed(seed_value)
    return address, page


def save_page(address: str, page_text: str, filename: str = OUTPUT_FILE) -> Path:
    path = Path(filename)
    path.write_text(f"Address: {address}\n\n{page_text}", encoding="utf-8")
    return path


BASE_HTML = """
<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>Library of Babel Clone</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 0; background: #111; color: #eee; }
    header { padding: 1rem; background: #1d1d1d; border-bottom: 1px solid #333; }
    main { padding: 1rem; max-width: 1200px; margin: 0 auto; }
    nav a { color: #8ab4f8; margin-right: 1rem; text-decoration: none; }
    .card { background: #181818; border: 1px solid #333; border-radius: 10px; padding: 1rem; margin-bottom: 1rem; }
    input, textarea { width: 100%; box-sizing: border-box; background: #111; color: #eee; border: 1px solid #444; border-radius: 8px; padding: .75rem; }
    textarea { min-height: 160px; }
    button, .btn { display: inline-block; width: auto; background: #2d6cdf; color: white; border: 0; padding: .75rem 1rem; border-radius: 8px; text-decoration: none; cursor: pointer; }
    pre { white-space: pre-wrap; word-wrap: break-word; background: #0d0d0d; border: 1px solid #333; padding: 1rem; border-radius: 8px; overflow-x: auto; }
    .flash { background: #3a2a00; border: 1px solid #7a5a00; padding: .75rem; border-radius: 8px; margin-bottom: 1rem; }
    @media (max-width: 800px) { }
  </style>
</head>
<body>
<header>
  <strong>Library of Babel Clone</strong>
  <nav>
    <a href=\"{{ url_for('home') }}\">Home</a>
    <a href=\"{{ url_for('config_view') }}\">Config</a>
  </nav>
</header>
<main>
  {% with messages = get_flashed_messages() %}
    {% if messages %}
      {% for message in messages %}
        <div class=\"flash\">{{ message }}</div>
      {% endfor %}
    {% endif %}
  {% endwith %}
  {% block body %}{% endblock %}
</main>
</body>
</html>
"""

HOME_HTML = """
{% extends 'base.html' %}
{% block body %}
<div class=\"card\">
  <h2>Search by text</h2>
  <form method=\"post\" action=\"{{ url_for('search') }}\">
    <textarea name=\"text\" placeholder=\"Enter text to locate\"></textarea>
    <p><button type=\"submit\">Search</button></p>
  </form>
</div>
<div class=\"card\">
  <h2>Browse by address</h2>
  <form method=\"post\" action=\"{{ url_for('browse') }}\">
    <input name=\"address\" placeholder=\"hexagon:wall:shelf:volume:page\">
    <p><button type=\"submit\">Browse</button></p>
  </form>
</div>
<div class=\"card\">
  <h2>Snippet search</h2>
  <form method=\"post\" action=\"{{ url_for('snippet') }}\">
    <textarea name=\"text\" placeholder=\"Enter a snippet\"></textarea>
    <p><button type=\"submit\">Find snippet</button></p>
  </form>
</div>
<div class=\"card\">
  <h2>Random page</h2>
  <form method=\"post\" action=\"{{ url_for('random_page') }}\">
    <input name=\"seed\" placeholder=\"Seed text\">
    <p><button type=\"submit\">Generate random page</button></p>
  </form>
</div>
{% endblock %}
"""

RESULT_HTML = """
{% extends 'base.html' %}
{% block body %}
<div class=\"card\">
  <h2>{{ title }}</h2>
  {% if address %}<p><strong>Address:</strong> {{ address }}</p>{% endif %}
  {% if download_url %}<p><a class=\"btn\" href=\"{{ download_url }}\">Download text file</a></p>{% endif %}
  {% if content %}<pre>{{ content }}</pre>{% endif %}
  <p><a class=\"btn\" href=\"{{ url_for('home') }}\">Back</a></p>
</div>
{% endblock %}
"""

CONFIG_HTML = """
{% extends 'base.html' %}
{% block body %}
<div class=\"card\">
  <h2>Config</h2>
  <pre>{{ config }}</pre>
</div>
{% endblock %}
"""


@app.route("/")
def home():
    return render_template_string_with_base(HOME_HTML)


def render_template_string_with_base(template: str, **context):
    templates = {
        "base.html": BASE_HTML,
        "home.html": HOME_HTML,
        "result.html": RESULT_HTML,
        "config.html": CONFIG_HTML,
    }
    return render_template_string_with_loader(template, templates, **context)


def render_template_string_with_loader(template: str, templates: dict[str, str], **context):
    from jinja2 import DictLoader
    app.jinja_loader = DictLoader(templates)
    return render_template_string(template, **context)


@app.route("/search", methods=["POST"])
def search():
    try:
        text = request.form.get("text", "")
        address = search_by_content(text)
        page = browse_by_address(address)
        save_page(address, page)
        return render_template_string_with_base(
            RESULT_HTML,
            title="Search result",
            address=address,
            content=page,
            download_url=url_for("download_file"),
        )
    except Exception as e:
        flash(str(e))
        return redirect(url_for("home"))


@app.route("/browse", methods=["POST"])
def browse():
    try:
        address = request.form.get("address", "")
        page = browse_by_address(address)
        save_page(address, page)
        return render_template_string_with_base(
            RESULT_HTML,
            title="Browse result",
            address=address,
            content=page,
            download_url=url_for("download_file"),
        )
    except Exception as e:
        flash(str(e))
        return redirect(url_for("home"))


@app.route("/snippet", methods=["POST"])
def snippet():
    try:
        text = request.form.get("text", "")
        address, page = search_snippet(text)
        save_page(address, page)
        return render_template_string_with_base(
            RESULT_HTML,
            title="Snippet result",
            address=address,
            content=page,
            download_url=url_for("download_file"),
        )
    except Exception as e:
        flash(str(e))
        return redirect(url_for("home"))


@app.route("/random", methods=["POST"])
def random_page():
    try:
        seed = request.form.get("seed", "")
        page = random_page_from_seed(stable_seed("random", seed))
        address = f"seed:{seed}"
        save_page(address, page)
        return render_template_string_with_base(
            RESULT_HTML,
            title="Random page",
            address=address,
            content=page,
            download_url=url_for("download_file"),
        )
    except Exception as e:
        flash(str(e))
        return redirect(url_for("home"))


@app.route("/config")
def config_view():
    config = (
        f"ALPHABET = {ALPHABET!r}\n"
        f"PAGE_LEN = {PAGE_LEN}\n"
        f"HEXAGONS = {HEXAGONS}\n"
        f"WALLS = {WALLS}\n"
        f"SHELVES = {SHELVES}\n"
        f"VOLUMES = {VOLUMES}\n"
        f"PAGES = {PAGES}\n"
        f"OUTPUT_FILE = {OUTPUT_FILE}\n"
    )
    return render_template_string_with_base(CONFIG_HTML, config=config)


@app.route("/download")
def download_file():
    path = Path(OUTPUT_FILE)
    if not path.exists():
        flash("No saved page yet.")
        return redirect(url_for("home"))
    return send_file(path, as_attachment=True, download_name=OUTPUT_FILE)


if __name__ == "__main__":
    app.run(debug=True)
