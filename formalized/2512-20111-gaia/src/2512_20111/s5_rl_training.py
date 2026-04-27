"""Section 5: Reinforcement Learning to Act through Belief Bottlenecks.

Includes the methods (belief length penalty, belief grading) and three
experimental settings: Combination Lock, multi-objective QA, ColBench.
"""

from gaia.lang import claim, contradiction, induction, setting, support

from .motivation import abbel_proposal, finding_rl_helps
from .s2_framework import abbel_two_call_loop
from .s4_eval_frontier import prompting_only_inadequate

# --- Method definitions ---

bg_grpo = setting(
    "GRPO (Group Relative Policy Optimization) is the RL algorithm used. "
    "Training is performed in VeRL-agent (Feng et al., 2025) [@Feng2025], a "
    "multi-context synchronous rollout framework. The base model is "
    "Qwen2.5-7B-Instruct with chain-of-thought prompting for both belief "
    "generation and action selection.",
    title="RL training stack (GRPO in VeRL-agent on Qwen2.5-7B-Instruct)",
)

method_belief_length_penalty = claim(
    "The belief length penalty (LP) is a small negative reward proportional to "
    "the longest belief state in the trajectory. Following Arora and Zanette "
    "[@AroraZanette2025], it is applied after advantage normalization so its "
    "impact diminishes as beliefs get shorter, avoiding over-compression. "
    "Because ABBEL's belief is isolated from chain-of-thought reasoning, the "
    "penalty does not penalize reasoning tokens.",
    title="Belief Length Penalty (LP) reward",
)

method_belief_grading = claim(
    "Belief grading creates a separate size-2 GRPO group per step: the original "
    "belief $b_t$ and a regenerated belief $b_t'$ from the same context "
    "$(p_I, b_{t-1}, a_{t-1}, o_{t-1}, p_b)$. Each is assigned a grading "
    "reward (problem-specific or general). Treating each belief as its own "
    "single-step trajectory (rather than adding the reward to the outcome "
    "reward) avoids the reward-hacking failure of agents solving tasks slowly "
    "to collect more step-wise rewards [@Lidayan2025]. Policy gradient steps "
    "on belief groups and trajectory groups are applied concurrently.",
    title="Belief Grading procedure",
    metadata={
        "figure": "artifacts/2512.20111.pdf, Fig. 3",
        "caption": "Overview of belief grading: regenerate b' from same context, grade both, apply GRPO to size-2 group.",
    },
)

# === Subsection 5.2.1: Combination Lock ===

bg_combo_lock = setting(
    "Combination Lock is a 3-character version of Wordle proposed by Arumugam "
    "and Griffiths [@Arumugam2025]: training uses a vocabulary of 10 digits "
    "and a 12-step horizon; testing uses a disjoint vocabulary of 16 letters "
    "and a 16-step horizon (compositional/horizon generalization). Each "
    "episode ends with reward $(H+1-\\text{steps to find code})/H$ on success, "
    "$-1$ on failure. Cumulative Regret = number of steps until the code is "
    "identified.",
    title="Combination Lock environment",
)

cl_belief_grader = setting(
    "The Combination Lock belief grader uses Grok-4-Fast-Free as an LLM parser "
    "to extract a list of possible numbers per position from each belief, "
    "compares to the ground-truth posterior computed from prior actions and "
    "observations, and assigns reward 1 if identical, 0 otherwise. Grading "
    "stops at the first incorrect belief in a trajectory to avoid penalizing "
    "purely-propagated errors.",
    title="Combination Lock belief grader",
)

# Initial / pre-training observation
obs_cl_initial_abbel_worse = claim(
    "On Combination Lock, the initial (zero-shot) performance of all ABBEL "
    "agents is significantly lower than VANILLA and BELIEF PROMPTING, "
    "consistent with the prompting-only findings from Section 4.",
    title="Combination Lock: initial ABBEL gap (Fig. 4a, train step 0)",
)

