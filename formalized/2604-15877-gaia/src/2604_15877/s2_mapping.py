"""Section 2.3-2.4: Mapping existing systems onto the spectrum and the missing diagonal."""

from gaia.lang import claim, setting, support, induction, contradiction

from .motivation import setup_scope
from .s2_spectrum import (
    def_level1,
    def_level2,
    def_level3,
)

# --- Mapping data: representative system counts ---

obs_l1_systems = claim(
    "Ten surveyed systems cluster at Level 1 (episodic memory), spanning diverse "
    "mechanisms: LLM-driven extraction (Mem0), agentic indexing (A-MEM), hierarchical "
    "storage (MemoryOS), reinforcement-learning-optimized memory operations (MemSkill, "
    "Memory-R1, Mem-α, MemPO), meta-learned memory architectures (ALMA), multi-agent "
    "coordination (MemMA), and governance with temporal decay (SSGM). Despite the "
    "mechanistic diversity, all ten converge on the same output format: structured "
    "episodic records.",
    title="Ten Level-1 systems cluster on episodic records",
    metadata={"source_table": "artifacts/2604.15877.pdf, Table 2"},
)

obs_l2_systems = claim(
    "Eight surveyed systems cluster at Level 2 (procedural skill). Voyager "
    "([@Wang2023voyager]) pioneered the paradigm; later entries include SkillWeaver, "
    "EvoSkill, CASCADE, AutoSkill, Trace2Skill, SkillRL, and EvolveR. CASCADE "
    "([@Huang2025cascade]) chains cumulative skill creation with autonomous evolution.",
    title="Eight Level-2 systems",
    metadata={"source_table": "artifacts/2604.15877.pdf, Table 2"},
)

obs_cross_level_systems = claim(
    "Two surveyed systems operate across Levels 1 and 2 simultaneously: ExpeL "
    "([@Zhao2024expel]) and AutoAgent ([@Wang2026autoagent]). Both use predetermined "
    "(fixed) levels without adaptive selection -- they are two-speed systems, not "
    "continuous spectra.",
    title="Two cross-level (L1-L2) systems with fixed levels",
)

obs_l3_empty = claim(
    "Level 3 (declarative rule) is notably sparse for *learned* rules: no surveyed "
    "system automates rule extraction from agent experience. Constitutional AI "
    "([@Bai2022cai]) uses pre-specified rules; reward-design methods (Potential-Based "
    "Reward Shaping [@Ng1999pbrs], process rewards [@Lightman2023verify], rule-based "
    "rewards [@Shao2024deepseekmath]) encode Level-3-type knowledge but are "
    "human-designed, not learned. Weight-level rules (via Reinforcement Learning from "
    "Human Feedback, RLHF [@Ouyang2022rlhf]) are static after training, opaque to "
    "inspection, and cannot be updated without retraining.",
    title="Level 3 is empty for learned rules",
)

obs_l3_partial_evidence = claim(
    "Recent empirical work provides initial Level-3 evidence: RuleShaping "
    "([@Zhang2026rules]) studies 25,000+ natural-language rules for coding agents and "
    "finds that **negative constraints (guardrails) improve performance by 7-14 "
    "percentage points** while positive directives hurt. SEVerA ([@Banerjee2026severa]) "
    "adds formal verification to self-evolving agents -- orthogonal to compression "
    "level but critical for correctness.",
    title="Initial Level-3 empirical evidence",
)

# --- Empirical performance comparisons (Table 1) ---

obs_skillrl_l2_vs_l1 = claim(
    "SkillRL ([@Xia2026skillrl]) reports a +68.5 percentage-point gain on the ALFWorld "
    "benchmark when using Level-2 skills versus Level-1 trajectory retrieval, holding "
    "the underlying agent constant.",
    title="SkillRL: +68.5pp L2 vs. L1 retrieval (ALFWorld)",
    metadata={"source_table": "artifacts/2604.15877.pdf, Table 1"},
)

obs_trace2skill_l2_vs_human = claim(
    "Trace2Skill ([@Ni2026trace2skill]) outperforms human-written skills by +21.5 "
    "percentage points on the SpreadsheetBench benchmark, indicating that automated "
    "Level-2 skill distillation can exceed manual skill curation.",
    title="Trace2Skill: +21.5pp L2 vs. human skill (SpreadsheetBench)",
    metadata={"source_table": "artifacts/2604.15877.pdf, Table 1"},
)

obs_trace2skill_l2_vs_none = claim(
    "Trace2Skill ([@Ni2026trace2skill]) reports a +42.1 percentage-point gain on "
    "SpreadsheetBench when using Level-2 skills versus a no-skill baseline.",
    title="Trace2Skill: +42.1pp L2 vs. no skill (SpreadsheetBench)",
    metadata={"source_table": "artifacts/2604.15877.pdf, Table 1"},
)

