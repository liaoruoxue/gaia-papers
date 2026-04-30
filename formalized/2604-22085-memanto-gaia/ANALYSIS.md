# Memanto: Typed Semantic Memory — Formalization Analysis

**Source**: [2604.22085](https://arxiv.org/abs/2604.22085) — "Memanto: Typed Semantic Memory with Information-Theoretic Retrieval for Long-Horizon Agents"
**Package**: `2604-24198-memanto-gaia`
**Date**: 2026-04-30

## Package Statistics

- **89 knowledge nodes** (11 settings, 2 questions, 76 claims)
- **15 strategies** (10 support, 1 deduction, 4 via composite/induction)
- **1 operator** (contradiction: vector-sufficient vs graph-necessary)
- **16 independent premises** with priors, 15 derived via BP, 44 orphaned (per-category scores + limitations)
- **Treewidth**: low, converged in 2 iterations (JT exact)

## Belief Propagation Results

| Claim | Belief | Type | Role |
|-------|--------|------|------|
| claim_recall_over_precision | 0.874 | derived | Key architecture principle |
| claim_vector_only_top | 0.910 | derived | Memanto top vector-only system |
| claim_memanto_competitive_simpler | 0.859 | derived | Competitive with simpler architecture |
| claim_memory_tax_exists | 0.845 | derived | Memory tax quantified |
| claim_zero_ingestion | 0.834 | derived | Zero-cost ingestion |
| claim_deterministic_retrieval | 0.873 | derived | ITS deterministic retrieval |
| claim_llm_noise_tolerance | 0.857 | derived | LLMs tolerate noisy context |
| claim_k40_inflection | 0.882 | derived | k=40 inflection point |
| claim_prompt_limited | 0.905 | derived | Prompt optimization limited |
| claim_vector_sufficient | 0.797 | derived | Vector-only sufficient |
| claim_core_thesis | 0.813 | derived | Main thesis (exported) |
| claim_graph_necessary | 0.051 | leaf | Alternative (rejected) |
| claim_conflict_resolution_prevents_drift | 0.750 | leaf | Design claim (unverified) |

## Structural Observations

### 1. Architecture Claims Stronger Than Main Result
As with the DataPRM formalization, architecture-level claims (recall_over_precision 0.874, deterministic_retrieval 0.873, vector_only_top 0.910) are individually stronger than the core thesis (0.813). The thesis depends on vector_sufficient (0.797) + recall_over_precision (0.874), and vector_sufficient is pulled down by the contradiction with graph_necessary — even though graph_necessary itself is near zero (0.051). The contradiction operator creates coupling that modestly suppresses vector_sufficient.

### 2. Contradiction Correctly Picks a Side
`claim_graph_necessary` (0.051) vs `claim_vector_sufficient` (0.797): the BP strongly rejects "graph augmentation is necessary" given Memanto's competitive performance. The contradiction operator correctly resolves this.

### 3. Recall Over Precision Is the Strongest Derived Principle
At 0.874, this is the most robust architectural finding. It has four high-confidence empirical premises (Stage 2 & 3 results) with a strong prior (0.92). This principle transfers beyond Memanto — any agentic memory system should prioritize recall expansion over precision engineering.

### 4. Weakest Point: Conflict Resolution
`claim_conflict_resolution_prevents_drift` (0.750) is the lowest-confidence non-orphaned claim. The mechanism exists by design, but the paper provides no independent empirical measurement of drift prevention. Future work could stress-test this with adversarial contradictory memory injection.

### 5. Core Thesis at 0.813
Moderate — pulled down by vector_sufficient's 0.797 (which is itself suppressed by the contradiction). The thesis is structurally sound but depends on a contested claim (whether vector-only is truly sufficient). Multi-hop weakness (70.8%) is an orphan that could challenge vector_sufficient if connected.

## Evidence Gaps

| Gap | What would strengthen it |
|-----|------------------------|
| Conflict resolution effectiveness | Stress-test with adversarial contradictions; measure drift with/without resolution |
| Vector-only sufficiency | Test on non-conversational tasks (code generation, research, multi-agent) |
| Multi-hop reasoning | Connect claim_multi_hop_weak (70.8%) to claim_vector_sufficient — currently orphaned |
| Scale under concurrency | Load test with 1000+ concurrent agents |
| MIB lossless claim | Independent benchmark of 32x compression vs full-dimension retrieval |

## Unmodeled Tensions

- **Multi-hop weakness vs vector-sufficiency**: LOCOMO Multi-Hop at 70.8% suggests graphs may help for complex cross-reference reasoning. This is not modeled as a contradiction (both can be true — vector-only is sufficient overall but weak for multi-hop), but it limits the scope of vector_sufficient.
- **Inference model contribution**: Stage 5 (Gemini 3 upgrade) added +4.8 pp, suggesting results may be partially attributable to model quality rather than memory architecture. Not modeled as a competing explanation.
- **Moorcheh dependency**: The ITS engine is proprietary (Moorcheh.ai cloud). Results depend on this specific engine and may not transfer to other vector stores.