# Prediction (claim) for ABBEL with belief grading
pred_cl_belief_grading_wins = claim(
    "If belief grading is an effective RL shaping reward in environments "
    "requiring complex belief-update reasoning, ABBEL trained with belief "
    "grading should match or exceed VANILLA and BELIEF PROMPTING success rates "
    "on Combination Lock, with belief lengths remaining significantly shorter "
    "than the interaction history.",
    title="Prediction: belief grading lets ABBEL surpass full-context baselines",
)

# Observation
obs_cl_bg_outperforms = claim(
    "After ~120 training steps, ABBEL with belief grading reaches a test "
    "success rate that exceeds both VANILLA (full-history baseline) and BELIEF "
    "PROMPTING on Combination Lock. Belief lengths first increase early in "
    "training but then decrease, remaining significantly shorter than the "
    "history beyond the first 2 environment steps.",
    title="Combination Lock: ABBEL-BG surpasses VANILLA (Fig. 4)",
    metadata={
        "figure": "artifacts/2512.20111.pdf, Fig. 4",
        "caption": "ABBEL-BG surpasses VANILLA on Combination Lock; belief length first grows then shrinks while staying shorter than history.",
    },
)

# Alternative: ABBEL without belief grading (still RL-trained)
pred_cl_abbel_no_bg = claim(
    "Without belief grading, RL-trained ABBEL would close the gap with the "
    "full-context baselines (because RL is generally effective for ABBEL) but "
    "would not surpass them, because complex belief-update reasoning needs "
    "the dense shaping signal that belief grading provides.",
    title="Prediction: ABBEL without belief grading only catches up",
)

obs_cl_abbel_no_bg_catches_up = claim(
    "ABBEL trained without belief grading does close the success-rate gap with "
    "the full-context baselines on Combination Lock, but its Cumulative Regret "
    "and final success rate are notably worse than ABBEL-BG, with longer "
    "belief states learned over training (still significantly shorter than the "
    "full history past the first two steps).",
    title="Combination Lock: ABBEL without BG catches up but trails BG (Fig. 4a, ablation)",
    metadata={
        "figure": "artifacts/2512.20111.pdf, Fig. 10 (Appendix D)",
        "caption": "Ablation: ABBEL without belief grading on Combination Lock.",
    },
)

# Support + contradiction: belief grading is the right explanation for
# ABBEL-BG > baselines on Combination Lock. The contradiction expresses
# that the "RL alone is enough" alternative is incompatible with the
# observed ablation pattern (without BG, ABBEL only catches up).
strat_cl_bg_explains = support(
    [pred_cl_belief_grading_wins, obs_cl_abbel_no_bg_catches_up],
    obs_cl_bg_outperforms,
    reason=(
        "@pred_cl_belief_grading_wins predicts that BG-trained ABBEL surpasses "
        "the baselines while keeping beliefs concise. The ablation "
        "@obs_cl_abbel_no_bg_catches_up shows that without BG, ABBEL only "
        "catches up rather than surpassing — isolating BG as the load-bearing "
        "ingredient. Together these support the observation @obs_cl_bg_outperforms "
        "that ABBEL-BG specifically exceeds VANILLA and BELIEF PROMPTING on "
        "Combination Lock."
    ),
    prior=0.9,
)

contradiction_cl_alt = contradiction(
    pred_cl_belief_grading_wins,
    pred_cl_abbel_no_bg,
    reason=(
        "The 'belief grading is load-bearing' prediction "
        "(@pred_cl_belief_grading_wins, which forecasts BG specifically "
        "surpasses baselines) and the 'RL alone is enough' alternative "
        "(@pred_cl_abbel_no_bg, which forecasts ABBEL without BG also "
        "surpasses) make incompatible predictions about the ablation "
        "outcome. The Fig. 10a result that without BG, ABBEL only catches "
        "up forces these two hypotheses apart."
    ),
    prior=0.95,
)

# === Subsection 5.2.2: Multi-objective Question Answering ===

