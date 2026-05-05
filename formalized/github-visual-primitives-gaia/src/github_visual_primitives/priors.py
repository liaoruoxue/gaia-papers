"""Priors for independent (leaf) claims in the DeepSeek Visual Primitives
formalization.

Calibration philosophy
----------------------

The Visual Primitives GitHub repository [@DeepSeekVisualPrimitives] was
released on 2026-04-30 and shortly afterward withdrawn. This package is
reconstructed from secondary sources -- a CSDN deep read
[@CSDNDeepRead], Phoenix Technology coverage [@PhoenixTech] and 36Kr
coverage [@ThirtySixKr]. Source-reliability discounts are applied as
follows:

* **Architectural and design claims corroborated across multiple
  secondary sources** (architecture table, training pipeline diagram,
  cold-start data table, 3-way reward model components, two-stage
  filter pipeline) -- 0.78-0.85. These are detailed descriptions that
  appear consistently across CSDN / Phoenix Technology / 36Kr and
  could not have been independently fabricated by any single
  re-reporter.
* **Empirical numerical results from the headline table** (Pixmo-Count
  / Maze Navigation / Path Tracing per-method scores) -- 0.72-0.80.
  These depend on the original repo's reported numbers; without the
  original repo we cannot independently verify them, and a withdrawn-
  then-reconstructed source justifies a conservative prior.
* **Foil claims used as alternatives in contradictions and abductions**
  (Perception-Gap-is-bottleneck assumption; more-tokens-equals-better
  assumption; trivial-confounds alternative) -- 0.20-0.35. These are
  *foils* against which the source argues; they are not claims of the
  source itself and should be suppressed by their respective
  contradictions / abductive comparisons.
* **Foundational language-property claim** (natural language is
  intrinsically imprecise for continuous visual reference) -- 0.85.
  Author-stated foundational diagnosis; well-grounded in linguistic /
  cognitive-science observations about the role of relational vs
  indexical reference.
* **Industry-state claim** (frontier models scale resolution / token
  count) -- 0.92. Widely-documented, multiply-corroborated state of
  practice.
* **Limitation observations** (trigger-word dependency, topology
  generalization weakness) -- 0.75. The source flags these limitations
  itself; the empirical evidence behind them is not separately
  reported in the secondary sources, so we discount modestly for
  reconstruction uncertainty.
"""

from .motivation import (
    claim_industry_chases_perception,
    claim_natural_language_imprecise_in_continuous_space,
)
from .s2_diagnosis_reference_gap import (
    claim_perception_gap_is_actual_bottleneck,
)
from .s4_architecture import (
    claim_architecture_table,
)
from .s5_data_pipeline import (
    claim_coldstart_table,
    claim_pretrain_filter_table,
)
from .s6_training_pipeline import (
    claim_pipeline_diagram,
)
from .s7_reward_model import (
    claim_format_rm,
    claim_quality_rm,
    claim_task_accuracy_rm,
)
from .s8_results import (
    claim_more_tokens_is_better,
    claim_results_table,
)
from .s9_limitations import (
    claim_lim_topology_weakness,
    claim_lim_trigger_word_dependency,
)
from .s11_wiring import (
    claim_alt_trivial_confounds,
)


