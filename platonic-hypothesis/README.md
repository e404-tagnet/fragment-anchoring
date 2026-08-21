<!-- TAGNET README HEADER — Catppuccin Mocha — do not edit by hand -->
<div align="center">

[![License](https://img.shields.io/github/license/e404-tagnet/fragment-anchoring?color=313244&labelColor=11111b&label=License&style=flat-square)](https://github.com/e404-tagnet/fragment-anchoring/blob/main/LICENSE)
[![Status](https://img.shields.io/badge/Status-stable-a6e3a1?labelColor=11111b&style=flat-square)](https://github.com/e404-tagnet/fragment-anchoring/pulse)
[![Version](https://img.shields.io/github/v/release/e404-tagnet/fragment-anchoring?color=313244&labelColor=11111b&label=Version&style=flat-square)](https://github.com/e404-tagnet/fragment-anchoring/releases)
[![Repo](https://img.shields.io/badge/Repo-fragment-anchoring-94e2d5?labelColor=11111b&style=flat-square&logo=github&logoColor=94e2d5)](https://github.com/e404-tagnet/fragment-anchoring)
[![Tagnet](https://img.shields.io/badge/By-Tagnet-89dceb?labelColor=11111b&style=flat-square&logo=tag&logoColor=89dceb)](https://tagnet.dev)

</div>
<!-- TAGNET README HEADER — end -->

# Platonic Representation Hypothesis: Empirical Convergence Testing

A complete experimental framework for validating whether semantic attractors exist as fixed points in representation space.

## Quick Start

```bash
pip install -r requirements.txt
python experiments/stage_runner.py
```

Or run specific stages:

```bash
python experiments/stage_runner.py --stage 1
python experiments/stage_runner.py --stage 2
```

Or launch the web interface:

```bash
python app.py
```

Then visit http://127.0.0.1:5000

## Project Structure

```
platonic-hypothesis/
├── config.py                           # Configuration for all stages
├── library_of_babel_core.py            # Generative text space
├── app.py                              # Flask web interface
├── requirements.txt                    # Python dependencies
│
├── embeddings/
│   ├── models.py                       # Embedding model definitions
│   └── convergence_test.py             # Stage One test harness
│
├── fragment_anchoring/
│   └── search.py                       # Fragment search engine
│
├── experiments/
│   └── stage_runner.py                 # Main experiment orchestrator
│
├── templates/
│   ├── home.html                       # Landing page
│   ├── stage_one.html                  # Stage One interface
│   ├── stage_two.html                  # Stage Two interface
│   └── config.html                     # Configuration viewer
│
└── experiment_logs/                    # Output directory (created at runtime)
    ├── stage_one_results_*.json
    └── experiment_results_*.json
```

## What This Is

A systematic test of the Platonic Representation Hypothesis:

**Thesis**: Different training mechanisms converge toward the same semantic attractor regions in embedding space. This convergence proves that attractors are fixed points in the topology of semantic space, independent of the path taken to reach them.

**Method**: Three sequential stages, each validating the hypothesis at a different level.

## The Three Stages

### Stage One: Embedding Space Convergence

Train four embedding models with radically different specifications:

1. **Transformer** (contrastive loss, general corpus)
2. **CNN** (triplet loss, specialized corpus)
3. **Language Model** (MLM objective, diverse data)
4. **Dimensional Reduction** (MSE loss, different approach)

Embed 150+ canonical concepts in each model. Measure whether the same semantic concepts cluster in the same regions across all models.

**Success Criteria**:
- Mean pairwise cosine similarity: 0.85 or higher
- Relative positioning preserved across models
- Fewer than 5% outliers
- Convergence holds within semantic domains

**Output**: Convergence metrics, similarity matrices, domain-specific analysis.

### Stage Two: Fragment Anchoring Validation

Use the Library of Babel (a deterministic, pseudo-infinite generative text space) to mirror Stage One testing.

Anchor known fragments from canonical texts (scripture, classical works) into the generative space. Use Fragment Anchoring methodology to search for and reconstruct surrounding text.

**Success Criteria**:
- Multiple independent fragment paths converge on the same source text
- Coherence correlation with known passages exceeds 85%
- No cross-contamination between different sources

**Output**: Fragment locations, convergence patterns, iteration logs.

### Stage Three: Topology Mapping (Future)

Use convergence data from Stages One and Two to map the attractor landscape. Predict where new concepts will cluster based on their semantic relationships.

## How Fragment Anchoring Works

### The Process

1. **Start with known fragments**: text you are certain about
2. **Generate hypotheses**: use an LLM to propose adjacent concepts
3. **Create queries**: pair fragments with hypotheses
4. **Search the space**: execute queries in the Library
5. **Score candidates**: measure coherence with known source
6. **Iterate**: use high-scoring candidates as new context

### Key Discipline

- Fragments are *known* (high confidence)
- Hypotheses are *guesses* (not treated as evidence)
- Queries are *tested* (executed and logged)
- Candidates are *scored* (not trusted implicitly)
- Iteration is *systematic* (not haphazard exploration)

The workbook (fragment_search_workbook.py) enforces this separation. Generate it with:

```bash
python fragment_search_workbook.py
```

## Configuration

Edit `config.py` to customize:

- **Embedding models**: architecture, loss, corpus, training
- **Canonical concepts**: the 150+ terms to embed
- **Convergence threshold**: similarity targets
- **Fragment sources**: texts to use as ground truth
- **Iteration limits**: how deep to explore

## Running Experiments

### Command Line (Recommended)

```bash
# Run all stages
python experiments/stage_runner.py

# Run specific stage
python experiments/stage_runner.py --stage 1

# Specify output directory
python experiments/stage_runner.py --output-dir ./my_results
```

### Web Interface

```bash
python app.py
```

Navigate to:
- `/` : Home
- `/stage-one` : Run Stage One test
- `/stage-two` : Run Fragment Anchoring
- `/experiment/run` : Run full experiment
- `/config` : View configuration

### Python API

```python
from experiments.stage_runner import PlatonicHypothesisRunner
from embeddings.convergence_test import ConvergenceTest
from fragment_anchoring.search import FragmentSearch

# Run full experiment
runner = PlatonicHypothesisRunner()
results = runner.run_all()

# Or run individual stages
convergence_test = ConvergenceTest()
results = convergence_test.run()
print(convergence_test.report())

# Fragment search
search = FragmentSearch()
fragment = search.add_fragment("in the beginning")
query = search.add_query([1], ["genesis"], "in the beginning...")
candidates = search.search_query(query)
```

## Interpreting Results

### Stage One Results

`stage_one_results_*.json` contains:

- **mean_pairwise_similarity**: Core metric. Target: >= 0.85
- **std_pairwise_similarity**: Consistency. Lower is better
- **outliers_below_0.7**: How many concept pairs diverge significantly
- **convergence_passed**: Boolean. Hypothesis viable?
- **domain_convergence**: Metrics broken down by semantic category

**Interpretation**:
- If mean similarity >= 0.85: hypothesis viable. Proceed to Stage Two.
- If mean similarity < 0.85: training mechanism matters more than topology. Hypothesis fails.

### Stage Two Results

Fragment anchoring logs:

- **Convergence patterns**: Do independent searches find the same source?
- **Coherence scores**: How well does generated context match known text?
- **Iteration efficiency**: How quickly do queries converge?

**Interpretation**:
- If convergence and coherence both high: same attractor principle operates in text space.
- If results are noisy: generative space behaves differently than embeddings.

## Mathematical Foundation

### Why Attractors Should Exist

Coherent text (and coherent embeddings) occupy narrow regions of high-dimensional space. Not by accident, but by mathematical necessity.

- Coherence is a constraint
- Constraints define regions
- Multiple paths into a region converge at fixed points

### Topology is Fixed

The attractor landscape is determined by the structure of semantic space itself, not by the method used to navigate it.

Different training mechanisms = different paths through the same landscape.

If attractors are truly fixed, different paths should arrive at the same destinations.

### Prediction via Elimination

You predict where representations will be by specifying what they cannot be.

Certain vector combinations violate coherence. Certain semantic relationships are impossible. The intersection of all constraints defines where attractors must exist.

## What We Are NOT Claiming

This is not about consciousness, emergence, or mysticism.

This is mathematics. Topology. Attractor dynamics. Information theory. Standard tools.

The "Platonic" framing is metaphorical shorthand for "mathematical ideals that exist independently of discovery."

## Troubleshooting

**No results in Stage One**:
- Check that numpy is installed: `pip install numpy`
- Verify model count: should be 4 models
- Check convergence threshold in config

**Fragment search timing out**:
- Library generation can be slow
- Consider reducing PAGE_LEN in config.py
- Or reduce number of concepts for testing

**Flask won't start**:
- Check port 5000 is available
- Verify flask is installed: `pip install flask`
- Try running on different port in config.py

## Next Steps

1. Run Stage One: validate embedding convergence
2. If Stage One passes, run Stage Two: validate text space
3. If both pass, explore Stage Three: topology mapping
4. Publish findings

## References

- Original Library of Babel concept: Jorge Luis Borges
- Embedding convergence: emerging research area
- Attractor dynamics: nonlinear dynamical systems theory
- Fragment recovery: classical textual criticism methods

## License

Research project. Share freely. Cite appropriately.

## Questions?

This is a testbed. Experiment. Validate. Report results.

The hypothesis either holds or it doesn't. Data will tell.

<!-- TAGNET README FOOTER — start -->

<div align="center">

**Like this work? Fuel the next widget / experiment / scaffold.**

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-%23FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/e404.tagnet)
[![Patreon](https://img.shields.io/badge/Support-Patreon-ff424d?logo=patreon&logoColor=white&style=for-the-badge)](https://www.patreon.com/VeritasExMachina?utm_campaign=creatorshare_creator)

<small>Crafted with caffeine, curiosity, and a Catppuccin palette · © e404-tagnet</small>

</div>
<!-- TAGNET README FOOTER — end -->
