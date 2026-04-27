"""
Section 4.1-4.2: Main Experimental Results — ARC vs ReAct vs ReSum
====================================================================

ARC is evaluated on five long-horizon information-seeking benchmarks against two baselines
(ReAct and ReSum) across five actor models. We model the empirical outcomes as observed
benchmark tables and use support/contradiction strategies against those observations to
test whether ARC outperforms the baselines.
"""

from gaia.lang import claim, setting, support, contradiction

from .motivation import (
    active_management_view,
    contribution_perspective,
)
from .s3_methodology import (
    dual_architecture,
    incremental_summarization,
    reflection_operator,
    incremental_preserves_evidence,
    reflection_enables_repair,
)

# --- Experimental setup ---

benchmark_setup = setting(
    "ARC is evaluated on five long-horizon information-seeking benchmarks: HotpotQA "
    "(Yang et al., 2018), GAIA text-only subset (Mialon et al., 2023), xBench-DeepSearch "
    "(Chen et al., 2025), BrowseComp (Wei et al., 2025a), and BrowseComp-ZH "
    "(Zhou et al., 2025a). HotpotQA uses a 512-question random sample evaluated under "
    "active search-and-browse (not oracle retrieval). BrowseComp uses subsets from "
    "BrowseComp-LongContext under an information-seeking agent setting. All other benchmarks "
    "use the full test set.",
    title="Benchmark setup (5 datasets)",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.1"},
)

baselines_setup = setting(
    "Two baselines are compared:\n"
    "- **ReAct** [@Yao2023]: directly concatenates the full raw interaction history at each step "
    "without any explicit context compression or revision.\n"
    "- **ReSum** [@Wu2025b]: performs passive, static summarization to control context length. "
    "When the interaction history approaches the maximum context budget, past interactions are "
    "compressed into a single summary.\n\n"
    "All baselines share the same Actor model, tool interface, and search mechanism. The only "
    "difference is how past interactions are represented and maintained.",
    title="Baselines setup (ReAct, ReSum)",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.1"},
)

actor_models_setup = setting(
    "Actor models evaluated: Qwen2.5-7B-Instruct, Qwen2.5-32B-Instruct (Team, 2024), "
    "Qwen3-14B, Qwen3-32B (Team, 2025), and DeepSeek-v3.2 (DeepSeek-AI, 2025). "
    "Across all settings, the same Context Manager is instantiated using GPT-OSS-120B "
    "(OpenAI, 2025a) — fixing the CM ensures performance differences arise from the context "
    "management strategy rather than disparities in CM capacity.",
    title="Actor models setup (5 actors, fixed CM = GPT-OSS-120B)",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.1"},
)

# --- Observed result tables (anchored with high prior) ---

table1_observation = claim(
    "Table 1 reports Pass@1 / Pass@3 accuracies for ReAct, ReSum, and ARC across five actor "
    "models and five benchmarks. Selected entries:\n\n"
    "**Qwen2.5-32B-Instruct** (Pass@1):\n"
    "- HotpotQA: ReAct 65.5, ReSum 68.6, ARC 71.3\n"
    "- GAIA: ReAct 28.5, ReSum 27.3, ARC 34.9\n"
    "- xBench-DS: ReAct 33.3, ReSum 36.3, ARC 40.7\n"
    "- BrowseComp: ReAct 1.0, ReSum 1.2, ARC 3.0\n"
    "- BrowseComp-ZH: ReAct 7.1, ReSum 7.4, ARC 18.0 (+10.9 vs ReAct, +10.6 vs ReSum)\n\n"
    "**Qwen3-14B** (Pass@1): GAIA ReAct 26.5 / ReSum 31.3 / ARC 41.0; xBench-DS ReAct 32.6 / "
    "ReSum 32.0 / ARC 46.0; BrowseComp-ZH ReAct 8.5 / ReSum 10.0 / ARC 17.9.\n\n"
    "**DeepSeek-v3.2** (Pass@1): GAIA ReAct 63.7 / ReSum 67.1 / ARC 69.1; BrowseComp ReAct 16.8 "
    "/ ReSum 22.2 / ARC 26.6; BrowseComp-ZH ReAct 37.7 / ReSum 45.7 / ARC 51.7.\n\n"
    "Across every reported actor, ARC's Pass@1 exceeds both ReAct and ReSum on the harder "
    "search-heavy settings (GAIA, xBench-DS, BrowseComp, BrowseComp-ZH).",
    title="Table 1 results: ARC > ReAct/ReSum across actors and benchmarks",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.2, Table 1"},
)