PRIORS: dict = {
    # ---------------------------------------------------------------------
    # Foundational language property claim (the headline of the diagnosis)
    # ---------------------------------------------------------------------
    claim_natural_language_imprecise_in_continuous_space: (
        0.85,
        "Foundational diagnosis: natural language is intrinsically "
        "imprecise for continuous visual reference. Author-stated "
        "structural property; well-grounded in linguistic / "
        "cognitive-science observations about the role of relational "
        "vs indexical reference. The Visual Primitives paper builds "
        "the entire Reference-Gap argument on top of this.",
    ),

    # ---------------------------------------------------------------------
    # Industry state claim (multiply corroborated state of practice)
    # ---------------------------------------------------------------------
    claim_industry_chases_perception: (
        0.92,
        "Frontier multimodal LLMs (GPT-5.4, Claude 4.6, Gemini 3 "
        "Flash) explicitly scale input resolution and visual-token "
        "budget; this is documented in their public model cards and "
        "across multiple independent practitioner reports.",
    ),

    # ---------------------------------------------------------------------
    # Architectural / design tables corroborated across secondary sources
    # ---------------------------------------------------------------------
    claim_architecture_table: (
        0.82,
        "Architecture summary table (DeepSeek-ViT 14x14 + 3x3 patch "
        "merge + CSA 4x + V4-Flash MoE 284B/13B + 7056x end-to-end). "
        "Numbers cross-validated across CSDN / Phoenix Tech / 36Kr "
        "coverage; modest discount for source-reliability since the "
        "GitHub repo was withdrawn.",
    ),
    claim_pretrain_filter_table: (
        0.8,
        "Pre-training filter table (97,984 -> 43,141 -> 31,701). "
        "Numbers cross-validated across multiple secondary sources; "
        "discount for the withdrawn repo.",
    ),
    claim_coldstart_table: (
        0.8,
        "Cold-start data composition table (Counting ~10K + VQA ~9K "
        "+ Maze 460K + Path Tracing 125K). Per-task design columns "
        "cross-validated; discount for the withdrawn repo.",
    ),
    claim_pipeline_diagram: (
        0.83,
        "Four-phase Expert-Merge-Distill pipeline diagram. The "
        "phase decomposition is consistent across secondary sources "
        "and matches DeepSeek's prior GRPO + RFT + distillation "
        "engineering practice.",
    ),

    # ---------------------------------------------------------------------
    # 3-way reward model components (design claims, not numbers)
    # ---------------------------------------------------------------------
    claim_format_rm: (
        0.83,
        "Format RM = rule-based {0,1} primitive-format + redundancy "
        "checker. Component design described consistently across "
        "secondary sources.",
    ),
    claim_quality_rm: (
        0.8,
        "Quality RM = LLM judge with {0, 0.5, 1.0} scoring on "
        "redundancy / consistency / self-contradiction / reward "
        "hacking. The four axes are described across secondary "
        "sources; modest discount because the LLM judge prompt and "
        "calibration are not publicly documented.",
    ),
    claim_task_accuracy_rm: (
        0.8,
        "Task-Specific Accuracy RM with per-task scoring (Counting "
        "smoothed exp decay; Maze: exploration progress + wall "
        "violation + path validity). Component design described "
        "across secondary sources.",
    ),

    # ---------------------------------------------------------------------
    # Headline empirical results table (lower priors due to
    # reconstruction uncertainty on numerical claims)
    # ---------------------------------------------------------------------
    claim_results_table: (
        0.75,
        "Headline results table -- DeepSeek 89.2 / 66.9 / 56.7% "
        "vs frontier on Pixmo-Count / Maze / Path Tracing. The "
        "numerical values depend on the original repo's reported "
        "numbers; without the original repo (withdrawn) we cannot "
        "independently verify. CSDN / 36Kr coverage gives the same "
        "numbers but the chain of provenance is single-rooted at "
        "the deleted repo. Conservative prior reflects this.",
    ),

    # ---------------------------------------------------------------------
    # Limitation observations
    # ---------------------------------------------------------------------
    claim_lim_trigger_word_dependency: (
        0.75,
        "Trigger-word dependency observation. The source flags this "
        "limitation itself; secondary sources describe the "
        "phenomenon but do not separately report the empirical "
        "evidence (qualitative ablations, prompt-perturbation "
        "studies). Modest discount for reconstruction uncertainty.",
    ),
    claim_lim_topology_weakness: (
        0.75,
        "Topology generalization weakness observation. The source "
        "flags this limitation itself; secondary sources describe "
        "the phenomenon but the supporting OOD experiments are not "
        "separately reported.",
    ),

    # ---------------------------------------------------------------------
    # Foils (these are claims the source argues against; their priors
    # set the *foil's* a priori plausibility, not the source's).
    # ---------------------------------------------------------------------
    claim_perception_gap_is_actual_bottleneck: (
        0.35,
        "Foil: 'Perception Gap is the bottleneck' -- the prevailing "
        "frontier-multimodal assumption. We give it a moderate-low "
        "prior (foil treated as plausible-but-disputed before "
        "evidence; the contradiction with the Reference-Gap "
        "diagnosis will further suppress it via BP).",
    ),
    claim_more_tokens_is_better: (
        0.35,
        "Foil: 'more visual tokens reliably improves visual "
        "reasoning'. Widely-held practitioner default; the "
        "contradiction with the 81-KV-entry outperformance will "
        "suppress it via BP. Note: even before the contradiction "
        "fires, the directional claim is already empirically "
        "fragile (token count plateaus exist on many benchmarks).",
    ),
    claim_alt_trivial_confounds: (
        0.25,
        "Abduction alternative: 'bigger MoE / more data / better "
        "base' explains the outperformance pattern. Calibrated "
        "specifically as pi(Alt) = 'can Alt alone explain Obs?' -- "
        "NOT as 'is Alt's calculation correct?'. The observation "
        "(panel-best at ~81 KV entries on Maze/Path) is "
        "directionally incompatible with what 'bigger MoE / more "
        "tokens' would predict, so Alt's explanatory power for the "
        "specific observation pattern is low. (Frontier models "
        "have comparable MoE scale and far more visual tokens; "
        "they nonetheless score near random on Maze/Path.)",
    ),
}
