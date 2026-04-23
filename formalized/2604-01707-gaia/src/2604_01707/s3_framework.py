"""Section 3: A Unified Framework for Agent Memory Systems"""

from gaia.lang import (
    claim, setting,
    support, deduction,
)
from .motivation import (
    gap_no_unified_framework,
    gap_no_comprehensive_comparison,
    setting_llm_agents,
    setting_context_window,
)

# ── Framework definition ──────────────────────────────────────────────────────

setting_framework_scope = setting(
    "The unified framework takes the current user message M and existing memory H as inputs, "
    "and processes them through four modular components: "
    "(1) Information Extraction, (2) Memory Management, (3) Memory Storage, (4) Information Retrieval. "
    "Each component captures a distinct functional aspect of how agent memory systems operate in practice.",
    title="Unified framework scope",
)

framework_proposed = claim(
    "This paper proposes a unified modular framework that decomposes all representative agent memory "
    "methods into four components: "
    "(1) **Information Extraction** — identifies and extracts essential information from M suitable "
    "for downstream processing (filtering redundancies, transforming into knowledge types such as triples); "
    "(2) **Memory Management** — integrates newly extracted information with existing memory H through "
    "operations such as connecting, integrating, transforming, updating, and filtering; "
    "(3) **Memory Storage** — organizes and persists processed memory using vector-based, graph-based, "
    "or hybrid storage formats; "
    "(4) **Information Retrieval** — retrieves the most relevant information from H to support reasoning "
    "or response generation when a new query arrives.",
    title="Unified framework proposed",
    background=[setting_framework_scope, setting_llm_agents],
)

strat_framework_addresses_gap = support(
    [gap_no_unified_framework, gap_no_comprehensive_comparison],
    framework_proposed,
    reason=(
        "The absence of a unified framework (@gap_no_unified_framework) and the lack of systematic "
        "comparison (@gap_no_comprehensive_comparison) motivate the design of a modular decomposition "
        "that maps all existing memory methods onto the same four-component structure, enabling "
        "apples-to-apples comparison of design choices."
    ),
    prior=0.92,
)

# ── Ten representative methods classified ─────────────────────────────────────

ten_methods_classified = claim(
    "Ten representative agent memory methods are classified under the unified framework by four dimensions:\n\n"
    "| Method | Information Extraction | Management Operations | Storage Structure | Retrieval Mechanism |\n"
    "|--------|----------------------|----------------------|-------------------|--------------------|\n"
    "| A-MEM | Direct archive, Summarization-based | Connect, Update | Flat, Vector | Vector-Based |\n"
    "| MemoryBank | Direct archive | Integrate, Update, Filter | Flat, Vector | Vector-Based |\n"
    "| MemGPT | Direct archive | Integrate, Transform, Update | Hierarchical, Vector | Lexical-Based, Vector-Based |\n"
    "| Mem0 | Direct archive, Summarization-based | Integrate, Update, Filter | Flat, Vector | Vector-Based |\n"
    "| Mem0g | Graph-based extract | Connect, Update, Filter | Flat, Graph | Vector-Based, Structure-Based |\n"
    "| MemoChat | Direct archive | Integrate | Flat | LLM-Assisted |\n"
    "| Zep | Direct archive, Graph-based extract | Connect, Transform, Update | Hierarchical, Graph | Lexical-Based, Vector-Based, Structure-Based |\n"
    "| MemTree | Direct archive | Connect, Integrate, Update | Flat, Tree | Vector-Based |\n"
    "| MemoryOS | Direct archive | Connect, Integrate, Transform, Update, Filter | Hierarchical, Vector | Lexical-Based, Vector-Based |\n"
    "| MemOS | Direct archive, Summarization-based | Connect, Integrate, Update | Hierarchical, Tree | Lexical-Based, Vector-Based |\n\n"
    "(Source: Table 1 of the paper)",
    title="Ten methods classified",
    background=[setting_framework_scope],
)

strat_classification_from_framework = support(
    [framework_proposed],
    ten_methods_classified,
    reason=(
        "The unified framework (@framework_proposed) provides a consistent set of four dimensions "
        "along which each method's design choices can be characterized. The classification in "
        "Table 1 is a direct application of this framework to ten representative methods from the literature."
    ),
    prior=0.93,
)
