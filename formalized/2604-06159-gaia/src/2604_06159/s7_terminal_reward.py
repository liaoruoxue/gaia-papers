"""Section 3.6-3.8: Sparse / terminal reward, ablations, LLM RLVR.

Sections 3.6 (terminal reward sequence credit assignment), 3.7
(anchor and target-matching ablations), and 3.8 (transfer to
billion-parameter LLM RLVR) of [@Kaddour2026]. These are the
sparse-reward sections that constitute the paper's *headline gap*:
under terminal reward, GRPO/PPO/DG degrade steeply with sequence
length while TPO maintains low error.

* Sec. 3.6 -- $H \\in \\{7, 8, 9, 10\\}$, exact-match terminal
  reward, 2,000 episodes; both prompt-matched and interaction-matched.
  TPO is best at every $H$ under both protocols.

* Sec. 3.7 -- Ablations isolate three TPO ingredients on the same
  terminal-reward benchmark: (i) the $p^{\\text{old}}$ anchor, (ii)
  target matching itself (vs. Group PG), (iii) GRPO's KL penalty.
  Removing any of the first two consistently hurts; the gaps widen
  with $H$.

* Sec. 3.8 -- LLM RLVR on Qwen3-1.7B and DeepSeek-R1-Distill-1.5B,
  three tasks (GSM8K, graph coloring, Knights & Knaves), $K=16$
  rollouts. TPO matches GRPO at saturation on GSM8K but is faster
  early; on the Reasoning Gym tasks the gap is much starker (graph
  coloring: GRPO fails entirely on Qwen3-1.7B at near-zero score
  while TPO reaches ~0.96).
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Sec. 3.6 setup
# ---------------------------------------------------------------------------

setup_terminal_reward = setting(
    "**Sec. 3.6 terminal-reward setup.** No intermediate feedback: "
    "the model receives an *exact-match* reward only after the full "
    "sequence is generated. Without per-token rewards, the paper "
    "reverts to *sequence-level* TPO and GRPO, each sampling $K = 8$ "
    "complete rollouts per prompt. Prompt-matched runs use $B = 100$; "
    "interaction-matched runs scale single-sample batch size and "
    "learning rate by $K = 8$ and $\\sqrt{K}$ respectively. Other "
    "hyperparameters match Sec. 3.4 ($V = 2$); $H \\in \\{7, 8, 9, "
    "10\\}$ over 2,000 episodes. Reported metric: exact-match error "
    "(fraction of sequences with any mistake), not token-level error "
    "[@Kaddour2026, Sec. 3.6].",
    title="Setup (3.6): terminal exact-match reward, $K=8$ rollouts, $H \\in \\{7,8,9,10\\}$",
)

# ---------------------------------------------------------------------------
# Sec. 3.6 numerical
# ---------------------------------------------------------------------------

claim_table3_terminal_results = claim(
    "**Table 3: Exact-match error (%) under terminal reward.** Bold = "
    "best per column; '-' = no meaningful learning ($> 95$%).\n\n"
    "| Method | $H=7$ pm | $H=8$ pm | $H=9$ pm | $H=10$ pm | $H=7$ im | $H=8$ im | $H=9$ im | $H=10$ im |\n"
    "|--------|---------:|---------:|---------:|----------:|---------:|---------:|---------:|----------:|\n"
    "| TPO | **6.9** | **8.6** | **6.1** | **7.4** | **1.8** | **2.8** | **5.3** | **19.0** |\n"
    "| GRPO | 14.5 | 27.6 | 30.0 | 50.4 | 9.6 | 23.2 | 36.2 | 48.7 |\n"
    "| GRPO (no KL) | 66.6 | 92.5 | - | - | 78.1 | 83.8 | - | - |\n"
    "| PPO | 12.0 | 26.3 | 90.6 | - | 38.6 | 62.1 | 66.2 | - |\n"
    "| DG | 33.8 | 58.8 | - | - | 47.7 | 69.4 | - | - |\n\n"
    "(pm = prompt-matched; im = interaction-matched). TPO attains "
    "the lowest exact-match error at *every* $H$ under *both* "
    "matching protocols. GRPO without KL fails at $H \\ge 8$, "
    "confirming KL is its primary stabilizer "
    "[@Kaddour2026, Table 3].",
    title="Numerical (3.6): TPO lowest at every $H$ under both matching protocols (Table 3)",
    metadata={
        "table": "artifacts/2604.06159.pdf, Table 3",
    },
)

claim_3_6_steep_baseline_degradation = claim(
    "**Baselines degrade steeply with $H$; TPO does not.** Under "
    "prompt-matched terminal reward, GRPO error rises from 14.5% at "
    "$H = 7$ to 50.4% at $H = 10$ (a $3.5\\times$ jump); PPO from "
    "12.0% to no learning ('-'); DG from 33.8% to no learning. TPO "
    "stays in the 6-9% band across all four $H$. The interaction-"
    "matched table shows a similar pattern: TPO gracefully degrades "
    "from 1.8% ($H=7$) to 19.0% ($H=10$) while baselines collapse. "
    "This is the strongest sparse-reward gap the paper documents.",
    title="Result (3.6): TPO 6-9% across $H \\in \\{7,...,10\\}$; baselines collapse with $H$",
    metadata={
        "figure": "artifacts/2604.06159.pdf, Figure 8",
        "caption": "Terminal reward learning curves, prompt- and interaction-matched.",
    },
)

claim_3_6_interaction_match_unchanged = claim(
    "**Under interaction matching, TPO's gap remains.** With "
    "single-sample baselines given $K = 8$ extra prompts (and learning "
    "rate scaled by $\\sqrt{K}$) per step, TPO is *still* lowest "
    "error at every tested $H$. The gap is *wider* under terminal "
    "reward than under bag-of-tokens (where interaction matching "
    "narrowed it substantially), because in the terminal-reward "
    "regime the bottleneck is *not gradient variance* but extracting "
    "useful signal from sparse outcomes -- the regime where target "
    "matching matters most [@Kaddour2026, Sec. 3.6].",
    title="Result (3.6): interaction matching does not close the gap under terminal reward",
)

# ---------------------------------------------------------------------------
# Sec. 3.7: ablations
# ---------------------------------------------------------------------------

setup_ablation_3_7 = setting(
    "**Sec. 3.7 ablation setup.** Same terminal-reward benchmark "
    "($H \\in \\{7, 8, 10\\}$, $V = 2$, $K = 8$, $B = 100$, 20 "
    "seeds). All methods use the *same* grouped full-sequence "
    "rollouts. Variants: 'TPO-no-anchor' removes the $p^{\\text{old}}$ "
    "anchor ($q_i \\propto \\exp(u_i)$, no rollout-snapshot "
    "weighting); 'Group PG' keeps the same candidates and "
    "standardized scores but replaces target matching with scalar-"
    "weighted policy gradient; 'GRPO (no KL)' removes the reverse-KL "
    "penalty ($\\beta = 0$).",
    title="Setup (3.7): same grouped rollouts; vary anchor / target-matching / KL ingredient",
)

claim_3_7_no_anchor_hurts = claim(
    "**Removing the $p^{\\text{old}}$ anchor consistently hurts (Sec. "
    "3.7).** TPO-no-anchor underperforms full TPO at every $H \\in "
    "\\{7, 8, 10\\}$ on terminal-reward reverse-copy (Figure 9). At "
    "$H = 10$, full TPO reaches 7.4% while TPO-no-anchor exceeds "
    "99% -- the anchor is doing real work, not a cosmetic addition.",
    title="Ablation (3.7): TPO without anchor exceeds 99% at $H=10$ vs. full TPO 7.4%",
    metadata={
        "figure": "artifacts/2604.06159.pdf, Figure 9",
    },
)

claim_3_7_target_matching_essential = claim(
    "**Target matching itself is essential (Group PG ablation).** "
    "Group PG keeps TPO's same candidates and standardized scores "
    "but replaces target matching with scalar-weighted REINFORCE; "
    "it is the *worst* method on the Sec. 3.7 ablation benchmark "
    "(Figure 9). At $H = 10$, Group PG also exceeds 99% error vs. "
    "TPO's 7.4%. Combined with the MNIST result (Group PG 7.2% vs. "
    "TPO 2.9%), this isolates target matching itself -- not the "
    "candidate set or the score signal -- as the active ingredient "
    "[@Kaddour2026, Sec. 3.7].",
    title="Ablation (3.7): Group PG (same signal, scalar update) exceeds 99% at $H=10$",
)

# ---------------------------------------------------------------------------
# Sec. 3.8: LLM RLVR
# ---------------------------------------------------------------------------

setup_llm_rlvr = setting(
    "**Sec. 3.8 LLM RLVR setup.** TPO and GRPO compared on two "
    "models -- Qwen3-1.7B [@Yang2025Qwen3] and DeepSeek-R1-Distill-"
    "Qwen-1.5B [@Guo2025R1] -- and three tasks: GSM8K [@Cobbe2021GSM8K], "
    "graph coloring (Reasoning Gym), and Knights & Knaves "
    "(Reasoning Gym) [@Stojanovski2025RG]. All runs use $K = 16$ "
    "rollouts per prompt; the paired runs differ *only* in the "
    "policy loss (TPO vs. clipped surrogate with $z$-scored "
    "advantages). Implementation: verl stack [@Sheng2024verl], AdamW "
    "at $10^{-5}$, batch size 16, $4 \\times$ A100-80GB GPUs. GSM8K "
    "uses LoRA (rank 32) and a KL penalty ($\\lambda_{\\text{KL}} = "
    "10^{-3}$) on both methods (Appendix G).",
    title="Setup (3.8): TPO vs. GRPO, 2 models x 3 tasks, $K=16$, identical except policy loss",
)

claim_3_8_gsm8k_match = claim(
    "**Sec. 3.8 -- GSM8K: TPO matches GRPO at saturation; faster "
    "early.** On GSM8K with Qwen3-1.7B (Figure 10, top-left), TPO "
    "reaches 50% accuracy roughly 10 steps before GRPO. Both "
    "converge to comparable final accuracy in the $\\sim 85$-87% "
    "range, consistent with the headline 'TPO matches PG-family on "
    "easy tasks; substantial outperformance only under sparse / "
    "harder tasks' [@Kaddour2026, Sec. 3.8].",
    title="Result (3.8): GSM8K -- TPO faster early, both reach ~85-87% (TPO matches GRPO)",
    metadata={
        "figure": "artifacts/2604.06159.pdf, Figure 10 (left column)",
    },
)

claim_3_8_graph_color_qwen_gap = claim(
    "**Sec. 3.8 -- Graph coloring (Qwen3-1.7B): GRPO fails entirely; "
    "TPO reaches ~0.96.** On Reasoning Gym graph coloring with Qwen3-"
    "1.7B (Figure 10, top-middle), GRPO produces a near-zero train "
    "mean score for the full 300-step budget while TPO reaches "
    "$\\sim 0.96$. This is the LLM-scale analogue of the sparse-"
    "reward stall observed earlier on token reversal: a real billion-"
    "parameter model on a real harder task shows the same "
    "qualitative gap, not just a quantitative speedup "
    "[@Kaddour2026, Sec. 3.8, Figure 10].",
    title="Result (3.8): graph coloring (Qwen3) -- GRPO ~0; TPO ~0.96",
    metadata={
        "figure": "artifacts/2604.06159.pdf, Figure 10 (top-middle)",
    },
)

claim_3_8_graph_color_r1_distill = claim(
    "**Sec. 3.8 -- Graph coloring (R1-Distill-1.5B): both learn but "
    "TPO converges higher.** On the same task with the DeepSeek-R1-"
    "Distill-Qwen-1.5B model (Figure 10, bottom-middle), both methods "
    "learn but TPO converges to $\\sim 0.96$ vs. GRPO's $\\sim 0.81$. "
    "Even when GRPO does learn at LLM scale, the converged ceiling is "
    "lower [@Kaddour2026, Sec. 3.8].",
    title="Result (3.8): graph coloring (R1-Distill) -- TPO 0.96 vs. GRPO 0.81",
)

claim_3_8_knk_same_pattern = claim(
    "**Sec. 3.8 -- Knights & Knaves: same pattern.** On Reasoning "
    "Gym Knights & Knaves (Figure 10, right column), the same "
    "pattern recurs: TPO outperforms GRPO on the train mean score "
    "for both Qwen3-1.7B and DeepSeek-R1-Distill-Qwen-1.5B. The "
    "harder tasks expose TPO's advantage more clearly than GSM8K, "
    "where both methods eventually saturate [@Kaddour2026, Sec. 3.8].",
    title="Result (3.8): Knights & Knaves -- TPO outperforms GRPO on both models",
    metadata={
        "figure": "artifacts/2604.06159.pdf, Figure 10 (right column)",
    },
)

claim_3_8_population_llm_rlvr = claim(
    "**Sec. 3.8 population conclusion: TPO's advantage transfers to "
    "billion-parameter LLM RLVR on harder tasks.** Across the 6 "
    "(model, task) pairs in Section 3.8, the headline pattern from "
    "the smaller experiments persists: comparable performance on "
    "easier tasks where both methods saturate (GSM8K), substantial "
    "advantage to TPO on harder Reasoning Gym tasks (graph coloring, "
    "Knights & Knaves) -- including the qualitative collapse of "
    "GRPO on graph coloring with Qwen3-1.7B. This is the answer to "
    "the section's opening question: 'Does TPO's advantage transfer "
    "to this setting?' -- yes [@Kaddour2026, Sec. 3.8].",
    title="Population (3.8): TPO advantage transfers to LLM RLVR on harder Reasoning Gym tasks",
)

__all__ = [
    "setup_terminal_reward",
    "setup_ablation_3_7",
    "setup_llm_rlvr",
    "claim_table3_terminal_results",
    "claim_3_6_steep_baseline_degradation",
    "claim_3_6_interaction_match_unchanged",
    "claim_3_7_no_anchor_hurts",
    "claim_3_7_target_matching_essential",
    "claim_3_8_gsm8k_match",
    "claim_3_8_graph_color_qwen_gap",
    "claim_3_8_graph_color_r1_distill",
    "claim_3_8_knk_same_pattern",
    "claim_3_8_population_llm_rlvr",
]
