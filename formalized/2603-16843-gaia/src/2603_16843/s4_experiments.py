"""Section 4: Experiments — main results, ablations, OOD generalization."""

from gaia.lang import claim, setting, support, induction, abduction, compare

from .motivation import (
    setup_passk,
    setup_rlvr,
    claim_distribution_sharpening,
    claim_agency_internalization,
    claim_test_time_cost,
)
from .s3_method import (
    claim_branching_targets_failures,
    claim_cf_internalizes_recovery,
    claim_lreh_stabilizes,
    claim_initialization_grpo,
    setup_cf_loss,
    setup_rehearsal_loss,
)

# ── Settings: experiment protocol ────────────────────────────────────────────

setup_eval_protocol = setting(
    "**Evaluation protocol.** LEAFE is compared against four baselines: Base "
    "(instruction-tuned model, no task fine-tuning), GRPO-RLVR (outcome-supervised "
    "RL with verifiable final rewards [@DeepSeekR1]), EarlyExp (reward-free "
    "agent learning that converts early interaction experience into supervision "
    "via Implicit World Modeling [@Zhang2025a]), and ACE (training-free "
    "prompt-based playbook evolution [@Zhang2025b]). Pass@1 and Pass@128 are "
    "reported on WebShop, ALFWorld, ScienceWorld, Sokoban (Qwen2.5-7B and "
    "Llama3.1-8B backbones); CodeContests (Qwen2.5-72B and Llama3-70B) reports "
    "Pass@1 and Pass@128 only against Base and GRPO. All Pass@128 numbers are "
    "computed from independent inference-time samples of the trained policy "
    "(no Stage-1 rollback at test time).",
    title="Evaluation protocol and baselines"
)

setup_benchmarks = setting(
    "**Benchmarks.** WebShop [@Yao2022a] (web navigation across >1M products), "
    "ALFWorld [@Shridhar2020] (text-based embodied household tasks), "
    "ScienceWorld [@Wang2022a] (text-based scientific experimentation), "
    "Sokoban [@Schrader2018] (planning puzzle), and CodeContests [@Li2022] "
    "(competitive programming with execution-based test feedback).",
    title="Agentic benchmarks"
)

# ── Observations: Tables 1 & 2 (Main Results) ────────────────────────────────

obs_main_results = claim(
    "Main Pass@1 / Pass@128 results across four interactive benchmarks "
    "(% success rate). LEAFE attains the highest Pass@128 in every benchmark / "
    "model cell shown:\n\n"
    "**WebShop**\n\n"
    "| Method     | Qwen2.5-7B P@1 | Qwen2.5-7B P@128 | Llama3.1-8B P@1 | Llama3.1-8B P@128 |\n"
    "|------------|----------------|------------------|-----------------|-------------------|\n"
    "| Base       | 0.05           | 5.20             | 0.00            | 1.80              |\n"
    "| EarlyExp   | 61.55          | 84.60            | 51.13           | 77.80             |\n"
    "| GRPO-RLVR  | 67.45          | 85.40            | 54.95           | 79.40             |\n"
    "| ACE        | 68.65          | 86.80            | 54.35           | 79.80             |\n"
    "| **LEAFE**  | 66.50          | **87.80**        | **56.25**       | **81.00**         |\n\n"
    "**ALFWorld**\n\n"
    "| Method     | Qwen2.5-7B P@1 | Qwen2.5-7B P@128 | Llama3.1-8B P@1 | Llama3.1-8B P@128 |\n"
    "|------------|----------------|------------------|-----------------|-------------------|\n"
    "| Base       | 26.07          | 78.57            | 29.82           | 74.29             |\n"
    "| EarlyExp   | 72.23          | 92.86            | 74.15           | 95.71             |\n"
    "| GRPO-RLVR  | 69.46          | 91.43            | 72.50           | 94.29             |\n"
    "| ACE        | 66.34          | 89.63            | 70.32           | 92.50             |\n"
    "| **LEAFE**  | 67.50          | **94.29**        | 71.79           | **96.43**         |\n\n"
    "**ScienceWorld**\n\n"
    "| Method     | Qwen2.5-7B P@1 | Qwen2.5-7B P@128 | Llama3.1-8B P@1 | Llama3.1-8B P@128 |\n"
    "|------------|----------------|------------------|-----------------|-------------------|\n"
    "| Base       | 7.00           | 47.33            | 7.17            | 48.67             |\n"
    "| EarlyExp   | 26.17          | 54.67            | 24.04           | 56.00             |\n"
    "| GRPO-RLVR  | 27.17          | 57.33            | 24.25           | 56.00             |\n"
    "| ACE        | 29.45          | 59.67            | 25.28           | 57.33             |\n"
    "| **LEAFE**  | 27.88          | **62.00**        | 22.70           | **59.33**         |\n\n"
    "**Sokoban**\n\n"
    "| Method     | Qwen2.5-7B P@1 | Qwen2.5-7B P@128 | Llama3.1-8B P@1 | Llama3.1-8B P@128 |\n"
    "|------------|----------------|------------------|-----------------|-------------------|\n"
    "| Base       | 6.90           | 43.80            | 17.70           | 61.40             |\n"
    "| EarlyExp   | 60.15          | 71.60            | 57.32           | 68.20             |\n"
    "| GRPO-RLVR  | 58.15          | 68.00            | 60.43           | 73.40             |\n"
    "| ACE        | 61.30          | 70.80            | 60.79           | 73.20             |\n"
    "| **LEAFE**  | **64.60**      | **78.40**        | **62.00**       | **77.20**         |",
    title="Main Pass@1 / Pass@128 results across four interactive benchmarks",
    metadata={"source_table": "artifacts/2603.16843.pdf, Table 1"}
)

