"""Section 4: What Makes RLVR with Spurious Rewards Work? — Code Reasoning"""

from gaia.lang import (
    claim, setting,
    support, deduction, abduction, induction, compare,
    contradiction,
)

from .motivation import (
    setup_rlvr, setup_models, setup_benchmarks,
    claim_pretraining_hypothesis, claim_rlvr_improves_qwen,
    claim_spurious_fails_non_qwen,
)

from .s2_spurious_rewards import (
    claim_qwen7b_math500_results, claim_random_gamma_robustness,
)

# ── Code reasoning: definitions and observations ───────────────────────────────

setup_code_reasoning_def = setting(
    "Code reasoning is defined as generating Python code as part of the "
    "reasoning chain to assist in solving a math problem — without access to "
    "a code execution environment. The model both writes the code AND predicts "
    "the output of that code autoregressively. Code reasoning frequency is "
    "measured as the percentage of MATH-500 responses containing the string "
    "'python'.",
    title="Code reasoning definition: generating Python code without execution environment",
)

claim_qwen_pretraining_code_freq = claim(
    "Before any RLVR training, Qwen2.5-Math-7B generates Python code in 65.0% "
    "of MATH-500 responses, and Qwen2.5-Math-1.5B in 53.6%, despite having no "
    "access to a code execution environment. This high baseline frequency of "
    "code-assisted reasoning is not observed in other model families:\n\n"
    "| Model | Code Frequency (pre-RL) |\n"
    "|-------|-------------------------|\n"
    "| Qwen2.5-Math-7B | 65.0% |\n"
    "| Qwen2.5-Math-1.5B | 53.6% |\n"
    "| Qwen2.5-7B | 92.2% (Bad-Code) |\n"
    "| OLMo2-7B-SFT | 98.0% (Bad-Code) |\n"
    "| Qwen2.5-1.5B | 0% (No-Code) |\n"
    "| OLMo2-7B | 0% (No-Code) |\n"
    "| Llama3.1-8B-Instruct | 0% (No-Code) |\n"
    "| Llama3.2-3B-Instruct | 0% (No-Code) |",
    title="Pre-RL code reasoning frequency: 65% for Qwen2.5-Math-7B, 0% for Llama/OLMo2",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Table 1"},
)

claim_code_accuracy_advantage = claim(
    "For Qwen2.5-Math-7B, MATH-500 accuracy when using code reasoning (60.9%) "
    "is substantially higher than when using only natural language (35.0%). "
    "For Qwen2.5-Math-1.5B, the same pattern holds (code: 52.6%, language: "
    "17.2%). This accuracy advantage does NOT hold for Bad-Code models: "
    "Qwen2.5-7B code accuracy is 39.9% versus 61.5% for language, and "
    "OLMo2-7B-SFT code accuracy is 21.0% versus 40.0% for language — code "
    "reasoning is counterproductive for these models.",
    title="Code reasoning accuracy advantage: 60.9% (code) vs 35.0% (language) for Qwen2.5-Math-7B",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Table 1"},
)

claim_code_freq_increases_rlvr = claim(
    "After RLVR training with any reward type (including spurious random and "
    "incorrect rewards), Qwen2.5-Math-7B's code reasoning frequency rapidly "
    "increases from 65% to ~90% within the first 15 training steps, and "
    "reaches as high as 95.6% for random reward. This increase in code "
    "frequency is strongly correlated with accuracy improvements across all "
    "reward types. With ground truth reward, code frequency also initially "
    "increases but then gradually decreases as natural language reasoning "
    "accuracy improves — suggesting ground truth provides genuine new learning "
    "while spurious rewards primarily amplify the existing code strategy.",
    title="RLVR increases code reasoning frequency from 65% to ~90%+ regardless of reward type",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Figure 6a"},
)

claim_lang_to_code_contribution = claim(
    "For Qwen2.5-Math-7B, 58.3% of the total MATH-500 accuracy gain from RLVR "
    "(averaged across spurious reward types) comes from the Lang→Code subset: "
    "problems where the model switches from natural language to code reasoning "
    "after RLVR. For Qwen2.5-Math-1.5B, this contribution is even higher "
    "at 78.7%. This shows that the dominant mechanism of improvement is "
    "converting language-reasoning problems to code-reasoning problems, not "
    "improving within each strategy type.\n\n"
    "| Model | Avg. Total Gain | C_Code→Code | C_Code→Lang | C_Lang→Code | C_Lang→Lang |\n"
    "|-------|----------------|-------------|-------------|-------------|-------------|\n"
    "| Qwen2.5-Math-7B | 23.5% | 11.6% | 8.6% | **58.3%** | 21.4% |\n"
    "| Qwen2.5-Math-1.5B | 28.5% | 2.8% | 2.0% | **78.7%** | 16.5% |\n"
    "| Qwen2.5-7B | 30.6% | 0.2% | **93.9%** | 0.0% | 5.9% |",
    title="Lang→Code strategy switching accounts for 58.3% (Qwen-Math-7B) and 78.7% (Qwen-Math-1.5B) of RLVR gains",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Table 2 and Figure 7"},
)