bg_qa = setting(
    "The multi-objective QA environment introduced by Zhou et al. (2025b) "
    "[@ZhouMEM12025]: each task asks the agent a set of questions (objectives), "
    "the agent iteratively queries an external knowledge base (each query "
    "returns the first 100 words of the 3 most relevant documents), and finally "
    "outputs semicolon-delimited answers. Training: 2 questions, 6 steps. "
    "Testing: up to 16 objectives, 20 steps (extreme horizon generalization). "
    "Reward = Exact Match (EM) count.",
    title="Multi-objective QA environment",
)

bg_mem1 = setting(
    "MEM1 [@ZhouMEM12025] is a contemporaneous memory-management RL approach "
    "where the entire chain-of-thought reasoning trace at each step is reused "
    "as the next step's memory (no separation between belief and reasoning). "
    "A length penalty cannot be applied to MEM1 without also penalizing "
    "reasoning.",
    title="MEM1 baseline (no belief/reasoning isolation)",
)

# Multi-objective QA observation (peak token usage and EM scores from Table 1)
obs_qa_peak_tokens_table = claim(
    "Multi-objective QA results, peak token usage per trajectory ($\\times 10^2$ "
    "tokens) and Exact Match score (mean over the test set):\n\n"
    "| Model | 2-Obj EM | 2-Obj Tokens | 8-Obj EM | 8-Obj Tokens | 16-Obj EM | 16-Obj Tokens |\n"
    "|-------|----------|--------------|----------|--------------|-----------|---------------|\n"
    "| VANILLA Zero | 0.30 | 11.25 | 0.37 | 16.06 | 0.40 | 15.40 |\n"
    "| VANILLA 14B Zero | 0.73 | 15.60 | 1.55 | 44.70 | 0.57 | 38.40 |\n"
    "| VANILLA (trained) | 0.79 | 17.87 | 2.54 | 64.07 | 3.06 | 96.08 |\n"
    "| MEM1 Base | 0.71 | 6.40 | 1.87 | 8.01 | 1.97 | 10.40 |\n"
    "| MEM1 Instruct | 0.79 | 6.69 | 1.88 | 9.13 | 2.50 | 10.58 |\n"
    "| ABBEL Zero | 0.53 | 6.85 | 1.28 | 8.67 | 1.62 | 9.46 |\n"
    "| ABBEL | 0.73 | 6.78 | 2.40 | 8.95 | **3.57** | 10.12 |\n"
    "| ABBEL LP | 0.70 | 6.56 | 2.19 | **7.61** | 3.43 | **7.64** |\n",
    title="Multi-objective QA: EM and peak tokens (Table 1)",
    metadata={
        "source_table": "artifacts/2512.20111.pdf, Table 1",
        "caption": "Multi-objective QA results. Lower tokens, higher EM.",
    },
)

obs_qa_abbel_outperforms_mem1 = claim(
    "On multi-objective QA with 4 or more objectives, ABBEL achieves "
    "significantly higher EM than MEM1 (Base and Instruct) and substantially "
    "higher than the zero-shot VANILLA models. At 16 objectives, ABBEL "
    "reaches EM = 3.57 vs MEM1 Instruct = 2.50 (43% higher) while using only "
    "~10.12 ($\\times 10^2$) peak tokens vs MEM1's 10.58.",
    title="ABBEL > MEM1 on multi-objective QA (Fig. 5a, Table 1)",
    metadata={
        "figure": "artifacts/2512.20111.pdf, Fig. 5a",
        "caption": "EM vs. # objectives. ABBEL closest to full-context VANILLA for 4+ objectives.",
    },
)

obs_qa_abbel_lp_memory = claim(
    "ABBEL LP (with belief length penalty) further reduces peak token usage "
    "compared to ABBEL while only slightly reducing EM. At 16 objectives, "
    "ABBEL LP uses 7.64 ($\\times 10^2$) peak tokens vs ABBEL's 10.12 — a "
    "24% reduction — and EM = 3.43 vs ABBEL's 3.57. ABBEL LP still "
    "significantly outperforms MEM1 in EM at 16 objectives (3.43 vs 2.50).",
    title="ABBEL LP trades small EM for large memory savings (Table 1)",
    metadata={
        "source_table": "artifacts/2512.20111.pdf, Table 1",
    },
)

