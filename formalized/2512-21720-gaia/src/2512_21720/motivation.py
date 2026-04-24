"""Introduction: Information-Theoretic Perspective on Agentic System Design"""

from gaia.lang import claim, setting, question, support, complement, contradiction

# ── Background / Settings ──────────────────────────────────────────────────────

agentic_lm_systems = setting(
    "Agentic language model (LM) systems — such as Deep Research and Claude Code — power modern AI "
    "workflows. These systems commonly leverage multi-LM architectures to overcome context window "
    "limitations, coordinating multiple models to manage reasoning and memory.",
    title="Agentic LM systems background",
)

compressor_predictor_pattern = setting(
    "A recurring pattern in multi-LM agentic systems is the compressor-predictor architecture: "
    "a smaller 'compressor' LM distills a raw, long context X into a compact text summary Z, "
    "which a larger 'predictor' LM then consumes to produce a final answer Y. "
    "The compressor can run locally on-device; the predictor may run in the cloud.",
    title="Compressor-predictor architectural pattern",
)

context_rot_def = setting(
    "Context rot refers to the empirical failure mode where LLM performance degrades as the number "
    "of input tokens increases beyond effective context capacity, causing models to miss or misweight "
    "relevant information in long contexts.",
    title="Context rot definition",
)

noisy_channel_framing = setting(
    "In information theory, a noisy channel model describes a communication system where a sender "
    "encodes a source X into a transmitted signal Z, which a receiver decodes to recover Y. "
    "Channel capacity and mutual information I(X; Z) quantify how much information the channel "
    "preserves about the original source.",
    title="Noisy channel information-theoretic framing",
)

# ── Research Questions ─────────────────────────────────────────────────────────

rq_compressor_vs_predictor = question(
    "Should practitioners scale the compressor LM or the predictor LM to most improve downstream "
    "performance in a compressor-predictor agentic system?",
    title="RQ1: Compressor vs predictor scaling",
)

rq_mi_proxy = question(
    "Can mutual information I(X; Z | Q) between the raw context X and its compression Z "
    "(conditioned on query Q) serve as a task-independent proxy for compression quality and "
    "downstream performance?",
    title="RQ2: Mutual information as task-agnostic proxy",
)

rq_deep_research = question(
    "Can small local compressor LMs (3B parameters) substitute for frontier-LM compressors in "
    "Deep Research pipelines while recovering nearly all of the accuracy at reduced API cost?",
    title="RQ3: Local compressors in Deep Research",
)

# ── Core Claims (Introduction) ─────────────────────────────────────────────────

design_adhoc = claim(
    "The design of compressor-predictor agentic systems is currently largely ad hoc: there is no "
    "principled way to evaluate compressor quality independently of the downstream task, and "
    "attributing gains to the compressor versus predictor requires costly, task-specific pairwise sweeps.",
    title="Current agentic system design is ad hoc",
    metadata={"source_section": "Introduction"},
)

mi_as_proxy_proposal = claim(
    "Mutual information I(X; Z | Q) between the raw context X and its compression Z, conditioned "
    "on query Q, is a task-agnostic proxy for compression quality — analogous to how perplexity "
    "serves as a task-agnostic proxy for downstream LM performance.",
    title="MI as task-agnostic compression quality proxy",
    metadata={"source_section": "Introduction, Abstract"},
)

compressor_scaling_dominates = claim(
    "Scaling the compressor LM yields substantially more performance gain per unit of compute than "
    "scaling the predictor LM. A 7B Qwen-2.5 compressor is 1.6x more accurate, 4.6x more concise, "
    "and conveys 5.5x more bits of mutual information per token than its 1.5B counterpart.",
    title="Compressor scaling dominates predictor scaling",
    metadata={"source_section": "Abstract, Section 3.1"},
)

deep_research_cost_reduction = claim(
    "In a Deep Research pipeline, local compressors as small as 3B parameters can recover 99% of "
    "frontier-LM accuracy (GPT-4o baseline) while reducing API costs to 26% of the uncompressed "
    "baseline (a 74% cost reduction).",
    title="Local compressors achieve near-frontier accuracy at 26% API cost",
    metadata={"source_section": "Abstract, Section 3.5"},
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_adhoc_motivates_mi = support(
    [design_adhoc],
    mi_as_proxy_proposal,
    reason=(
        "Because there is no task-agnostic way to evaluate compressor quality "
        "(@design_adhoc), the authors are motivated to adopt an information-theoretic "
        "framing: viewing the compressor as a noisy channel (@noisy_channel_framing), "
        "mutual information I(X; Z | Q) naturally captures how much of the original "
        "context is preserved in the compression — without requiring a downstream task."
    ),
    prior=0.80,
)

__all__ = [
    "agentic_lm_systems",
    "compressor_predictor_pattern",
    "context_rot_def",
    "noisy_channel_framing",
    "rq_compressor_vs_predictor",
    "rq_mi_proxy",
    "rq_deep_research",
    "design_adhoc",
    "mi_as_proxy_proposal",
    "compressor_scaling_dominates",
    "deep_research_cost_reduction",
]
