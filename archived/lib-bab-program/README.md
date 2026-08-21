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

A configurable Library of Babel-style project in Python with a shared core module, a Tkinter desktop GUI, and a Flask web app.

## Overview

This repository demonstrates a deterministic text-to-address and address-to-text system inspired by the Library of Babel idea. The core logic lives in a shared Python module so both interfaces behave the same way.

## Project files

- `library_of_babel_core.py` — shared engine used by both apps.
- `library_of_babel_gui.py` — Tkinter desktop interface.
- `library_of_babel_webapp.py` — Flask browser interface.

## How it works

The project uses a fixed alphabet and page length. Input text is normalized to the allowed alphabet, converted to a large base-N integer, and mapped to an address made of hexagon, wall, shelf, volume, and page coordinates.

The reverse path turns an address into a page of text by converting the address coordinates back into a deterministic integer and decoding that into characters.

There is also a snippet-search mode that creates a repeatable pseudo-random page from a search string.

## Requirements

- Python 3.10 or newer.
- Tkinter for the desktop GUI, which is usually included with Python.
- Flask for the web app.

Install Flask if needed:

```bash
pip install flask
```

## Setup

1. Put all three Python files in the same directory.
2. Edit the config values at the top of `library_of_babel_core.py` if you want a different alphabet or coordinate space.
3. Run either interface directly.

## Usage

### Desktop GUI

```bash
python library_of_babel_gui.py
```

Use the tabs to:
- search by text,
- browse by address,
- run snippet search,
- generate a deterministic random page,
- and save page text to a file.

### Web app

```bash
python library_of_babel_webapp.py
```

Then open the local address shown by Flask, usually `http://127.0.0.1:5000/`.

Use the browser interface to:
- search by text,
- browse by address,
- run snippet search,
- generate a random page,
- view the config,
- and download the latest saved page text.

## Core module summary

The shared module provides these main functions:

- `normalize(text)` — keep only allowed characters.
- `pad_page(text)` — fit text to the configured page length.
- `text_to_int(text)` — convert text into a big integer.
- `int_to_text(n)` — convert an integer back into page text.
- `search_by_content(text)` — turn text into an address.
- `browse_by_address(address)` — turn an address into page text.
- `search_snippet(text)` — generate a deterministic pseudo-random page from a snippet.
- `random_page_from_seed(seed)` — generate a repeatable random page.
- `save_page(address, page_text)` — save a page to disk.

## Config values

These are the most important settings in `library_of_babel_core.py`:

- `ALPHABET` — the allowed characters.
- `PAGE_LEN` — the number of characters in each page.
- `HEXAGONS`, `WALLS`, `SHELVES`, `VOLUMES`, `PAGES` — the coordinate space.
- `OUTPUT_FILE` — the default file name for saved page output.

## Limitations

This is a practical clone, not an exact reproduction of Jonathan Basile’s website internals. The coordinate counts, search behavior, and random-page generation are simplified and configurable.

## Development

If you want to extend it, the cleanest approach is to keep all new logic in the shared core module and have both interfaces call into it.

Possible next improvements:

- add a proper package layout,
- add tests,
- add a real page-search index,
- add HTML templates for the Flask app,
- or add a browser-based frontend that calls the Flask backend.

<!-- TAGNET README FOOTER — start -->

<div align="center">

**Like this work? Fuel the next widget / experiment / scaffold.**

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-%23FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/e404.tagnet)
[![Patreon](https://img.shields.io/badge/Support-Patreon-ff424d?logo=patreon&logoColor=white&style=for-the-badge)](https://www.patreon.com/VeritasExMachina?utm_campaign=creatorshare_creator)

<small>Crafted with caffeine, curiosity, and a Catppuccin palette · © e404-tagnet</small>

</div>
<!-- TAGNET README FOOTER — end -->
