"""Priors for arXiv 2601.12030: ARC — Active and Reflection-driven Context Management.

All claims here are independent (leaf) premises in the BP graph — i.e., they are
not the conclusion of any strategy. Priors reflect reviewer confidence that the
claim is true as stated, given the paper's evidence quality and external context.

The paper's main empirical content is anchored on four observation tables
(Tables 1-4). These observation claims get high priors (~0.95) because reading
numbers off a table is highly reliable. Derived "ARC outperforms X" /
"ARC frequency is best" etc. are the conclusions of support strategies and
inherit their belief from BP propagation, so they are NOT priored here.

Independent narrative leaves (limitations, motivation primitives, counterfactuals
used as contradiction targets) are also priored individually below.
"""

from . import (
    # Motivation independent leaves
    context_rot,
    raw_history_limitation,
    passive_summarization_limitation,
    passive_strategies_share_limitation,
    # Methodology mechanism claims (used as premises, treated as independent leaves)
    incremental_preserves_evidence,
    reflection_enables_repair,
    decoupling_enables_reuse,
    # Observation tables (the empirical anchors)
    table1_observation,
    table2_observation,
    table3_observation,
    table4_observation,
    # Counterfactual leaves used as contradiction targets
    react_better_than_arc,
    resum_better_than_arc,
    checklist_alone_strong,
    cm_emergent_only,
    budget_triggered_best,
    # Limitations (acknowledged by authors)
    limitation_overhead,
    limitation_scope,
    limitation_training_data,
)

PRIORS = {
    # --- Motivation primitives (well-attested in the literature) ---
    context_rot: (
        0.85,
        "Context rot is a documented phenomenon (Hong et al., 2025 and prior work on attention "
        "dilution / long-context degradation). High confidence the framing is sound, slight "
        "discount because the framing collapses several distinct mechanisms (credit assignment, "
        "representational bottleneck, attention dilution) under one label."
    ),
    raw_history_limitation: (
        0.88,
        "ReAct-style raw concatenation is widely documented to scale poorly with horizon length. "
        "High confidence; small discount because some recent long-context models tolerate raw "
        "history better than older ones."
    ),
    passive_summarization_limitation: (
        0.82,
        "The argument that passive summarization is limited rests on plausible mechanism "
        "(early errors persist after compression) plus indirect support from the paper's own "
        "ARC vs ReSum comparison. Moderate-high confidence; the limitation is real but the "
        "magnitude is debated."
    ),
    passive_strategies_share_limitation: (
        0.78,
        "The shared-limitation framing is a useful synthesis but has a slight tendency to "
        "strawman by characterizing all length-driven approaches uniformly. The core point "
        "(no semantic re-evaluation) is sound."
    ),

    # --- Methodology mechanism claims (used as premises in strategies) ---
    # These describe the design rationale of ARC's two mechanisms. They are
    # mostly definitional / mechanistic claims that follow from the architecture.
    incremental_preserves_evidence: (
        0.85,
        "The claim that always-on incremental summarization preserves the most recent turn's "
        "semantics before abstraction accumulates is largely a design property of the per-turn "
        "summarize-then-update protocol. High confidence; small discount because 'preserves "
        "evidence' depends on the fidelity of the summarizer, which is empirical."
    ),
    reflection_enables_repair: (
        0.88,
        "Reflection's non-local rewrite capability is definitional in the operator R (Eq. 2). "
        "High confidence the mechanism is as described; small residual uncertainty because the "
        "quality of the repair depends on the CM's ability to detect actual misalignment, which "
        "is itself imperfect."
    ),
    decoupling_enables_reuse: (
        0.9,
        "The decoupling between Actor and CM is structural — once the CM has its own model and "
        "its own training signal, it can be plugged into different Actors. The Section 4.4 "
        "experiment substitutes CMs to demonstrate this in practice. Very high confidence."
    ),

    # --- Observation tables (high confidence: direct numeric reads of authors' tables) ---
    table1_observation: (
        0.95,
        "Table 1 numbers are direct reads of the authors' reported experimental results across "
        "5 actors x 5 benchmarks. Very high confidence the numbers are reported as stated. "
        "Residual uncertainty: small possibility of typos / rounding artifacts. Whether the "
        "numbers are reproducible across seeds is a separate question (the paper does not "
        "report seed-level variance for Pass@1)."
    ),
    table2_observation: (
        0.95,
        "Table 2 ablation numbers are direct reads of the authors' reported values. Very high "
        "confidence as a textual report. Same caveat about seed-level variance applies; the "
        "Reflection+Checklist-Only catastrophic drop on BrowseComp-ZH (6.9) is large enough "
        "to be robust to noise."
    ),
    table3_observation: (
        0.93,
        "Table 3 CM-choice numbers are direct reads. High confidence as reported. Slight "
        "discount because ARC-CM training data may overlap with evaluation distribution in "
        "ways not fully ablated, which could inflate ARC-CM's relative advantage."
    ),
    table4_observation: (
        0.93,
        "Table 4 frequency numbers are direct reads, averaged across three benchmarks. High "
        "confidence; small discount because averaging across heterogeneous benchmarks can "
        "obscure benchmark-specific reversals."
    ),

    # --- Counterfactual leaves (these are the negations the paper argues against; ---
    #     they are independent leaves whose contradiction-strategies pull belief down)
    react_better_than_arc: (
        0.5,
        "Neutral prior: the counterfactual claim that ReAct beats ARC is independent of its "
        "negation in the BP graph. The contradiction strategy against Table 1 will drive its "
        "posterior toward zero."
    ),
    resum_better_than_arc: (
        0.5,
        "Neutral prior on the counterfactual that ReSum beats ARC; contradiction against "
        "Table 1 will drive the posterior down."
    ),
    checklist_alone_strong: (
        0.5,
        "Neutral prior on the counterfactual that checklist-only reflection is strongly "
        "beneficial; contradiction against Table 2 will drive it down."
    ),
    cm_emergent_only: (
        0.5,
        "Neutral prior on the counterfactual that CM quality is purely emergent from scale; "
        "contradiction against Table 3 will drive it down."
    ),
    budget_triggered_best: (
        0.5,
        "Neutral prior on the counterfactual that budget-triggered management is best; "
        "contradiction against Table 4 will drive it down."
    ),

    # --- Limitations (author-acknowledged) ---
    limitation_overhead: (
        0.92,
        "The CM is an additional model call; the overhead is essentially definitional. Very "
        "high confidence."
    ),
    limitation_scope: (
        0.9,
        "The paper explicitly evaluates only on info-seeking benchmarks. The scope limitation "
        "is a factual statement about what was tested, with very high confidence."
    ),
    limitation_training_data: (
        0.85,
        "The CM is SFT-trained on filtered trajectories; the dependence on curated data is a "
        "real practical limitation. High confidence; small discount because data efficiency "
        "is an active research area and the limitation may be partly addressable."
    ),
}
