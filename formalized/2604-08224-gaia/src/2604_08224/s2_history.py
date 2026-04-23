"""Section 2: Historical Progression — Weights, Context, and Harness Eras"""

from gaia.lang import claim, setting, support, induction

from .motivation import (
    externalization_thesis,
    representational_transformation_claim,
    llm_baseline_limits,
    cognitive_artifacts_framework,
)

# ── Era definitions (settings — these are definitional stages) ────────────
weights_era_def = setting(
    "The **weights era** (pre-2022) treated LLM capability as entirely parametric. "
    "Progress was achieved by scaling model size (parameters, training compute, data). "
    "Agent-like behaviors — reasoning, tool use, memory — were embedded implicitly in "
    "the parameter distribution rather than in explicit external structures.",
    title="Weights era definition",
)

context_era_def = setting(
    "The **context era** (approximately 2022–2024) shifted focus to input design: "
    "few-shot prompting, chain-of-thought (CoT), ReAct, and retrieval-augmented "
    "generation (RAG) demonstrated that behavior could change dramatically without "
    "modifying weights. Capability moved from parameters into prompts and retrieval "
    "systems.",
    title="Context era definition",
)

harness_era_def = setting(
    "The **harness era** (2024 and onwards) embeds models inside persistent "
    "infrastructure: memory stores, skill registries, protocol definitions, "
    "sandboxes, sub-agent orchestrators, compression pipelines, and approval loops. "
    "Early exemplars — AutoGPT, BabyAGI — wrapped LLMs in simple loops. Modern "
    "frameworks — AutoGen, MetaGPT, CAMEL, Reflexion — formalized multi-agent "
    "collaboration and persistent feedback as first-class concerns.",
    title="Harness era definition",
)

# ── Claims about each era's limitations ──────────────────────────────────
weights_era_limits = claim(
    "The weights era faced three irreducible limitations that motivated the shift "
    "toward the context era: (1) **updating** — changing a single fact requires "
    "retraining the full model; (2) **auditability** — knowledge distributed across "
    "billions of parameters is opaque and cannot be directly inspected; (3) "
    "**personalization** — a single weight configuration cannot simultaneously "
    "encode the distinct histories and preferences of millions of users [@Zhou2026].",
    title="Weights era limitations",
    background=[weights_era_def],
)

context_era_limits = claim(
    "The context era introduced its own irreducible constraints: (1) **finite context** "
    "— context windows are bounded and costly, and the 'lost in the middle' phenomenon "
    "shows degraded model attention for centrally-placed information in long contexts; "
    "(2) **ephemeral state** — all in-context history disappears between sessions; "
    "(3) **workflow complexity** — multi-step workflows cannot be managed through "
    "prompting alone, especially when tasks require persistent state or concurrent "
    "sub-tasks [@Zhou2026].",
    title="Context era limitations",
    background=[context_era_def],
)

# ── Historical progression as an observed pattern ────────────────────────
historical_arc_claim = claim(
    "The field of LLM-based agents has followed an observable three-stage progression: "
    "**Weights → Context → Harness**. Each stage addressed the failure modes of the "
    "preceding one through representational shift: weights failures motivated context-era "
    "retrieval and prompting; context failures motivated harness-era persistent "
    "infrastructure. The progression is not mere feature addition but a qualitative "
    "change in where capability resides [@Zhou2026].",
    title="Weights-Context-Harness historical arc",
    background=[weights_era_def, context_era_def, harness_era_def],
)

# ── Recall-to-recognition as the key context-era mechanism ───────────────
recall_to_recognition = claim(
    "The context era's key epistemic mechanism is a **recall-to-recognition "
    "transformation**: rather than the model memorizing facts internally, retrieval "
    "systems place relevant documents in context, and the model recognizes their "
    "application. RAG implements this transformation — external storage converts "
    "hard recall (reproduce fact from weights) into easier recognition (identify "
    "relevant passage placed in context) [@Zhou2026].",
    title="Recall-to-recognition transformation",
    background=[context_era_def, cognitive_artifacts_framework],
)

