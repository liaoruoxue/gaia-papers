# Critical Analysis: Inside the Scaffold: A Source-Code Taxonomy of Coding Agent Architectures

## Package statistics

| Item | Count |
|------|------:|
| Modules | 1 (`motivation.py`) |
| Settings | 2 |
| Questions | 0 |
| Claims | 7 (2 independent, 5 derived) |
| Strategies | 5 (all `support`) |
| Operators | 0 |
| Independent leaf priors set | 2 / 2 |
| BP iterations to convergence | 2 (Junction Tree, exact) |

Strategy-type distribution: 100% `support`. This is the appropriate default
for an abstract-only formalisation -- there are no theory-vs-experiment
comparisons, no induction over multiple datasets, and no exhaustive case
splits to model because the source body is not available.

## BP belief summary

| Claim | Role | Belief |
|-------|------|-------:|
| `source_code_taxonomy_built` | leaf | 0.930 |
| `structural_patterns_derived` | leaf | 0.920 |
| `keyword_state_management` | derived | 0.897 |
| `keyword_tool_capability_categories` | derived | 0.897 |
| `keyword_loop_primitives` | derived | 0.892 |
| `keyword_context_compaction` | derived | 0.884 |
| `keyword_agentic_memory` | derived | 0.875 |

All five derived keyword claims land in the 0.87-0.90 band, consistent with
their being directly entailed (modulo the soft `support` priors) by the two
abstract-level leaf claims, with mild variation tracking the prior placed
on each `support` strategy.

## Summary

The package is a minimal but valid formalisation built from the only
material available in the artifact: a two-sentence abstract and a
five-keyword list. Two abstract sentences are extracted as independent leaf
claims (`source_code_taxonomy_built`, `structural_patterns_derived`); the
five keywords (`agentic memory`, `loop primitives`, `context compaction`,
`tool capability categories`, `state management`) are extracted as derived
topic-coverage claims and connected to the abstract leaves through five
parallel `support` strategies (one per keyword). The reasoning graph is
shallow (max depth 1) and contains no contradictions, abductions, or
inductions because the source body is not accessible.

## Weak points

| Claim | Belief | Issue |
|-------|------:|-------|
| `keyword_agentic_memory` | 0.875 | The most interpretive of the five keywords -- agentic memory is not literally one of the three axes ("context, tools, state") named in the abstract; lower `support` prior (0.88) reflects that. |
| `keyword_context_compaction` | 0.884 | Strong textual hook ("context"), but compaction specifically is the inferred mechanism, not a directly stated claim. |

No claim falls below 0.5; no abduction alternative needs review (there are
no abductions). The structural risk is uniformly low because the graph is
small.

## Evidence gaps

The dominant evidence gap is the source itself: this package formalises
only the abstract and keyword list. The following claims could only be
verified or refined with access to the full PDF body:

| Gap | What is missing | What would close it |
|-----|-----------------|---------------------|
| Corpus provenance | Which open-source coding agents were surveyed? Sample size? Selection criteria? | Methods section of the PDF. |
| Taxonomy axes | Are "context / tools / state" the only top-level axes, or just headline examples? | Taxonomy definition section. |
| Memory typology | What concrete memory categories does the taxonomy enumerate? | Results / taxonomy table. |
| Loop-primitive enumeration | Which loop primitives are recognised, with what distinguishing features? | Loop-primitives section. |
| Tool-category schema | What capability categories are used and how are they delineated? | Tool taxonomy section. |

## Contradictions

None modelled. There are no internal tensions in the abstract stub; the
two abstract sentences are mutually reinforcing (a "source-code taxonomy"
is exactly the kind of artefact that arises from "analysing real-world
implementations to derive structural patterns").

## Confidence assessment

| Tier | Belief band | Claims |
|------|-------------|--------|
| Very high (>= 0.90) | 0.90-1.00 | `source_code_taxonomy_built`, `structural_patterns_derived` |
| High (0.75-0.90) | 0.87-0.90 | All five derived keyword-topic claims |
| Moderate / tentative | -- | None |

## Caveats specific to this package

1. **Stub-level formalisation.** No section files (`s2_*.py`, `s3_*.py`,
   ...) exist because the artifact is abstract-only. If/when the full PDF
   is re-ingested, this package should be re-run through the formalisation
   skill to add the body-level claims (the actual taxonomy categories,
   per-axis sub-types, and any quantitative breakdowns of how many
   surveyed agents fall into which bucket).
2. **Keyword claims are interpretive.** Each "keyword" claim restates the
   keyword as a topic-coverage assertion ("the taxonomy provides a
   treatment of X"). These are intentionally conservative -- a future
   formalisation should replace each keyword claim with the corresponding
   concrete taxonomic claim from the PDF body (e.g. the specific list of
   loop primitives, the specific set of tool categories).
3. **Citation coverage.** `references.json` contains only the arXiv
   abstract page and the cited GitHub repository
   (`aorwall/moatless-tools`). No paper-internal citations could be
   extracted from the abstract.