obs_codecontests_results = claim(
    "Pass@1 / Pass@128 on CodeContests with larger backbones (% success rate). "
    "LEAFE improves Pass@128 by up to **+14%** over the base model:\n\n"
    "| Method     | Qwen2.5-72B P@1 | Qwen2.5-72B P@128 | Llama3-70B P@1 | Llama3-70B P@128 |\n"
    "|------------|------------------|---------------------|----------------|---------------------|\n"
    "| Base       | 10.00            | 33.94               | 7.35           | 24.85               |\n"
    "| GRPO-RLVR  | 20.45            | 36.97               | 13.64          | 27.88               |\n"
    "| **LEAFE**  | 17.12            | **47.88**           | 14.09          | **33.94**           |\n\n"
    "Note: EarlyExp and ACE are not reported on CodeContests because the "
    "benchmark uses execution feedback rather than the interactive-environment "
    "interface those methods target.",
    title="CodeContests Pass@1 / Pass@128 (large backbones)",
    metadata={"source_table": "artifacts/2603.16843.pdf, Table 2"}
)

obs_grpo_passk_pattern = claim(
    "Across the eight (benchmark, backbone) cells in Table 1 plus the two "
    "CodeContests cells, GRPO sometimes wins Pass@1 (e.g. WebShop / Qwen2.5-7B: "
    "GRPO 67.45 vs. LEAFE 66.50; CodeContests / Qwen2.5-72B: GRPO 20.45 vs. "
    "LEAFE 17.12) but LEAFE wins or ties **every** Pass@128 comparison. Most "
    "strikingly, on CodeContests / Qwen2.5-72B GRPO improves Pass@128 by only "
    "+3 points over Base (33.94 → 36.97) while LEAFE improves by +14 points "
    "(33.94 → 47.88).",
    title="GRPO sometimes wins P@1 but LEAFE consistently wins P@128",
    metadata={"source_table": "artifacts/2603.16843.pdf, Tables 1 and 2"}
)

# ── Observations: Table 3 (Stage 1 sampling strategies) ──────────────────────

obs_stage1_sampling = claim(
    "On CodeContests, holding the execution budget fixed, LEAFE Stage-1 "
    "tree-based experience-guided rollback branching attains higher Pass@128 "
    "than either independent sampling (IS) or iterative refinement (IR):\n\n"
    "| Model         | IS Pass@128 | IR Pass@128 | LEAFE Stage-1 Pass@128 |\n"
    "|---------------|-------------|-------------|------------------------|\n"
    "| Qwen2.5-32B   | 48.92       | 51.48       | **55.52**              |\n"
    "| Qwen2.5-72B   | 48.65       | 49.52       | **54.30**              |\n"
    "| Llama3-70B    | 30.20       | 38.10       | **42.50**              |",
    title="Stage-1 branching beats IS and IR under equal budget",
    metadata={"source_table": "artifacts/2603.16843.pdf, Table 3"}
)

# ── Observations: Table 4 (Lcf vs Lreh ablation) ─────────────────────────────

