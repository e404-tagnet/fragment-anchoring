<!-- TAGNET README HEADER — Catppuccin Mocha — do not edit by hand -->
<div align="center">

[![License](https://img.shields.io/github/license/e404-tagnet/fragment-anchoring?color=313244&labelColor=11111b&label=License&style=flat-square)](https://github.com/e404-tagnet/fragment-anchoring/blob/main/LICENSE)
[![Status](https://img.shields.io/badge/Status-wip-f9e2af?labelColor=11111b&style=flat-square)](https://github.com/e404-tagnet/fragment-anchoring/pulse)
[![Version](https://img.shields.io/github/v/release/e404-tagnet/fragment-anchoring?color=313244&labelColor=11111b&label=Version&style=flat-square)](https://github.com/e404-tagnet/fragment-anchoring/releases)
[![Repo](https://img.shields.io/badge/Repo-fragment-anchoring-94e2d5?labelColor=11111b&style=flat-square&logo=github&logoColor=94e2d5)](https://github.com/e404-tagnet/fragment-anchoring)
[![Tagnet](https://img.shields.io/badge/By-Tagnet-89dceb?labelColor=11111b&style=flat-square&logo=tag&logoColor=89dceb)](https://tagnet.dev)

</div>
<!-- TAGNET README HEADER — end -->

# fragment-anchoring

A research testbed for navigating generative text spaces with known fragments as anchors.

The rough idea: if you have a phrase or concept you are sure about, you can use it as a Bayesian constraint to bias search through an otherwise unbounded language model probability space. This repo builds the machinery to test that claim in a controlled way.

## What lives here

Three pieces, oldest to newest:

* `archived/` — early Library of Babel experiments, Python clones and sketches. Kept for reference but not the active work.
* `library_of_babel_project/` — a working Flask web app around a deterministic Babel-style generator. Lets you search by text, browse by address, run snippet searches, and generate seeded pages.
* `platonic-hypothesis/` — the current focus. A framework for testing whether semantic attractors in embedding space show up as convergent regions in generative text space too. It has embedding convergence tests, a fragment search engine, and the positioning write-ups.

The two documents worth reading first are both in `platonic-hypothesis/`:

* `Positioning_Fragment_Anchoring_Library_of_Babel.md` — why the Library of Babel is a good testbed for the method.
* `Positioning_Platonic_Representation_Hypothesis.md` — the larger claim about fixed semantic attractors and the three-stage experiment to test it.

## Quick start

If you just want to play with the Library of Babel web app:

```bash
cd library_of_babel_project
pip install flask
python app.py
```

Then open `http://127.0.0.1:5000`.

If you want to run the current experiments:

```bash
cd platonic-hypothesis
pip install -r requirements.txt
python experiments/stage_runner.py
```

## The claim in one sentence

Coherent text and coherent representations may cluster in narrow regions of their respective spaces. Known fragments give us coordinates for finding those regions.

## Status

This is a work in progress. Stage One (embedding convergence) and Stage Two (fragment anchoring in the Library) are partially implemented. Stage Three (topology mapping) is still mostly a plan.

## License

GPL-3.0. See [LICENSE](./LICENSE).

<!-- TAGNET README FOOTER — start -->
---

<div align="center">

**Like this work? Fuel the next widget / experiment / scaffold.**

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-%23FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/e404.tagnet)
[![Patreon](https://img.shields.io/badge/Support-Patreon-ff424d?logo=patreon&logoColor=white&style=for-the-badge)](https://www.patreon.com/VeritasExMachina?utm_campaign=creatorshare_creator)

<small>Crafted with caffeine, curiosity, and a Catppuccin palette · © e404-tagnet</small>

</div>
<!-- TAGNET README FOOTER — end -->
