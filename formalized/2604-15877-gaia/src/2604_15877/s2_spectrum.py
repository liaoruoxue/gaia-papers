"""Section 2: The Experience Compression Spectrum -- formal framework and properties."""

from gaia.lang import claim, setting, support, deduction

from .motivation import setup_scope, setup_cls_theory, shared_problem

# --- Formal definitions (Section 2.1) ---

def_interaction_trace = setting(
    "**Definition 2.1 (Interaction Trace).** An interaction trace "
    "$T = \\{(s_t, a_t, o_t, f_t)\\}_{t=1}^{N}$ is a sequence of states $s_t$, actions "
    "$a_t$, observations $o_t$, and feedback signals $f_t$ collected during agent "
    "execution.",
    title="Definition 2.1: interaction trace",
)

def_compression_function = setting(
    "**Definition 2.2 (Experience Compression Function).** An experience compression "
    "function $C_L: T \\to K_L$ maps interaction traces to knowledge artifacts at "
    "compression level $L \\in \\{0, 1, 2, 3\\}$. The output space $K_L$ corresponds to "
    "one of the four spectrum levels (raw trace, episodic memory, procedural skill, "
    "declarative rule).",
    title="Definition 2.2: experience compression function",
)

# --- The four levels (Section 2.1) ---

def_level0 = setting(
    "**Level 0 (Raw Trace).** The uncompressed interaction record. Format: complete logs, "
    "execution trajectories. Compression ratio: 1:1. Reusability: minimal -- entirely "
    "context-bound.",
    title="Level 0: raw trace",
)

def_level1 = setting(
    "**Level 1 (Episodic Memory).** Structured extraction of *what happened*, preserving "
    "key contextual details while discarding redundant interaction mechanics. Format: "
    "key-value pairs, timestamped event summaries (e.g., '[2026-03-15] User requested Q3 "
    "revenue analysis via SQL. Preferred tabular format.'). Compression ratio: ~5-20x. "
    "Reusability: low to moderate -- tied to specific episodes.",
    title="Level 1: episodic memory",
)

def_level2 = setting(
    "**Level 2 (Procedural Skill).** Extraction of *how to act* in a class of situations, "
    "abstracting across instances into reusable behavioral patterns. Format: structured "
    "routines, code snippets, workflow templates (e.g., 'DATA ANALYSIS: (1) Confirm "
    "source, (2) Select tool, (3) Present in preferred format, (4) Verify.'). "
    "Compression ratio: ~50-500x. Reusability: high -- transferable across similar "
    "situations.",
    title="Level 2: procedural skill",
)

def_level3 = setting(
    "**Level 3 (Declarative Rule).** Extraction of *what principles govern decisions* -- "
    "domain-invariant knowledge. Format: natural-language principles, constraints, "
    "policies (e.g., 'Always verify computed results against source data before "
    "presenting.'). Compression ratio: ~1,000x or more. Reusability: highest -- "
    "domain-general but may lack actionable specificity.",
    title="Level 3: declarative rule",
)

# --- Section 2.2 properties: trade-offs along the spectrum ---

generalizability_tradeoff = claim(
    "Generalizability versus specificity trade-off: as compression level increases from "
    "Level 0 to Level 3, the extracted knowledge becomes more broadly applicable but less "
    "context-specific. Higher-level artifacts (skills, rules) discard concrete contextual "
    "details to expose patterns that transfer across instances; lower-level artifacts "
    "(raw traces, episodic memories) retain context at the cost of reusability.",
    title="Generalizability vs. specificity trade-off",
)

strat_generalizability = support(
    [shared_problem],
    generalizability_tradeoff,
    reason=(
        "The unifying view (@shared_problem) identifies the spectrum's axis as "
        "compression of interaction experience into reusable knowledge. Definitionally "
        "(@def_level0, @def_level1, @def_level2, @def_level3), the four levels differ "
        "in how much contextual detail they retain: Level 0 retains everything (1:1) "
        "and is context-bound, while Level 3 retains only abstract principles (>1000x) "
        "and is domain-general. The trade-off is therefore intrinsic to the level "
        "definitions."
    ),
    prior=0.92,
    background=[def_level0, def_level1, def_level2, def_level3],
)

# --- Concrete compression-ratio illustrations ---

obs_mem0_compression = claim(
    "Mem0 ([@Chhikara2025mem0]) compresses multi-session conversation history (~26,000 "
    "tokens) into retrieved memory entries (~1,800 tokens), achieving roughly 15x "
    "compression at Level 1.",
    title="Mem0 ~15x Level-1 compression",
)

obs_trace2skill_compression = claim(
    "Trace2Skill ([@Ni2026trace2skill]) distills traces from 200 tasks via 128 parallel "
    "sub-agents into a compact skill directory, achieving roughly 100-500x compression "
    "at Level 2.",
    title="Trace2Skill ~100-500x Level-2 compression",
)

# --- Acquisition vs maintenance cost ---

acquisition_maintenance_tradeoff = claim(
    "Acquisition versus maintenance cost trade-off: Level 1 episodic memories are cheap "
    "to acquire (one trace per memory) but expensive to maintain at scale -- a Level-1-"
    "only system accumulating thousands of entries per day will exhaust any practical "
    "retrieval budget within weeks. Level 3 declarative rules require many traces to "
    "induce but form a compact, low-maintenance set. This trade-off makes upward "
    "compression not merely desirable but **necessary** for agents that operate at scale "
    "over extended deployments.",
    title="Acquisition vs. maintenance cost trade-off",
)

storage_cost_calculation = claim(
    "A worked storage estimate illustrates the maintenance burden. A Level-1-only agent "
    "storing 1,000 episodes at ~500 tokens each maintains a ~500K-token knowledge store "
    "that must be indexed and searched at every decision. Compressing the same content "
    "into Level-2 skills reduces storage to ~5K tokens; into Level-3 rules, ~500 tokens "
    "-- a 100-1,000x reduction in storage and retrieval overhead that compounds across "
    "thousands of daily decisions.",
    title="Storage estimate: 500K -> 5K -> 500 tokens",
)

strat_maintenance_tradeoff = support(
    [storage_cost_calculation],
    acquisition_maintenance_tradeoff,
    reason=(
        "The storage estimate (@storage_cost_calculation) makes the maintenance asymmetry "
        "concrete: Level 1 storage scales linearly with episode count (500 tokens per "
        "episode), while higher-level artifacts compress thousands of episodes into a "
        "small fixed set. With thousands of daily decisions, Level-1 storage and "
        "retrieval costs become prohibitive within weeks, while Level-3 storage remains "
        "essentially flat. This grounds the qualitative trade-off in a quantitative "
        "scaling argument."
    ),
    prior=0.9,
)

# --- Spectrum is descriptive, not procedural ---

spectrum_not_pipeline = claim(
    "The four levels describe an output space, not a fixed processing order. A system "
    "may compress directly from Level 0 to Level 3, or maintain knowledge at multiple "
    "levels simultaneously. The spectrum specifies the granularity of the extracted "
    "artifacts; it does not prescribe a sequential pipeline.",
    title="Spectrum is descriptive, not procedural",
)
