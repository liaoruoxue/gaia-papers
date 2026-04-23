"""Section 3: Memory Externalization — State Across Time"""

from gaia.lang import claim, setting, support, induction

from .motivation import (
    externalization_thesis,
    representational_transformation_claim,
    cognitive_artifacts_framework,
    kirsh_complementary_strategies,
    llm_baseline_limits,
)

# ── Memory type taxonomy (setting — definitional) ───────────────────────
memory_taxonomy_def = setting(
    "Memory externalization is decomposed into four functional layers, each addressing "
    "a distinct temporal need: (1) **working context** — live task state (open files, "
    "checkpoints, intermediate variables, active hypotheses); (2) **episodic experience** "
    "— records of prior runs (decisions, tool calls, failures, outcomes, reflections); "
    "(3) **semantic knowledge** — domain facts and general heuristics persisting across "
    "episodes; (4) **personalized memory** — user-specific preferences, habits, and "
    "recurring constraints. Each layer obeys distinct retention, retrieval, and "
    "privacy policies.",
    title="Four-layer memory taxonomy",
)

# ── Memory architectural progression (settings) ──────────────────────────
monolithic_context_def = setting(
    "**Monolithic context** architecture: all relevant history or summary is placed "
    "directly in the prompt. Simple and transparent, but unscalable: state disappears "
    "with the session, summaries drift over time, and token capacity is consumed by "
    "history rather than present reasoning.",
    title="Monolithic context architecture",
)

retrieval_storage_def = setting(
    "**Context with retrieval storage** architecture: near-term working state stays "
    "in context while longer-horizon traces are stored externally and retrieved on "
    "demand. Examples include GraphRAG (graph structure and community-level retrieval), "
    "ENGRAM (latent memory compression), and SYNAPSE (spreading activation over "
    "episodic-semantic graphs). Dominant in production copilots and coding agents.",
    title="Context with retrieval storage architecture",
)

hierarchical_memory_def = setting(
    "**Hierarchical memory** architecture: explicit extraction, consolidation, and "
    "forgetting operations manage memory as a lifecycle rather than a passive store. "
    "Two design branches: (a) resource decoupling — MemGPT, MemoryOS separate hot "
    "working state from cold storage with tier-based swapping; (b) semantic decoupling "
    "— MemoryBank, MIRIX, MemOS separate events, profiles, and world-knowledge into "
    "functionally distinct stores.",
    title="Hierarchical memory architecture",
)

adaptive_memory_def = setting(
    "**Adaptive memory** architecture: memory modules evolve and update in response "
    "to feedback during execution. Examples: MemEvolve decomposes into independently "
    "evolving encode/store/retrieve/manage modules; MemVerse maintains short-term "
    "cache and multimodal knowledge graph with periodic distillation; MemRL updates "
    "retrieval through non-parametric reinforcement learning; GAM refines retrieval "
    "over multiple interaction rounds.",
    title="Adaptive memory architecture",
)

# ── Core claims ───────────────────────────────────────────────────────────
memory_recall_recognition = claim(
    "Memory externalization achieves its core benefit by converting an **internal "
    "intractable recall problem** into an **external, bounded recognition-and-retrieval "
    "problem**: the model no longer recovers relevant history from its parameters but "
    "recognizes curated history that the memory system has surfaced. This parallels "
    "Norman's shopping-list example — the power lies not in added information but in "
    "task restructuring [@Zhou2026].",
    title="Memory as recall-to-recognition transformation",
    background=[memory_taxonomy_def, cognitive_artifacts_framework],
)

retrieval_quality_primacy = claim(
    "For memory externalization, retrieval quality matters more than raw storage "
    "capacity: a vast store with weak retrieval still presents the wrong problem "
    "representation to the model (wrong records distract; right records missed mean "
    "effective amnesia), while modest storage with strong indexing and contextual "
    "selection makes downstream reasoning easier. The success criterion is 'Did we "
    "make the current decision legible?' not 'How much can we store?' [@Zhou2026].",
    title="Retrieval quality over raw capacity",
    background=[memory_taxonomy_def],
)

memory_architectural_progression = claim(
    "Memory architecture has followed a four-stage progression — monolithic context → "
    "retrieval storage → hierarchical orchestration → adaptive systems — where each "
    "stage addresses a different failure mode of the preceding one rather than merely "
    "adding capacity. The progression shifts responsibility from the model's parameters "
    "to external infrastructure, and from passive storage to active managed state "
    "[@Zhou2026].",
    title="Four-stage memory architectural progression",
    background=[
        monolithic_context_def,
        retrieval_storage_def,
        hierarchical_memory_def,
        adaptive_memory_def,
    ],
)

memory_as_managed_infrastructure = claim(
    "In mature multi-agent systems, memory is not isolated storage but managed state "
    "infrastructure requiring operating-system-level controls: read/write permissions, "
    "conflict resolution, and access quotas across concurrent agents. InfiAgent's "
    "file-centric abstraction treats the file system as the authoritative record where "
    "all state — planning through tool outputs — is written in real time, with agents "
    "reading curated workspace snapshots rather than lengthy history [@Zhou2026].",
    title="Memory as managed state infrastructure in multi-agent systems",
    background=[adaptive_memory_def],
)

episodic_to_skill_boundary = claim(
    "There is a functional boundary between memory and skills: repeated procedural "
    "regularities that first appear in episodic traces cease to be 'memory proper' "
    "once promoted to explicit reusable guidance — at that point they belong to the "
    "skill layer. Memory and skills are therefore not independent silos but dynamically "
    "coupled: the memory layer produces the raw material (experience traces) from which "
    "skills are distilled [@Zhou2026].",
    title="Episodic experience to skill promotion boundary",
    background=[memory_taxonomy_def],
)