obs_lcf_ablation = claim(
    "On ScienceWorld, adding the counterfactual loss $\\mathcal{L}_{\\mathrm{cf}}$ "
    "on top of the rehearsal loss $\\mathcal{L}_{\\mathrm{reh}}$ raises Pass@128 "
    "substantially while leaving Pass@1 nearly unchanged:\n\n"
    "| Model         | Lreh P@1 | Lcf+Lreh P@1 | Lreh P@128 | Lcf+Lreh P@128 |\n"
    "|---------------|----------|---------------|------------|------------------|\n"
    "| Qwen2.5-7B    | 27.67    | 27.88         | 59.33      | **62.00**        |\n"
    "| Llama3.1-8B   | 22.54    | 22.70         | 57.33      | **59.33**        |\n"
    "| Qwen2.5-14B   | 37.17    | 36.50         | 67.33      | **72.00**        |\n\n"
    "The Pass@128 gain (e.g. +4.67 points on Qwen2.5-14B) isolates the "
    "contribution of experience-to-policy distillation from the rehearsal "
    "regularizer.",
    title="Lcf is the key driver of Pass@128 gains (ablation)",
    metadata={"source_table": "artifacts/2603.16843.pdf, Table 4"}
)

# ── Observations: Table 5 (OOD generalization) ───────────────────────────────

obs_ood_mbpp = claim(
    "Out-of-distribution generalization on MBPP (models trained on "
    "CodeContests). Values are Pass@128 (%); deltas vs. the corresponding base "
    "model in parentheses:\n\n"
    "| Method | Qwen2.5-32B   | Qwen2.5-72B   | Llama3-70B   |\n"
    "|--------|----------------|----------------|----------------|\n"
    "| Base   | 85.45          | 83.33          | 78.31          |\n"
    "| GRPO   | 81.22 (−4.23)  | 81.22 (−2.11)  | 74.07 (−4.24)  |\n"
    "| LEAFE  | 85.45 (+0.00)  | **85.13 (+1.80)** | **79.63 (+1.32)** |\n\n"
    "GRPO degrades on every backbone; LEAFE matches or beats Base on every "
    "backbone.",
    title="OOD MBPP Pass@128 — GRPO degrades, LEAFE preserves or improves",
    metadata={"source_table": "artifacts/2603.16843.pdf, Table 5"}
)

# ── Observations: Table 6 (synergy / trade-offs) ─────────────────────────────

obs_synergy_ablation = claim(
    "Pass@1 / Pass@128 (%) for LEAFE alone vs. LEAFE plus an auxiliary training "
    "target (EarlyExp = EE for ALFWorld, GRPO-RLVR = RL for CodeContests). "
    "Auxiliary targets consistently raise Pass@1 but can lower Pass@128:\n\n"
    "| Task         | Model         | LEAFE alone (P@1 / P@128) | LEAFE + Aux (P@1 / P@128)         |\n"
    "|--------------|---------------|----------------------------|-------------------------------------|\n"
    "| ALFWorld     | Qwen2.5-7B    | 67.50 / 94.29              | 67.86 / 95.71 (w/ EE)               |\n"
    "| ALFWorld     | Llama3.1-8B   | 71.79 / 96.43              | 74.46 / 93.57 (w/ EE) — P@128 drops |\n"
    "| CodeContests | Qwen2.5-32B   | 9.34 / 34.35               | 14.09 / 33.94 (w/ RL) — P@128 drops |\n"
    "| CodeContests | Qwen2.5-72B   | 11.15 / 40.00              | 17.12 / 47.88 (w/ RL)               |\n"
    "| CodeContests | Llama3-70B    | 9.33 / 30.30               | 14.09 / 33.94 (w/ RL)               |",
    title="Auxiliary RL/EE raise P@1 but can constrain P@128",
    metadata={"source_table": "artifacts/2603.16843.pdf, Table 6"}
)

# ── Derived claims: paper's interpretive conclusions ─────────────────────────

claim_leafe_beats_grpo_passk = claim(
    "**LEAFE consistently outperforms GRPO at large $K$ (Pass@128) across "
    "interactive and code-generation benchmarks.** The advantage is most "
    "pronounced on CodeContests / Qwen2.5-72B (LEAFE 47.88 vs. GRPO 36.97, a "
    "+10.9 point gap) and on Sokoban / Qwen2.5-7B (LEAFE 78.40 vs. GRPO 68.00, "
    "a +10.4 point gap), and holds in every cell of Tables 1 and 2.",
    title="LEAFE > GRPO at Pass@128 (consistently)"
)