obs_skillsbench_curated = claim(
    "SkillsBench ([@Li2026skillsbench]) reports that **curated** Level-2 skills "
    "improve multi-task performance by +16.2 percentage points over a no-skill "
    "baseline.",
    title="SkillsBench: +16.2pp curated L2 vs. none",
    metadata={"source_table": "artifacts/2604.15877.pdf, Table 1"},
)

obs_skillsbench_selfgen = claim(
    "SkillsBench ([@Li2026skillsbench]) reports that LLM-self-generated Level-2 "
    "skills produce **+0.0 percentage points** of improvement on multi-task tasks -- "
    "no benefit -- in contrast to the +16.2pp gain from curated skills.",
    title="SkillsBench: +0.0pp LLM-self-generated L2",
    metadata={"source_table": "artifacts/2604.15877.pdf, Table 1"},
)

obs_evoskill_l2_vs_none = claim(
    "EvoSkill ([@Alzubi2026evoskill]) reports a +5.3% gain on the BrowseComp "
    "benchmark when using Level-2 skills versus no skill, providing additional "
    "empirical support for the L2-over-L1 pattern (though smaller in magnitude than "
    "the SkillRL/Trace2Skill results).",
    title="EvoSkill: +5.3% L2 vs. no skill (BrowseComp)",
    metadata={"source_table": "artifacts/2604.15877.pdf, Table 1"},
)

obs_ruleshaping_l3 = claim(
    "RuleShaping ([@Zhang2026rules]) reports a +7-14 percentage-point gain from "
    "Level-3 negative constraints compared to a zero-shot baseline on the SWE-bench "
    "coding benchmark.",
    title="RuleShaping: +7-14pp L3 constraints (SWE-bench)",
    metadata={"source_table": "artifacts/2604.15877.pdf, Table 1"},
)

# --- Empirical claim: higher compression yields better performance (within studies) ---

higher_compression_better = claim(
    "An emerging empirical consensus, drawing on cross-level performance comparisons "
    "from multiple studies, supports the claim that **higher-compression "
    "representations (Level 2 skills) consistently outperform lower-compression "
    "baselines (Level 1 retrieval, no skill)** within the same study, on benchmarks "
    "spanning embodied reasoning (ALFWorld), spreadsheet manipulation "
    "(SpreadsheetBench), web browsing (BrowseComp), and multi-task evaluation. "
    "Although results from different studies cannot be directly compared, the "
    "**direction** is consistent across all comparisons except SkillsBench's "
    "self-generated condition.",
    title="Higher compression consistently outperforms lower (within-study)",
)

# Build induction over the cross-level comparisons (chainable binary form)
s_skillrl = support(
    [higher_compression_better],
    obs_skillrl_l2_vs_l1,
    reason="The higher-compression-better generalization predicts SkillRL's L2-over-L1 advantage on ALFWorld.",
    prior=0.85,
)
s_trace2skill_human = support(
    [higher_compression_better],
    obs_trace2skill_l2_vs_human,
    reason="The generalization predicts Trace2Skill's L2-over-human-skill advantage on SpreadsheetBench.",
    prior=0.8,
)
s_trace2skill_none = support(
    [higher_compression_better],
    obs_trace2skill_l2_vs_none,
    reason="The generalization predicts Trace2Skill's L2-over-no-skill advantage on SpreadsheetBench.",
    prior=0.85,
)
s_skillsbench_curated = support(
    [higher_compression_better],
    obs_skillsbench_curated,
    reason="The generalization predicts SkillsBench's curated-L2 advantage on multi-task evaluation.",
    prior=0.8,
)
s_evoskill = support(
    [higher_compression_better],
    obs_evoskill_l2_vs_none,
    reason="The generalization predicts EvoSkill's L2-over-no-skill advantage on BrowseComp.",
    prior=0.7,
)

ind_compression_12 = induction(
    s_skillrl, s_trace2skill_human,
    law=higher_compression_better,
    reason="ALFWorld and SpreadsheetBench are independent benchmarks, evaluated by different groups with different agent backbones.",
)
ind_compression_123 = induction(
    ind_compression_12, s_trace2skill_none,
    law=higher_compression_better,
    reason="The L2-vs-no-skill comparison adds an independent baseline (no-skill instead of human skill).",
)
ind_compression_1234 = induction(
    ind_compression_123, s_skillsbench_curated,
    law=higher_compression_better,
    reason="SkillsBench provides an independent multi-task benchmark with curated rather than auto-generated skills.",
)
ind_compression_12345 = induction(
    ind_compression_1234, s_evoskill,
    law=higher_compression_better,
    reason="BrowseComp adds a fifth independent web-browsing benchmark; the direction is consistent across all five.",
)

