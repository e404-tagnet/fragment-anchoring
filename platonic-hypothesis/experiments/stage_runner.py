"""Main experiment runner for all stages."""

import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from embeddings.convergence_test import ConvergenceTest
from fragment_anchoring.search import FragmentSearch
from config import STAGE_ONE_CONFIG, STAGE_TWO_CONFIG


class PlatonicHypothesisRunner:
    """Orchestrates all stages of the Platonic Representation Hypothesis experiment."""
    
    def __init__(self, output_dir: str = "experiment_logs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results = {}
        self.timestamp = datetime.now().isoformat()
    
    def run_stage_one(self) -> Dict:
        """Run Stage One: Embedding Convergence Test."""
        print("\n" + "="*60)
        print("STAGE ONE: EMBEDDING CONVERGENCE TEST")
        print("="*60 + "\n")
        
        test = ConvergenceTest(STAGE_ONE_CONFIG)
        results = test.run()
        
        print("\n" + test.report())
        
        # Save results
        filename = test.save_results(str(self.output_dir))
        print(f"\nResults saved to: {filename}")
        
        self.results["stage_one"] = results
        return results
    
    def run_stage_two(self) -> Dict:
        """Run Stage Two: Fragment Anchoring Validation."""
        print("\n" + "="*60)
        print("STAGE TWO: FRAGMENT ANCHORING VALIDATION")
        print("="*60 + "\n")
        
        search = FragmentSearch()
        
        # Add some test fragments (would be from scripture in real scenario)
        print("Adding test fragments...")
        fragments = [
            ("in the beginning", "exact_string", 1.0),
            ("word", "isolated_word", 0.8),
            ("light", "exact_string", 0.9),
        ]
        
        for text, ftype, conf in fragments:
            fragment = search.add_fragment(text, ftype, conf)
            print(f"  Added: {fragment}")
        
        # Add test queries
        print("\nCreating queries...")
        query1 = search.add_query(
            [1, 2],
            ["genesis", "creation"],
            "in the beginning word"
        )
        print(f"  Added: {query1}")
        
        # Execute queries
        print("\nExecuting queries...")
        candidates = search.search_query(query1)
        print(f"  Found {len(candidates)} candidates")
        
        # Score candidates
        if candidates:
            print("\nScoring candidates...")
            for candidate in candidates:
                score = search.score_candidate(candidate, "in the beginning was the word")
                print(f"  Candidate {candidate.id}: score={score:.2f}")
        
        # Summarize
        summary = search.get_summary()
        print("\nStage Two Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
        
        results = {
            "summary": summary,
            "fragments": len(search.fragments),
            "queries": len(search.queries),
            "candidates": len(search.candidates),
        }
        
        self.results["stage_two"] = results
        return results
    
    def run_all(self) -> Dict:
        """Run all stages sequentially."""
        print("\n" + "="*60)
        print("PLATONIC REPRESENTATION HYPOTHESIS")
        print("Full Experiment Run")
        print("="*60)
        
        try:
            self.run_stage_one()
            self.run_stage_two()
        except Exception as e:
            print(f"\nExperiment failed with error: {e}")
            return {"error": str(e)}
        
        # Save final results
        self.save_final_results()
        
        print("\n" + "="*60)
        print("EXPERIMENT COMPLETE")
        print("="*60)
        
        return self.results
    
    def save_final_results(self) -> str:
        """Save all results to a master file."""
        filename = self.output_dir / f"experiment_results_{self.timestamp.replace(':', '-')}.json"
        with open(filename, "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\nFinal results saved to: {filename}")
        return str(filename)


def main():
    """Command-line entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Platonic Hypothesis experiments")
    parser.add_argument("--stage", type=int, choices=[1, 2], help="Run specific stage")
    parser.add_argument("--output-dir", default="experiment_logs", help="Output directory")
    
    args = parser.parse_args()
    
    runner = PlatonicHypothesisRunner(args.output_dir)
    
    if args.stage == 1:
        runner.run_stage_one()
    elif args.stage == 2:
        runner.run_stage_two()
    else:
        runner.run_all()


if __name__ == "__main__":
    main()