obs_qa_vanilla_close = claim(
    "The trained full-context VANILLA model only slightly outperforms ABBEL on "
    "multi-objective QA, with no advantage at 16 objectives despite using "
    "~9.5x more memory (96.08 vs 10.12 $\\times 10^2$ peak tokens). Zero-shot "
    "VANILLA models cannot handle 16 objectives at all (~3.5x lower EM than "
    "ABBEL Zero), suggesting 16 objectives approaches the limit of long-context "
    "models.",
    title="Trained VANILLA only marginally better, uses 9.5x more memory",
    metadata={
        "source_table": "artifacts/2512.20111.pdf, Table 1",
    },
)

# Pred/alt for QA
pred_qa_isolation_helps = claim(
    "If isolating the belief state from reasoning (the key architectural "
    "difference between ABBEL and MEM1) is what enables better memory–"
    "performance trade-offs, then ABBEL should outperform MEM1 in EM at the "
    "same memory budget, and ABBEL LP should be applicable (penalize belief "
    "without penalizing reasoning) while MEM1 cannot apply a length penalty "
    "without harming reasoning.",
    title="Prediction: belief–reasoning isolation drives the QA advantage",
)

alt_qa_just_better_rl = claim(
    "Alternative explanation: ABBEL's QA advantage comes from incidental RL "
    "training details (hyperparameters, prompt design) rather than from the "
    "architectural isolation of belief from reasoning. Under this alternative, "
    "MEM1 with the same training tweaks would match ABBEL.",
    title="Alternative: incidental training details drive the QA advantage",
)

strat_qa_isolation_explains = support(
    [pred_qa_isolation_helps, obs_qa_abbel_lp_memory],
    obs_qa_abbel_outperforms_mem1,
    reason=(
        "@pred_qa_isolation_helps (belief–reasoning isolation drives the "
        "advantage) predicts that ABBEL beats MEM1 in EM at comparable memory, "
        "and additionally predicts that a length penalty applied to the "
        "isolated belief (@obs_qa_abbel_lp_memory) further trades EM for "
        "memory — something MEM1 cannot do because its 'memory' includes "
        "reasoning (@bg_mem1). Together these directly support the headline "
        "observation @obs_qa_abbel_outperforms_mem1 that ABBEL outperforms "
        "MEM1 on multi-objective QA."
    ),
    prior=0.85,
    background=[bg_mem1],
)

contradiction_qa_alt = contradiction(
    pred_qa_isolation_helps,
    alt_qa_just_better_rl,
    reason=(
        "The 'incidental training details' alternative (@alt_qa_just_better_rl) "
        "predicts that re-implementing MEM1 with the same training tweaks (the "
        "MEM1 Instruct ablation reported in the paper) would close the gap, "
        "and that a length-penalty advantage would not exist. Both predictions "
        "fail in the data. These two hypotheses make incompatible claims "
        "about what would happen under apples-to-apples retraining and under "
        "LP application."
    ),
    prior=0.92,
)

# === Subsection 5.2.3: ColBench Collaborative Programming ===

bg_colbench = setting(
    "ColBench [@ZhouSweet2025] is a collaborative back-end programming "
    "environment: the agent is given an under-specified high-level task "
    "description and a function signature, can ask the user up to 10 questions "
    "to gather information, and finally submits Python code (up to 50 lines). "
    "The user is simulated by Gemma 3 27B-it with access to the hidden tests "
    "and a reference solution. Outcome reward = fraction of 10 hidden unit "
    "tests passed. Test Pass Rate is the mean across episodes; Success Rate is "
    "the fraction of tasks with all 10 tests passing.",
    title="ColBench environment",
)

cb_general_belief_grader = setting(
    "The ColBench belief grader is domain-general (no ground-truth posterior "
    "needed): how useful $b_{t+1}$ is for reconstructing $o_t$ given $b_t$ "
    "and $a_t$, defined as the agent model's log probability "
    "$f_{BG}(b_{t+1}) = \\log p(o_t \\mid b_t, a_t, b_{t+1})$. This is "
    "proportional to $\\log p(b_{t+1} \\mid b_t, a_t, o_t) - \\log p(b_{t+1} "
    "\\mid b_t, a_t)$ plus a constant: the second term encourages $b_{t+1}$ to "
    "contain new information relative to the prior, the first encourages that "
    "new information to be explainable by $o_t$.",
    title="Domain-general belief grader (log-probability of last observation)",
)

