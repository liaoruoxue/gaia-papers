"""Section 4: Information Extraction"""

from gaia.lang import (
    claim, setting,
    support,
)
from .s3_framework import framework_proposed

# ── Three extraction methods ──────────────────────────────────────────────────

setting_extraction_role = setting(
    "Information extraction is the first component in the unified framework. "
    "It identifies and extracts information from the current message M that is both useful "
    "and necessary for downstream memory processing.",
    title="Extraction component role",
)

extraction_direct_archiving = claim(
    "Direct archiving is the most straightforward extraction method: the agent system archives "
    "raw messages and timestamps without any processing. It is used by all ten representative methods "
    "as a baseline extraction approach.",
    title="Direct archiving extraction",
    background=[setting_extraction_role],
)

extraction_summarization = claim(
    "Summarization-based extraction employs LLMs to generate concise informational summaries from "
    "one or more dialogue turns. Methods such as A-MEM and Mem0 extract keywords and contextual tags "
    "from M, or prompt the LLM to produce an abstracted summary of the raw text. "
    "A representative prompt structure produces a JSON object with 'summary', 'keywords', and 'tags' fields.",
    title="Summarization-based extraction",
    background=[setting_extraction_role],
)

extraction_graph_based = claim(
    "Graph-based extraction leverages LLMs to extract fine-grained entities and relations from M, "
    "forming subject-predicate-object triples for knowledge graph construction (e.g., Mem0g, Zep). "
    "Temporal metadata such as creation or invalidation timestamps are recorded to support dynamic "
    "updates and temporal reasoning within the graph-based memory.",
    title="Graph-based extraction",
    background=[setting_extraction_role],
)

strat_three_extraction_types = support(
    [framework_proposed],
    extraction_summarization,
    reason=(
        "The unified framework (@framework_proposed) identifies information extraction as the first "
        "stage of memory processing. Survey of existing methods reveals three distinct extraction "
        "paradigms — direct archiving, summarization-based, and graph-based — covering the range "
        "from zero-processing to structured knowledge extraction."
    ),
    prior=0.92,
)

# ── Information completeness tradeoff ─────────────────────────────────────────

extraction_completeness_tradeoff = claim(
    "Graph-based extraction (triples only) may lose information compared to methods that retain "
    "raw dialogue fragments. Specifically, graph extraction converts unstructured text into "
    "subject-predicate-object triples, potentially discarding semantic nuance and contextual detail "
    "that cannot be represented in triple form. This may explain why Mem0 (direct archive + "
    "summarization) outperforms Mem0g (graph-based only) in many experimental cases.",
    title="Extraction completeness tradeoff",
    background=[setting_extraction_role],
)
