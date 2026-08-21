<!-- TAGNET README HEADER — Catppuccin Mocha — do not edit by hand -->
<div align="center">

[![License](https://img.shields.io/github/license/e404-tagnet/fragment-anchoring?color=313244&labelColor=11111b&label=License&style=flat-square)](https://github.com/e404-tagnet/fragment-anchoring/blob/main/LICENSE)
[![Status](https://img.shields.io/badge/Status-stable-a6e3a1?labelColor=11111b&style=flat-square)](https://github.com/e404-tagnet/fragment-anchoring/pulse)
[![Version](https://img.shields.io/github/v/release/e404-tagnet/fragment-anchoring?color=313244&labelColor=11111b&label=Version&style=flat-square)](https://github.com/e404-tagnet/fragment-anchoring/releases)
[![Repo](https://img.shields.io/badge/Repo-fragment-anchoring-94e2d5?labelColor=11111b&style=flat-square&logo=github&logoColor=94e2d5)](https://github.com/e404-tagnet/fragment-anchoring)
[![Tagnet](https://img.shields.io/badge/By-Tagnet-89dceb?labelColor=11111b&style=flat-square&logo=tag&logoColor=89dceb)](https://tagnet.dev)

</div>
<!-- TAGNET README HEADER — end -->

# Library of Babel Clone

A Python implementation of Borges’ Library of Babel with a Flask web interface.

## Run the app

1. Install Flask:
   ```bash
   pip install flask
   ```
2. Start the server:
   ```bash
   python app.py
   ```
3. Open in your browser:
   ```text
   http://127.0.0.1:5000
   ```

## Files

- `app.py` – Flask web app
- `library_of_babel_core.py` – Core logic (addresses, page generation, search)
- `templates/` – HTML templates
- `README.md` – This file

## How to use each search box

### 1) Search by text

**What to type:**  
Up to 3200 characters using only: `a–z`, space, comma, and period.

**What it does:**  
- Treats your text as the full content of a page (padded with spaces if shorter).  
- Converts that text into a deterministic address in the library.

**What you get back:**  
- An address: `hexagon:wall:shelf:volume:page`  
- The full 3200‑character page that contains exactly your text.

**Example input:**
```text
hello world
```

### 2) Browse by address

**What to type:**  
An address in the form:
```text
hexagon:wall:shelf:volume:page
```
Example:
```text
1:1:1:1:1
```
All numbers must be in valid ranges (1‑based).

**What it does:**  
- Converts that address into the unique 3200‑character page at that location.

**What you get back:**  
- The full page text (3200 characters) for that address.  
- The same address shown above the text.

### 3) Snippet search

**What to type:**  
A short phrase or sentence using only `a–z`, space, comma, and period.

**What it does:**  
- Embeds your snippet somewhere inside a deterministically generated 3200‑character page.

**What you get back:**  
- An address where that snippet appears.  
- A full 3200‑character page containing your snippet somewhere in it.

**Example input:**
```text
the quick brown fox
```

### 4) Random page

**What to type:**  
Any seed text you like, e.g.:
```text
my secret seed 123
```

**What it does:**  
- Uses your seed to generate a deterministic random page. Same seed → same page every time.

**What you get back:**  
- A label like `seed:my secret seed 123`.  
- A 3200‑character pseudo‑random page generated from that seed.

## Notes

- Allowed characters: `a–z`, space, comma, period. Everything else is ignored.
- Each page is exactly 3200 characters long.
- The library structure:
  - Hexagons: 1,000,000
  - Walls per hexagon: 4
  - Shelves per wall: 5
  - Volumes (books) per shelf: 32
  - Pages per volume: 410

<!-- TAGNET README FOOTER — start -->

<div align="center">

**Like this work? Fuel the next widget / experiment / scaffold.**

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-%23FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/e404.tagnet)
[![Patreon](https://img.shields.io/badge/Support-Patreon-ff424d?logo=patreon&logoColor=white&style=for-the-badge)](https://www.patreon.com/VeritasExMachina?utm_campaign=creatorshare_creator)

<small>Crafted with caffeine, curiosity, and a Catppuccin palette · © e404-tagnet</small>

</div>
<!-- TAGNET README FOOTER — end -->