# ColBench observation table (Table 2)
obs_cb_table = claim(
    "ColBench results across training steps (mean ± SEM over 2 seeds for "
    "ABBEL/ABBEL-BG; over 1 seed test set for VANILLA):\n\n"
    "| Step | Model | Test Pass Rate | Success Rate | Peak Tokens ($\\times 10^2$) |\n"
    "|------|-------|----------------|--------------|------------------------------|\n"
    "| 0 | VANILLA | 0.2827 ± 0.0125 | 0.1748 ± 0.0119 | 4.5938 ± 0.1532 |\n"
    "| 0 | ABBEL | 0.2642 ± 0.0125 | 0.1709 ± 0.0118 | 3.2953 ± 0.0525 |\n"
    "| 50 | VANILLA | 0.4456 ± 0.0139 | 0.3047 ± 0.0144 | 8.9805 ± 0.1396 |\n"
    "| 50 | ABBEL | 0.3844 ± 0.0140 | 0.2651 ± 0.0093 | 3.4078 ± 0.0499 |\n"
    "| 50 | ABBEL-BG | 0.4560 ± 0.0132 | 0.3228 ± 0.0079 | 3.9693 ± 0.2542 |\n"
    "| 100 | VANILLA | 0.5260 ± 0.0141 | 0.3936 ± 0.0153 | 7.8845 ± 0.1084 |\n"
    "| 100 | ABBEL | 0.4655 ± 0.0112 | 0.3286 ± 0.0121 | 3.8614 ± 0.0711 |\n"
    "| 100 | ABBEL-BG | 0.4577 ± 0.0004 | 0.3262 ± 0.0021 | 3.4149 ± 0.3210 |\n",
    title="ColBench: ABBEL vs VANILLA over training (Table 2)",
    metadata={
        "source_table": "artifacts/2512.20111.pdf, Table 2",
    },
)

obs_cb_abbel_memory_efficient = claim(
    "On ColBench at training step 100, ABBEL achieves 88.5% of VANILLA's Test "
    "Pass Rate (0.4655 vs 0.5260) while using only 49% as much peak memory "
    "(3.86 vs 7.88, $\\times 10^2$ tokens). ABBEL-BG at step 100 has similar "
    "Test Pass Rate (0.4577) with even less memory (3.41).",
    title="ColBench: ABBEL ~half memory at ~88% of VANILLA's pass rate",
)

obs_cb_bg_data_efficient = claim(
    "At step 50, ABBEL-BG reaches Test Pass Rate 0.4560 — on par with VANILLA "
    "(0.4456) and significantly better than ABBEL without belief grading "
    "(0.3844). This indicates that the domain-general belief grader makes "
    "ABBEL more data-efficient: ABBEL without BG only catches up at step 100.",
    title="ColBench: belief grading makes ABBEL data-efficient",
)

obs_cb_zero_shot_parity = claim(
    "Zero-shot (training step 0), ABBEL and VANILLA perform on par on ColBench "
    "(Test Pass Rate 0.2642 vs 0.2827) because ABBEL biases the agent to ask "
    "more questions before submitting (~6 vs VANILLA's ~2.8), making it more "
    "likely to gather necessary clarifications. This question-asking bias also "
    "explains why zero-shot VANILLA has the lowest Peak Tokens (it submits "
    "earlier).",
    title="ColBench: ABBEL biases agent to ask more questions (zero-shot parity)",
)

# === Cross-experiment induction: RL helps ABBEL across all three settings ===

s_rl_cl = support(
    [finding_rl_helps],
    obs_cl_bg_outperforms,
    reason="@finding_rl_helps (RL fine-tuning lets ABBEL match/exceed full-context baselines while using less memory) predicts the Combination Lock result @obs_cl_bg_outperforms.",
    prior=0.9,
)

