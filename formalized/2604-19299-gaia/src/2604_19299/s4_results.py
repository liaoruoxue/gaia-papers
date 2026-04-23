"""Section 4: Results and Analysis"""

from gaia.lang import (
    claim, setting, support, deduction, abduction, induction,
    contradiction, compare,
)
from .motivation import (
    slm_inherent_limits, agent_potential, react_framework, slm_definition,
)
from .s3_methodology import (
    base_slm_design, sas_design, mas_design,
    metric_completion_rate, metric_nrq, metric_composite_z,
    experimental_scope, model_families, task_scope,
)

# ── Section 4.1 – Overall system trade-off observations ──────────────────────

obs_sas_nrq = claim(
    "The Single-Agent System (SAS) achieves a Normalized Response Quality (NRQ) of "
    "4.85, representing a clear improvement over the Base SLM baseline (NRQ = 0.00 by "
    "construction). The Multi-Agent System (MAS) achieves only NRQ = 0.36, representing "
    "minimal additional gain beyond the Base SLM.",
    title="Observed NRQ: SAS=4.85, MAS=0.36, Base=0.00",
    metadata={"source_table": "artifacts/2604.19299.pdf, Table 2"},
)

obs_completion_rates = claim(
    "Completion rates across architectures (Table 2):\n\n"
    "| Architecture | Completion Rate |\n"
    "|---|---|\n"
    "| Base SLM | 99.67% |\n"
    "| SAS | 79.92% |\n"
    "| MAS | 72.01% |\n\n"
    "Reliability degrades substantially as architectural complexity increases, with "
    "MAS failing to return a valid response on roughly 28% of samples.",
    title="Observed completion rates by architecture (Table 2)",
    metadata={"source_table": "artifacts/2604.19299.pdf, Table 2"},
)

obs_latency_tokens = claim(
    "Average latency nearly doubles for agent paradigms compared to the Base SLM "
    "(SAS: 23.27s, MAS: 22.76s vs. Base: 12.39s). Token usage per sample rises "
    "sharply: Base = 2,356 tokens, SAS = 8,040 tokens, MAS = 14,618 tokens. Tokens "
    "per second also increase (Base: 190 t/s, SAS: 345 t/s, MAS: 642 t/s), but this "
    "throughput gain does not offset the total latency increase.",
    title="Observed latency and token usage by architecture (Table 2)",
    metadata={"source_table": "artifacts/2604.19299.pdf, Table 2"},
)

obs_energy_per_token = claim(
    "Energy per token (in millijoules) decreases with architectural complexity: "
    "Base SLM = 1.83 mJ/token, SAS = 1.02 mJ/token, MAS = 0.52 mJ/token—a 71% "
    "reduction from Base to MAS. However, token count per sample increases "
    "3.4x for SAS and 6.2x for MAS, so total energy per sample is higher for "
    "agent paradigms despite the lower per-token cost.",
    title="Observed energy per token by architecture (Table 2)",
    metadata={"source_table": "artifacts/2604.19299.pdf, Table 2"},
)

# ── Section 4.2 – Efficiency–Effectiveness trade-off ─────────────────────────

obs_sas_pareto = claim(
    "In the efficiency–effectiveness trade-off space (composite Z-score vs. "
    "energy/token on a log scale, Fig. 2), SAS consistently occupies the upper-left "
    "quadrant: achieving strong effectiveness (mostly $Z_c > 0.4$) at relatively "
    "low energy levels. This indicates SAS improves performance without large "
    "coordination cost.",
    title="SAS occupies Pareto-optimal region of efficiency–effectiveness space",
    metadata={"figure": "artifacts/2604.19299.pdf, Figure 2",
              "caption": "Fig. 2: Efficiency-Effectiveness trade-off across model-architecture settings."},
)

obs_base_uturn = claim(
    "In the efficiency–effectiveness trade-off space (Fig. 2), Base SLMs (8B–10B "
    "variants) exhibit a 'U-turn' pattern: they move toward the lower-right region "
    "combining high energy use with lower effectiveness ($Z_c < -0.5$). Smaller "
    "Base SLMs perform moderately but larger ones underperform even smaller ones. "
    "This reveals diminishing and eventually negative returns from parameter scaling "
    "alone, without an agent paradigm.",
    title="Base SLM U-turn: large models combine high energy with low effectiveness",
    metadata={"figure": "artifacts/2604.19299.pdf, Figure 2"},
)

obs_mas_variance = claim(
    "MAS shows high variance in the efficiency–effectiveness trade-off space (Fig. 2): "
    "it can reach high effectiveness but often requires more energy due to coordination "
    "overhead, and smaller MAS configurations sometimes perform worse than equivalent "
    "SAS configurations.",
    title="MAS high variance in efficiency–effectiveness trade-off",
    metadata={"figure": "artifacts/2604.19299.pdf, Figure 2"},
)

# ── Section 4.3 – Task–Architecture Adaptation ───────────────────────────────

