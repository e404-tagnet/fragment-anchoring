"""Stage One: Embedding convergence testing."""

import json
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime
from pathlib import Path
from .models import create_model, BaseEmbeddingModel
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import STAGE_ONE_CONFIG


class ConvergenceTest:
    """Tests whether different embedding models converge on the same attractors."""
    
    def __init__(self, config: Dict = None):
        self.config = config or STAGE_ONE_CONFIG
        self.models: Dict[str, BaseEmbeddingModel] = {}
        self.concept_embeddings: Dict[str, Dict[str, np.ndarray]] = {}
        self.convergence_matrix = None
        self.results = {}
        self.timestamp = datetime.now().isoformat()
    
    def setup_models(self) -> None:
        """Initialize all models."""
        print("Setting up models...")
        for model_name, model_config in self.config["models"].items():
            model = create_model(
                model_config["type"],
                model_config["embedding_dim"]
            )
            self.models[model_name] = model
            print(f"  Created {model_name}")
    
    def train_models(self, corpus: List[str] = None) -> None:
        """Train all models."""
        if corpus is None:
            corpus = self.config["canonical_concepts"]
        
        print(f"Training {len(self.models)} models on {len(corpus)} concepts...")
        for model_name, model in self.models.items():
            epochs = self.config["models"][model_name].get("epochs", 10)
            model.train(corpus, epochs=epochs)
            print(f"  Trained {model_name}")
    
    def embed_concepts(self) -> None:
        """Embed canonical concepts in all models."""
        print("Embedding concepts...")
        concepts = self.config["canonical_concepts"]
        for model_name, model in self.models.items():
            self.concept_embeddings[model_name] = model.embed_concepts(concepts)
            print(f"  Embedded {len(concepts)} concepts in {model_name}")
    
    def compute_convergence_matrix(self) -> np.ndarray:
        """Compute pairwise cosine similarity between model embeddings."""
        concepts = self.config["canonical_concepts"]
        model_names = list(self.models.keys())
        n_models = len(model_names)
        
        convergence = np.zeros((n_models, n_models, len(concepts)))
        
        for i, model1 in enumerate(model_names):
            for j, model2 in enumerate(model_names):
                for k, concept in enumerate(concepts):
                    vec1 = self.concept_embeddings[model1][concept]
                    vec2 = self.concept_embeddings[model2][concept]
                    similarity = np.dot(vec1, vec2) / (
                        np.linalg.norm(vec1) * np.linalg.norm(vec2) + 1e-8
                    )
                    convergence[i, j, k] = similarity
        
        self.convergence_matrix = convergence
        return convergence
    
    def compute_metrics(self) -> Dict:
        """Compute convergence metrics."""
        if self.convergence_matrix is None:
            raise ValueError("Run compute_convergence_matrix first")
        
        concepts = self.config["canonical_concepts"]
        model_names = list(self.models.keys())
        metrics = {}
        
        # Mean pairwise similarity (excluding diagonal)
        similarities = []
        for i in range(len(model_names)):
            for j in range(i + 1, len(model_names)):
                for k in range(len(concepts)):
                    similarities.append(self.convergence_matrix[i, j, k])
        
        mean_similarity = np.mean(similarities)
        std_similarity = np.std(similarities)
        min_similarity = np.min(similarities)
        max_similarity = np.max(similarities)
        
        metrics["mean_pairwise_similarity"] = float(mean_similarity)
        metrics["std_pairwise_similarity"] = float(std_similarity)
        metrics["min_similarity"] = float(min_similarity)
        metrics["max_similarity"] = float(max_similarity)
        
        # Check threshold
        threshold = self.config["convergence_threshold"]
        passed = mean_similarity >= threshold
        metrics["convergence_passed"] = passed
        metrics["threshold"] = threshold
        
        # Outlier analysis
        outliers = sum(1 for s in similarities if s < 0.7)
        metrics["outliers_below_0.7"] = outliers
        metrics["outlier_percentage"] = (outliers / len(similarities)) * 100
        
        self.results = metrics
        return metrics
    
    def compute_domain_convergence(self) -> Dict:
        """Compute convergence within semantic domains."""
        domains = {
            "animals": ["dog", "cat"],
            "spatial": ["house", "tree", "mountain", "river", "door"],
            "temporal": ["time", "begin", "end", "continue"],
            "emotional": ["love", "hate", "happy", "sad"],
            "abstract": ["truth", "lie", "good", "evil"],
        }
        
        domain_metrics = {}
        for domain, words in domains.items():
            if all(w in self.config["canonical_concepts"] for w in words):
                sims = []
                model_names = list(self.models.keys())
                for i in range(len(model_names)):
                    for j in range(i + 1, len(model_names)):
                        for word in words:
                            idx = self.config["canonical_concepts"].index(word)
                            sims.append(self.convergence_matrix[i, j, idx])
                
                domain_metrics[domain] = {
                    "mean_similarity": float(np.mean(sims)),
                    "std_similarity": float(np.std(sims)),
                }
        
        return domain_metrics
    
    def run(self) -> Dict:
        """Execute full convergence test."""
        print("\n=== Stage One: Embedding Convergence Test ===\n")
        
        self.setup_models()
        self.train_models()
        self.embed_concepts()
        self.compute_convergence_matrix()
        
        print("\nComputing metrics...")
        metrics = self.compute_metrics()
        domain_metrics = self.compute_domain_convergence()
        
        results = {
            "timestamp": self.timestamp,
            "metrics": metrics,
            "domain_convergence": domain_metrics,
            "models": list(self.models.keys()),
            "n_concepts": len(self.config["canonical_concepts"]),
        }
        
        return results
    
    def save_results(self, output_dir: str = "experiment_logs") -> str:
        """Save results to JSON file."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        filename = output_path / f"stage_one_results_{self.timestamp.replace(':', '-')}.json"
        with open(filename, "w") as f:
            json.dump(self.results, f, indent=2)
        
        return str(filename)
    
    def report(self) -> str:
        """Generate human-readable report."""
        if not self.results:
            return "No results to report. Run the test first."
        
        report = []
        report.append("=== Convergence Test Results ===\n")
        
        metrics = self.results.get("metrics", {})
        report.append(f"Mean Pairwise Similarity: {metrics.get('mean_pairwise_similarity', 0):.4f}")
        report.append(f"Std Pairwise Similarity: {metrics.get('std_pairwise_similarity', 0):.4f}")
        report.append(f"Min Similarity: {metrics.get('min_similarity', 0):.4f}")
        report.append(f"Max Similarity: {metrics.get('max_similarity', 0):.4f}")
        report.append(f"Convergence Threshold: {metrics.get('threshold', 0):.4f}")
        report.append(f"Threshold Passed: {metrics.get('convergence_passed', False)}\n")
        
        report.append(f"Outliers Below 0.7: {metrics.get('outliers_below_0.7', 0)}")
        report.append(f"Outlier Percentage: {metrics.get('outlier_percentage', 0):.2f}%\n")
        
        domain_metrics = self.results.get("domain_convergence", {})
        if domain_metrics:
            report.append("Domain-Specific Convergence:")
            for domain, values in domain_metrics.items():
                report.append(
                    f"  {domain}: {values['mean_similarity']:.4f} "
                    f"(+/- {values['std_similarity']:.4f})"
                )
        
        return "\n".join(report)