s_rl_qa = support(
    [finding_rl_helps],
    obs_qa_abbel_outperforms_mem1,
    reason="@finding_rl_helps predicts the multi-objective QA result @obs_qa_abbel_outperforms_mem1 (RL-trained ABBEL beats MEM1 with comparable or less memory).",
    prior=0.9,
)

s_rl_cb = support(
    [finding_rl_helps],
    obs_cb_abbel_memory_efficient,
    reason="@finding_rl_helps predicts the ColBench result @obs_cb_abbel_memory_efficient (RL-trained ABBEL achieves close to VANILLA performance with about half the memory).",
    prior=0.9,
)

ind_rl_pair = induction(
    s_rl_cl,
    s_rl_qa,
    law=finding_rl_helps,
    reason="Combination Lock (highly structured) and multi-objective QA (lengthy unstructured observations) are independent environments providing distinct evidence for the law that RL closes/exceeds the ABBEL gap.",
)

ind_rl_three = induction(
    ind_rl_pair,
    s_rl_cb,
    law=finding_rl_helps,
    reason="ColBench (collaborative coding, long-form generation) is a third independent setting confirming the law across yet another regime.",
)

# === Discussion-level synthesis: ABBEL is a viable testbed ===

abbel_useful_testbed = claim(
    "ABBEL is a useful framework for studying the trade-off between context "
    "length and task performance in long-horizon LLM agents: it produces "
    "interpretable beliefs, supports interpretable RL shaping (belief grading "
    "and length penalty), and across diverse environments either matches or "
    "exceeds full-context baselines after RL while using significantly less "
    "memory.",
    title="ABBEL is a viable framework for long-horizon LLM agents (Discussion)",
)

strat_synthesis = support(
    [finding_rl_helps, prompting_only_inadequate],
    abbel_useful_testbed,
    reason=(
        "Even though prompting-only ABBEL has clear failure modes "
        "(@prompting_only_inadequate), the cross-environment RL evidence "
        "(@finding_rl_helps) — Combination Lock (BG surpasses), multi-objective "
        "QA (beats MEM1, ~10x less memory than VANILLA), ColBench (49% memory "
        "at 88% performance) — establishes ABBEL as a useful framework "
        "deserving further study, including for context management beyond "
        "multi-step interaction."
    ),
    prior=0.88,
    background=[abbel_proposal, abbel_two_call_loop],
)

# === Wire remaining orphaned observations into the BP graph ===

# Combination Lock initial gap is a direct realization of the prompting
# inadequacy law from Section 4.
strat_cl_initial_gap = support(
    [prompting_only_inadequate],
    obs_cl_initial_abbel_worse,
    reason=(
        "@prompting_only_inadequate (prompting-only ABBEL underperforms "
        "full-context baselines) directly predicts the Combination Lock "
        "step-0 gap @obs_cl_initial_abbel_worse — Combination Lock requires "
        "complex belief-update reasoning, exactly the regime where "
        "prompting-only ABBEL is weakest."
    ),
    prior=0.9,
)

# Combination Lock no-BG ablation realizes the predicted no-BG behavior.
strat_cl_no_bg_obs = support(
    [pred_cl_abbel_no_bg],
    obs_cl_abbel_no_bg_catches_up,
    reason=(
        "@pred_cl_abbel_no_bg predicts that without belief grading, RL-trained "
        "ABBEL closes the gap with full-context baselines but does not surpass "
        "them. The ablation in Fig. 10a shows exactly this: ABBEL without BG "
        "catches up in success rate but trails ABBEL-BG in Cumulative Regret "
        "and final success rate."
    ),
    prior=0.9,
)

# QA peak-tokens table directly supports the ABBEL-vs-MEM1 and ABBEL-LP claims.
strat_qa_table_supports_mem1 = support(
    [obs_qa_peak_tokens_table],
    obs_qa_abbel_outperforms_mem1,
    reason=(
        "The Table 1 row-by-row figures (@obs_qa_peak_tokens_table) directly "
        "give the EM and peak-token comparisons that establish "
        "@obs_qa_abbel_outperforms_mem1: ABBEL EM beats MEM1 EM at 4+ "
        "objectives with comparable peak-token counts."
    ),
    prior=0.97,
)

