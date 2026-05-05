"""Section 6 (Conclusion and Limitations) and Section 4.2 (Training Dynamics).

This module captures (a) the synthesis claims that the published mixed-policy
gains trace back to deflated baselines, (b) the training-dynamics observations
that distinguish SFT-then-RL from mixed-policy methods, (c) the implications
for empirical ML practice (cross-framework validation), and (d) the
authors' own limitations.

Source: [@Limozin2026SFTthenRL, Sec. 4.2; Sec. 6].
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# Training-dynamics observations (Section 4.2)
# ---------------------------------------------------------------------------

claim_qwen_training_dynamics = claim(
    "**Training-reward dynamics on Qwen2.5-Math-7B.** The RL phase of "
    "SFT-then-RL starts above 80% training reward (preceding SFT has "
    "internalized expert knowledge) and continues to improve. LUFFY "
    "[@LUFFY] and ReLIFT [@ReLIFT] never reach the reward level that "
    "SFT-then-RL *begins* with, suggesting that interleaving off- and "
    "on-policy signals within a single stage is less efficient than "
    "performing them sequentially -- or even than performing SFT alone "
    "[@Limozin2026SFTthenRL, Sec. 4.2; Fig. 3 top].",
    title="Dynamics: SFT-then-RL starts above LUFFY/ReLIFT's final reward on Qwen",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Fig. 3 (top row)",
        "caption": "Fig. 3 top: Qwen2.5-Math-7B training dynamics; SFT-then-RL begins above mixed-policy plateaus.",
    },
)

claim_response_length_dynamics = claim(
    "**Response-length dynamics.** The RL phase of SFT-then-RL on Qwen "
    "starts at approximately 5k tokens (verbose style inherited from "
    "DeepSeek-R1 [@DeepSeekR1] demonstrations) and *gradually converges* "
    "toward 3.7k tokens as RL prunes unnecessary verbosity while "
    "retaining problem-solving capability. Mixed-policy methods instead "
    "show *gradually increasing* lengths (which Ma et al. [@ReLIFT] "
    "interpret as developing more thorough reasoning, an "
    "interpretation the paper questions). On Llama-3.1-8B, mixed-policy "
    "response lengths quickly diverge toward the context limit "
    "[@Limozin2026SFTthenRL, Sec. 4.2; Fig. 3].",
    title="Dynamics: SFT-then-RL response length converges down (3.7k); mixed-policy diverges up",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Fig. 3 (middle column)",
        "caption": "Fig. 3 middle: response length over RL steps.",
    },
)

claim_entropy_dynamics = claim(
    "**Policy-entropy dynamics.** Yan et al. [@LUFFY] and Ma et al. "
    "[@ReLIFT] emphasize that their approaches maintain higher entropy "
    "than pure RL, attributing this to *sustained exploration*. In "
    "SFT-then-RL the entropy remains relatively constant for both "
    "models, consistent with RL refining an already-strong policy "
    "rather than exploring from scratch. The paper takes this as "
    "*alternative evidence* that SFT-then-RL is in a refining regime, "
    "not as a deficiency [@Limozin2026SFTthenRL, Sec. 4.2; Fig. 3 "
    "right column].",
    title="Dynamics: SFT-then-RL entropy stays constant (refining); mixed-policy is exploring",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Fig. 3 (right column)",
        "caption": "Fig. 3 right: policy entropy.",
    },
)

# ---------------------------------------------------------------------------
# Synthesis: published gains = deflated baselines (the central claim)
# ---------------------------------------------------------------------------

claim_synthesis_baselines_deflated = claim(
    "**Synthesis: the reported gains of mixed-policy optimization for "
    "LLM reasoning trace back to deflated baselines rather than "
    "methodological innovation.** The CPU-offloaded optimizer bug in "
    "DeepSpeed [@DeepSpeed] silently drops intermediate micro-batches "
    "during gradient accumulation (affecting TRL [@TRL], OpenRLHF "
    "[@OpenRLHF], and Llama-Factory [@LlamaFactory]); fixing it alone "
    "recovers most of the gap. A second loss aggregation bug in "
    "OpenRLHF [@OpenRLHF] incorrectly weights per-mini-batch losses "
    "and contributes a further measurable degradation on top of "
    "training instability. Together, the two fixes close the gap to "
    "the independently implemented verl [@verl] baseline. Once "
    "corrected, the SFT-then-RL pipeline exceeds all five evaluated "
    "mixed-policy methods on in-distribution math benchmarks and "
    "achieves comparable or superior OOD performance "
    "[@Limozin2026SFTthenRL, Sec. 6].",
    title="Synthesis: published mixed-policy gains = deflated baselines (not methodological advances)",
)

# ---------------------------------------------------------------------------
# Implications
# ---------------------------------------------------------------------------

claim_implication_cross_framework = claim(
    "**Implication 1: framework-level diversity is essential for "
    "robustness.** Silent bugs in widely used SFT pipelines were "
    "sufficient to deflate baselines across multiple independent "
    "papers. Empirical ML results should be cross-validated across "
    "independently implemented frameworks (DeepSpeed [@DeepSpeed], "
    "verl [@verl], FSDP [@FSDP], etc.) to guard against systematic "
    "baseline deflation [@Limozin2026SFTthenRL, Sec. 6].",
    title="Implication: cross-framework validation is essential to detect silent baseline deflation",
)

claim_implication_other_areas = claim(
    "**Implication 2: because the bugs affect general-purpose SFT "
    "pipelines (not mixed-policy code specifically), they could "
    "potentially invalidate empirical claims in *other* research areas "
    "that rely on the same affected frameworks** (TRL [@TRL], OpenRLHF "
    "[@OpenRLHF], Llama-Factory [@LlamaFactory]). Any 2024-2026 "
    "experiment that used DeepSpeed CPU-offloaded optimizers or "
    "OpenRLHF/Llama-Factory loss aggregation for SFT is potentially "
    "affected -- not just mixed-policy LLM-reasoning [@Limozin2026SFTthenRL, "
    "Sec. 6].",
    title="Implication: bug effects extend beyond mixed-policy LLM reasoning to other ML areas",
)

claim_restored_confidence = claim(
    "**Implication 3: the findings restore confidence in the SFT-then-"
    "RL paradigm.** A correctly trained SFT-then-RL baseline matches "
    "or exceeds every published mixed-policy method on math reasoning "
    "benchmarks for both Qwen2.5-Math-7B [@Qwen25Math] and "
    "Llama-3.1-8B [@Llama3]. The standard two-stage pipeline is *not* "
    "obsolete -- the recent reports of mixed-policy superiority were "
    "artifacts. SFT-then-RL remains the strongest published method for "
    "LLM reasoning post-training [@Limozin2026SFTthenRL, Sec. 6].",
    title="Implication: SFT-then-RL is restored as the strongest published post-training paradigm",
)

# ---------------------------------------------------------------------------
# Limitations (authors' own)
# ---------------------------------------------------------------------------

claim_lim_domain_scope = claim(
    "**Limitation 1: domain scope.** The study focuses on mathematical "
    "reasoning with Qwen2.5-Math-7B [@Qwen25Math] and Llama-3.1-8B "
    "[@Llama3]; the authors do not train on other domains (code, "
    "general reasoning) or larger model scales, where SFT quality may "
    "matter differently [@Limozin2026SFTthenRL, Sec. 6].",
    title="Limitation: math-only domain; other tasks (code, general reasoning) and scales untested",
)

claim_lim_model_families = claim(
    "**Limitation 2: only two model families considered.** The mixed-"
    "policy papers themselves do not consider other model families, "
    "so the comparison is constrained to Qwen2.5-Math-7B and "
    "Llama-3.1-8B. Whether the conclusions extend to different model "
    "families remains untested [@Limozin2026SFTthenRL, Sec. 6].",
    title="Limitation: only Qwen2.5-Math-7B + Llama-3.1-8B (mirrors mixed-policy literature)",
)

claim_lim_mixed_atop_corrected = claim(
    "**Limitation 3: nuance in the comparison.** Mixed-policy methods "
    "position themselves as *single-stage alternatives* to SFT-then-RL, "
    "and that framing is their core contribution. Applying mixed-policy "
    "training atop a correctly trained SFT checkpoint *might* yield "
    "further gains, but none of these works report such a setup "
    "(it would counter their thesis). The paper's results therefore "
    "invalidate the published comparisons without precluding that a "
    "mixed-policy stage could add value on top of a proper SFT "
    "baseline [@Limozin2026SFTthenRL, Sec. 6].",
    title="Limitation: mixed-policy atop a correctly trained SFT checkpoint is untested",
)

claim_lim_relift_hpt_unverified = claim(
    "**Limitation 4: SFT setup not fully verifiable for ReLIFT and "
    "HPT.** ReLIFT [@ReLIFT] uses Llama-Factory [@LlamaFactory] but "
    "has not released its exact configuration, and HPT [@HPT] does "
    "not detail its SFT hyperparameters. The bug-attribution "
    "assessment for these two methods assumes both inherit the same "
    "affected pipelines, which is consistent with their stated "
    "framework choices but not directly verifiable "
    "[@Limozin2026SFTthenRL, Sec. 6].",
    title="Limitation: ReLIFT/HPT SFT configs unverified (bug attribution is inference, not measurement)",
)

# ---------------------------------------------------------------------------
# The "alternative explanation" claim used by the central abduction
# ---------------------------------------------------------------------------

claim_alt_methodological_advance = claim(
    "**Alternative hypothesis: mixed-policy methods do represent a "
    "genuine methodological advance, and the SFT-then-RL pipeline's "
    "apparent superiority is an artifact of this paper's specific "
    "implementation choices (verl [@verl] hyperparameters, Math-Verify "
    "evaluator, chat template).** Under this alternative, the gap "
    "would be expected to disappear under different evaluation "
    "protocols. This alternative is internally coherent (mixed-policy "
    "methods do address a real signal-sparsity problem at the "
    "conceptual level) but its predictive power is weak: the "
    "independently implemented verl baseline matches the patched "
    "OpenRLHF result to within the seed variance (53.8 vs 54.0 in "
    "Table 2) -- this is a *cross-framework* match, not a single-"
    "implementation result. Furthermore the bug mechanisms are "
    "verifiable from source code and produce predicted training-"
    "dynamics signatures (suppressed grad norm, shifted loss mean), "
    "so the bug attribution does not depend on a specific evaluation "
    "protocol [@Limozin2026SFTthenRL, Sec. 4; Fig. 2].",
    title="Alt: mixed-policy gains are real, paper's superior numbers are implementation-specific",
)

# ---------------------------------------------------------------------------
# Ground truth that discriminates: cross-framework match
# ---------------------------------------------------------------------------

claim_obs_cross_framework_match = claim(
    "**Discriminating observation: the patched OpenRLHF (54.0 +/- 0.2) "
    "matches the independently implemented verl baseline (53.8 +/- 0.1) "
    "on the Table 2 evaluation subset.** Two independent training "
    "stacks -- patched DeepSpeed + OpenRLHF (with both bugs fixed) "
    "and verl + FSDP (which never had the bugs) -- arrive at "
    "statistically equivalent SFT scores. Under the bug-attribution "
    "hypothesis this is the *expected* outcome (both stacks now "
    "implement the gradient-accumulation contract correctly). Under "
    "the methodological-advance alternative this match is awkward: "
    "the alternative would have to attribute the convergence to "
    "shared evaluation noise, but the standard deviations are tight "
    "(0.1-0.2) and the per-benchmark scores agree row-by-row "
    "[@Limozin2026SFTthenRL, Table 2].",
    title="Observation: patched OpenRLHF (54.0) matches verl (53.8) -- cross-framework convergence",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Table 2 (last two rows)",
        "caption": "Table 2: + fix both = 54.0 +/- 0.2; verl = 53.8 +/- 0.1.",
    },
)

# ---------------------------------------------------------------------------
# Predictions of each side
# ---------------------------------------------------------------------------

claim_pred_bug_explains = claim(
    "**Prediction (bug-attribution hypothesis):** if the mixed-policy "
    "gains are caused by the two SFT framework bugs, then (a) two "
    "independent training stacks both lacking the bugs (patched "
    "OpenRLHF + verl) should converge to statistically equivalent "
    "scores; (b) per-bug fixes should produce the predicted "
    "training-dynamics signatures (loss-aggregation -> variability; "
    "optimizer -> mean shift + suppressed grad norm); (c) the bug "
    "fixes should shift the SFT score from 48.3 toward 53.8 by the "
    "Table 2 attribution.",
    title="Prediction (H): cross-framework match + per-bug dynamics signatures + Table 2 waterfall",
)

claim_pred_alt_explains = claim(
    "**Prediction (alternative methodological-advance hypothesis):** if "
    "mixed-policy methods represent a genuine methodological advance, "
    "then a properly tuned SFT-then-RL pipeline should *not* exceed "
    "mixed-policy methods in any framework, and any apparent "
    "superiority should depend on implementation-specific choices "
    "(verl-specific hyperparameters, Math-Verify quirks, chat-"
    "template selection). Cross-framework match between two corrected "
    "stacks would be unexpected under this alternative.",
    title="Prediction (Alt): SFT-then-RL should not exceed mixed-policy regardless of implementation",
)

__all__ = [
    "claim_qwen_training_dynamics",
    "claim_response_length_dynamics",
    "claim_entropy_dynamics",
    "claim_synthesis_baselines_deflated",
    "claim_implication_cross_framework",
    "claim_implication_other_areas",
    "claim_restored_confidence",
    "claim_lim_domain_scope",
    "claim_lim_model_families",
    "claim_lim_mixed_atop_corrected",
    "claim_lim_relift_hpt_unverified",
    "claim_alt_methodological_advance",
    "claim_obs_cross_framework_match",
    "claim_pred_bug_explains",
    "claim_pred_alt_explains",
]
