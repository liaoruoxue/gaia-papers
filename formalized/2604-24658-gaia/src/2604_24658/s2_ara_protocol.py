"""Section 2: The ARA Protocol -- four-layer design philosophy and architecture.

Defines the Agent-Native Research Artifact (ARA) as a file-system
ontology that transforms research from a narrative document into a
machine-executable knowledge package. The protocol is grounded in a
single principle (*Knowledge over Narrative*) and materializes four
agent-relevant questions (why? how? what was tried? what are the
numbers?) as four independent file-system layers with cross-layer
forensic bindings.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Design philosophy (§2.1)
# ---------------------------------------------------------------------------

setup_design_principle_knowledge_over_narrative = setting(
    "**Design principle: Knowledge over Narrative.** The ARA protocol is "
    "grounded in a single principle: the organized, evolving knowledge "
    "produced during research is the **primary scientific object**; the "
    "narrative paper is a **compiled view** of that object, generated "
    "on demand for human readers. This inverts the prevailing assumption "
    "that the paper *is* the artifact and the underlying research "
    "process is a private byproduct.",
    title="Setup: 'Knowledge over Narrative' principle",
)

claim_four_question_decomposition = claim(
    "**Four structurally distinct questions an agent asks of a research "
    "project.** An agent engaging with research asks four "
    "structurally-distinct questions, each with incompatible structural "
    "needs:\n\n"
    "| Question | Structural need | Conflicts with |\n"
    "|---|---|---|\n"
    "| **Why** does this work (scientific reasoning) | stable, citable units | code's continuous iteration |\n"
    "| **How** is it implemented (executable code) | continuously-evolving source | reasoning's stability |\n"
    "| **What was tried** along the way (exploration) | inherently branching | narrative's linearity |\n"
    "| **What are the numbers** (raw evidence) | machine-precise values | prose rounding/paraphrase |\n\n"
    "A narrative paper forces all four answers from the same linear "
    "prose, but the structural needs *conflict*. Compressing them into "
    "one document is not merely suboptimal but **lossy**: once flattened "
    "into narrative, the original structure cannot be recovered.",
    title="Four agent-relevant questions with mutually-conflicting structural needs",
)

claim_progressive_disclosure = claim(
    "**Progressive disclosure: agents load only the layers a task "
    "requires.** Because agent context windows are a shared, finite "
    "resource, the four-layer file-system structure further supports "
    "*progressive disclosure*: an agent reads PAPER.md (~500 tokens) "
    "first to triage relevance, then loads only the layers and files "
    "relevant to its current task, avoiding context pollution from "
    "irrelevant material. The architecture's layer index turns linear "
    "document scanning into *targeted file lookup*.",
    title="Progressive disclosure: layered structure enables partial loads",
)

claim_factual_density_requirement = claim(
    "**Factual-density requirement.** Within each ARA layer, artifact "
    "text *maximizes information per token*: subjective qualifiers, "
    "hedges, and narrative connectives are stripped, and statements "
    "requiring judgment carry **provenance** rather than rhetoric. This "
    "is enforced uniformly across the four layers (the §3 Live Research "
    "Manager applies it to the captured-event payloads; the §4 ARA "
    "Compiler applies it to legacy-source extraction).",
    title="Factual-density requirement: telegraphic, provenance-tagged content",
)

# ---------------------------------------------------------------------------
# Layer definitions (§2.2)
# ---------------------------------------------------------------------------

claim_layer_cognitive = claim(
    "**Layer 1 -- Cognitive Layer (`/logic`): structured scientific "
    "reasoning.** The agent reads `/logic` first to understand *what was "
    "done and why*. Files: `problem.md` (observations, gaps, key "
    "insight), `solution/` (architecture, algorithm, "
    "convergence-critical heuristics), `claims.md` (falsifiable "
    "assertions with explicit proof pointers), `experiments.md` "
    "(verification plan), and `related_work.md` (typed citation "
    "dependencies, not passive references). Typed dependencies turn "
    "literature review into a machine-executable graph: imports inject "
    "prior definitions, bounds propagate constraints, and baseline "
    "entries enable automatic regression detection.",
    title="Cognitive Layer: claims, experiments, heuristics, typed dependencies",
)

claim_layer_physical = claim(
    "**Layer 2 -- Physical Layer (`/src`): executable code calibrated to "
    "contribution type.** Two modes, declared in `PAPER.md` frontmatter "
    "as `src_mode: kernel|repo`:\n\n"
    "- **Kernel mode** (algorithmic contributions): only the core "
    "modules with typed I/O signatures -- often **1-2 orders of "
    "magnitude smaller** than the full repository. Stripped of "
    "environment-specific code so a coding agent regenerates fresh "
    "boilerplate on demand; the same kernel yields a *better* "
    "surrounding implementation as agent capabilities improve.\n"
    "- **Repository mode** (systemic contributions: CUDA kernels, "
    "distributed training, systems architectures): the full "
    "implementation is retained but annotated via an `index.md` "
    "manifest that maps each source file to the ARA component it "
    "implements. Forensic bindings connect code regions to claims, "
    "constraints, and heuristics.\n\n"
    "Both modes co-include: `configs/` (every hyperparameter annotated "
    "with rationale and search range) and `environment.md` (pinned "
    "dependencies, hardware, seeds).",
    title="Physical Layer: kernel mode (algorithmic) or repo mode (systemic)",
)

claim_layer_exploration = claim(
    "**Layer 3 -- Exploration Graph (`/trace`): the branching research "
    "DAG.** `exploration_tree.yaml` stores the complete research "
    "directed acyclic graph as a nested YAML tree with five typed node "
    "kinds -- `question`, `decision`, `experiment`, `dead_end`, "
    "`pivot` -- where nesting encodes parent->child edges and an "
    "`also_depends_on` field captures convergence points. Functions as "
    "a *git log for research*: agents traverse branches directly, and "
    "**`dead_end` nodes preserve the hypothesis, failure mode, and "
    "lesson** that narrative papers discard. Per-session logs in "
    "`sessions/` provide a chronological index.",
    title="Exploration Graph: typed DAG with dead_end nodes preserving failure knowledge",
    metadata={"source_figure": "Fig. 5 (artifacts/2604.24658.pdf, p. 4)"},
)

claim_layer_evidence = claim(
    "**Layer 4 -- Evidence Layer (`/evidence`): raw outputs grounding "
    "every claim.** `results/` contains machine-readable metric tables "
    "and generated data with *exact* values and source annotations; "
    "`logs/` captures training curves, resource usage, and diagnostics. "
    "The layer holds **outputs only**, so every claim's proof chain "
    "flows `claims.md -> experiments.md -> /evidence/`. Withholding "
    "ground-truth enables *layered access control*: a verification "
    "agent can be granted the code kernel and algorithm descriptions "
    "while the evidence layer is withheld, preventing fabrication by "
    "copying expected values. The same separation makes every ARA a "
    "ready-to-use *training environment*: task in `/logic/experiments.md`, "
    "reward in `/evidence/`, preference signals in every accept/reject/"
    "revision logged in `/trace/`.",
    title="Evidence Layer: raw outputs, separable from logic for blind verification",
)

# ---------------------------------------------------------------------------
# Cross-layer bindings
# ---------------------------------------------------------------------------

claim_forensic_bindings = claim(
    "**Forensic bindings: cross-layer claim->code->evidence references.** "
    "The four layers are not merely co-located directories: cross-layer "
    "*forensic bindings* explicitly link each claim in `/logic` to (a) "
    "the experiment that verifies it, (b) the implementation in `/src` "
    "that produces the experiment, and (c) the raw output in "
    "`/evidence` that supports it. These bindings are first-class data: "
    "they are validated structurally by ARA Seal Level 1 (every "
    "experiment ID in `claims.md`'s Proof field must resolve to an "
    "entry in `experiments.md`; every code reference in heuristics must "
    "point to a valid module in `/src`) and traversed by review agents.",
    title="Forensic bindings: machine-validated claim<->code<->evidence links",
    metadata={"source_figure": "Fig. 5 (artifacts/2604.24658.pdf, p. 4)"},
)

claim_two_tax_response_mapping = claim(
    "**The four layers are the structural response to the two taxes.** "
    "Each ARA layer addresses a specific failure mode of narrative "
    "compilation:\n\n"
    "| Tax | Failure mode | ARA layer that addresses it |\n"
    "|---|---|---|\n"
    "| Storytelling Tax | Branching trajectory collapsed | Exploration Graph (`/trace`): typed DAG with `dead_end` nodes |\n"
    "| Engineering Tax (descriptive half) | Conceptual description vs executable spec | Cognitive Layer (`/logic`): falsifiable claims + experiments + heuristics |\n"
    "| Engineering Tax (operational half) | Code without operational specification | Physical Layer (`/src`): kernel/repo mode + `configs/` + `environment.md` |\n"
    "| Either tax | Claims drift from numbers | Evidence Layer (`/evidence`) bound by forensic bindings |\n\n"
    "The four-layer decomposition is *not arbitrary*: it is the minimal "
    "set required to materialize each of the four agent-relevant "
    "questions while preserving the cross-layer bindings that narrative "
    "compilation destroys.",
    title="Four-layer architecture systematically addresses both taxes",
)

claim_capability_relative_sufficiency = claim(
    "**Sufficiency is capability-relative.** An ARA is *sufficient* "
    "when a sufficiently-capable coding agent can reproduce the core "
    "claim **zero-shot**, without human intervention or external "
    "context beyond the artifact. Sufficiency therefore measures "
    "whether the artifact *contains* the information needed for "
    "reproduction, not whether any present-day agent can fully exploit "
    "it. At the limit of agent capability, a complete ARA is "
    "reproducible by definition, so artifacts authored today remain "
    "valid as agents advance.",
    title="Sufficiency criterion: zero-shot reproducible by a sufficiently-capable agent",
)

# ---------------------------------------------------------------------------
# Reproduction-critical taxonomy (App. A.1) -- 10 information categories
# ---------------------------------------------------------------------------

claim_reproduction_taxonomy = claim(
    "**Ten reproduction-critical information categories drive the "
    "layer decomposition.** Analyzing 3,050 leaf rubric requirements "
    "from a 5-paper PaperBench subset reveals **ten categories** "
    "(Table 6, App. A.1), each with a primary ARA layer that addresses "
    "it. Hyperparameters -- the single most-discussed reproduction "
    "barrier -- account for only **17.2%** of leaves; the remaining "
    "82.8% comprise evaluation protocols, experiment matrices, logging "
    "requirements, result interpretation, and implementation tricks "
    "that PDFs systematically under-specify.\n\n"
    "| Category | % | ARA Layer |\n"
    "|---|---:|---|\n"
    "| Combinatorial experiment matrix | 24.1 | `experiments.md` |\n"
    "| Evaluation protocol | 18.5 | `experiments.md` |\n"
    "| Hyperparameters | 17.2 | `configs/training.md` |\n"
    "| Metric logging | 10.4 | `experiments.md` |\n"
    "| Result interpretation | 8.6 | `claims.md` + `evidence/` |\n"
    "| Architecture spec | 5.8 | `architecture.md` |\n"
    "| Mathematical formulation | 4.5 | `algorithm.md` |\n"
    "| Implementation tricks | 4.2 | `heuristics.md` |\n"
    "| Data pipeline | 3.8 | `configs/`, `environment.md` |\n"
    "| Environment / infra | 2.9 | `environment.md` |\n",
    title="Ten reproduction-critical categories drive the four-layer decomposition",
    metadata={"source_table": "Table 6 (artifacts/2604.24658.pdf, App. A.1, p. 24)"},
)

claim_combinatorial_explosion_dominant = claim(
    "**The combinatorial-explosion challenge is dominant, not the "
    "missing-hyperparameter one.** The single largest reproduction-"
    "requirement category (24.1%) is the *combinatorial experiment "
    "matrix*: the cross-product of models × datasets × configurations × "
    "seeds that PDFs compress into a single sentence or a results-table "
    "header. An agent must mentally decompose the matrix to enumerate "
    "individual runs. This is harder to recover than hyperparameters "
    "because the *enumeration itself* is implicit in narrative prose.",
    title="Combinatorial-experiment-matrix gap is larger than the hyperparameter gap",
)

claim_high_weight_requires_understanding = claim(
    "**Weight-2 requirements demand understanding, not just extraction.** "
    "All weight-2 requirements in the PaperBench rubrics belong to the "
    "*Result Interpretation* category: qualitative claims about what "
    "the results should *show* (directional trends, comparative "
    "rankings, mechanistic explanations). These test whether the agent "
    "*understands* the results, not just whether the code ran. ARA's "
    "`claims.md` (with explicit `Falsification criteria`) and "
    "`experiments.md` (with `Expected outcome` directional predictions) "
    "directly encode these verification targets, making the "
    "claim<->experiment connection explicit rather than requiring the "
    "agent to re-derive it from prose.",
    title="Weight-2 (high-priority) requirements probe understanding, addressed by claims.md schema",
)

__all__ = [
    "setup_design_principle_knowledge_over_narrative",
    "claim_four_question_decomposition",
    "claim_progressive_disclosure",
    "claim_factual_density_requirement",
    "claim_layer_cognitive",
    "claim_layer_physical",
    "claim_layer_exploration",
    "claim_layer_evidence",
    "claim_forensic_bindings",
    "claim_two_tax_response_mapping",
    "claim_capability_relative_sufficiency",
    "claim_reproduction_taxonomy",
    "claim_combinatorial_explosion_dominant",
    "claim_high_weight_requires_understanding",
]