claim_bad_code_reduction = claim(
    "For Bad-Code models (Qwen2.5-7B and OLMo2-7B-SFT), which generate code "
    "frequently but with lower accuracy than natural language, RLVR with "
    "meaningful rewards (ground truth, majority vote) steers models away from "
    "code reasoning. For Qwen2.5-7B, 93.9% of its total 30.6% gain comes from "
    "the Code→Lang subset (problems where the model switches away from code to "
    "language reasoning). This is the inverse of the Qwen2.5-Math pattern.",
    title="Bad-Code models: RLVR gains come from reducing code reasoning (Code→Lang contributes 93.9%)",
)

# ── Intervention: explicitly inducing/inhibiting code reasoning ───────────────

claim_code_prompting_results = claim(
    "Forcing Qwen2.5-Math models to begin responses with 'Let's solve this "
    "using Python.' (code-forcing prompt) yields:\n\n"
    "| Model | Original | Prompting | Abs. Diff |\n"
    "|-------|----------|-----------|----------|\n"
    "| Qwen2.5-Math-1.5B | 36.2% | 60.4% | +24.2% |\n"
    "| Qwen2.5-Math-7B | 49.4% | 64.4% | +15.0% |\n"
    "| Qwen2.5-1.5B | 3.0% | 13.0% | +10.0% |\n"
    "| Qwen2.5-7B | 41.6% | 22.2% | -19.4% |\n"
    "| Llama3.2-3B-Instruct | 36.8% | 8.2% | -28.6% |\n"
    "| Llama3.1-8B-Instruct | 36.8% | 15.2% | -21.6% |\n"
    "| OLMo2-7B | 9.0% | 7.8% | -1.2% |\n"
    "| OLMo2-7B-SFT | 21.4% | 18.6% | -2.8% |\n\n"
    "Code forcing helps only models with effective code reasoning (Qwen-Math "
    "and Qwen2.5-1.5B) and hurts those without it.",
    title="Code-forcing prompt: +24.2%/+15% for Qwen-Math, -28.6%/-21.6% for Llama-Instruct",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Table 3"},
)

claim_python_reward_results = claim(
    "A Python reward (rewarding responses containing the string 'python') "
    "induces Qwen2.5-Math-7B to generate code reasoning in >99% of responses "
    "within 20 training steps, and yields performance gains comparable to or "
    "exceeding code-forcing via prompting on Qwen2.5-Math models. Other models "
    "demonstrate limited improvement from the Python reward.",
    title="Python reward RLVR: >99% code frequency in 20 steps, gains match or exceed code-forcing prompts",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Figure 8"},
)

claim_compound_reward_no_python = claim(
    "Compound rewards that intersect the original spurious reward with a "
    "'no Python' constraint (reward only if response satisfies the spurious "
    "condition AND does not contain 'python') test whether code reasoning is "
    "causally responsible for the spurious-reward gains. Results:\n"
    "- Format reward with no-Python: Qwen2.5-Math-7B gains cease entirely "
    "(confirming code reasoning is the mechanism for format reward).\n"
    "- Incorrect reward with no-Python: MATH-500 gains persist, but harder "
    "benchmarks (AMC, AIME) show reduced gains (other behaviors like reduced "
    "repetition may contribute).\n"
    "- Bad-Code models (Qwen2.5-7B, OLMo2-7B-SFT): compound rewards often "
    "outperform originals (OLMo2-7B-SFT gains +8.9 and +5.5 pp under "
    "format+no-Python and incorrect+no-Python vs. degradation under originals).",
    title="Compound no-Python reward: confirms code reasoning drives format reward; partially drives incorrect reward",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Figure 9"},
)

# ── GRPO clipping bias mechanism ──────────────────────────────────────────────

