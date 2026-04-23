"""Section 4: Skills Externalization — Procedural Expertise"""

from gaia.lang import claim, setting, support, induction

from .motivation import (
    externalization_thesis,
    llm_baseline_limits,
    representational_transformation_claim,
)
from .s3_memory import episodic_to_skill_boundary

# ── Definitional settings ─────────────────────────────────────────────────
skill_content_def = setting(
    "Externalized skills package three categories of procedural knowledge: "
    "(1) **operational procedures** — step-by-step workflows and execution sequences; "
    "(2) **decision heuristics** — guidance for choosing among options given context; "
    "(3) **normative constraints** — rules, safety boundaries, and audit requirements "
    "governing execution. Together these constitute the 'procedural expertise' that "
    "previously had to be improvised from model weights at each invocation.",
    title="Skill content categories",
)

skill_lifecycle_def = setting(
    "Skills are managed through a five-stage lifecycle: (1) **specification** — formal "
    "description of the skill's interface, parameters, and semantics; (2) **discovery** "
    "— finding appropriate skills given a task description (routing, embedding-based "
    "search); (3) **progressive disclosure** — revealing skill detail incrementally as "
    "the agent needs it; (4) **execution binding** — linking the skill to a runtime "
    "system that can execute it; (5) **composition** — combining multiple skills into "
    "larger workflows.",
    title="Skill lifecycle: specify-discover-disclose-bind-compose",
)

skill_acquisition_def = setting(
    "Skills can be acquired through four modes: (1) **authored** — human-written "
    "procedures; (2) **distilled** — extracted automatically from execution traces "
    "and episodic records; (3) **discovered** — learned from agent-environment "
    "interaction; (4) **composed** — assembled from combinations of existing skills. "
    "The distillation pathway is the primary coupling point between the memory layer "
    "and the skill layer.",
    title="Skill acquisition modes",
)

skill_evolution_def = setting(
    "Skill externalization evolved through three stages: (1) **atomic execution "
    "primitives** — individual function calls and API bindings, the foundational "
    "tool-use capability; (2) **large-scale primitive selection** — managing hundreds "
    "or thousands of tools through embedding-based discovery and routing (the challenge "
    "of function-calling at scale); (3) **packaged expertise** — full capability "
    "bundles bundling specification, discovery, disclosure, execution, and composition "
    "mechanisms into reusable skill packages.",
    title="Three-stage skill evolution",
)

# ── Core claims ───────────────────────────────────────────────────────────
generation_to_composition = claim(
    "Skills externalize procedural expertise by converting **improvised generation** "
    "into **validated composition**: agents assemble behavior from pre-validated "
    "reusable components rather than deriving procedures anew from model weights at "
    "each invocation. This addresses the variance problem — repeated tasks execute "
    "consistently rather than producing different (sometimes wrong) results each time "
    "[@Zhou2026].",
    title="Skills transform generation into composition",
    background=[skill_content_def, llm_baseline_limits],
)

skill_boundary_conditions = claim(
    "Skill externalization faces four key boundary conditions that limit reusability: "
    "(1) **semantic alignment** — skill specifications must match actual usage patterns "
    "or discovery fails; (2) **portability and staleness** — skills authored for one "
    "agent or context may not transfer to different agents or updated environments; "
    "(3) **unsafe composition** — combinations of individually safe skills may produce "
    "unsafe behavior; (4) **context-dependent degradation** — skill performance may "
    "drop in unfamiliar settings even when the skill is well-specified [@Zhou2026].",
    title="Skill boundary conditions",
    background=[skill_lifecycle_def, skill_acquisition_def],
)

skill_scale_challenge = claim(
    "The transition from atomic tool use to large-scale primitive selection introduces "
    "a qualitatively new challenge: with hundreds or thousands of tools available, "
    "the agent must solve a **discovery and routing problem** before it can execute "
    "any skill. Embedding-based skill search and hierarchical capability trees become "
    "necessary infrastructure rather than optional additions [@Zhou2026].",
    title="Skill discovery challenge at scale",
    background=[skill_evolution_def],
)

skill_distillation_coupling = claim(
    "The **distillation** acquisition mode creates the primary dynamic coupling between "
    "memory and skills: execution traces stored in episodic memory are periodically "
    "extracted and promoted into explicit reusable skill specifications. This means "
    "skill libraries improve as agents accumulate experience — the skill layer is not "
    "static but co-evolves with the episodic memory layer [@Zhou2026].",
    title="Skill distillation from episodic memory",
    background=[skill_acquisition_def],
)

packaged_expertise_claim = claim(
    "The highest stage of skill evolution — packaged expertise — represents a shift "
    "from individual tool calls to complete capability bundles that include specification, "
    "discovery, progressive disclosure, execution binding, and composition mechanisms "
    "as first-class features. Systems like Voyager (Minecraft skill library) exemplify "
    "this pattern: skills are not just callable functions but self-describing, "
    "discoverable, composable capability artifacts [@Zhou2026].",
    title="Packaged expertise as the mature skill form",
    background=[skill_evolution_def, skill_lifecycle_def],
)

