# Fragment Search Workbook

Navigate the library of babble. Find what might exist.

## What This Is

A systematic method for reconstructing or discovering text within a generative probability space using known fragments as Bayesian anchors. You work with phrases you're confident about—things you remember or can verify—then use them to constrain the search through what an LLM could plausibly generate.

This is useful for two overlapping problems:

1. **Recovery**: You've lost a reference to something real. You remember a phrase. Use it to narrow the generative space until you find the coherent context that felt like it surrounded that phrase.
2. **Exploration**: You have fragments that anchor a conceptual territory. What does the generative space naturally produce within that region? Does it cohere? What emerges?

The workbook is your casebook. It enforces the separation between what you *know*, what you *guess*, and what you *found*.

## The Core Idea

Large language models are probability distributions over text. A fragment like "temporal displacement engine" doesn't exist everywhere in that distribution—it clusters around specific conceptual neighbourhoods. 

Your job is to:
1. Start with known fragments (high confidence).
2. Generate plausible neighbours (hypotheses about adjacent concepts).
3. Query the generative space with both anchors.
4. Score what emerges, noting how well it coheres with your fragment.
5. Use promising candidates as new context for the next round.

You're not searching an index. You're biasing a generative process toward regions where your fragment is likely to appear naturally.

## Workflow

### 1. Fragments Sheet
Enter only text you're confident about. Mark the type:
- **exact_string**: Consecutive phrases you remember precisely.
- **isolated_word**: Single words you're certain appeared, but context is fuzzy.
- **concept**: Thematic territory, not literal text.

Confidence should reflect your certainty in recall, not searchability. `1.0` means you're sure this was in the original; `0.5` means you half-remember it.

### 2. Hypotheses Sheet
Use an LLM to propose related phrases, but *record them as hypotheses*. Don't treat them as evidence. Note the fragment they relate to and why they're plausible neighbours.

Example: If you have "nuclear fission," hypotheses might include "chain reaction," "reactor core," "critical mass"—natural semantic adjacencies, not confirmations.

### 3. Queries Sheet
Construct prompts that pair known fragments with hypotheses. The query is the actual instruction to the generative model.

Example query:
```
"Write a paragraph about nuclear fission and chain reaction in a hard science-fiction context."
```

Record:
- The fragments you're anchoring with
- The hypotheses you're testing
- Assumed ordering (which fragment appears first, or proximity assumption)
- Character gap limit (optional; usually irrelevant in generative space)
- Query status: `not_run`, `queued`, `run`, `rejected`, `promising`

### 4. Run Your Queries
Execute these against an LLM (Claude, GPT, local model—your choice). Paste results into the Candidates sheet.

### 5. Candidates Sheet
Score each result without pretending LLM hallucination is evidence. Use these metrics:

- **exact_matches**: How many of your known fragments appear verbatim?
- **distinctive_matches**: Semantic variations of your fragments—close but not identical.
- **order_score**: Do fragments appear in the sequence you specified? (0-5)
- **proximity_score**: How close are anchors to each other? (0-5)
- **coherence_score**: Does the text *feel* like it belonged together? (0-5)
- **topic_score**: Does it stay in the territory you expected? (0-5)

The **total_score** is automatic. Decision field:
- **unreviewed**: Fresh candidate, not yet assessed.
- **promising**: Worth using as context for another round.
- **rejected**: Incoherent or off-target.
- **verified**: Independent evidence supports this (high bar).

### 6. Iterate
Use high-scoring candidates as additional context for the next round of queries. Gradually densify the region around your fragments.

## Important Constraints

**This is not magical.** It's systematic bias injection into a generative process.

- **Fragments must be distinctive.** Common phrases like "the way forward" won't constrain the space; they appear everywhere. Rarer phrases ("temporal displacement engine") are your lever.
- **You're not finding truth; you're finding coherence.** A high-scoring candidate is *plausible*, not *proven*. Treat it as evidence only if you have external verification.
- **Coherence ≠ accuracy.** An LLM can generate beautifully coherent nonsense. Hypotheses are not facts.
- **The generative space shifts.** Different models, different prompts, different temperatures—you'll get different results. Document your model and settings.

## When to Stop

Mark a candidate **verified** only when:
1. You've found it independently (found the actual source).
2. Multiple independent model runs converge on the same text.
3. The fragment appears in external corpora.

One coherent generation is not enough. That's how you end up with confident false memories.

## Tips

- **Seed with multiple fragments** if you have them. Two anchors define a narrower region than one.
- **Vary your hypotheses.** If one set doesn't yield promising candidates, try different adjacent concepts.
- **Document everything.** Note which model, which prompt version, which parameters. Reproducibility matters.
- **Use temperature/sampling strategically.** Low temperature (coherent, narrow) for verification queries. Higher temperature (exploratory) for hypothesis generation.
- **Don't fall in love with candidates.** Humans are pattern-matching machines. You'll unconsciously rate candidates higher if they *feel* right. Make your scoring rubric explicit and stick to it.

## The Philosophical Bit

This approach treats the "library of babble" as a real thing—a probability space of all coherent texts. Most of what's in that space doesn't exist in the real world. But some of it does, or *could*. Your fragments are your anchor. Everything else is navigation.

If you're recovering something real, you're using probability to bias the search toward where truth clusters. If you're exploring, you're using fragments to ask: "What does the generative space naturally produce in this neighbourhood?"

Both are valid. Just don't confuse them.