# --- Predictions / interpretive claims ---

arc_outperforms_react = claim(
    "ARC outperforms ReAct (raw history concatenation) on long-horizon information-seeking "
    "benchmarks across actor models, with the largest gains on harder benchmarks. For example, "
    "with Qwen2.5-32B-Instruct, ARC improves BrowseComp-ZH Pass@1 from 7.1 to 18.0 (+10.9 "
    "absolute), and improves GAIA Pass@1 from 28.5 to 34.9 (+6.4 absolute).",
    title="ARC outperforms ReAct",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.2, Table 1"},
)

arc_outperforms_resum = claim(
    "ARC outperforms ReSum (passive periodic summarization) on long-horizon benchmarks. "
    "For example, with Qwen2.5-32B-Instruct, ARC improves BrowseComp-ZH Pass@1 from 7.4 to "
    "18.0 (+10.6 absolute), and with Qwen3-14B improves GAIA Pass@1 from 31.3 to 41.0 (+9.7 "
    "absolute). The 11% absolute improvement on BrowseComp-ZH highlighted in the abstract refers "
    "to the Qwen2.5-32B-Instruct setting.",
    title="ARC outperforms ReSum",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.2, Table 1, Abstract"},
)

react_better_than_arc = claim(
    "ReAct (raw history) outperforms ARC on the long-horizon information-seeking benchmarks "
    "in Table 1.",
    title="(Counterfactual) ReAct beats ARC",
    metadata={"source": "Counterfactual to Table 1"},
)

resum_better_than_arc = claim(
    "ReSum (passive periodic summarization) outperforms ARC on the long-horizon "
    "information-seeking benchmarks in Table 1.",
    title="(Counterfactual) ReSum beats ARC",
    metadata={"source": "Counterfactual to Table 1"},
)

gain_amplifies_with_difficulty = claim(
    "The advantage of ARC over passive baselines amplifies on harder, longer-horizon tasks. "
    "Gains are most pronounced on GAIA, xBench-DS, BrowseComp, and BrowseComp-ZH and smaller on "
    "HotpotQA — supporting the interpretation that the harder the task, the more context must "
    "be actively managed (not merely compressed).",
    title="ARC gain amplifies with task difficulty",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.2, Table 1"},
)

arc_lifts_both_small_and_large_actors = claim(
    "ARC substantially lifts weaker actors (Qwen2.5-7B-Instruct on BrowseComp-ZH: 4.7 -> 13.1 "
    "Pass@1; Qwen3-14B on GAIA: 26.5 -> 41.0) while still improving strong actors "
    "(DeepSeek-v3.2 on BrowseComp-ZH: 37.7 -> 51.7). Context management is therefore "
    "complementary to model scaling, not a substitute for it.",
    title="ARC benefits both small and large actors",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.2, Table 1"},
)

context_degradation_is_dominant_failure = claim(
    "The empirical pattern that passive baselines under-perform on long-horizon tasks supports "
    "the view that long-horizon failures are often driven by *context degradation* (rot, "
    "drift, attention dilution) rather than insufficient reasoning capacity, and that "
    "reflection-driven reorganization helps prevent error accumulation and unproductive loops.",
    title="Long-horizon failures driven by context degradation",
    metadata={"source": "artifacts/2601.12030.pdf, Section 4.2"},
)

# --- Strategies ---
# Anchor pattern: support / contradiction against the observed Table 1 entry,
# with the table itself anchored at high prior in priors.py.

strat_arc_beats_react = support(
    [table1_observation],
    arc_outperforms_react,
    background=[benchmark_setup, baselines_setup, actor_models_setup],
    reason=(
        "Table 1 (@table1_observation) directly reports Pass@1 numbers showing ARC > ReAct on "
        "every reported actor x benchmark cell on the harder long-horizon datasets. The "
        "controlled setup (@benchmark_setup, @baselines_setup, @actor_models_setup) — same Actor, "
        "tools, search mechanism, and fixed CM — isolates context-management strategy as the "
        "only varying factor, so the observed gap is causally attributable to ARC."
    ),
    prior=0.92,
)