# ── Reasoning strategies ──────────────────────────────────────────────────
strat_gen_to_comp = support(
    [externalization_thesis],
    generation_to_composition,
    reason=(
        "The generation-to-composition transformation (@generation_to_composition) is "
        "the skill-layer instance of the general externalization mechanism in "
        "@externalization_thesis: procedural expertise (operational procedures, decision "
        "heuristics, normative constraints defined in @skill_content_def) is relocated "
        "from weight-space improvisation to external validated artifacts. The variance "
        "problem — procedures rederived inconsistently — is addressed by composition "
        "from stable pre-validated components."
    ),
    prior=0.88,
    background=[skill_content_def, llm_baseline_limits],
)

strat_boundary_conditions = support(
    [generation_to_composition],
    skill_boundary_conditions,
    reason=(
        "The four boundary conditions (@skill_boundary_conditions) follow from "
        "examining the skill lifecycle and acquisition modes for failure points: "
        "specification failures → semantic misalignment; distillation/portability "
        "failures → staleness; composition stage failures → unsafe combinations; "
        "execution binding in new contexts → context-dependent degradation. These "
        "are the natural failure modes of the generation-to-composition transformation "
        "(@generation_to_composition)."
    ),
    prior=0.82,
    background=[skill_lifecycle_def, skill_acquisition_def],
)

strat_scale_challenge = support(
    [generation_to_composition],
    skill_scale_challenge,
    reason=(
        "The scale challenge (@skill_scale_challenge) follows from the second stage "
        "of skill evolution (large-scale primitive selection, described in "
        "@skill_evolution_def) combined with the discovery stage of the lifecycle "
        "(defined in @skill_lifecycle_def): when the number of available tools grows "
        "from single digits to thousands, skill discovery becomes a combinatorially "
        "hard retrieval problem requiring dedicated infrastructure — it cannot "
        "be solved by enumeration in a prompt."
    ),
    prior=0.85,
    background=[skill_evolution_def, skill_lifecycle_def],
)

strat_distillation_coupling = support(
    [episodic_to_skill_boundary],
    skill_distillation_coupling,
    reason=(
        "The distillation coupling claim (@skill_distillation_coupling) follows "
        "directly from @episodic_to_skill_boundary: the episodic-to-skill promotion "
        "process is the mechanism by which distillation happens — episodic memory "
        "records are the raw material, and skills are the distilled output. The "
        "skill acquisition modes (described in @skill_acquisition_def) confirm "
        "distillation as the primary coupling pathway."
    ),
    prior=0.85,
    background=[skill_acquisition_def],
)

strat_packaged_expertise = support(
    [generation_to_composition, skill_distillation_coupling],
    packaged_expertise_claim,
    reason=(
        "Packaged expertise (@packaged_expertise_claim) is the convergence of the "
        "third stage in the skill evolution (full capability bundles, described in "
        "@skill_evolution_def) with all five stages of the lifecycle (defined in "
        "@skill_lifecycle_def). Voyager exemplifies this: skills are self-describing, "
        "discoverable, composable artifacts produced by distillation "
        "(@skill_distillation_coupling) from Minecraft gameplay trajectories. "
        "The generation-to-composition transformation (@generation_to_composition) "
        "is scaled from atomic tools to full multi-step capability bundles."
    ),
    prior=0.82,
    background=[skill_evolution_def, skill_lifecycle_def],
)

# ── Induction: scale and distillation confirm generation-to-composition ──
atomic_tool_claim = claim(
    "Atomic tool use (individual API function calls) is the foundational form of "
    "skill externalization: a single validated function replaces ad-hoc code "
    "generation by the model, producing consistent and reliable execution for "
    "that atomic operation.",
    title="Atomic tool use confirms generation-to-composition",
)

packaged_scale_claim = claim(
    "Packaged expertise systems such as Voyager demonstrate that the "
    "generation-to-composition transformation scales to complex multi-step tasks: "
    "agents compose entire capability bundles from pre-validated skill packages "
    "rather than generating multi-step procedures from scratch.",
    title="Packaged expertise confirms generation-to-composition at scale",
)

s_atomic = support(
    [generation_to_composition],
    atomic_tool_claim,
    reason=(
        "@generation_to_composition predicts that skill externalization converts "
        "improvised generation into composition — confirmed at the atomic level by "
        "function calling, where a standardized API replaces per-invocation code generation."
    ),
    prior=0.90,
)

s_packaged = support(
    [generation_to_composition],
    packaged_scale_claim,
    reason=(
        "@generation_to_composition predicts the transformation applies beyond atomic "
        "tools to full skill packages — confirmed by Voyager-style packaged expertise "
        "systems where complex game tasks are executed by composing validated skills."
    ),
    prior=0.85,
)

ind_gen_to_comp = induction(
    s_atomic,
    s_packaged,
    law=generation_to_composition,
    reason=(
        "Atomic tool use and packaged expertise are independent confirmations of the "
        "generation-to-composition law at different scales — atomic (single function) "
        "and complex (multi-step capability bundles) — inductively supporting the law."
    ),
)
