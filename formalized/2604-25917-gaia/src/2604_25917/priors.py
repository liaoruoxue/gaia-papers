"""Priors for independent (leaf) claims in the 2604.25917 RecursiveMAS
formalization.

Calibration philosophy
----------------------

* **Numerical readouts from the paper's own tables and figures**
  (Table 2 per-task accuracy / runtime / tokens, Tables 3-9, Figures
  5-6 efficiency tables) -- 0.92-0.95. Each is a directly measured
  benchmark or training-cost value with the per-task / per-method
  breakdown reproduced exactly from the source.
* **Method-description claims for related-work / baseline
  characterizations** (recursive LM family, latent-space
  communication, MAS topology / textual feedback / per-agent
  training literatures) -- 0.88-0.92. Author-stated
  characterizations of competing methods drawn from those papers
  directly.
* **Setup-fact priors** (d_h << |V| in modern LLMs) -- 0.95.
  Universal practical fact about modern Transformer hyperparameters.
* **Abduction-component prediction claims** (latent vs trivial
  alternatives) -- moderate, with H ~ 0.55 and Alt ~ 0.2. The
  alternative's pi(Alt) is the probability that the trivial
  alternative *alone* explains the 5-fact fingerprint, NOT whether
  trivial alternatives have correct intrinsic accounts of any single
  fact in isolation. Since trivial alternatives predict the OPPOSITE
  signs for fact (ii) speedup and fact (iii) token reduction, pi(Alt)
  is held substantially below pi(H).
* **Setup-anchored secondary observations** (Fig. 1 scaling-law
  qualitative observation) -- 0.9. Direct claim from the figure.
"""

from .motivation import (
    claim_text_channel_bandwidth_assumption,
)
from .s2_preliminary import (
    claim_dh_ll_v_in_practice,
)
from .s5_main_results import (
    claim_table2_full,
    claim_table3,
    claim_table6_distillation,
    claim_table7_mixture,
    claim_table8_deliberation,
    claim_scaling_law_observation,
)
from .s6_efficiency import (
    claim_speedup_table,
    claim_token_reduction_table,
)
from .s7_in_depth import (
    claim_table4_link_designs,
    claim_table5_training_cost,
    claim_table9_latent_length,
)
from .s8_related_work import (
    claim_mas_topology_literature,
    claim_textual_feedback_optimization_literature,
    claim_per_agent_training_literature,
    claim_recursive_lm_literature,
    claim_latent_space_communication_literature,
)
from .s10_wiring import (
    claim_pred_latent_explains,
    claim_pred_alt_explains,
)


