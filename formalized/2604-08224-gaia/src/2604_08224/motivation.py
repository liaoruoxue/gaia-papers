"""Introduction and Motivation: Externalization as the Engine of LLM Agent Progress"""

from gaia.lang import claim, setting, question, support, deduction

# ── Foundational settings ──────────────────────────────────────────────────
cognitive_artifacts_framework = setting(
    "Norman's cognitive-artifact theory (1991, 1993) holds that external aids "
    "do not merely amplify fixed internal capability — they transform the structure "
    "of the task itself. A shopping list does not extend memory capacity; it converts "
    "an unbounded recall problem into a bounded recognition problem. The power lies in "
    "representational transformation, not additive storage.",
    title="Norman's cognitive-artifact theory",
)

kirsh_complementary_strategies = setting(
    "Kirsh's 'complementary strategies' (1994) describe how agents improve performance "
    "by reorganizing the external environment so that cognitive work offloads into it. "
    "Each side — agent and environment — handles what it does best. This provides the "
    "theoretical basis for externalization as a design principle in AI systems.",
    title="Kirsh complementary strategies",
)

llm_baseline_limits = setting(
    "Large language model (LLM) base systems face three structural limitations that "
    "motivation the externalization agenda: (1) the continuity problem — context windows "
    "are ephemeral and session state is lost between interactions; (2) the variance problem "
    "— procedures are improvised anew each time rather than executed from a validated "
    "template; (3) the coordination problem — tool and agent interactions rely on fragile "
    "ad-hoc prompting rather than governed contracts.",
    title="Structural limitations of base LLM systems",
)

# ── Core thesis ────────────────────────────────────────────────────────────
externalization_thesis = claim(
    "LLM agent progress increasingly depends on **externalization** — the progressive "
    "relocation of cognitive burdens from model parameters into persistent, inspectable, "
    "and reusable external structures. Agent infrastructure matters not merely because "
    "it adds auxiliary components, but because it transforms hard cognitive burdens into "
    "forms that the model can solve more reliably [@Zhou2026].",
    title="Externalization thesis",
    background=[cognitive_artifacts_framework],
)

three_externalization_dimensions = claim(
    "LLM agent infrastructure is organized around three complementary externalization "
    "dimensions: (1) **memory** externalizes state across time, converting ephemeral "
    "in-context recall into persistent recognition-and-retrieval; (2) **skills** "
    "externalize procedural expertise, converting improvised generation into validated "
    "composition; (3) **protocols** externalize interaction structure, converting "
    "ad-hoc coordination into governed, machine-readable contracts. A fourth element, "
    "the **harness**, coordinates all three at runtime but is not itself a fourth "
    "kind of externalization [@Zhou2026].",
    title="Three externalization dimensions",
    background=[llm_baseline_limits],
)

representational_transformation_claim = claim(
    "Externalization achieves its benefit through representational transformation rather "
    "than additive storage. The three dimensions — memory, skills, protocols — each convert "
    "a computationally hard problem (unbounded recall, improvised generation, ad-hoc "
    "coordination) into a computationally easier one (bounded retrieval, modular "
    "composition, governed exchange). The model's weights remain unchanged; the problem "
    "it must solve becomes easier [@Zhou2026].",
    title="Externalization as representational transformation",
    background=[cognitive_artifacts_framework, kirsh_complementary_strategies],
)

# ── Motivating example ──────────────────────────────────────────────────────
software_engineering_example = claim(
    "In a mature software-engineering agent, rather than embedding repository knowledge, "
    "coding conventions, and workflow procedures entirely in prompts or model weights, the "
    "system distributes these across: persistent memory stores (episodic traces, project "
    "conventions), skill documents (validated coding procedures, test templates), "
    "protocolized tool interfaces (standardized API schemas), and control logic "
    "(harness orchestration). The model weights are unchanged; the representational "
    "problem it must solve has been simplified [@Zhou2026].",
    title="Motivating software-engineering agent example",
    background=[llm_baseline_limits],
)

# ── Research question ────────────────────────────────────────────────────────
q_unification = question(
    "What is the unifying principle governing the diverse architectural choices in modern "
    "LLM agents, and how do memory, skills, and protocols relate to each other and to "
    "model scaling?",
)

# ── Supporting reasoning ─────────────────────────────────────────────────────
strat_thesis_from_problem = support(
    [externalization_thesis, software_engineering_example],
    representational_transformation_claim,
    reason=(
        "The externalization thesis (@externalization_thesis) identifies the mechanism "
        "— cognitive burden relocation — while the software engineering example "
        "(@software_engineering_example) instantiates it concretely. Together they "
        "support the representational-transformation claim: the benefit of externalization "
        "is not additive capacity but task restructuring, consistent with "
        "@cognitive_artifacts_framework."
    ),
    prior=0.85,
)

strat_dimensions_from_limits = support(
    [externalization_thesis],
    three_externalization_dimensions,
    reason=(
        "The three structural limitations described in @llm_baseline_limits — continuity, "
        "variance, coordination — map one-to-one onto the three externalization dimensions "
        "in @three_externalization_dimensions. Memory addresses continuity, skills address "
        "variance, protocols address coordination. @externalization_thesis provides the "
        "unifying logic that each limitation motivates a corresponding externalization "
        "dimension. This structural correspondence supports the tri-partite decomposition claim."
    ),
    prior=0.9,
    background=[llm_baseline_limits],
)
