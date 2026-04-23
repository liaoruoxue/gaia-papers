"""Section 6: Empirical Validations"""

from gaia.lang import claim, setting, support, compare, abduction, induction

from .motivation import (
    mara_exists,
    empirical_diversity_collapse,
    kl_type_not_primary_driver,
)
from .s4_mode_coverage_analysis import (
    low_beta_unimodal,
    equal_reward_unimodal,
    typical_settings_unimodal,
)
from .s5_mara import (
    mara_solution_is_uniform,
    mara_works_fwd_kl,
    mara_algorithm_def,
    mara_threshold_setting,
)

# ── Settings ───────────────────────────────────────────────────────────────────

task_1_2_def = setting(
    "The 1-2 task (Section 6.1): a language model (Qwen2.5-3B) is trained to generate "
    "a uniformly random integer that is either 1 or 2. "
    "It receives reward 1.0 for correct output (producing '1' or '2' in XML format), "
    "and reward 0.0 otherwise. "
    "Since both '1' and '2' are equally correct, an optimal diverse policy should generate them "
    "with near-equal probability (~0.5 each). "
    "The base policy has higher likelihood for '1' than '2'. "
    "Training is evaluated across multiple $\\beta$ values and random seeds.",
    title="1-2 task setup (Section 6.1)",
    metadata={"source": "artifacts/2510.20817.pdf, Section 6.1; Appendix C.2"},
)

creative_qa_def = setting(
    "The creative question answering task (Section 6.2): Qwen3-1.7B is trained on 10k WildChat English prompts "
    "using Skywork-Reward-V2-Qwen3-4B as the reward model. "
    "MARA is used as a drop-in in an RLOO-style algorithm. "
    "Evaluation uses a held-out NoveltyBench test set with Skywork-Reward-Gemma-2-27B-v0.2. "
    "Metrics: In-dist. Reward (training RM on training set), Out-dist. Reward (eval RM on test set), "
    "Ngram EAD (expectation-adjusted distinct n-grams, n=1..5), "
    "Semantic Div (cosine distance in all-MiniLM-L6-v2 embedding space), "
    "Mean Distinct (number of distinct concepts per Zhang et al. 2025).",
    title="Creative QA task setup (Section 6.2)",
    metadata={"source": "artifacts/2510.20817.pdf, Section 6.2; Appendix C.3"},
)

drug_discovery_def = setting(
    "The drug discovery task (Section 6.3): Chemical language models (CLMs) generate SMILES strings "
    "optimized for two reward functions: "
    "SYNTH (binding potency + synthesizability via any reactions) and "
    "SYNTH-ALL-AMIDE (binding potency + synthesizability via only amide coupling reactions). "
    "Each reward is a product of four components: "
    "docking score (QuickVina2-GPU against ClpP protein), QED (drug-likeness), "
    "HBD constraint (< 4 hydrogen-bond donors), and Syntheseus synthesizability. "
    "MARA is applied to REINVENT (state-of-the-art RL-based CLM algorithm). "
    "Evaluation metrics: Yield (unique molecules above reward threshold), "
    "OB100 (reward evaluations to generate 100 threshold-passing molecules), "
    "IntDiv1 (intra-set structural diversity), #Circles (sphere packing diversity). "
    "Budget: 10,000 reward function evaluations.",
    title="Drug discovery task setup (Section 6.3)",
    metadata={"source": "artifacts/2510.20817.pdf, Section 6.3; Appendix C.4"},
)

# ── Experimental observation claims ───────────────────────────────────────────

exp_12_vanilla_collapses = claim(
    "On the 1-2 task, vanilla KL-regularized RL (without MARA), across a range of $\\beta$ values "
    "and random seeds, all but one run collapse into generating only a single answer. "
    "Most collapse to generating '1', which has higher likelihood under the base policy. "
    "Rewards remain high (~1.0) since both answers are valid, confirming this is a diversity collapse, "
    "not a correctness failure.",
    title="Vanilla RL collapses to single answer on 1-2 task",
    metadata={"figure": "artifacts/2510.20817.pdf, Figure 6a, Figure 10"},
)

exp_12_mara_diverse = claim(
    "MARA on the 1-2 task successfully preserves diversity: many runs learn to generate '1' and '2' "
    "with near-uniform probability (~0.5 each, measured by valid-answer entropy), "
    "while maintaining correctness (reward ~1.0). "
    "This holds for both reverse and forward KL regularization across all tested $\\beta$ values "
    "($\\beta \\in \\{0.001, 0.01, 0.02, 0.03\\}$).",
    title="MARA preserves diversity on 1-2 task",
    metadata={"figure": "artifacts/2510.20817.pdf, Figure 6a"},
)

exp_12_pareto = claim(
    "The Pareto front of model checkpoints (reward vs. valid-answer entropy) on the 1-2 task shows "
    "that MARA dominates vanilla RL for both reverse and forward KL regularization: "
    "MARA achieves higher entropy (diversity) at equal or better reward (quality). "
    "Vanilla RL runs cluster at low entropy even at high reward.",
    title="MARA dominates vanilla RL on quality-diversity Pareto front (1-2 task)",
    metadata={"figure": "artifacts/2510.20817.pdf, Figure 6b"},
)