# ── Design-question shift ──────────────────────────────────────────────────
design_question_shift = claim(
    "The harness era represents a fundamental reframing of the agent design question: "
    "from 'What should we tell the model?' (the context-era question of prompt and "
    "retrieval engineering) to 'What environment should the model operate in?' "
    "(the harness-era question of infrastructure, memory, skills, and protocol "
    "design). This reframing implies that capability is distributed across weights, "
    "context, memory, skills, protocols, and orchestration logic — not concentrated "
    "in any single component [@Zhou2026].",
    title="Design question shift: prompt → environment",
)

# ── Reasoning strategies ──────────────────────────────────────────────────
strat_arc_from_limits = support(
    [weights_era_limits, context_era_limits, externalization_thesis],
    historical_arc_claim,
    reason=(
        "The historical arc (@historical_arc_claim) follows from the failure-mode "
        "structure: @weights_era_limits — updating, auditability, personalization — "
        "motivate the context era's retrieval and prompting solutions. "
        "@context_era_limits — finite windows, ephemeral state, workflow complexity — "
        "motivate the harness era's persistent infrastructure. "
        "@externalization_thesis supplies the unifying logic: each transition "
        "relocates cognitive burden into a more external, inspectable form."
    ),
    prior=0.88,
)

strat_recall_recognition = support(
    [historical_arc_claim],
    recall_to_recognition,
    reason=(
        "The recall-to-recognition transformation (@recall_to_recognition) is an "
        "instance of Norman's cognitive-artifact principle (see @cognitive_artifacts_framework): "
        "RAG converts an internal recall operation (retrieve fact from weights) into "
        "an external recognition operation (identify relevant retrieved passage). "
        "The context era, which @historical_arc_claim confirms as the second stage, "
        "is defined by exactly this RAG-style transformation."
    ),
    prior=0.85,
    background=[context_era_def, cognitive_artifacts_framework],
)

strat_design_shift = support(
    [historical_arc_claim, representational_transformation_claim],
    design_question_shift,
    reason=(
        "The design-question shift (@design_question_shift) follows from the historical "
        "arc (@historical_arc_claim): once capability moves from weights into infrastructure, "
        "the design locus shifts from model internals to the surrounding environment. "
        "@representational_transformation_claim provides the theoretical grounding: "
        "externalization changes the problem structure, not just the implementation."
    ),
    prior=0.85,
)

# ── Induction over eras ───────────────────────────────────────────────────
era_progression_law = claim(
    "Each successive capability era for LLM agents is characterized by relocating "
    "cognitive burdens further from model weights into explicit, inspectable, and "
    "updatable external structures — a monotonic externalization trend across the "
    "history of the field.",
    title="Monotonic externalization law across eras",
)

s_weights_supports_law = support(
    [era_progression_law],
    weights_era_limits,
    reason=(
        "The law (@era_progression_law) predicts that the weights era would be limited "
        "by its failure to externalize — which @weights_era_limits confirms: updating, "
        "auditability, and personalization problems all stem from keeping capability "
        "parametric. Confirmation of the prediction flows back to support the law."
    ),
    prior=0.85,
)

s_context_supports_law = support(
    [era_progression_law],
    context_era_limits,
    reason=(
        "The law (@era_progression_law) predicts that the context era would advance "
        "externalization but face new limits at its boundary — which @context_era_limits "
        "confirms: finite windows, ephemeral state, and workflow complexity are exactly "
        "the limits of prompt-level externalization without persistent infrastructure."
    ),
    prior=0.85,
)

ind_era_law = induction(
    s_weights_supports_law,
    s_context_supports_law,
    law=era_progression_law,
    reason=(
        "Two independent eras confirm the externalization law: the weights era's "
        "limitations and the context era's limitations both follow from insufficient "
        "externalization, supporting the monotonic externalization trend."
    ),
)
