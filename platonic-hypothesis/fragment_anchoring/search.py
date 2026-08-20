"""Fragment anchoring search module for Stage Two."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from library_of_babel_core import (
    search_by_content, browse_by_address, search_snippet, random_page_from_seed, stable_seed
)
from typing import List, Dict, Tuple, Optional


class FragmentAnchor:
    """Represents a known fragment to search for."""
    
    def __init__(self, id: int, text: str, fragment_type: str = "exact_string", confidence: float = 1.0):
        self.id = id
        self.text = text
        self.fragment_type = fragment_type  # exact_string, isolated_word, concept
        self.confidence = confidence
        self.appearances = []
    
    def __repr__(self):
        return f"Fragment({self.id}, '{self.text}', {self.fragment_type})"


class Query:
    """Represents a search query combining fragments and hypotheses."""
    
    def __init__(self, id: int, fragments: List[int], hypotheses: List[str], query_text: str):
        self.id = id
        self.fragments = fragments
        self.hypotheses = hypotheses
        self.query_text = query_text
        self.status = "not_run"  # not_run, queued, run, rejected, promising
        self.results = []
    
    def __repr__(self):
        return f"Query({self.id}, fragments={self.fragments}, status={self.status})"


class Candidate:
    """Represents a candidate result from a query."""
    
    def __init__(self, id: int, query_id: int, text: str, address: str = ""):
        self.id = id
        self.query_id = query_id
        self.text = text
        self.address = address
        self.scores = {
            "exact_matches": 0,
            "distinctive_matches": 0,
            "order_score": 0,
            "proximity_score": 0,
            "coherence_score": 0,
            "topic_score": 0,
        }
        self.decision = "unreviewed"  # unreviewed, promising, rejected, verified
    
    def compute_total_score(self) -> float:
        """Sum all component scores."""
        return sum(self.scores.values())
    
    def __repr__(self):
        return f"Candidate({self.id}, query={self.query_id}, decision={self.decision})"


class FragmentSearch:
    """Main fragment anchoring search engine."""
    
    def __init__(self):
        self.fragments: Dict[int, FragmentAnchor] = {}
        self.queries: Dict[int, Query] = {}
        self.candidates: Dict[int, Candidate] = {}
        self.fragment_counter = 0
        self.query_counter = 0
        self.candidate_counter = 0
        self.iteration_log = []
    
    def add_fragment(self, text: str, fragment_type: str = "exact_string", 
                    confidence: float = 1.0) -> FragmentAnchor:
        """Add a known fragment."""
        self.fragment_counter += 1
        fragment = FragmentAnchor(self.fragment_counter, text, fragment_type, confidence)
        self.fragments[self.fragment_counter] = fragment
        return fragment
    
    def add_query(self, fragment_ids: List[int], hypotheses: List[str], 
                 query_text: str) -> Query:
        """Add a query combining fragments and hypotheses."""
        self.query_counter += 1
        query = Query(self.query_counter, fragment_ids, hypotheses, query_text)
        self.queries[self.query_counter] = query
        return query
    
    def search_fragment(self, fragment: FragmentAnchor) -> Optional[Tuple[str, str]]:
        """Search for a fragment in the Library."""
        try:
            address = str(search_by_content(fragment.text))
            page = browse_by_address(address)
            fragment.appearances.append((address, page))
            return address, page
        except Exception as e:
            print(f"Search failed for fragment '{fragment.text}': {e}")
            return None, None
    
    def search_query(self, query: Query) -> List[Candidate]:
        """Execute a query and return candidates."""
        query.status = "run"
        results = []
        
        try:
            address, page = search_by_content(query.query_text)
            if page:
                query.status = "promising"
                self.candidate_counter += 1
                candidate = Candidate(self.candidate_counter, query.id, page, address)
                self.candidates[self.candidate_counter] = candidate
                query.results.append(candidate)
                results.append(candidate)
                self.iteration_log.append({
                    "type": "query",
                    "query_id": query.id,
                    "candidate_id": candidate.id,
                    "address": address,
                })
            else:
                query.status = "rejected"
        except Exception as e:
            query.status = "rejected"
            print(f"Query execution failed: {e}")
        
        return results
    
    def score_candidate(self, candidate: Candidate, known_text: str = "") -> float:
        """Score a candidate against known source text."""
        candidate_text = candidate.text.lower()
        known_text = known_text.lower()
        
        # Exact matches: how many fragments appear verbatim
        exact_matches = 0
        for fragment in self.fragments.values():
            if fragment.text.lower() in candidate_text:
                exact_matches += 1
        candidate.scores["exact_matches"] = min(exact_matches, 5)
        
        # Coherence: simple text similarity
        if known_text:
            common_words = len(set(candidate_text.split()) & set(known_text.split()))
            total_words = len(set(candidate_text.split()) | set(known_text.split()))
            coherence = common_words / total_words if total_words > 0 else 0
            candidate.scores["coherence_score"] = int(coherence * 5)
        else:
            candidate.scores["coherence_score"] = 2  # Neutral
        
        # Topic score: rough semantic similarity
        candidate.scores["topic_score"] = 2  # Neutral placeholder
        
        return candidate.compute_total_score()
    
    def iterate(self, promising_candidates: List[Candidate]) -> List[Query]:
        """Use promising candidates as context for next iteration."""
        new_queries = []
        for candidate in promising_candidates:
            # Extract text snippets from candidate as new context
            text = candidate.text[:200]  # First 200 chars as context
            
            # Create new query using candidate text as hypothesis
            fragment_ids = list(self.fragments.keys())[:2]  # Use first 2 fragments
            new_query = Query(
                self.query_counter + 1,
                fragment_ids,
                [text],
                f"{' '.join([self.fragments[fid].text for fid in fragment_ids])} {text}"
            )
            self.queries[new_query.id] = new_query
            self.query_counter += 1
            new_queries.append(new_query)
            
            self.iteration_log.append({
                "type": "iteration",
                "source_candidate": candidate.id,
                "new_query": new_query.id,
            })
        
        return new_queries
    
    def get_summary(self) -> Dict:
        """Get summary statistics."""
        return {
            "n_fragments": len(self.fragments),
            "n_queries": len(self.queries),
            "n_candidates": len(self.candidates),
            "promising_candidates": sum(
                1 for c in self.candidates.values() if c.decision == "promising"
            ),
            "verified_candidates": sum(
                1 for c in self.candidates.values() if c.decision == "verified"
            ),
        }