# --- The fidelity caveat (SkillsBench self-generated counter-example) ---

fidelity_matters = claim(
    "Compression level alone is insufficient; the **fidelity of the compression "
    "process** determines whether the artifact is useful or merely compact noise. "
    "Curated Level-2 skills produce gains (+16.2pp) but LLM-self-generated Level-2 "
    "skills produce no benefit (+0.0pp) on the same SkillsBench evaluation. "
    "Therefore, achieving the right output format is necessary but not sufficient -- "
    "the extraction process must distill genuinely useful patterns.",
    title="Compression fidelity matters as much as level",
)

strat_fidelity = support(
    [obs_skillsbench_curated, obs_skillsbench_selfgen],
    fidelity_matters,
    reason=(
        "SkillsBench provides a within-study comparison that holds the compression "
        "level constant (both conditions are Level 2) and varies only the extraction "
        "process. Curated skills (@obs_skillsbench_curated) yield +16.2pp while "
        "LLM-self-generated skills (@obs_skillsbench_selfgen) yield +0.0pp. The same "
        "level produces opposite outcomes depending on extraction quality, so level "
        "alone cannot account for skill effectiveness."
    ),
    prior=0.92,
)

# --- The missing diagonal ---

missing_diagonal = claim(
    "The mapping reveals that systems cluster at Level 1 or Level 2, with minimal "
    "cross-level work and virtually no automated Level 3 work. We call this gap the "
    "**missing diagonal** -- the absence of systems that can: "
    "(1) **adaptively select** the appropriate compression level $L^*$ for a given "
    "trace $T$; "
    "(2) **promote** knowledge upward (from level $L$ to level $L' > L$) when "
    "sufficient evidence accumulates (many memories -> one skill -> one rule); "
    "(3) **demote** knowledge downward (from level $L$ to level $L' < L$) when a rule "
    "proves too abstract for a specific context.",
    title="The missing diagonal: no adaptive cross-level system",
)

strat_missing_diagonal = support(
    [obs_l1_systems, obs_l2_systems, obs_cross_level_systems, obs_l3_empty],
    missing_diagonal,
    reason=(
        "The mapping data establish the missing-diagonal claim by exhaustion: "
        "ten systems cluster at Level 1 (@obs_l1_systems), eight at Level 2 "
        "(@obs_l2_systems), and only two operate across Levels 1-2 -- both with fixed, "
        "non-adaptive level selection (@obs_cross_level_systems). Level 3 is empty "
        "for learned rules (@obs_l3_empty). No system in the survey supports adaptive "
        "level selection or upward/downward promotion-demotion. The claim follows by "
        "case enumeration over the 20+ surveyed systems."
    ),
    prior=0.93,
    background=[def_level1, def_level2, def_level3],
)

# --- Why the gap exists: framing, not engineering ---

framing_limitation = claim(
    "The missing diagonal reflects a **problem-framing limitation**, not missing "
    "engineering effort. Each community defines its output format a priori "
    "(memory papers fix L1, skill papers fix L2), so adaptive level selection is "
    "structurally outside the design space rather than merely unimplemented. Adaptive "
    "level selection is a **meta-learning problem**: learning what kind of knowledge "
    "to extract, not just what knowledge to extract.",
    title="Missing diagonal stems from framing, not engineering",
)

# --- Scalability bottleneck argument ---

scalability_bottleneck = claim(
    "The missing diagonal is also a **scalability bottleneck**: a Level-1-only system "
    "accumulating episodic memories faces linear growth in storage and retrieval cost, "
    "eventually degrading performance as irrelevant entries dilute useful knowledge. "
    "Upward compression (L1 -> L2 -> L3) is the natural solution: consolidate recurring "
    "patterns into compact skills or rules that scale sub-linearly with experience "
    "volume.",
    title="L1-only systems face linear-cost scalability bottleneck",
)

# --- Barriers to automated L3 extraction ---

l3_barriers = claim(
    "Four technical barriers explain the empty Level-3 cell: "
    "(i) distinguishing causal regularities from incidental correlations is harder than "
    "episode extraction; "
    "(ii) rules without Level-2 grounding risk being too abstract; "
    "(iii) no methodology exists for evaluating rule quality (infinite regress of "
    "meta-evaluation); "
    "(iv) using LLM-as-Judge gives a false sense that evaluation is solved.",
    title="Four barriers to automated L3 extraction",
)