strat_qa_table_supports_lp = support(
    [obs_qa_peak_tokens_table, method_belief_length_penalty],
    obs_qa_abbel_lp_memory,
    reason=(
        "@obs_qa_peak_tokens_table provides the LP-row peak-token figures, "
        "and @method_belief_length_penalty defines the mechanism. Together "
        "they establish that ABBEL LP achieves ~24% memory savings at 16 "
        "objectives with only a small EM drop."
    ),
    prior=0.93,
)

strat_qa_table_supports_vanilla_close = support(
    [obs_qa_peak_tokens_table],
    obs_qa_vanilla_close,
    reason=(
        "@obs_qa_peak_tokens_table shows VANILLA (trained) vs ABBEL EM at "
        "16 objectives is essentially tied (3.06 vs 3.57) while VANILLA uses "
        "9.5x more peak tokens (96.08 vs 10.12), and zero-shot VANILLA fails "
        "at 16 objectives."
    ),
    prior=0.97,
)

# ColBench: detailed table supports memory-efficiency, BG-data-efficiency,
# and zero-shot-parity observations.
strat_cb_memory = support(
    [obs_cb_table],
    obs_cb_abbel_memory_efficient,
    reason=(
        "@obs_cb_table provides the step-100 figures: ABBEL Test Pass Rate "
        "0.4655 vs VANILLA 0.5260 (88.5%), peak tokens 3.86 vs 7.88 (49%). "
        "These directly establish @obs_cb_abbel_memory_efficient."
    ),
    prior=0.97,
)

strat_cb_data_efficient = support(
    [obs_cb_table, method_belief_grading],
    obs_cb_bg_data_efficient,
    reason=(
        "@obs_cb_table shows step-50 ABBEL-BG = 0.4560 (matching VANILLA's "
        "0.4456) versus ABBEL = 0.3844. @method_belief_grading is the "
        "mechanism. Together they establish that BG accelerates ABBEL learning "
        "on ColBench."
    ),
    prior=0.92,
)

strat_cb_zero_shot = support(
    [obs_cb_table, abbel_two_call_loop],
    obs_cb_zero_shot_parity,
    reason=(
        "@obs_cb_table shows step-0 ABBEL Test Pass Rate (0.2642) is on par "
        "with VANILLA (0.2827). @abbel_two_call_loop's two-call structure "
        "biases the agent toward asking more questions (no history of past "
        "answers means each turn the agent re-evaluates how much information "
        "it has), explaining the parity at step 0 and VANILLA's lower zero-shot "
        "Peak Tokens."
    ),
    prior=0.85,
)

__all__ = [
    "bg_grpo",
    "method_belief_length_penalty",
    "method_belief_grading",
    # Combination Lock
    "bg_combo_lock",
    "cl_belief_grader",
    "obs_cl_initial_abbel_worse",
    "pred_cl_belief_grading_wins",
    "obs_cl_bg_outperforms",
    "pred_cl_abbel_no_bg",
    "obs_cl_abbel_no_bg_catches_up",
    "strat_cl_bg_explains",
    "contradiction_cl_alt",
    # Multi-objective QA
    "bg_qa",
    "bg_mem1",
    "obs_qa_peak_tokens_table",
    "obs_qa_abbel_outperforms_mem1",
    "obs_qa_abbel_lp_memory",
    "obs_qa_vanilla_close",
    "pred_qa_isolation_helps",
    "alt_qa_just_better_rl",
    "strat_qa_isolation_explains",
    "contradiction_qa_alt",
    # ColBench
    "bg_colbench",
    "cb_general_belief_grader",
    "obs_cb_table",
    "obs_cb_abbel_memory_efficient",
    "obs_cb_bg_data_efficient",
    "obs_cb_zero_shot_parity",
    # Cross-experiment
    "ind_rl_three",
    "abbel_useful_testbed",
    "strat_synthesis",
]