claim_grpo_clipping_bias = claim(
    "Under random rewards, the expected group-relative advantage $\\hat{A}$ is "
    "zero, so the expected gradient without clipping is also zero. However, "
    "GRPO's PPO-style clipping term introduces a nonzero gradient bias. "
    "Specifically, for token $y_t$ with old policy probability $\\pi_{\\text{old},x}(y_t)$"
    " and importance ratio $R_\\theta = \\pi_{\\theta,x}(y_t)/\\pi_{\\text{old},x}(y_t)$, "
    "the clipping bias is proportional to $\\mu > 0$ and creates:\n"
    "- Positive gradient (increases $\\pi_{\\theta,x}(y_t)$) when $R_\\theta < 1 - \\epsilon_c$\n"
    "- Negative gradient (decreases $\\pi_{\\theta,x}(y_t)$) when $R_\\theta > 1 + \\epsilon_c$\n"
    "- Zero gradient in the clipping region $[1-\\epsilon_c, 1+\\epsilon_c]$\n"
    "This creates an asymmetric effect: tokens with high prior probability "
    "($\\pi_{\\text{old}} \\approx 0.85$) have upper clipping threshold $\\approx 1.02 > 1$, "
    "so they almost never receive negative gradient bias, while low-probability "
    "tokens face much more frequent penalization.",
    title="GRPO clipping bias derivation: asymmetric gradient favors high-prior token patterns",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Appendix B.1.2"},
)

claim_clipping_amplifies_prior = claim(
    "The GRPO clipping bias systematically increases the average token "
    "probability ($\\pi_\\theta$) of the model's high-prior responses under "
    "random rewards. Empirical evidence: average token probability increases "
    "monotonically during random-reward training with clipping (purple line, "
    "reaching ~0.93+), while it remains approximately constant without clipping "
    "(green line, staying near 0.85). Clipping also correlates with the "
    "observed increase in code reasoning frequency.",
    title="Empirical: clipping increases token probability and code frequency; no-clipping does not",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Figure 12"},
)

claim_no_clipping_no_gain = claim(
    "When GRPO clipping is disabled (via direct removal, increased mini-batch "
    "size to match rollout size, or reduced rollout size to ensure $\\pi_\\theta = "
    "\\pi_{\\text{old}}$), random-reward training does NOT produce robust "
    "MATH-500 performance improvement across seeds. Average results across "
    "seeds show no meaningful gain. The standard GRPO with clipping consistently "
    "achieves ~21 pp improvement. Removing clipping from the implementation "
    "(not batch size) produces high variance — occasionally high performance "
    "due to inherent training stochasticity, but not reliably.",
    title="Without GRPO clipping, random rewards yield no robust improvement (confirming clipping as mechanism)",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Figure 11 and Figure 13"},
)

claim_clipping_qwen_specificity = claim(
    "The clipping bias mechanism operates on all models, but it only improves "
    "performance when the model's high-prior behaviors are effective reasoning "
    "strategies. For Qwen2.5-Math: code reasoning occurs at 65% baseline with "
    "64% accuracy (vs 35% without code) — so amplifying it improves performance. "
    "For No-Code models (Llama, OLMo2-7B): no code reasoning to amplify, so "
    "clipping bias has no beneficial behavioral pattern to reinforce. For "
    "Bad-Code models (OLMo2-7B-SFT): code reasoning has 21% accuracy (worse "
    "than 40% for natural language) — amplifying it hurts performance.",
    title="Clipping bias is universal but only beneficial when high-prior behaviors correlate with correctness",
)

# ── No-repetition pattern ──────────────────────────────────────────────────────