obs_mas_bankruptcy = claim(
    "MAS performs best on bankruptcy prediction across most model scales, though often "
    "with a small leading advantage margin. This suggests that multi-agent coordination "
    "can specifically benefit high-risk financial classification tasks where multiple "
    "specialized perspectives add value despite coordination cost.",
    title="MAS advantage on bankruptcy prediction tasks",
    metadata={"figure": "artifacts/2604.19299.pdf, Figure 3"},
)

obs_sas_reasoning_tasks = claim(
    "SAS performs best for reasoning and generation tasks including question answering, "
    "summarization, and credit risk prediction. For Qwen2.5-0.5B and Llama-2-7B, SAS "
    "achieves over 150% improvement compared to other setups, demonstrating that "
    "single-agent design significantly strengthens mid-sized model performance on "
    "complex tasks.",
    title="SAS >150% improvement on QA and summarization for mid-sized models",
    metadata={"figure": "artifacts/2604.19299.pdf, Figure 3"},
)

obs_base_classification = claim(
    "The Base SLM remains competitive for classification and token-level tasks including "
    "named entity recognition (NER), sentiment analysis, and stock price prediction, "
    "especially in the Gemma and Phi model families. For Gemma-3-270M specifically, "
    "the Base SLM outperforms agent paradigms by a large margin on most tasks because "
    "agent paradigms fail to run correctly on this very small model (270M parameters).",
    title="Base SLM competitive on NER, sentiment, stock prediction",
    metadata={"figure": "artifacts/2604.19299.pdf, Figure 3"},
)

no_universal_winner = claim(
    "No single paradigm (Base, SAS, or MAS) dominates across all financial task "
    "categories and model sizes. The optimal paradigm depends on both the model "
    "family and the task type.",
    title="No universal best paradigm across all task types",
)

# ── Section 4.4 – Failure Mode Analysis ──────────────────────────────────────

obs_agent_more_failures = claim(
    "Agentic systems (SAS and MAS) produce substantially more failed inferences than "
    "the Base SLM. The Base SLM either produces an output or times out, while SAS and "
    "MAS use multi-turn reasoning with tool calls, multiplying sources of system-level "
    "failure (Fig. 4).",
    title="Agent systems produce more failures than Base SLM",
    metadata={"figure": "artifacts/2604.19299.pdf, Figure 4"},
)

obs_sas_failure_modes = claim(
    "In SAS, the dominant failure modes are (1) Context Length Exceeded — long iterative "
    "ReAct prompts exhaust the model's context window — and (2) No Delegation — "
    "the agent fails to produce a valid final answer. These are structural and "
    "budget-related failures arising from the think–act–observe loop.",
    title="SAS failure modes: Context Length Exceeded and No Delegation",
    metadata={"figure": "artifacts/2604.19299.pdf, Figure 4"},
)

obs_mas_failure_modes = claim(
    "In MAS, the dominant failure modes are (1) Delegation Failure — inter-agent "
    "handoffs fail — and (2) No Delegation — the supervisor fails to route the task. "
    "MAS avoids Timeout and Output Protocol Violation errors compared to SAS, but "
    "adds new coordination failure vectors such as infinite delegation loops.",
    title="MAS failure modes: Delegation Failure and No Delegation",
    metadata={"figure": "artifacts/2604.19299.pdf, Figure 4"},
)

# ── Derived conclusions ───────────────────────────────────────────────────────

sas_best_overall_tradeoff = claim(
    "Among the three paradigms evaluated, Single-Agent Systems (SAS) achieve the best "
    "balance between task effectiveness (NRQ = 4.85, Pareto-optimal in efficiency–"
    "effectiveness space) and deployment cost (moderate latency ~23s, lower energy "
    "per token than Base at scale, 79.92% completion rate). SAS is the recommended "
    "default paradigm for resource-constrained SLM financial deployment.",
    title="SAS achieves best overall performance-cost trade-off",
)

mas_limited_gains = claim(
    "Multi-Agent Systems (MAS) add significant coordination overhead (token usage "
    "6.2x Base, latency ~23s, completion rate 72.01%) relative to SAS while delivering "
    "only marginal additional NRQ gains (0.36 vs. SAS's 4.85). MAS is not justified "
    "as a general-purpose deployment paradigm for SLMs.",
    title="MAS yields marginal gains over SAS at high overhead",
)

# ── Reasoning strategies ──────────────────────────────────────────────────────

