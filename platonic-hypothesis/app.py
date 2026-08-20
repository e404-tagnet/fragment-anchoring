"""Flask web application for Platonic Hypothesis experiments."""

from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
import sys
import json

sys.path.insert(0, str(Path(__file__).parent))

from embeddings.convergence_test import ConvergenceTest
from fragment_anchoring.search import FragmentSearch
from experiments.stage_runner import PlatonicHypothesisRunner
from config import FLASK_CONFIG

app = Flask(__name__)
app.secret_key = FLASK_CONFIG["secret_key"]

# Global experiment state
current_runner = None
fragment_search = None


@app.route("/")
def home():
    """Home page."""
    return render_template("home.html")


@app.route("/stage-one", methods=["GET", "POST"])
def stage_one():
    """Stage One: Embedding Convergence Testing."""
    if request.method == "POST":
        try:
            test = ConvergenceTest()
            results = test.run()
            report = test.report()
            return jsonify({
                "status": "success",
                "report": report,
                "metrics": test.results,
            })
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    
    return render_template("stage_one.html")


@app.route("/stage-two", methods=["GET", "POST"])
def stage_two():
    """Stage Two: Fragment Anchoring."""
    global fragment_search
    
    if request.method == "GET":
        fragment_search = FragmentSearch()
        return render_template("stage_two.html")
    
    if request.method == "POST":
        data = request.get_json()
        action = data.get("action")
        
        try:
            if action == "add_fragment":
                fragment = fragment_search.add_fragment(
                    data.get("text"),
                    data.get("type", "exact_string"),
                    data.get("confidence", 1.0)
                )
                return jsonify({
                    "status": "success",
                    "fragment": {
                        "id": fragment.id,
                        "text": fragment.text,
                        "type": fragment.fragment_type,
                    }
                })
            
            elif action == "add_query":
                query = fragment_search.add_query(
                    data.get("fragment_ids", []),
                    data.get("hypotheses", []),
                    data.get("query_text", "")
                )
                return jsonify({
                    "status": "success",
                    "query": {
                        "id": query.id,
                        "status": query.status,
                    }
                })
            
            elif action == "search":
                query_id = data.get("query_id")
                query = fragment_search.queries[query_id]
                candidates = fragment_search.search_query(query)
                
                return jsonify({
                    "status": "success",
                    "candidates": [
                        {
                            "id": c.id,
                            "address": c.address,
                            "text": c.text[:200],
                        } for c in candidates
                    ]
                })
            
            elif action == "get_summary":
                summary = fragment_search.get_summary()
                return jsonify({
                    "status": "success",
                    "summary": summary,
                })
            
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    
    return jsonify({"status": "error", "message": "Invalid request"}), 400


@app.route("/experiment/run", methods=["POST"])
def run_experiment():
    """Run full experiment."""
    global current_runner
    
    try:
        current_runner = PlatonicHypothesisRunner()
        results = current_runner.run_all()
        
        return jsonify({
            "status": "success",
            "message": "Experiment completed",
            "results": results,
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/experiment/download", methods=["GET"])
def download_results():
    """Download experiment results."""
    try:
        log_dir = Path("experiment_logs")
        latest_file = max(log_dir.glob("*.json"), key=lambda p: p.stat().st_mtime)
        return send_file(latest_file, as_attachment=True)
    except Exception:
        return jsonify({"status": "error", "message": "No results found"}), 404


@app.route("/config", methods=["GET"])
def config_view():
    """View configuration."""
    from config import STAGE_ONE_CONFIG, STAGE_TWO_CONFIG, BABEL_CONFIG
    
    config_info = {
        "stage_one": {
            "models": list(STAGE_ONE_CONFIG["models"].keys()),
            "concepts": len(STAGE_ONE_CONFIG["canonical_concepts"]),
            "threshold": STAGE_ONE_CONFIG["convergence_threshold"],
        },
        "stage_two": {
            "sources": STAGE_TWO_CONFIG["source_texts"],
            "iterations": STAGE_TWO_CONFIG["iteration_cycles"],
            "threshold": STAGE_TWO_CONFIG["coherence_threshold"],
        },
        "babel": BABEL_CONFIG,
    }
    
    return render_template("config.html", config=json.dumps(config_info, indent=2))


if __name__ == "__main__":
    app.run(
        host=FLASK_CONFIG["host"],
        port=FLASK_CONFIG["port"],
        debug=FLASK_CONFIG["debug"]
    )
