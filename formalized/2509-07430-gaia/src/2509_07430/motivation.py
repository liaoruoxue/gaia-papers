"""Introduction: Diversity Collapse in RLVR and the Role of Divergence Choice"""

from gaia.lang import claim, setting, question

# ── Settings ──────────────────────────────────────────────────────────────────

rlvr_setting = setting(
    "Reinforcement Learning with Verifiable Reward (RLVR) is a paradigm for fine-tuning "
    "large language models (LLMs) using rule-based reward signals from verifiable domains "
    "(e.g., mathematics, code/SQL). The agent (LLM policy $\\pi_\\theta$) generates responses "
    "and receives binary or scalar rewards $r(a|q)$ without relying on a separate reward model.",
    title="RLVR definition",
)

pass_at_k_setting = setting(
    "Pass@k is a multi-attempt performance metric for LLMs: given $k$ independent samples "
    "from the model for a query, Pass@k is 1 if at least one sample is correct. "
    "Pass@1 (greedy accuracy) measures single-attempt performance; Pass@k for $k > 1$ "
    "measures coverage and diversity of the model's solution space.",
    title="Pass@k metric definition",
)

reverse_kl_setting = setting(
    "Reverse KL-divergence $D_{KL}(\\pi_\\theta \\| \\pi_{ref})$ is a mode-seeking divergence: "
    "minimizing it forces the policy $\\pi_\\theta$ to concentrate probability mass on modes "
    "of the reference $\\pi_{ref}$, collapsing low-probability regions even if they contain "
    "correct solutions.",
    title="Reverse KL mode-seeking property (definition)",
)

f_divergence_setting = setting(
    "An f-divergence between distributions $p$ and $q$ is defined as "
    "$D_f(p \\| q) = \\int q(x) f\\!\\left(\\frac{p(x)}{q(x)}\\right) dx$, "
    "where $f$ is a strictly convex function with $f(1) = 0$. "
    "Special cases: forward-KL uses $f(u) = -\\log u$; "
    "Jensen-Shannon (JS) uses $f(u) = u \\log u - (u+1)\\log\\frac{u+1}{2}$; "
    "reverse-KL uses $f(u) = u \\log u$.",
    title="f-divergence definition",
)

# ── Questions ─────────────────────────────────────────────────────────────────

q_diversity_collapse = question(
    "Why does RLVR training improve Pass@1 (single-attempt accuracy) while simultaneously "
    "degrading Pass@k (multi-attempt diversity) compared to the base model, and how can "
    "this diversity collapse be mitigated?",
    title="Core research question",
)

# ── Claims ────────────────────────────────────────────────────────────────────

pass1_improves = claim(
    "Standard RLVR training (e.g., GRPO, DAPO) consistently improves Pass@1 (greedy "
    "single-attempt accuracy) on in-domain benchmarks compared to the base model.",
    title="RLVR improves Pass@1",
)

passk_degrades = claim(
    "Standard RLVR training (e.g., GRPO, DAPO) causes Pass@k ($k > 1$) to degrade "
    "below the base model's Pass@k, indicating that the policy's solution distribution "
    "has narrowed (diversity collapse). For example, on the AIME24 math benchmark with "
    "Llama-3.1-8B-Instruct, GRPO reduces Pass@64 from 40.0 to 33.3 compared to the "
    "base model.",
    title="RLVR degrades Pass@k",
)

catastrophic_forgetting = claim(
    "Standard RLVR training causes catastrophic forgetting of out-of-domain knowledge: "
    "SQL-task-trained models (Llama-3.1-8B-Instruct) show average out-of-domain math "
    "performance (across AIME24, AMC23, Math500, Olympiad, Minerva, College Math) "
    "dropping from a base of 60.35 to 52.37 (GRPO) and 52.63 (DAPO), a loss of "
    "approximately 8 percentage points.",
    title="Catastrophic forgetting in out-of-domain tasks",
)

rkl_accelerates_collapse = claim(
    "Reverse KL-divergence, when used as a regularizer in RLVR objectives, actively "
    "accelerates diversity collapse by enforcing mode-seeking behavior—the policy converges "
    "to a narrow set of high-probability solutions and reduces Pass@k further compared to "
    "methods with no divergence constraint.",
    title="Reverse KL accelerates diversity collapse",
)

divergence_choice_neglected = claim(
    "The choice of divergence in RLVR objectives has been neglected as a design dimension, "
    "with most prior methods either omitting divergence constraints (GRPO, DAPO) or using "
    "reverse KL, neither of which preserves solution diversity.",
    title="Divergence choice neglected in prior RLVR work",
)

mass_covering_preserves = claim(
    "Mass-covering f-divergences (forward-KL, Jensen-Shannon divergence) can be used as "
    "implicit rehearsal mechanisms in RLVR training to preserve solution diversity and "
    "prevent catastrophic forgetting, while still allowing improvements in Pass@1.",
    title="Mass-covering divergences preserve diversity",
)

__all__ = [
    "pass1_improves",
    "passk_degrades",
    "catastrophic_forgetting",
    "rkl_accelerates_collapse",
    "divergence_choice_neglected",
    "mass_covering_preserves",
]
