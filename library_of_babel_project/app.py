from pathlib import Path
from flask import Flask, flash, redirect, render_template, request, send_file, url_for
from library_of_babel_core import ALPHABET, HEXAGONS, OUTPUT_FILE, PAGE_LEN, PAGES, SHELVES, VOLUMES, WALLS
from library_of_babel_core import browse_by_address, save_page, search_by_content, search_snippet, random_page_from_seed, stable_seed

app = Flask(__name__)
app.secret_key = "library-of-babel-secret-change-me"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search", methods=["POST"])
def search():
    try:
        text = request.form.get("text", "")
        address = str(search_by_content(text))
        page = browse_by_address(address)
        save_page(address, page)
        return render_template("result.html", title="Search result", address=address, content=page)
    except Exception as e:
        flash(str(e))
        return redirect(url_for("home"))

@app.route("/browse", methods=["POST"])
def browse():
    try:
        address = request.form.get("address", "")
        page = browse_by_address(address)
        save_page(address, page)
        return render_template("result.html", title="Browse result", address=address, content=page)
    except Exception as e:
        flash(str(e))
        return redirect(url_for("home"))

@app.route("/snippet", methods=["POST"])
def snippet():
    try:
        text = request.form.get("text", "")
        address, page = search_snippet(text)
        save_page(str(address), page)
        return render_template("result.html", title="Snippet result", address=str(address), content=page)
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
        return render_template("result.html", title="Random page", address=address, content=page)
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
    return render_template("config.html", config=config)

@app.route("/download")
def download_file():
    path = Path(OUTPUT_FILE)
    if not path.exists():
        flash("No saved page yet.")
        return redirect(url_for("home"))
    return send_file(path, as_attachment=True, download_name=OUTPUT_FILE)

if __name__ == "__main__":
    app.run(debug=True)
