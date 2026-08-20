"""Configuration for Platonic Hypothesis experiments."""

# Stage One: Embedding Convergence Testing
STAGE_ONE_CONFIG = {
    "models": {
        "transformer": {
            "type": "transformer",
            "loss": "contrastive",
            "corpus": "general",
            "embedding_dim": 256,
            "epochs": 10,
        },
        "cnn": {
            "type": "cnn",
            "loss": "triplet",
            "corpus": "specialized",
            "embedding_dim": 256,
            "epochs": 10,
        },
        "language_model": {
            "type": "language_model",
            "loss": "mlm",
            "corpus": "diverse",
            "embedding_dim": 256,
            "epochs": 10,
        },
        "reduction": {
            "type": "reduction",
            "loss": "mse",
            "corpus": "general",
            "embedding_dim": 256,
            "epochs": 5,
        },
    },
    "canonical_concepts": [
        "dog", "cat", "house", "tree", "water", "fire", "love", "hate",
        "run", "walk", "think", "speak", "see", "hear", "touch",
        "big", "small", "hot", "cold", "happy", "sad", "fast", "slow",
        "time", "space", "number", "color", "shape", "sound", "taste",
        "mother", "father", "child", "friend", "enemy", "king", "servant",
        "book", "word", "song", "art", "truth", "lie", "good", "evil",
        "mountain", "river", "sky", "earth", "sun", "moon", "star",
        "door", "window", "bridge", "road", "path", "wall", "roof",
        "begin", "end", "continue", "stop", "rise", "fall", "grow", "die",
        "give", "take", "buy", "sell", "make", "break", "fix", "build",
    ],
    "convergence_threshold": 0.85,
    "similarity_metric": "cosine",
}

# Stage Two: Fragment Anchoring
STAGE_TWO_CONFIG = {
    "source_texts": [
        "genesis",
        "luke",
        "proverbs",
        "psalms",
        "revelation",
    ],
    "fragments_per_source": 3,
    "iteration_cycles": 3,
    "coherence_threshold": 0.85,
    "gap_limit_chars": 500,
}

# Fragment Anchoring Workbook
WORKBOOK_CONFIG = {
    "output_file": "fragment_search_workbook.xlsx",
    "sheet_names": [
        "Instructions",
        "Fragments",
        "Hypotheses",
        "Queries",
        "Candidates",
    ],
}

# Library of Babel
BABEL_CONFIG = {
    "alphabet": "abcdefghijklmnopqrstuvwxyz,. ",
    "page_length": 3200,
    "hexagons": 1312000,
    "walls": 4,
    "shelves": 5,
    "volumes": 32,
    "pages": 410,
}

# Flask App
FLASK_CONFIG = {
    "secret_key": "platonic-hypothesis-secret-key-change-in-production",
    "debug": True,
    "host": "127.0.0.1",
    "port": 5000,
}

# Experiment Logging
LOGGING_CONFIG = {
    "log_dir": "experiment_logs",
    "log_level": "INFO",
    "timestamp_format": "%Y-%m-%d %H:%M:%S",
}