exp_creative_qa_table = claim(
    "On the creative QA task (non-verifiable, reward model), MARA outperforms both GRPO and RLOO "
    "in terms of out-of-distribution reward and most diversity metrics. "
    "Specifically (Table 1): "
    "- MARA (fwd) achieves the highest Out-dist. Reward: $1.604 \\pm 0.113$ vs. RLOO: $1.280 \\pm 0.100$ and GRPO: $1.317 \\pm 0.102$. "
    "- MARA (fwd) achieves the highest Ngram EAD: $0.568 \\pm 0.012$ vs. RLOO: $0.514 \\pm 0.014$. "
    "- MARA (fwd) achieves the highest Mean Distinct: $4.62 \\pm 0.258$ vs. RLOO: $3.88 \\pm 0.243$. "
    "- Semantic Div is the one metric where the Base Model ($0.220$) outperforms all trained models; "
    "MARA (fwd) matches RLOO at $0.193$.",
    title="MARA outperforms GRPO and RLOO on creative QA (Table 1)",
    metadata={"source": "artifacts/2510.20817.pdf, Table 1"},
)

exp_drug_synth_yield = claim(
    "On the SYNTH drug discovery task at threshold 0.80 (Table 2a/5), "
    "MARA achieves higher Yield than REINVENT: $6834 \\pm 78$ vs. $6569 \\pm 186$ unique molecules "
    "(statistically significant, one-sided t-test, $p < 0.05$). "
    "MARA also achieves lower OB100 ($1015 \\pm 55$ vs. $1042 \\pm 66$, not statistically significant). "
    "IntDiv1 and #Circles are competitive (not significantly different).",
    title="MARA improves yield on SYNTH task at threshold 0.80",
    metadata={"source": "artifacts/2510.20817.pdf, Table 2a"},
)

exp_drug_amide_yield = claim(
    "On the SYNTH-ALL-AMIDE drug discovery task at threshold 0.85 (Table 2b/6), "
    "MARA achieves higher Yield than REINVENT: $1235 \\pm 130$ vs. $1098 \\pm 88$ unique molecules "
    "(statistically significant). "
    "MARA also achieves lower OB100 ($3943 \\pm 303$ vs. $4360 \\pm 257$, statistically significant). "
    "MARA also achieves slightly higher IntDiv1 ($0.733 \\pm 0.009$ vs. $0.721 \\pm 0.016$). "
    "This is the more challenging reward function (amide-only synthesis constraint).",
    title="MARA improves yield and efficiency on SYNTH-ALL-AMIDE task at threshold 0.85",
    metadata={"source": "artifacts/2510.20817.pdf, Table 2b"},
)

exp_drug_global_diversity = claim(
    "On drug discovery tasks, MARA does not explicitly optimize for global structural diversity "
    "(IntDiv1, #Circles), yet it is competitive with REINVENT on these metrics. "
    "MARA focuses on ensuring all high-reward molecules are found (local diversity over threshold), "
    "while global diversity (sub-structural coverage) is not degraded.",
    title="MARA maintains global diversity on drug discovery tasks",
    metadata={"source": "artifacts/2510.20817.pdf, Tables 2, 5, 6"},
)

# ── Strategies ────────────────────────────────────────────────────────────────

# Abduction: vanilla collapse explained by unimodal objective vs exploration failure
alt_exploration = claim(
    "Vanilla RL collapse on the 1-2 task is due to insufficient exploration or optimization budget, "
    "not an intrinsic property of the RL objective. "
    "With enough training steps or better exploration, the policy would converge to a balanced distribution.",
    title="Alternative: collapse is due to insufficient exploration",
)

s_h_collapse = support(
    [typical_settings_unimodal],
    exp_12_mara_diverse,
    reason=(
        "The 1-2 task uses equal rewards for correct answers (1.0 for both '1' and '2'). "
        "From @equal_reward_unimodal (a component of @typical_settings_unimodal): "
        "when rewards are equal, the optimal solution preserves the reference probability ratio. "
        "Since '1' has higher base probability than '2', the objective is the CAUSE of collapse. "
        "If the objective is the cause, then MARA (which directly targets a multimodal objective) "
        "should successfully prevent collapse — as confirmed by @exp_12_mara_diverse.",
    ),
    prior=0.88,
    background=[task_1_2_def],
)

s_alt_collapse = support(
    [alt_exploration],
    exp_12_mara_diverse,
    reason=(
        "If collapse were due to insufficient exploration, MARA (which only changes reward magnitudes) "
        "should NOT be able to prevent collapse without additional exploration mechanisms. "
        "However, MARA does prevent collapse (@exp_12_mara_diverse), which is INCONSISTENT with "
        "the exploration-failure hypothesis — lowering the prior on this alternative.",
    ),
    prior=0.35,
    background=[task_1_2_def],
)

pred_objective = claim(
    "If the RL objective has a unimodal optimal solution (theory), "
    "then a method that directly constructs a multimodal target (MARA) should prevent collapse "
    "without any exploration changes.",
    title="Prediction: MARA prevents collapse if objective is the cause",
)