# Abduction: SAS effectiveness — best explanation of the NRQ evidence
pred_sas_effective = claim(
    "The SAS paradigm, by providing tool access (calculator, wiki/web search) within "
    "a ReAct loop, predicts meaningful NRQ improvement over the Base SLM for financial "
    "tasks requiring external knowledge or multi-step computation.",
    title="SAS paradigm prediction: tool access improves NRQ",
)
alt_sas_ineffective = claim(
    "Alternatively, SLMs may lack sufficient instruction-following capability to use "
    "tools correctly, predicting that SAS provides no reliable NRQ improvement and "
    "only adds latency overhead.",
    title="Alternative: SLMs too limited for effective tool use",
)
s_sas_h = support(
    [pred_sas_effective], obs_sas_nrq,
    reason=(
        "Tool-augmented agents can retrieve external knowledge and perform accurate "
        "calculations, directly compensating for SLM knowledge gaps. The prediction "
        "that @pred_sas_effective correctly leads to @obs_sas_nrq = 4.85."
    ),
    prior=0.85,
)
s_sas_alt = support(
    [alt_sas_ineffective], obs_sas_nrq,
    reason=(
        "If SLMs cannot follow tool-use instructions reliably, tool invocations "
        "produce hallucinated calls, lowering NRQ. The alternative @alt_sas_ineffective "
        "does not predict the observed NRQ of 4.85; it predicts NRQ near 0 or negative."
    ),
    prior=0.2,
)
comp_sas = compare(
    pred_sas_effective, alt_sas_ineffective, obs_sas_nrq,
    reason=(
        "The observed NRQ of 4.85 is consistent with effective tool use "
        "and inconsistent with a prediction of near-zero improvement."
    ),
    prior=0.9,
)
abduction_sas_effectiveness = abduction(
    s_sas_h, s_sas_alt, comp_sas,
    reason=(
        "Both @pred_sas_effective and @alt_sas_ineffective attempt to explain the "
        "same observation @obs_sas_nrq. Abduction selects the better explanation."
    ),
)

# Support chain: SAS best overall trade-off
strat_sas_best_tradeoff = support(
    [obs_sas_nrq, obs_sas_pareto, obs_completion_rates, obs_latency_tokens],
    sas_best_overall_tradeoff,
    reason=(
        "SAS NRQ of 4.85 (@obs_sas_nrq) shows clear effectiveness improvement. "
        "@obs_sas_pareto shows SAS is Pareto-optimal in energy vs. effectiveness. "
        "@obs_completion_rates shows SAS maintains 79.92% completion, substantially "
        "above MAS (72.01%). @obs_latency_tokens shows latency is approximately "
        "doubled vs. Base (23.27s vs. 12.39s), a manageable trade-off for the "
        "significant NRQ gain. Together these metrics jointly support SAS as the "
        "best overall deployment choice."
    ),
    prior=0.87,
    background=[metric_nrq, metric_completion_rate],
)

strat_mas_limited = support(
    [obs_sas_nrq, obs_completion_rates, obs_latency_tokens, obs_energy_per_token],
    mas_limited_gains,
    reason=(
        "MAS NRQ = 0.36 vs. SAS NRQ = 4.85 (@obs_sas_nrq) shows marginal gains "
        "over SAS. @obs_completion_rates shows MAS at 72.01% vs. SAS 79.92% — "
        "lower reliability. @obs_latency_tokens shows MAS consumes 14,618 tokens/sample "
        "vs. SAS 8,040 — 82% more tokens for minimal NRQ gain. Despite lower energy "
        "per token (@obs_energy_per_token), the much higher token count makes MAS "
        "less efficient overall."
    ),
    prior=0.88,
    background=[metric_nrq, metric_completion_rate],
)

strat_no_universal_winner = support(
    [obs_mas_bankruptcy, obs_sas_reasoning_tasks, obs_base_classification],
    no_universal_winner,
    reason=(
        "The heatmap (Fig. 3) shows task-level variation: @obs_mas_bankruptcy shows "
        "MAS wins on bankruptcy prediction. @obs_sas_reasoning_tasks shows SAS wins "
        "on QA and summarization. @obs_base_classification shows Base wins on NER and "
        "sentiment. This cross-task divergence establishes that no single paradigm is "
        "universally optimal."
    ),
    prior=0.92,
    background=[task_scope, model_families],
)

strat_agent_failures = support(
    [obs_sas_failure_modes, obs_mas_failure_modes],
    obs_agent_more_failures,
    reason=(
        "SAS failures are driven by context window exhaustion and no-delegation errors "
        "(@obs_sas_failure_modes). MAS failures are driven by delegation failures and "
        "coordination breakdowns (@obs_mas_failure_modes). Both mechanisms are absent "
        "in the Base SLM, which either succeeds or times out. Therefore agent paradigms "
        "systematically introduce additional failure vectors, explaining the higher "
        "overall failure counts."
    ),
    prior=0.9,
    background=[react_framework],
)

# Contradiction: scaling law vs. agent design finding
scaling_law_predicts_monotone = claim(
    "The scaling law hypothesis [@Kaplan2020] predicts that model task performance "
    "is a monotonically increasing function of parameter count and compute: larger "
    "models within the same SLM range (up to 10B) should consistently outperform "
    "smaller ones.",
    title="Scaling law prediction: monotone performance vs. parameter count",
)

not_both_scaling_and_uturn = contradiction(
    scaling_law_predicts_monotone,
    obs_base_uturn,
    reason=(
        "The scaling law predicts monotone improvement (@scaling_law_predicts_monotone). "
        "The observed U-turn (@obs_base_uturn) shows 8B–10B Base SLMs achieving "
        "$Z_c < -0.5$, worse than smaller models. Both cannot simultaneously hold: "
        "if scaling were monotone, larger Base SLMs should outperform smaller ones, "
        "but the data shows the opposite."
    ),
    prior=0.92,
)