claim_no_repetition_pattern = claim(
    "A no-repetition reward (score=1 if response has no string repeated more "
    "than 10 times, else 0) also improves Qwen2.5-Math-7B and Qwen2.5-Math-1.5B "
    "on MATH-500 and AMC, but not other models. Qwen-Math models have a higher "
    "baseline tendency to produce repetitive outputs; answers using code "
    "reasoning typically do not have this issue. This demonstrates that code "
    "reasoning is not the only pretraining-instilled pattern that RLVR can "
    "surface — reduced repetition is another.",
    title="No-repetition reward also improves Qwen-Math performance: second example of surfaceable pretraining pattern",
    metadata={"figure": "artifacts/2506.10947-spurious-rewards.pdf, Figure 17"},
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_code_freq_pretraining = support(
    [claim_qwen_pretraining_code_freq],
    claim_pretraining_hypothesis,
    reason=(
        "The high baseline code reasoning frequency in Qwen2.5-Math-7B (65%) "
        "and Qwen2.5-Math-1.5B (53.6%) before any RLVR training "
        "(@claim_qwen_pretraining_code_freq) is direct evidence that these "
        "models have code-assisted math reasoning patterns already present from "
        "pretraining. The model has seen many code-augmented math reasoning "
        "traces during pretraining, which is the representation that RLVR "
        "(@claim_pretraining_hypothesis) is hypothesized to surface."
    ),
    prior=0.9,
    background=[setup_code_reasoning_def],
)

strat_code_accuracy_causal = support(
    [claim_code_accuracy_advantage, claim_code_freq_increases_rlvr],
    claim_lang_to_code_contribution,
    reason=(
        "Since code reasoning achieves 60.9% accuracy vs 35.0% for language "
        "on Qwen2.5-Math-7B (@claim_code_accuracy_advantage), and RLVR "
        "systematically converts language-reasoning problems to code-reasoning "
        "ones (@claim_code_freq_increases_rlvr), the resulting accuracy "
        "improvement is quantified in @claim_lang_to_code_contribution as "
        "58.3% of total gains from the Lang→Code subset."
    ),
    prior=0.9,
)

strat_clipping_causes_amplification = support(
    [claim_grpo_clipping_bias, claim_clipping_amplifies_prior],
    claim_no_clipping_no_gain,
    reason=(
        "The theoretical derivation (@claim_grpo_clipping_bias) shows that "
        "clipping creates an asymmetric gradient bias favoring high-prior tokens. "
        "The empirical observation (@claim_clipping_amplifies_prior) shows this "
        "bias manifests as increased average token probability and code frequency. "
        "Together these predict that removing clipping should eliminate the "
        "mechanism — confirmed by @claim_no_clipping_no_gain."
    ),
    prior=0.85,
)

strat_clipping_explains_qwen_specificity = support(
    [claim_clipping_qwen_specificity, claim_grpo_clipping_bias, claim_code_accuracy_advantage],
    claim_pretraining_hypothesis,
    reason=(
        "The clipping-bias mechanism (@claim_grpo_clipping_bias) amplifies "
        "high-prior behavioral patterns, but only benefits performance if those "
        "patterns are effective (@claim_clipping_qwen_specificity). For "
        "Qwen2.5-Math, high-prior code reasoning correlates with high accuracy "
        "(@claim_code_accuracy_advantage), so clipping amplification → performance "
        "gain. This provides a concrete mechanistic account of @claim_pretraining_hypothesis."
    ),
    prior=0.8,
)

# Intervention abduction: prompting vs training for code elicitation
alt_code_elicitation_only_prompt = claim(
    "Code reasoning elicitation is achievable through prompting alone, without "
    "RLVR training — the gains attributed to RLVR might simply be prompt effects.",
)

# Shared observation for abduction: code-frequency increase during RLVR
obs_code_freq_gain = claim(
    "Under RLVR training with spurious rewards (format, random, incorrect), "
    "Qwen2.5-Math-7B's code reasoning frequency increases rapidly from 65% to "
    "~90%+ within the first 15 steps, even though no prompt change is applied — "
    "the frequency increase is driven by the training dynamics, not by prompting.",
    title="Code frequency increases during spurious-reward RLVR without any prompt change",
)

s_h_rlvr_elicits = support(
    [claim_code_freq_increases_rlvr, claim_lang_to_code_contribution],
    obs_code_freq_gain,
    reason=(
        "RLVR training (@claim_code_freq_increases_rlvr) converts language-reasoning "
        "problems to code-reasoning ones even with spurious rewards, accounting for "
        "the majority of gains (@claim_lang_to_code_contribution). "
        "Since no prompt change occurs during training, this establishes the "
        "training-time effect (@obs_code_freq_gain) as distinct from prompt effects."
    ),
    prior=0.9,
)

s_alt_prompt_sufficient = support(
    [alt_code_elicitation_only_prompt],
    obs_code_freq_gain,
    reason=(
        "Prompting alone (@alt_code_elicitation_only_prompt) also increases code "
        "frequency and improves performance on Qwen-Math. If prompting were sufficient, "
        "we might expect similar code-frequency dynamics — but prompting cannot explain "
        "why code frequency increases during spurious-reward RLVR without any prompt change."
    ),
    prior=0.2,
)

pred_rlvr_broader = claim(
    "If RLVR causes code elicitation, it should produce behaviors beyond what "
    "prompting can induce, and compound rewards controlling code should affect "
    "performance specifically through the code channel.",
)

pred_prompt_same = claim(
    "If prompting alone is sufficient, compound no-Python rewards should not "
    "specifically affect the gains — any RLVR-induced gain should persist.",
)

comp_elicitation = compare(
    pred_rlvr_broader, pred_prompt_same, obs_code_freq_gain,
    reason=(
        "Compound no-Python rewards specifically eliminate format-reward gains "
        "(@claim_compound_reward_no_python), confirming that code reasoning is "
        "causally required for format-reward RLVR improvements, not just a "
        "correlation. RLVR training induces code frequency increases without "
        "prompt changes, distinguishing it from mere prompting effects."
    ),
    prior=0.85,
)

abd_code_elicitation = abduction(
    s_h_rlvr_elicits, s_alt_prompt_sufficient, comp_elicitation,
    reason=(
        "Both RLVR-based code elicitation and prompt-based elicitation are tested. "
        "The compound reward evidence and no-prompt-change observation distinguish them."
    ),
)