pred_exploration = claim(
    "If collapse is due to exploration failure, then MARA (which only changes reward magnitudes, "
    "not the exploration strategy) should NOT prevent collapse.",
    title="Alt prediction: exploration-only change needed to prevent collapse",
)

comp_mara_effectiveness = compare(
    pred_objective,
    pred_exploration,
    exp_12_mara_diverse,
    reason=(
        "MARA succeeds empirically: Figure 6a shows MARA runs preserve diversity (high entropy) "
        "while achieving high reward, for both KL variants. "
        "The objective-based prediction @pred_objective is confirmed: only reward magnitude changes "
        "were made (no exploration changes), yet collapse is prevented. "
        "The exploration prediction @pred_exploration is falsified: MARA prevents collapse without "
        "addressing exploration.",
    ),
    prior=0.87,
)

abd_collapse_cause = abduction(
    s_h_collapse,
    s_alt_collapse,
    comp_mara_effectiveness,
    reason=(
        "Both the unimodal-objective hypothesis and the exploration-failure hypothesis "
        "attempt to explain the same observation: vanilla RL collapse on the 1-2 task. "
        "The MARA experiment serves as a natural discriminator: "
        "MARA only changes reward magnitudes (not exploration), "
        "so if it prevents collapse, the objective is the cause.",
    ),
)

# Strategies for other experiments
strat_12_pareto = support(
    [exp_12_mara_diverse, exp_12_vanilla_collapses],
    exp_12_pareto,
    reason=(
        "The Pareto front aggregates checkpoints across training. "
        "From @exp_12_mara_diverse: MARA maintains both high entropy and high reward simultaneously. "
        "From @exp_12_vanilla_collapses: vanilla RL achieves high reward but low entropy. "
        "Therefore on the reward-entropy Pareto front, MARA checkpoints are higher entropy "
        "at all reward levels, and MARA dominates.",
    ),
    prior=0.9,
)

strat_creative = support(
    [mara_solution_is_uniform, mara_works_fwd_kl],
    exp_creative_qa_table,
    reason=(
        "The creative QA task is non-verifiable: rewards come from a reward model, not ground-truth. "
        "MARA adapts by setting $\\tau$ per batch as an upper percentile of sampled rewards (@mara_threshold_setting). "
        "From @mara_solution_is_uniform: the MARA target distribution places equal mass on all "
        "above-threshold responses, encouraging the model to find diverse high-quality responses. "
        "From @mara_works_fwd_kl: MARA works for both KL variants. "
        "Table 1 shows MARA (fwd) achieves the best out-of-distribution reward and diversity.",
    ),
    prior=0.8,
    background=[creative_qa_def, mara_threshold_setting],
)

strat_drug_synth = support(
    [mara_solution_is_uniform],
    exp_drug_synth_yield,
    reason=(
        "In drug discovery, CLMs are evaluated on the number of UNIQUE high-reward molecules found "
        "(Yield) within a fixed budget. "
        "From @mara_solution_is_uniform: MARA's target distribution places uniform probability on all "
        "above-threshold molecules, directly encouraging exploration of the high-reward space. "
        "This matches the SYNTH task result: MARA improves Yield ($6834$ vs $6569$, +4%) at threshold 0.80.",
    ),
    prior=0.8,
    background=[drug_discovery_def, mara_algorithm_def],
)

strat_drug_amide = support(
    [mara_solution_is_uniform],
    exp_drug_amide_yield,
    reason=(
        "The SYNTH-ALL-AMIDE task is more constrained (only amide reactions allowed), "
        "leading to a harder search problem with fewer high-reward molecules. "
        "From @mara_solution_is_uniform: MARA's uniform target distribution incentivizes exploring "
        "the amide-synthesis-compatible space rather than exploiting a narrow learned mode. "
        "At threshold 0.85 — the harder threshold where diversity matters most — "
        "MARA shows larger improvements: Yield +12.5% and OB100 -9.6%.",
    ),
    prior=0.82,
    background=[drug_discovery_def, mara_algorithm_def],
)

# Induction over experimental domains to support general MARA effectiveness
s_mara_llm1 = support(
    [mara_exists],
    exp_12_mara_diverse,
    reason="MARA achieves diversity on the verifiable 1-2 LLM task",
    prior=0.87,
)

s_mara_llm2 = support(
    [mara_exists],
    exp_creative_qa_table,
    reason="MARA improves quality and diversity on the non-verifiable creative QA LLM task",
    prior=0.8,
)

s_mara_clm = support(
    [mara_exists],
    exp_drug_synth_yield,
    reason="MARA improves drug discovery optimization in chemical language models — a completely different domain",
    prior=0.8,
)

ind_llm_tasks = induction(
    s_mara_llm1,
    s_mara_llm2,
    law=mara_exists,
    reason="The 1-2 task and creative QA task are independent: different models, tasks, and reward types",
)

ind_all_domains = induction(
    ind_llm_tasks,
    s_mara_clm,
    law=mara_exists,
    reason="The drug discovery experiments use a different model architecture (CLM) and domain from LLM experiments",
)