PRIORS: dict = {
    # -----------------------------------------------------------------
    # Setup-fact prior: d_h << |V| in modern LLMs
    # -----------------------------------------------------------------
    claim_dh_ll_v_in_practice: (
        0.97,
        "Universal practical fact about modern Transformer LLMs: "
        "hidden dim d_h is in the 10^3-10^4 range while vocabulary "
        "size |V| is in the 10^4-10^5 range. Verifiable across all "
        "open-weight model cards (Qwen, Llama, Gemma, Mistral, "
        "DeepSeek). The high prior reflects that this is a "
        "universally observable hyperparameter pattern, not a "
        "research claim.",
    ),

    # -----------------------------------------------------------------
    # Tables 2-9: per-task / per-method numerical readouts
    # -----------------------------------------------------------------
    claim_table2_full: (
        0.93,
        "Table 2: per-task per-method accuracy / runtime / token "
        "values across r=1, 2, 3 for both Light and Scaled "
        "RecursiveMAS vs Recursive-TextMAS. The paper reports a "
        "5-run mean with std +/- 0.0041 for accuracy, +/- 26 for "
        "runtime, +/- 33 for tokens. Direct measurement; the prior "
        "is high but not 0.95 because of the multi-cell breadth "
        "(more cells = more chances for transcription error).",
    ),
    claim_table3: (
        0.93,
        "Table 3: RecursiveMAS at r=3 vs broader baselines (Single-"
        "LoRA, Single-Full-SFT, MoA, TextGrad, LoopLM, Recursive-"
        "TextMAS) on 6 benchmarks. All baselines are run under "
        "identical backbones and matched training budgets per "
        "Section 5.2 narrative. Direct measurement.",
    ),
    claim_table4_link_designs: (
        0.93,
        "Table 4: 4-design ablation (1-Layer / Res+1L / 2-Layer / "
        "Res+2L) on 3 benchmarks (MATH500, GPQA-D, LiveCodeBench). "
        "Section 6 ablation under scaled Sequential-Style "
        "RecursiveMAS at r=3.",
    ),
    claim_table5_training_cost: (
        0.93,
        "Table 5: 3-method training-cost analysis (LoRA / Full-SFT "
        "/ RecursiveMAS) under scaled Sequential-Style. Reports "
        "GPU memory, trainable params, USD cost, avg accuracy. "
        "Cost estimation follows the convention of [@Liu2025; "
        "@Lu2023].",
    ),
    claim_table6_distillation: (
        0.93,
        "Table 6: Distillation-Style RecursiveMAS vs Expert / "
        "Learner standalone, accuracy + runtime per task. 5 "
        "benchmarks (AIME2026, GPQA-D, LiveCodeBench, MBPP+, "
        "MedQA).",
    ),
    claim_table7_mixture: (
        0.93,
        "Table 7: Mixture-Style RecursiveMAS vs each domain "
        "specialist (Math / Code / Science) on 4 benchmarks. "
        "Direct measurement.",
    ),
    claim_table8_deliberation: (
        0.93,
        "Table 8: Deliberation-Style RecursiveMAS vs Reflector / "
        "Tool-Caller solo on 4 benchmarks (AIME2026, GPQA-D, "
        "HotpotQA, Bamboogle). Direct measurement.",
    ),
    claim_table9_latent_length: (
        0.93,
        "Table 9: latent-thoughts length sweep m in {0, 16, 32, "
        "..., 128} across 3 benchmarks. The full sweep is "
        "tabulated; saturation at m ~ 80 is read off the table.",
    ),

    # -----------------------------------------------------------------
    # Figs. 5-6 efficiency tables (averages over Table 2 cells)
    # -----------------------------------------------------------------
    claim_speedup_table: (
        0.93,
        "Fig. 5 averages: 1.2x / 1.9x / 2.4x speedup at r=1/2/3. "
        "Cross-task average over the 12 paired (RecursiveMAS, "
        "TextMAS) Time cells per round (6 tasks x Light + Scaled).",
    ),
    claim_token_reduction_table: (
        0.93,
        "Fig. 6 averages: 34.6% / 65.5% / 75.6% token reduction at "
        "r=1/2/3. Cross-task average over the 12 paired Token "
        "cells per round.",
    ),

    # -----------------------------------------------------------------
    # Setup-anchored qualitative observation
    # -----------------------------------------------------------------
    claim_scaling_law_observation: (
        0.9,
        "Fig. 1 (Top): qualitative description of the performance "
        "landscape over training-recursion x inference-recursion "
        "depths. Section 5.1 narrative confirms 'strongest results "
        "consistently appearing in the upper-right region'. Direct "
        "qualitative reading of the heatmap; modest discount "
        "because the exact landscape numbers are presented "
        "graphically rather than tabulated.",
    ),

    # -----------------------------------------------------------------
    # Related-work category descriptions
    # -----------------------------------------------------------------
    claim_mas_topology_literature: (
        0.92,
        "Standard MAS topologies (sequential, mixture-of-agents) "
        "are extensively documented across the surveys "
        "[@MASsurvey; @AutoGen] and primary works [@CAMEL; "
        "@ChatDev; @MoA; @GraphOfAgents]. Consensus-level "
        "characterization.",
    ),
    claim_textual_feedback_optimization_literature: (
        0.91,
        "Textual-feedback MAS optimization (TextGrad, prompt-"
        "based context refinement) is documented in [@TextGrad] "
        "and follow-on works. The 'optimize the inter-agent text "
        "channel' framing is the literal stated objective of "
        "those methods.",
    ),
    claim_per_agent_training_literature: (
        0.9,
        "Per-agent MAS training (MALT [@MALT], Sirius [@Sirius], "
        "multi-agent fine-tuning [@MultiAgentFinetune]) is "
        "documented in those papers. The 'each agent trained "
        "separately' characterization is their literal stated "
        "approach.",
    ),
    claim_recursive_lm_literature: (
        0.93,
        "Recursive (looped) LM literature (LoopLM [@LoopLM], "
        "TinyRecursive [@TinyRecursive], MoR [@MoR], Geiping et "
        "al. [@Geiping2025], HRM [@HRM], LoopRPT [@LoopRPT], "
        "Zhang et al. [@RecursiveLM2025]) is documented in those "
        "papers. The 'recursion within a single LM' "
        "characterization is the literal scope of every cited "
        "work.",
    ),
    claim_latent_space_communication_literature: (
        0.9,
        "Latent-space LLM communication literature (DuLatentComm "
        "[@DuLatentComm], C2C [@C2C], KVcomm [@KVcomm], "
        "ThoughtComm [@ThoughtComm], ZouLatentMAS "
        "[@ZouLatentMAS]) is documented in those papers. The "
        "'one-shot or pairwise' characterization fits the "
        "designs reported there; RecursiveMAS distinguishes "
        "itself by recursive system-level use.",
    ),

    # -----------------------------------------------------------------
    # Motivation-section text-channel-bandwidth assumption
    # -----------------------------------------------------------------
    claim_text_channel_bandwidth_assumption: (
        0.7,
        "The 'text channel is the bandwidth bottleneck' "
        "assumption is implicit in standard MAS practice and "
        "TextGrad-style optimizers, but it is the foil that "
        "RecursiveMAS argues against. We hold the prior at 0.7 "
        "to reflect that the assumption is widely held in "
        "practice but disputable; it sits in a contradiction "
        "with the RecursiveMAS empirical findings, so BP will "
        "pull it down based on those findings.",
    ),

    # -----------------------------------------------------------------
    # Abduction component prediction claims
    # -----------------------------------------------------------------
    claim_pred_latent_explains: (
        0.55,
        "Hypothesis prediction: the latent-space recursion "
        "mechanism predicts the 5-fact fingerprint (accuracy + "
        "speedup + token reduction + cross-pattern + cost "
        "dominance). The prediction is precise and follows from "
        "Proposition 3.1 + Theorem 4.1; we hold the prior "
        "moderate (0.55) because the prediction itself is a "
        "claim about which mechanisms produce which "
        "fingerprints, not the underlying theorems.",
    ),
    claim_pred_alt_explains: (
        0.2,
        "Alternative prediction: trivial confounds (more "
        "compute / longer chains / better models) predict at "
        "most a uniform accuracy lift. CRUCIALLY, this is "
        "pi(Alt) = 'can the trivial alternative alone explain "
        "the OBSERVED 5-fact pattern?' -- not 'can it explain "
        "any single isolated fact?'. Since trivial alternatives "
        "predict the OPPOSITE sign for facts (ii) speedup and "
        "(iii) token reduction (more compute = slower; longer "
        "chains = more tokens), they cannot jointly explain the "
        "observed positive signs. pi(Alt) is held low (0.2) "
        "because the alternative's explanatory power for the "
        "FULL fingerprint is poor, regardless of how correctly "
        "any individual confound description is.",
    ),
}


__all__ = ["PRIORS"]
