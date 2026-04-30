# Critical Analysis: How are AI agents used? Evidence from 177,000 MCP tools

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

Strategy-type distribution: 100% `support`. This is the appropriate default for
an abstract-only formalisation -- there are no theory-vs-experiment comparisons,
no induction over multiple datasets, and no exhaustive case splits to model
because the source body is not available.

## BP belief summary

| Claim | Role | Belief |
|-------|------|-------:|
| `empirical_177k_tools_analyzed` | leaf | 0.920 |
| `evidence_based_scale_study` | leaf | 0.930 |
| `keyword_tool_ecosystem_monitoring` | derived | 0.897 |
| `keyword_agentic_action` | derived | 0.884 |
| `keyword_mcp_server_usage_trends` | derived | 0.863 |
| `keyword_agent_consequentiality` | derived | 0.841 |
| `keyword_high_stakes_ai_deployment` | derived | 0.816 |

All five derived keyword claims land in the 0.82-0.90 band, consistent with
their being directly entailed (modulo the soft `support` priors) by the two
abstract-level leaf claims.

## Summary

The package is a minimal but valid formalisation built from the only material
available in the artifact: a two-sentence abstract and a five-keyword list.
Two abstract sentences are extracted as independent leaf claims; the five
keywords are extracted as derived topic-coverage claims and connected to the
abstract leaves through five `support` strategies (one per keyword), with the
`high_stakes` strategy chained on top of `consequentiality` and
`usage_trends`. The resulting reasoning graph is shallow (max depth 2) and
contains no contradictions, abductions, or inductions because the source body
is not accessible.

## Weak points

| Claim | Belief | Issue |
|-------|------:|-------|
| `keyword_high_stakes_ai_deployment` | 0.816 | Two-hop derivation; if either upstream keyword claim is weakened, this one decays faster. |
| `keyword_agent_consequentiality` | 0.841 | The strongest interpretive leap from the abstract -- "consequentiality" is not literally stated, only implied by the keyword list. Lower `support` prior (0.80) reflects that. |

No claim falls below 0.5; no abduction alternative needs review (there are
no abductions). The structural risk is uniformly low because the graph is
small.

## Evidence gaps

The dominant evidence gap is the source itself: this package formalises only
the abstract and keyword list. The following claims could only be verified
or refined with access to the full PDF body:

| Gap | What is missing | What would close it |
|-----|-----------------|---------------------|
| Tool population provenance | How were the 177,000 tools sampled? Snapshot date? | Methods section of the PDF. |
| Usage-trend specifics | Which tool categories dominate, by what factor? | Results section / figures. |
| Consequentiality classification | What scheme distinguishes consequential from advisory tools? | Methods + taxonomy section. |
| High-stakes category list | Which categories are flagged high-stakes, with what criteria? | Discussion / risk-assessment section. |

## Contradictions

None modelled. There are no internal tensions in the abstract stub; the two
abstract sentences are mutually reinforcing ("empirical analysis of N tools"
+ "evidence-based study of how agents use tools at scale").

## Confidence assessment

| Tier | Belief band | Claims |
|------|-------------|--------|
| Very high (>= 0.90) | 0.90-1.00 | `evidence_based_scale_study`, `empirical_177k_tools_analyzed` |
| High (0.75-0.90) | 0.82-0.90 | All five derived keyword-topic claims |
| Moderate / tentative | -- | None |

## Caveats specific to this package

1. **Stub-level formalisation.** No section files (`s2_*.py`, `s3_*.py`, ...)
   exist because the artifact is abstract-only. If/when the full PDF is
   re-ingested, this package should be re-run through the formalisation skill
   to add the body-level claims.
2. **Keyword claims are interpretive.** Each "keyword" claim restates the
   keyword as a topic-coverage assertion ("the work provides evidence on X").
   These are intentionally conservative -- a future formalisation should
   replace each keyword claim with the corresponding concrete empirical
   claim from the PDF body.
3. **Citation coverage.** `references.json` contains only the MCP protocol
   site and the `modelcontextprotocol/servers` registry. No paper-internal
   citations could be extracted from the abstract.