claim_leafe_beats_alternatives = claim(
    "**LEAFE attains the highest Pass@128 across all interactive benchmarks "
    "compared to EarlyExp, GRPO-RLVR, and ACE** under the same fixed interaction "
    "budget — ten of ten cells in Table 1 (four benchmarks × Qwen2.5-7B and "
    "Llama3.1-8B, plus the two CodeContests / large-backbone rows).",
    title="LEAFE > EarlyExp / GRPO / ACE at Pass@128"
)

claim_internalization_supported = claim(
    "The combined evidence from main results, the Lcf ablation, and the OOD "
    "generalization experiment supports LEAFE's central thesis that "
    "**reflective-experience distillation internalizes feedback-grounded agency** "
    "into the model weights, rather than merely sharpening the existing "
    "trajectory distribution.",
    title="Internalization thesis is empirically supported"
)

claim_grpo_sharpens_evidence = claim(
    "The pattern of GRPO sometimes winning Pass@1 while plateauing or "
    "regressing at Pass@128 (and on OOD MBPP) is the empirical signature of "
    "distribution sharpening: the policy concentrates probability on the "
    "narrow set of behaviors GRPO already rewards, at the cost of behavioral "
    "coverage and generalization.",
    title="Empirical evidence that GRPO induces distribution sharpening"
)

claim_aux_pass1_pass128_tradeoff = claim(
    "Adding an auxiliary outcome-driven objective (EarlyExp or GRPO-RLVR) on "
    "top of LEAFE consistently lifts Pass@1 but can suppress Pass@128 (e.g. "
    "ALFWorld / Llama3.1-8B 96.43 → 93.57; CodeContests / Qwen2.5-32B 34.35 "
    "→ 33.94). This trade-off is consistent with the auxiliary target re-aligning "
    "the policy with terminal rewards and thereby narrowing the exploration "
    "ceiling that LEAFE alone preserves.",
    title="Auxiliary target → Pass@1 ↑, Pass@128 sometimes ↓"
)

# ── Limitations (as claims) ──────────────────────────────────────────────────

claim_lim_feedback_quality = claim(
    "LEAFE is most effective when the environment provides clear, diagnostic "
    "feedback. Its benefits may diminish when feedback is weak, delayed, or "
    "hard to attribute to specific decision points.",
    title="Limitation: requires diagnostic feedback"
)

claim_lim_resettable_env = claim(
    "LEAFE assumes the environment can be reliably reset to a rollback point "
    "$\\tau$ and that the prefix $a_{1:\\tau-1}$ can be replayed deterministically. "
    "This assumption can be violated in non-deterministic or stateful real-world "
    "environments.",
    title="Limitation: requires resettable / replayable environments"
)

# ── Strategies: empirical generalizations via induction ──────────────────────

# Induction: LEAFE > GRPO at Pass@128 — supported across multiple (benchmark,
# model) cells. The "law" is the LEAFE-beats-GRPO claim and each cell of Tables
# 1 and 2 acts as an independent prediction site.
s_grpo_main = support(
    [claim_leafe_beats_grpo_passk], obs_main_results,
    reason=(
        "If LEAFE consistently beats GRPO at Pass@128 "
        "(@claim_leafe_beats_grpo_passk), the main interactive-benchmark "
        "table (@obs_main_results) should show LEAFE numerically ≥ GRPO in "
        "every Pass@128 cell — which it does (eight of eight cells)."
    ),
    prior=0.9,
    background=[setup_passk, setup_eval_protocol, setup_benchmarks]
)

s_grpo_codecontests = support(
    [claim_leafe_beats_grpo_passk], obs_codecontests_results,
    reason=(
        "On CodeContests with large backbones (@obs_codecontests_results), "
        "the same pattern holds: LEAFE Pass@128 = 47.88 / 33.94 vs. GRPO "
        "36.97 / 27.88 on Qwen2.5-72B and Llama3-70B respectively, the very "
        "regime where the LEAFE > GRPO claim (@claim_leafe_beats_grpo_passk) "
        "is most strongly stated."
    ),
    prior=0.9,
    background=[setup_passk]
)

ind_leafe_beats_grpo = induction(
    s_grpo_main, s_grpo_codecontests,
    law=claim_leafe_beats_grpo_passk,
    reason=(
        "Two independent observation tables (interactive benchmarks vs. "
        "execution-feedback CodeContests) on different model families both "
        "confirm the same Pass@128 ordering; this is the canonical induction "
        "from heterogeneous evidence to a general empirical regularity."
    )
)

