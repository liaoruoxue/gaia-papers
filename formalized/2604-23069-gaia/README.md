# 2604-23069-gaia

Gaia formalization of Wu et al. (2026), "ContextWeaver: Selective and
Dependency-Structured Memory Construction for LLM Agents."
([arXiv:2604.23069](https://arxiv.org/abs/2604.23069))

## Overview

Wu et al. introduce **ContextWeaver**, a selective and dependency-structured
memory framework for tool-using LLM agents. The paper diagnoses a structural
gap shared by sliding-window, prompt-compression, and retrieval-based memory
systems: all three select content by *recency*, *salience*, or *semantic
similarity*, none of which captures the *dependency structure* (causal:
tool-output triggers follow-up edit; logical: a step reuses, refines, or
resolves an earlier hypothesis) that links one reasoning step to the next.

ContextWeaver replaces these dependency-blind signals with an explicit
**directed acyclic graph (DAG)** over reasoning steps, built incrementally
via three coordinated components: (1) a **dependency-based construction
module** that links each step to the earlier steps it relies on through an
LLM-based Logical Dependency Analyzer; (2) **compact dependency summaries**
that condense root-to-step paths into reusable per-node units; and (3) a
**lightweight validation layer** that records execution outcomes (passed /
failed / unknown / superseded) and excludes failed/superseded nodes from
future parent selection. The framework's output is a *weaved* context that
keeps full thought-action-observation triples for ancestors and compresses
observations of non-ancestors with the same lightweight placeholder used by
the sliding-window baseline -- isolating *selection mechanism* from
*compression intensity*.

Empirically, on **SWE-Bench Verified** and **SWE-Bench Lite**, ContextWeaver
improves pass@1 over a sliding-window baseline (Claude Sonnet 4 Unified:
66.0 vs 63.2 Verified, 53.7 vs 52.3 Lite; GPT-5 Hybrid: 58.6 vs 57.4
Verified, 51.3 vs 48.3 Lite) *while* reducing reasoning steps (-4.7%
Verified, -7.3% Lite iterations) and tokens-per-resolve (-2.8% Verified,
-2.3% Lite). On a 100-instance Verified subset (5 runs, Claude Sonnet 4),
ContextWeaver also exhibits lower run-to-run variance (1.55 vs 1.94 std).
The Unified-vs-Hybrid contrast on GPT-5 (Unified underperforms Sliding
Window; Hybrid -- where Claude builds the graph -- outperforms it) is the
paper's key evidence that *graph-construction quality*, not raw execution
capability, mediates the gain.

## Package Structure

| Module | Section of paper | Content |
|--------|------------------|---------|
| `motivation.py` | Sec. 1 + Abstract | Long-context limits, recency/salience/similarity gap, three-component thesis, headline empirical claim |
| `s2_related_work.py` | Sec. 2 | Per-family limitations (compression, retrieval/hierarchical, episodic graphs, static analysis, LLM summarization), cross-family dependency-gap synthesis |
| `s3_setup.py` | Sec. 3 (preamble) | Algorithm 1 four-step pipeline, node structure, DAG / multi-parent design, hyperparameters W and m, weaved-context definition |
| `s4_dependency_construction.py` | Sec. 3.1 | Node Extraction (query-conditioned), Parent Selection (Logical Dependency Analyzer + Top-m), Ancestry BFS, Context Weaving rule, observation-compression placeholder, Appendix E.2 walkthrough |
| `s5_dependency_summarization.py` | Sec. 3.2 | Incremental recurrence dep_summary_k = LLM_SUM({parent.dep_summary}, summary_k), reusable-unit + cost advantages, usage discipline (analyzer-only, never injected into agent context) |
| `s6_validation_layer.py` | Sec. 3.3 | TestTracker per-test parsing, ValidationDetector node-level labels (passed/failed/unknown/superseded), failed/superseded skipping rule, prepended test summary |
| `s7_evaluation.py` | Sec. 4.1 | SWE-Bench Verified + Lite, Claude Sonnet 4 / GPT-5 / Gemini 3 Flash, SWE-Agent harness, sliding-window + LLM-summarization baselines, Unified vs. Hybrid regimes, variance protocol |
| `s8_main_results.py` | Sec. 4.2-4.4 | Table 1 (per-(model, benchmark) pass@1), Table 2 (variance subset), case studies (django-14631, pytest-7205), iteration scaling (Fig. 2a), token efficiency (Fig. 2b), iteration distribution (Fig. 4) |
| `s9_ablations.py` | Sec. 4.5-4.6 + App. F.1 | Table 3a (DAG vs Tree), Table 3b (window-size sensitivity), Table 4a (GPT-4o cross-model sanity check) |
| `s10_discussion_limitations.py` | Sec. 5 + Limitations + App. E.1 | Conclusion, future work, test-driven scope limitation, LLM-builder dependency, qualitative-error-analysis findings (38 unique CW vs 27 unique SW solves out of 500) |
| `s11_wiring.py` | (cross-cutting) | All `support` / `induction` / `abduction` / `compare` / `contradiction` strategies wiring premises -> conclusions across modules |

## Headline Empirical Results (Verbatim from the paper)

### Table 1: Performance Comparison Across Settings (pass@1, %)

| Model | Method | Verified | Lite |
|-------|--------|---------:|-----:|
| Claude Sonnet 4 | **ContextWeaver** | **66.0** | **53.7** |
| Claude Sonnet 4 | Sliding Window | 63.2 | 52.3 |
| Claude Sonnet 4 | LLM Summarization | 64.2 | 53.0 |
| GPT-5 | ContextWeaver | 56.8 | 42.0 |
| GPT-5 | ContextWeaver -- Hybrid | **58.6** | **51.3** |
| GPT-5 | Sliding Window | 57.4 | 48.3 |
| GPT-5 | LLM Summarization | 46.7 | 32.3 |
| Gemini 3 Flash | ContextWeaver | 58.4 | **47.0** |
| Gemini 3 Flash | Sliding Window | **60.4** | 46.0 |
| Gemini 3 Flash | LLM Summarization | 56.8 | 43.3 |

### Table 2: 100-Instance Verified Subset, 5 Runs (Claude Sonnet 4)

| Method | Pass@1 (%) | Pass@5 (%) | Avg Steps | % Instances Fewer Steps |
|--------|-----------:|-----------:|----------:|------------------------:|
| **ContextWeaver** | **68.0 +/- 1.55** | **81.0** | **55.8** | **73%** |
| Sliding Window | 67.2 +/- 1.94 | 78.0 | 59.2 | 27% |

### Efficiency Summary

- **Tokens-per-resolve savings**: -2.8% Verified, -2.3% Lite (Claude Sonnet 4)
- **Iteration savings**: -4.7% Verified, -7.3% Lite (averaged over all + over resolves)
- **Run-to-run variance reduction**: 1.55 (CW) vs 1.94 (SW) std on 100-instance Verified

## Reasoning Graph

```mermaid
---
config:
  flowchart:
    rankSpacing: 80
    nodeSpacing: 30
---
graph TB

    classDef premise fill:#ddeeff,stroke:#4488bb,color:#333
    classDef exported fill:#d4edda,stroke:#28a745,stroke-width:2px,color:#333
    classDef weak fill:#fff9c4,stroke:#f9a825,stroke-dasharray: 5 5,color:#333
    classDef contra fill:#ffebee,stroke:#c62828,color:#333
```

For the full per-module reasoning graph, see `.github-output/docs/`. For the
package's analytical assessment (weak points, evidence gaps, confidence
tiers), see `ANALYSIS.md`.

## Belief Propagation Summary

- **Method**: Junction Tree (exact)
- **Convergence**: 2 iterations, 45 ms
- **Total beliefs computed**: 147
- **Top-5 named beliefs**:
  - `contra_recency_sufficient_vs_cw` -- 0.9994 (the contradiction operator forces the recency-suffices foil down)
  - `claim_gpt5_hybrid_verified` -- 0.9990
  - `pred_graph_quality_mediator` -- 0.9989
  - `claim_algorithm1_steps` -- 0.9960
  - `pred_execution_capability` -- 0.9954

The headline empirical claim `claim_headline_swe_bench` reaches BP belief
**0.96**; the dependency-modeling thesis `claim_dependency_modeling_thesis`
reaches **0.72**; the prevailing recency/salience/similarity-suffices foil
`claim_separate_layers_assumption` is suppressed to **0.22**.

## Source

Wu, Yating; Zhang, Yuhao; Ghosh, Sayan; Basu, Sourya; Deoras, Anoop; Huan,
Jun; Gupta, Gaurav. *ContextWeaver: Selective and Dependency-Structured
Memory Construction for LLM Agents.* arXiv:2604.23069v1 [cs.CL], 24 Apr
2026. ([arxiv.org/abs/2604.23069](https://arxiv.org/abs/2604.23069))