strat_arc_beats_resum = support(
    [table1_observation],
    arc_outperforms_resum,
    background=[benchmark_setup, baselines_setup, actor_models_setup],
    reason=(
        "Table 1 (@table1_observation) directly reports Pass@1 numbers showing ARC > ReSum on "
        "the harder benchmarks. The 11% absolute BrowseComp-ZH improvement claimed in the "
        "abstract corresponds to Qwen2.5-32B-Instruct (7.4 -> 18.0 = +10.6, rounded). The "
        "controlled setup ensures this gap reflects active vs passive context management, "
        "not differences in Actor or CM capacity."
    ),
    prior=0.92,
)

strat_react_beats_arc_contra = contradiction(
    table1_observation,
    react_better_than_arc,
    reason=(
        "Table 1 (@table1_observation) shows ARC's Pass@1 strictly above ReAct on every reported "
        "actor x benchmark cell on the long-horizon datasets, directly contradicting the claim "
        "that ReAct beats ARC."
    ),
    prior=0.95,
)

strat_resum_beats_arc_contra = contradiction(
    table1_observation,
    resum_better_than_arc,
    reason=(
        "Table 1 (@table1_observation) shows ARC's Pass@1 above ReSum on the harder long-horizon "
        "benchmarks across every reported actor (e.g., GAIA, xBench-DS, BrowseComp, "
        "BrowseComp-ZH), directly contradicting the claim that ReSum beats ARC."
    ),
    prior=0.95,
)

strat_difficulty_amplification = support(
    [table1_observation],
    gain_amplifies_with_difficulty,
    background=[benchmark_setup],
    reason=(
        "Comparing ARC vs ReSum gaps in Table 1 (@table1_observation): on HotpotQA the gap is "
        "small (Qwen2.5-32B: 71.3 - 68.6 = +2.7), but on GAIA and BrowseComp-ZH it is several "
        "times larger (+7.6 and +10.6 respectively), and similar amplification holds across "
        "actors. This monotonically increasing gap with benchmark difficulty supports the "
        "amplification claim."
    ),
    prior=0.85,
)

strat_lifts_small_and_large = support(
    [table1_observation],
    arc_lifts_both_small_and_large_actors,
    background=[actor_models_setup],
    reason=(
        "Table 1 (@table1_observation) reports gains both for the smallest tested actor "
        "(Qwen2.5-7B-Instruct: BrowseComp-ZH 4.7 -> 13.1) and the strongest tested actor "
        "(DeepSeek-v3.2: BrowseComp-ZH 37.7 -> 51.7). The presence of substantial gains at "
        "both ends of the capacity spectrum directly substantiates the complementarity claim."
    ),
    prior=0.85,
)

strat_context_degradation = support(
    [arc_outperforms_react, arc_outperforms_resum, gain_amplifies_with_difficulty],
    context_degradation_is_dominant_failure,
    background=[active_management_view],
    reason=(
        "If long-horizon failures were dominated by limited reasoning capacity, varying the "
        "context-management strategy while holding the Actor fixed would have little effect. "
        "Instead the experiments show large, difficulty-amplified gains from active management "
        "(@arc_outperforms_react, @arc_outperforms_resum, @gain_amplifies_with_difficulty), "
        "consistent with the active-management view (@active_management_view) that context "
        "degradation, not reasoning capacity, is the dominant failure mode."
    ),
    prior=0.75,
)

strat_perspective_supported = support(
    [context_degradation_is_dominant_failure, arc_outperforms_resum],
    contribution_perspective,
    reason=(
        "The paper's perspective contribution (@contribution_perspective) — that context "
        "management requires *active* maintenance, not just length compression — is supported "
        "by the empirical observation that passive ReSum is substantially worse than active ARC "
        "(@arc_outperforms_resum), and that the gap traces to context degradation effects "
        "(@context_degradation_is_dominant_failure)."
    ),
    prior=0.8,
)

__all__ = [
    "benchmark_setup",
    "baselines_setup",
    "actor_models_setup",
    "table1_observation",
    "arc_outperforms_react",
    "arc_outperforms_resum",
    "react_better_than_arc",
    "resum_better_than_arc",
    "gain_amplifies_with_difficulty",
    "arc_lifts_both_small_and_large_actors",
    "context_degradation_is_dominant_failure",
    "strat_arc_beats_react",
    "strat_arc_beats_resum",
    "strat_react_beats_arc_contra",
    "strat_resum_beats_arc_contra",
    "strat_difficulty_amplification",
    "strat_lifts_small_and_large",
    "strat_context_degradation",
    "strat_perspective_supported",
]