# Induction: LEAFE > all four baselines at Pass@128 — same observation table
# (Table 1) supplemented by the auxiliary-augmented rows (Table 6) which keep
# LEAFE on top across additional configurations.
s_alt_main = support(
    [claim_leafe_beats_alternatives], obs_main_results,
    reason=(
        "Table 1 (@obs_main_results) shows LEAFE Pass@128 ≥ every baseline "
        "(EarlyExp, GRPO, ACE) on every cell — direct confirmation of the "
        "general statement (@claim_leafe_beats_alternatives)."
    ),
    prior=0.9,
    background=[setup_eval_protocol]
)

s_alt_synergy = support(
    [claim_leafe_beats_alternatives], obs_synergy_ablation,
    reason=(
        "The synergy table (@obs_synergy_ablation) shows that even when "
        "auxiliary objectives lift Pass@1, LEAFE-derived models remain "
        "competitive at Pass@128, consistent with LEAFE supplying the "
        "exploration-coverage component absent from the baselines."
    ),
    prior=0.7,
    background=[setup_eval_protocol]
)

ind_leafe_beats_alt = induction(
    s_alt_main, s_alt_synergy,
    law=claim_leafe_beats_alternatives,
    reason=(
        "The main table is the headline confirmation; the synergy table "
        "extends the comparison to LEAFE + auxiliary-objective configurations, "
        "providing a second independent observation site for the same general "
        "claim."
    )
)

# Direct support: GRPO sharpening
strat_grpo_sharpens = support(
    [obs_grpo_passk_pattern, obs_ood_mbpp],
    claim_grpo_sharpens_evidence,
    reason=(
        "GRPO's Pass@1-up / Pass@128-flat pattern (@obs_grpo_passk_pattern) "
        "combined with its negative deltas on OOD MBPP (@obs_ood_mbpp, e.g. "
        "−4.24 on Llama3-70B) is the empirical signature of distribution "
        "sharpening: the policy is concentrating mass on rewarded modes at "
        "the cost of exploration coverage and generalization, exactly what "
        "Section 1 predicts (@claim_distribution_sharpening)."
    ),
    prior=0.85,
    background=[setup_passk, setup_rlvr]
)

# Direct support: synergy trade-off
strat_aux_tradeoff = support(
    [obs_synergy_ablation],
    claim_aux_pass1_pass128_tradeoff,
    reason=(
        "Reading off the Synergy & Trade-offs table (@obs_synergy_ablation) "
        "directly: ALFWorld / Llama3.1-8B Pass@128 falls 96.43 → 93.57 with "
        "EE; CodeContests / Qwen2.5-32B falls 34.35 → 33.94 with RL — both "
        "while Pass@1 rises. This is the trade-off the claim asserts."
    ),
    prior=0.92
)

# ── Abduction: does the evidence support 'internalization' (H) over 'just  ─
# another sharpening recipe' (Alt)? ──────────────────────────────────────────

alt_leafe_just_sharpening = claim(
    "An alternative explanation for LEAFE's Pass@128 gains is that it is "
    "simply a more effective form of distribution sharpening — concentrating "
    "mass on a different (perhaps larger) set of pre-existing successful "
    "trajectories rather than internalizing a genuinely new recovery skill.",
    title="Alternative: LEAFE is just a different sharpening recipe"
)

# Predictions of H vs Alt against obs_lcf_ablation (the Lreh-vs-Lcf+Lreh
# ablation): under H, removing Lcf should preferentially hurt Pass@128 (the
# coverage/recovery component) while leaving Pass@1 (rehearsal) intact. Under
# Alt the two losses would be near-substitutes.
pred_internalization = claim(
    "If LEAFE genuinely internalizes recovery (@claim_internalization_supported), "
    "then the counterfactual loss $\\mathcal{L}_{\\mathrm{cf}}$ should "
    "selectively raise Pass@128 (the coverage metric) while leaving Pass@1 "
    "essentially unchanged: the rehearsal loss already captures Pass@1 "
    "competence, and only $\\mathcal{L}_{\\mathrm{cf}}$ supplies the corrective "
    "alternatives that expand coverage.",
    title="Prediction (internalization): Lcf raises P@128 selectively"
)

pred_just_sharpening = claim(
    "If LEAFE were merely an alternative sharpening recipe "
    "(@alt_leafe_just_sharpening), $\\mathcal{L}_{\\mathrm{cf}}$ and "
    "$\\mathcal{L}_{\\mathrm{reh}}$ would be near-substitutes that together "
    "redistribute probability over the same successful-mode set — so removing "
    "$\\mathcal{L}_{\\mathrm{cf}}$ should hurt Pass@1 and Pass@128 in roughly "
    "the same proportion, not produce a selective Pass@128 drop.",
    title="Prediction (sharpening alt): Lcf and Lreh affect P@1 and P@128 similarly"
)

