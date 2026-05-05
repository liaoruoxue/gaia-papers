"""Section 4: The ARA Compiler -- backward-compatibility for legacy artifacts.

The Live Research Manager (§3) only produces high-fidelity ARAs going
forward. The scientific record contains millions of legacy PDFs. The
ARA Compiler is the second agent skill in the system: it translates any
combination of legacy sources (PDF, repo, expert rubric, MALT
trajectory) into a complete ARA, with quality enforced via in-loop ARA
Seal Level 1 validation (§5).
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# Design principles (§4.1)
# ---------------------------------------------------------------------------

claim_universal_input_canonical_output = claim(
    "**P1: Universal input, canonical output.** The Compiler is "
    "many-to-one: it accepts any combination of PDFs, code "
    "repositories, datasets, human-curated rubrics (e.g., PaperBench "
    "claim decompositions [@Starace2025PaperBench]), and experimental "
    "trajectory logs (e.g., RE-Bench MALT traces [@Wijk2025REBench]), "
    "and always produces a single ARA conforming to §2. **Degradation "
    "is graceful**: a PDF alone yields a valid artifact with stub-level "
    "physical layers; richer inputs progressively populate more "
    "complete layers.",
    title="Compiler P1: any sources -> single canonical ARA, with graceful degradation",
)

claim_high_fidelity_preservation = claim(
    "**P2: High-fidelity preservation.** A narrative paper compresses "
    "and selects; the Compiler decompresses and restores. Every "
    "numerical result, hyperparameter, architectural detail, and "
    "negative finding in the sources must appear *somewhere* in the "
    "artifact. Any PDF-accessible information missing from the ARA "
    "constitutes a **compilation failure** -- evaluated in §7.2 "
    "(Cat. A: 96.7% PaperBench fidelity confirms generated ARAs "
    "preserve PDF-recoverable information).",
    title="Compiler P2: every source-fact must appear in the ARA (or it is a failure)",
)

claim_knowledge_lineage_not_extraction = claim(
    "**P3: Knowledge lineage, not flat extraction.** Narrative "
    "compilation destroys the **provenance chains** connecting claims "
    "to experiments to evidence to code. Plain-text extraction recovers "
    "*content* but not these connections: parsing a PDF into Markdown "
    "populates four directories yet leaves them structurally isolated. "
    "The Compiler performs **forensic reconstruction**, recovering "
    "cross-layer forensic bindings from sources where lineage exists "
    "only implicitly (scattered across prose, figure captions, "
    "appendix tables, code comments). *Recovering this lineage, not "
    "populating layers, is the core compilation problem.*",
    title="Compiler P3: forensic reconstruction of cross-layer lineage is the core problem",
)

# ---------------------------------------------------------------------------
# Implementation (§4.2)
# ---------------------------------------------------------------------------

claim_top_down_four_stages = claim(
    "**Top-down generation: four ordered stages (Figure 7).** The skill "
    "instructs the host agent to construct the artifact *top-down*, "
    "mirroring how a researcher explains their work to a new "
    "collaborator: high-level concepts first, details next, "
    "implementation last:\n\n"
    "1. **Semantic Deconstruction** -- strips narrative framing to "
    "expose raw research content (formulations, configurations, "
    "results, dependencies, failed approaches), rewritten in fact-dense "
    "telegraphic form -- *eliminating the Storytelling Tax at the "
    "source level*.\n"
    "2. **Cognitive Mapping** -- populates `/logic`: motivation chain "
    "(observations -> gaps -> insight), falsifiable claims with proof "
    "pointers, formal concepts, solution structure, with every claim "
    "linked to the experiment that verifies it.\n"
    "3. **Physical Grounding** -- generates `/src`: annotated "
    "configurations, typed code stubs, environment manifest. When a "
    "code repository is available, stubs are replaced with actual "
    "implementations and the agent performs **code-paper "
    "reconciliation**, cross-referencing the codebase against claims "
    "to surface tacit knowledge -- implicit assumptions, undocumented "
    "tricks, extra parameters [@Li2026TacitKnowledge] -- written back "
    "to `/logic` as provenance-tagged heuristics.\n"
    "4. **Exploration Graph Extraction** -- reconstructs the research "
    "DAG as a nested YAML tree with `dead_end` leaf nodes documenting "
    "hypothesis, failure mode, and lesson.\n\n"
    "This ordering ensures each layer is informed by the one above: "
    "cognitive structure guides physical generation, and the "
    "exploration graph contextualizes both.",
    title="Four-stage top-down compilation: deconstruct -> cognitive -> physical -> exploration",
    metadata={"source_figure": "Fig. 7 (artifacts/2604.24658.pdf, p. 7)"},
)

claim_iterative_validation = claim(
    "**Iterative refinement via in-loop validation feedback.** After "
    "initial generation, ARA Seal Level 1 checks (§5.2) -- schema "
    "conformance, cross-layer reference resolution, required-field "
    "completeness -- run *within the same agent conversation*, "
    "returning failures as structured diagnostics that drive targeted "
    "fixes. This generate -> validate -> fix loop typically converges "
    "in **2-3 rounds**, turning Level 1 from a post-hoc report into "
    "actionable feedback. Empirically (App. H.2.1): every one of the "
    "30 ARAs (23 PaperBench + 7 RE-Bench) converges to Level-1 pass "
    "within ≤3 iterations; first-iteration pass rate is **0/30**, "
    "confirming Level 1 is a non-trivial filter rather than a rubber "
    "stamp.",
    title="In-loop ARA Seal L1 feedback: 0/30 first-iteration passes, all converge in ≤3 rounds",
)

claim_source_aware_enrichment = claim(
    "**Source-aware enrichment routes auxiliary sources to the right "
    "layer.** Beyond PDF + code, auxiliary sources are routed to where "
    "they most directly populate: **code repositories** replace stubs "
    "with verified implementations in `/src`; **evaluation rubrics** "
    "(e.g., PaperBench rubrics) anchor `/logic` with expert-verified "
    "claim decompositions; **trajectory logs** (e.g., MALT) seed "
    "`/trace` with `dead_end` nodes the PDF omits. When a library of "
    "previously-compiled ARAs is available, the Compiler additionally "
    "performs *collective inference*: it retrieves heuristics and "
    "configurations from same-domain artifacts, flags common patterns "
    "the current paper omits, and adds them as candidate heuristics "
    "tagged `collective_inference` so downstream agents can distinguish "
    "stated from inferred knowledge.",
    title="Source-aware enrichment: rubric -> /logic; trajectory -> /trace; cross-ARA -> collective_inference",
)

claim_compiler_failure_distribution = claim(
    "**Empirical Compiler failure distribution.** Across all Compiler "
    "iterations on the 30-ARA evaluation corpus, Level 1 failures "
    "break down as: dangling cross-layer references (**42%**), missing "
    "schema fields on claims/experiments/heuristics (**31%**), "
    "insufficient node counts in `exploration_tree.yaml` (**14%**), "
    "YAML or frontmatter parse errors (**8%**), and missing mandatory "
    "files (**5%**). The distribution is stable across papers and "
    "matches the failure taxonomy in App. H.1, validating that the "
    "Level-1 schema tests the right structural invariants.",
    title="Compiler L1 failure distribution: dangling refs (42%) dominate, schema gaps (31%) follow",
    metadata={"source_section": "App. H.2.1 (artifacts/2604.24658.pdf, p. 44)"},
)

__all__ = [
    "claim_universal_input_canonical_output",
    "claim_high_fidelity_preservation",
    "claim_knowledge_lineage_not_extraction",
    "claim_top_down_four_stages",
    "claim_iterative_validation",
    "claim_source_aware_enrichment",
    "claim_compiler_failure_distribution",
]