memory_failure_modes = claim(
    "Memory externalization failures are fundamentally representational-design failures "
    "rather than implementation bugs: (a) **stale memories** misrepresent the present "
    "state to the model; (b) **over-abstraction** loses operational details needed for "
    "task execution; (c) **under-abstraction** floods context with noise that degrades "
    "model reasoning; (d) **poisoned memories** contaminate future reasoning chains "
    "[@Zhou2026].",
    title="Memory externalization failure modes",
    background=[memory_taxonomy_def],
)

# ── Reasoning strategies ──────────────────────────────────────────────────
strat_recall_recognition = support(
    [externalization_thesis],
    memory_recall_recognition,
    reason=(
        "The recall-to-recognition claim (@memory_recall_recognition) follows from "
        "applying @externalization_thesis to the memory domain: externalization "
        "relocates the recall burden (recovering history from parameters) into external "
        "stores, converting it into recognition (identifying retrieved content). "
        "Norman's cognitive-artifact theory (in @cognitive_artifacts_framework) "
        "explains why this restructuring — not just added capacity — is the source "
        "of benefit."
    ),
    prior=0.88,
    background=[memory_taxonomy_def, cognitive_artifacts_framework],
)

strat_retrieval_quality = support(
    [memory_recall_recognition],
    retrieval_quality_primacy,
    reason=(
        "The retrieval-quality primacy claim (@retrieval_quality_primacy) follows "
        "from the recall-to-recognition mechanism (@memory_recall_recognition): if "
        "the benefit of externalization is task restructuring rather than storage "
        "capacity, then the quality of what is surfaced (retrieval accuracy) determines "
        "whether the restructuring succeeds. Systems like GraphRAG, ENGRAM, and SYNAPSE "
        "(described in @retrieval_storage_def) improve retrieval quality as their core "
        "design objective, consistent with this claim."
    ),
    prior=0.85,
    background=[retrieval_storage_def],
)

strat_progression = support(
    [memory_recall_recognition, memory_failure_modes],
    memory_architectural_progression,
    reason=(
        "The four-stage progression claim (@memory_architectural_progression) follows "
        "from reading the architectural stages as a failure-mode chain: monolithic "
        "context fails at scale; retrieval storage solves scale but exposes retrieval "
        "quality as the binding constraint (@retrieval_quality_primacy); hierarchical "
        "orchestration adds lifecycle management beyond retrieval; adaptive systems "
        "add runtime policy optimization. The failure modes in @memory_failure_modes "
        "(stale, over-abstracted, under-abstracted, poisoned) drive each transition."
    ),
    prior=0.85,
    background=[
        monolithic_context_def,
        retrieval_storage_def,
        hierarchical_memory_def,
        adaptive_memory_def,
    ],
)

strat_managed_infrastructure = support(
    [memory_architectural_progression],
    memory_as_managed_infrastructure,
    reason=(
        "The managed-infrastructure claim (@memory_as_managed_infrastructure) is "
        "the endpoint of the architectural progression (@memory_architectural_progression): "
        "adaptive systems that dynamically evolve retrieval policy in multi-agent "
        "settings require access controls and conflict resolution — operating-system-level "
        "capabilities. InfiAgent's file-centric approach is the most explicit "
        "instantiation of treating memory as authoritative managed state."
    ),
    prior=0.82,
    background=[adaptive_memory_def],
)

strat_episodic_boundary = support(
    [externalization_thesis],
    episodic_to_skill_boundary,
    reason=(
        "The episodic-to-skill boundary (@episodic_to_skill_boundary) follows from "
        "@externalization_thesis applied to the two distinct cognitive burdens of "
        "state (memory) and procedure (skills): the taxonomy in @memory_taxonomy_def "
        "defines episodic records as 'records of prior runs' while skills are defined "
        "as 'reusable capability packages.' The promotion of regularized episodic traces "
        "to explicit reusable procedures is the coupling mechanism between the two "
        "externalization dimensions."
    ),
    prior=0.8,
    background=[memory_taxonomy_def],
)

# ── Induction: retrieval architectures confirm retrieval-quality primacy ─
graphrag_claim = claim(
    "GraphRAG adds graph structure and community-level retrieval to standard RAG, "
    "improving retrieval quality by enabling non-local relevance recovery across "
    "document communities rather than relying on nearest-neighbor embedding search alone.",
    title="GraphRAG improves retrieval quality",
)

synapse_claim = claim(
    "SYNAPSE uses spreading activation over episodic-semantic graphs to recover "
    "less-locally relevant memories, addressing the limitation of embedding-only "
    "retrieval systems that miss non-adjacent relevant records.",
    title="SYNAPSE spreading activation improves retrieval",
)

s_graphrag = support(
    [retrieval_quality_primacy],
    graphrag_claim,
    reason=(
        "GraphRAG is a direct implementation of @retrieval_quality_primacy: it improves "
        "retrieval quality (graph structure, community-level aggregation) rather than "
        "increasing storage capacity, consistent with the primacy of retrieval quality."
    ),
    prior=0.85,
)

s_synapse = support(
    [retrieval_quality_primacy],
    synapse_claim,
    reason=(
        "SYNAPSE is another direct instantiation of @retrieval_quality_primacy: "
        "spreading activation addresses retrieval quality (recovering non-local relevant "
        "records) rather than expanding storage capacity."
    ),
    prior=0.85,
)

ind_retrieval_quality = induction(
    s_graphrag,
    s_synapse,
    law=retrieval_quality_primacy,
    reason=(
        "GraphRAG and SYNAPSE are independent architectural innovations both motivated "
        "by improving retrieval quality rather than storage capacity, inductively "
        "supporting the retrieval-quality primacy law."
    ),
)