cmp_internalization = compare(
    pred_internalization, pred_just_sharpening, obs_lcf_ablation,
    reason=(
        "Table 4 (@obs_lcf_ablation) shows the predicted asymmetric pattern "
        "exactly: across all three model sizes, Pass@1 changes by ≤ 0.7 "
        "points when $\\mathcal{L}_{\\mathrm{cf}}$ is removed, while Pass@128 "
        "drops by 2–4.7 points. This matches the internalization prediction "
        "and is incompatible with the substitutability prediction of the "
        "sharpening alternative."
    ),
    prior=0.88
)

s_internalization_obs = support(
    [claim_internalization_supported], obs_lcf_ablation,
    reason=(
        "Under the internalization hypothesis (@claim_internalization_supported), "
        "$\\mathcal{L}_{\\mathrm{cf}}$ is the loss that distills corrective "
        "alternatives (@claim_cf_internalizes_recovery), so its removal should "
        "selectively erode the coverage measured by Pass@128 — exactly the "
        "asymmetric pattern observed in @obs_lcf_ablation."
    ),
    prior=0.85,
    background=[setup_cf_loss, setup_rehearsal_loss]
)

s_alt_just_sharpening_obs = support(
    [alt_leafe_just_sharpening], obs_lcf_ablation,
    reason=(
        "If LEAFE were merely a sharpening recipe, $\\mathcal{L}_{\\mathrm{cf}}$ "
        "and $\\mathcal{L}_{\\mathrm{reh}}$ would be redundant probabilistic "
        "reweighting losses — removing either should affect both metrics "
        "proportionally. The observed selective Pass@128 collapse in "
        "@obs_lcf_ablation is hard to reconcile with this view."
    ),
    prior=0.18
)

abd_internalization = abduction(
    s_internalization_obs, s_alt_just_sharpening_obs, cmp_internalization,
    reason=(
        "The internalization thesis and the 'LEAFE is just a better sharpener' "
        "alternative make different predictions about how Pass@1 and Pass@128 "
        "should co-vary with $\\mathcal{L}_{\\mathrm{cf}}$. Table 4's "
        "asymmetric pattern preferentially supports internalization."
    )
)

# Internalization claim should also be linked back to the OOD evidence. We
# avoid double counting by routing through obs_ood_mbpp via a separate support.
strat_internalization_ood = support(
    [obs_ood_mbpp],
    claim_internalization_supported,
    reason=(
        "Internalized agency should generalize across distributions; OOD MBPP "
        "(@obs_ood_mbpp) shows LEAFE preserving or exceeding base-model "
        "Pass@128 on every backbone while GRPO degrades. This generalization "
        "behavior is consistent with the internalization hypothesis "
        "(@claim_internalization_supported) and inconsistent with mere "
        "in-distribution distribution sharpening."
    ),
    prior=0.78
)

# Stage-1 branching beats IS/IR
claim_stage1_branching_better = claim(
    "Tree-based experience-guided rollback branching (LEAFE Stage 1) is a "
    "more effective use of a fixed execution budget on CodeContests than "
    "either independent sampling or iterative refinement. It dominates both "
    "baselines for every backbone in Table 3.",
    title="Stage-1 branching > IS / IR under fixed budget"
)

strat_stage1_branching = support(
    [obs_stage1_sampling],
    claim_stage1_branching_better,
    reason=(
        "Direct reading of @obs_stage1_sampling: LEAFE Stage-1 Pass@128 "
        "(55.52 / 54.30 / 42.50) exceeds IR (51.48 / 49.52 / 38.10) which in "
        "turn exceeds IS (48.92 / 48.65 / 30.20) on Qwen2.5-32B / Qwen2.5-72B "
        "/ Llama3-70B. The dominance is uniform across all three models."
    ),
    prior=0.92,
    background=[setup_passk]
)

# Note: we considered modelling 'distribution sharpening' and 'LEAFE beats
# GRPO at Pass@128' as a contradiction, but they are actually mutually
# supportive (sharpening predicts GRPO's plateau, which makes room for LEAFE
# to beat it). Flagged in the Critical Analysis as an unmodeled tension
# rather than a hard contradiction.
