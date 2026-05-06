# LKM Smoke — 2602.07885 MemFly: Compression-Fidelity in Agentic Memory

**Date**: 2026-05-06
**Query**: "information bottleneck compression fidelity tradeoff in agentic memory; greedy AIB algorithm; retrieval-centric memory has limits"

## Match Result

- top_k=15, scores [0.015, 0.029] — slightly higher signal than paper 1
- 14 papers in `data.papers`
- ⚠️ **Self-citation issue**: Top result `MemFly` is the paper itself (DOI 10.48550/arXiv.2602.07885)

→ Pipeline lesson: must filter `data.papers[*].doi` against `arXiv.{paper_id}` before treating as prior.

## Filtered Candidate Priors

| Date | Paper | DOI | Relevance |
|------|-------|-----|-----------|
| 2025-12 | **ABBEL: LLM Agents Acting through Belief Bottlenecks Expressed in Language** | 2512.20111 | ⭐ Same belief-bottleneck framing, 2 months earlier — direct prior |
| 2026-03 | AMemGym: Interactive Memory Benchmarking | 2603.01966 | ❌ Concurrent/later (Mar 2026) — not a prior, but eval set |

## ABBEL Evidence Chain (gcn_ad89e9a84a684d20)

```
Conclusion: "ABBEL with belief-length penalty achieves multi-objective QA on 300-word obs..."
Chain 0: 1 factor / 1 premise
  P0: belief-length penalty for trajectory = -λ(max_t |b_t|)
```

Shallow chain — only 1 premise. Not a P1-P4 rich chain.

## Self-positioning Verify

Should grep MemFly PDF for "ABBEL" / "Lidayan" / "2512.20111".
**TODO**: not yet performed (would need PDF download + pdftotext).

## Verdict

- Compression-fidelity IB framing is **shared with ABBEL** (Dec 2025) but ABBEL is belief-trajectory penalty, MemFly is online IB optimization on streaming history. Distinct enough mathematically.
- Without rich evidence chain, can't do P1-P4 layer-attack mapping. Falls back to qualitative comparison.

## What this tells us about the pipeline

- **Self-citation filter is mandatory**: LKM may index the paper being analyzed; we must exclude it.
- **Date filter recommended**: Papers indexed after the target paper's submission can't be priors (filter by `publication_date` or DOI's arxiv prefix).
- ABBEL has only 1-premise chain — LKM's chain depth varies by paper indexing maturity, not just topic.
