"""Prior assignments for independent (leaf) claims."""

from . import (
    claim_silent_errors,
    claim_grounding_errors,
    claim_prm_scaling_failure,
    claim_diversity_over_purity,
    claim_7k_instances,
    claim_process_beats_outcome,
    claim_no_entropy_collapse,
)

PRIORS = {
    # ── Problem characterization (leaf claims from motivation.py) ──────────────
    claim_silent_errors: (
        0.92,
        "Table 1 provides concrete example (5.5km buffer not rendered despite "
        "successful save). The failure mode is well-documented and reproducible.",
    ),
    claim_grounding_errors: (
        0.92,
        "Table 1 provides concrete example (KeyError 'dataset' vs 'Dataset'). "
        "The error type is clearly defined and common in data analysis.",
    ),
    claim_prm_scaling_failure: (
        0.88,
        "Table 2 shows consistent negative scaling across multiple PRMs "
        "(Qwen2.5-Math-PRM-72B: 33.33%→31.33%, Math-Shepherd: 23.28%→19.31%).",
    ),

    # ── RL training (leaf claims from s4_training.py) ──────────────────────────
    claim_process_beats_outcome: (
        0.88,
        "Figure 5(a) shows DataPRM with process reward achieves 78.73% on DABench "
        "and 64.84% on TableBench, outperforming both SFT and outcome-only models. "
        "The experimental result is clearly demonstrated.",
    ),
    claim_no_entropy_collapse: (
        0.87,
        "Figure 5(b)(c) shows outcome-only training causes entropy to drop to ~0.12 "
        "after 200 steps with reward plateauing, while process-supervised training "
        "maintains entropy at ~0.18 with steadily rising reward.",
    ),

    # ── Data pipeline (leaf claims from s3_data.py) ────────────────────────────
    claim_diversity_over_purity: (
        0.85,
        "The paper argues diversity > purity for training data quality, supported "
        "by the pipeline design choice to include error-containing trajectories. "
        "Plausible but the ablation is implicit rather than direct.",
    ),
    claim_7k_instances: (
        0.95,
        "Directly stated in the paper as a fact of the pipeline output.",
    ),
}
