# 2603-17244-gaia

Gaia formalization of Park (2026), "Graph-Native Cognitive Memory for AI
Agents: Formal Belief Revision Semantics for Versioned Memory
Architectures." Reference implementation: https://github.com/KumihoIO.

## Overview

Park introduces **Kumiho**, a graph-native cognitive memory architecture
whose central architectural thesis is that the structural primitives
required for AI-agent cognitive memory -- immutable revisions, mutable tag
pointers, typed dependency edges, URI-based addressing -- are *identical*
to those required for managing agent-produced outputs (code, designs,
documents, intermediate results) as versionable, addressable, dependency-
linked assets. Rather than building a memory layer plus a separate asset
tracker, Kumiho commits to ONE graph-native primitive set serving both
roles. Agents use the same graph to remember, to find each other's
outputs, and to build upon them.

The central formal contribution is a correspondence between the AGM
belief-revision framework [@AGM1985] and the operational semantics of the
property-graph memory system, framed at the *belief base* level
[@Hansson1999Textbook]. The paper proves satisfaction of the basic AGM
postulates K*2-K*6 plus Hansson's Relevance + Core-Retainment, provides a
principled rejection of the Recovery postulate grounded in immutable
versioning, and formally avoids the Flouris et al. impossibility for
description logics by working over a deliberately weak propositional
fragment $L_G$.

Empirically, Kumiho achieves 0.447 four-category F1 on the official LoCoMo
token-level metric (n=1,540, the highest reported score across retrieval
categories), 97.5% adversarial refusal accuracy (n=446), 93.3% judge
accuracy on LoCoMo-Plus (n=401, vs. 45.7% for the best published baseline
Gemini 2.5 Pro), and 100% pass rate on a 49-scenario AGM compliance test
suite.

## Package Structure

| Module | Section of paper | Content |
|--------|------------------|---------|
| `motivation.py` | Sec. 1 (Introduction + abstract) | Agent-output bottleneck, structural-correspondence insight, headline contributions |
| `s2_related_work.py` | Sec. 2-3 | Per-system characterizations (Graphiti, Mem0, Letta, A-MEM, MAGMA, Hindsight, MemOS), benchmark setup, AGM background, context-extension deficiencies |
| `s3_structural_primitives.py` | Sec. 4-6 + 13 | Asset-management correspondence, Item-Revision-Tag model, kref:// URI scheme, six edge types, seven core design principles |
| `s4_correspondence_thesis.py` | Sec. 4 + 12 | Dual-purpose graph thesis, comparative analysis tables (8, 9), per-baseline comparisons |
| `s5_agm_correspondence.py` | Sec. 7 | Definitions 7.1-7.8, postulates K*2-K*8, Relevance, Core-Retainment, Recovery violation, Levi/Harper identities, Flouris avoidance, complexity bounds |
| `s6_revision_semantics.py` | Sec. 7-8 | NL-to-triple boundary, partial-merging strategies, symbolic/sub-symbolic asymmetric bridge, retrieval semantics under belief revision |
| `s7_kumiho_architecture.py` | Sec. 8-11, 14 | Hybrid retrieval (CombMAX), Dream State pipeline + safety guards, BYO-storage privacy, MCP integration, reference implementation |
| `s8_evaluation.py` | Sec. 15 | Token compression, LoCoMo (Tables 12, 13), LoCoMo-Plus (Tables 15, 16, 17), AGM compliance (Table 18), case studies, limitations |
| `s9_use_cases.py` | Sec. 4.3, 5.2, 10.3 | Multi-agent creative pipeline, decision auditability, coding agents, multi-channel session identity |
| `s10_discussion_limitations.py` | Sec. 16-17 | Future evaluation roadmap, formal extensions (entrenchment, richer logics, partial-merge), conclusion synthesis |
| `s11_wiring.py` | (cross-cutting) | All `support`, `deduction`, `abduction`, `induction`, `contradiction` strategies wiring the claims together |
| `priors.py` | -- | Prior probabilities for 62 independent leaf claims |

## Statistics

- **357 knowledge nodes** (27 settings, 1 question, 329 claims)
- **133 strategies** (12 deduction, 99 support, 2 abduction, 2 compare, 8 induction)
- **2 contradiction operators**
- **62 independent claims with priors** (calibrated 0.25-0.97)
- **BP convergence**: 2 iterations, 807ms (Junction Tree exact inference)

## Top Beliefs (Pass 6)

| Belief | Claim | Significance |
|--------|-------|--------------|
| 1.000 | claim_reference_implementation | Reference impl. (Kumiho server, SDK, MCP, dashboard) is grounded in P2/P8/P9 + complexity bounds |
| 1.000 | claim_conclusion_unification | Conclusion that the contribution is the architectural synthesis + formal grounding |
| 0.999 | claim_locomo_plus_headline | LoCoMo-Plus 93.3% / 98.5% recall vs. best-baseline 45.7% (+47.6pp) |
| 0.999 | claim_recovery_violation | Recovery postulate is intentionally violated by the immutable revision design |
| 0.999 | claim_k5_consistency | K*5 Consistency holds via Supersedes-replaces-not-accumulates |
| 0.997 | claim_p1_structural_reuse | Principle 1: ONE primitive set for memory AND asset management |
| 0.996 | claim_byo_storage_benefits | BYO-storage yields data residency + zero-raw-content + exfiltration-resistance + compliance |
| 0.996 | claim_flouris_avoidance | L_G avoids Flouris DL impossibility via single-layer + propositional connectives + CWA-classical-negation duality |
| 0.994 | claim_agm_correspondence_thesis | Central formal contribution: AGM correspondence at Hansson belief-base level |
| 0.025 | claim_separate_layers_assumption | Separate-memory-vs-asset-layers prevailing view -- correctly suppressed by `contradiction_separate_vs_unified` |

## Critical Findings

- **Headline contribution belief 0.84** -- honest synthesis of five pillars
- **Both abductions correctly resolve**:
  - Structural-correspondence isomorphism (H wins; alternative "just a graph DB" suppressed to 0.36)
  - Recovery-rejection-as-principled (H wins; alternative "architectural bug" suppressed to 0.33)
- **Open empirical question correctly preserved**: unified-vs-multi-graph (Kumiho vs. MAGMA) -- the contradiction operator prevents BP from picking either side, reflecting Park's own framing.

See `ANALYSIS.md` for the full critical analysis (weak points, evidence gaps,
contradictions, confidence assessment).

## License

The source paper [@Park2026Kumiho] is licensed CC BY-NC-ND 4.0 (c) 2026
Kumiho Inc. Contact: support@kumiho.io. This Gaia formalization is
derivative metadata and operates under fair-use citation; the original
paper PDF is included in `artifacts/`.
