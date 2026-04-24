"""Section 3: DRA Failure Taxonomy — systematic classification of agent failures"""

from gaia.lang import (
    claim, setting,
    support, deduction,
)

from .motivation import dra_definition, asymmetry_of_verification


# ── Taxonomy construction settings ────────────────────────────────────────────

taxonomy_dataset = setting(
    "The WebAggregatorQA dataset [@Wang2025] is used for constructing the DRA failure taxonomy. "
    "It exercises core DRA capabilities including multi-step reasoning, multimodal inputs, "
    "web browsing, and general tool-use proficiency across 10+ domains. It is selected to avoid "
    "data leakage from the evaluation benchmarks (GAIA, BrowseComp, XBench-DeepSearch).",
    title="Taxonomy construction dataset: WebAggregatorQA",
)

agent_backbone = setting(
    "Cognitive Kernel-Pro (CK-Pro) [@Fang2025b], a high-performing fully open-source multi-module "
    "DRA framework, with Claude-3.7-Sonnet as the backbone model, is used to generate trajectories "
    "for taxonomy construction.",
    title="Agent and backbone model for trajectory collection",
)

annotation_protocol = setting(
    "Two independent research-staff annotators inspect each erroneous trajectory against human "
    "reference solution traces from WebAggregatorQA, recording error points (concrete, localized "
    "mistakes) with supporting trajectory steps. Sets are reconciled by merging duplicates and "
    "retaining distinct items. Average inter-annotator overlap is 63.0%, indicating high agreement.",
    title="Error annotation protocol",
)

taxonomy_construction_method = setting(
    "An iterative analysis and labeling process with two annotators with multiple years of AI "
    "research experience: initial labels from clustering 50 error points, then iterative refinement "
    "comparing/merging labels, removing inadequate categories, and refining definitions.",
    title="Taxonomy construction methodology",
)

# ── Trajectory corpus claims ───────────────────────────────────────────────────

trajectory_corpus = claim(
    "The taxonomy construction corpus comprises 2,997 agent actions across 90 distinct tasks. "
    "Trajectory lengths range from 2 to 156 steps (average 33.3 steps). Token counts range from "
    "18.7K to 60.0M tokens (average 8.2M tokens, total 738M tokens). The correct/incorrect ratio "
    "is 0.96 (nearly balanced).",
    title="Trajectory corpus statistics",
    background=[taxonomy_dataset, agent_backbone],
    metadata={"source_table": "artifacts/2601.15808.pdf, Table 1"},
)

high_token_count = claim(
    "DRA trajectories average 8.2M tokens, far exceeding any LLM's context window. This makes "
    "direct holistic verification infeasible and necessitates trajectory summarization as a "
    "preprocessing step before verification.",
    title="DRA trajectory token count exceeds LLM context window",
    background=[agent_backbone],
)

strat_token_infeasibility = support(
    [trajectory_corpus],
    high_token_count,
    reason=(
        "@trajectory_corpus establishes that DRA trajectories average 8.2M tokens. @high_token_count "
        "states this exceeds any LLM context window, making direct holistic verification infeasible. "
        "The infeasibility follows from the quantitative comparison of trajectory token count "
        "against practical LLM context window limits (typically 128K–2M tokens)."
    ),
    prior=0.95,
)

error_points_count = claim(
    "The annotation process yields 555 error points across all incorrect trajectories in the "
    "WebAggregatorQA corpus.",
    title="Total annotated error points",
    background=[annotation_protocol],
)

# ── Five major failure categories ─────────────────────────────────────────────

taxonomy_five_categories = claim(
    "The DRA Failure Taxonomy classifies 555 agent failures into five major categories and "
    "thirteen sub-categories:\n\n"
    "1. **Finding Sources** (most frequent): errors in information acquisition — consulting the "
    "wrong evidence, relying on generic searches, secondary-source dependence\n"
    "2. **Reasoning Failures** (second most common): premature conclusions, misinterpretation, "
    "hallucinated or overconfident claims\n"
    "3. **Problem Understanding and Decomposition**: misunderstanding instructions, goal drift\n"
    "4. **Action Errors**: UI failures, format mistakes, wrong modality use\n"
    "5. **Max Step Reached**: cascading early mistakes lead to long, unproductive trajectories\n\n"
    "Finding Sources dominates, with the largest flows corresponding to consulting wrong evidence "
    "and relying on generic searches — upstream information acquisition is the most frequent failure.",
    title="DRA Failure Taxonomy: five major categories",
    background=[taxonomy_dataset, annotation_protocol, taxonomy_construction_method],
    metadata={"figure": "artifacts/2601.15808.pdf, Figure 3",
              "caption": "DRA failure taxonomy categorizing 555 agent failures into five major classes and thirteen subclasses"},
)

strat_taxonomy_from_corpus = support(
    [error_points_count],
    taxonomy_five_categories,
    reason=(
        "@error_points_count (555 annotated error points) provides the corpus from which the "
        "iterative clustering and labeling procedure (@taxonomy_construction_method) derives the "
        "five-category, thirteen-subclass taxonomy (@taxonomy_five_categories). The taxonomy "
        "emerges inductively from the empirical error patterns [@Wan2026]."
    ),
    prior=0.85,
)

finding_sources_dominant = claim(
    "Information acquisition failures (Finding Sources category) dominate DRA failure modes, "
    "representing the largest single failure class in the taxonomy. Sub-categories include "
    "consulting wrong evidence, relying on generic searches instead of targeted queries, and "
    "over-reliance on secondary sources that may be incomplete or inaccurate.",
    title="Finding Sources is the dominant failure category",
    background=[taxonomy_five_categories],
)

strat_finding_sources = support(
    [taxonomy_five_categories],
    finding_sources_dominant,
    reason=(
        "@taxonomy_five_categories explicitly states that Finding Sources has the largest flows "
        "and that upstream information acquisition is the most frequent point of collapse. "
        "@finding_sources_dominant directly follows from this observation in the taxonomy figure."
    ),
    prior=0.90,
)

rubrics_from_taxonomy = claim(
    "The DRA Failure Taxonomy directly informs rubric construction for DeepVerifier: each failure "
    "category and sub-category corresponds to a dimension in the rubric used to evaluate agent "
    "trajectories. The taxonomy provides a principled, data-driven basis for structured verification "
    "rather than ad hoc judgment criteria.",
    title="Rubrics derived from failure taxonomy",
    background=[taxonomy_five_categories, asymmetry_of_verification],
)

strat_rubrics_derivation = support(
    [taxonomy_five_categories],
    rubrics_from_taxonomy,
    reason=(
        "The five major categories and thirteen sub-categories of @taxonomy_five_categories "
        "are translated into rubric dimensions for @rubrics_from_taxonomy. By exploiting the "
        "@asymmetry_of_verification, each rubric dimension targets a specific known vulnerability, "
        "making verification tractable by decomposing it into focused sub-checks [@Wan2026]."
    ),
    prior=0.87,
)
