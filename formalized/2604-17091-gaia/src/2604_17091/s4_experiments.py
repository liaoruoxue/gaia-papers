"""Section 4: Experimental Evaluation"""

from gaia.lang import claim, setting, support, abduction, induction, compare

from .motivation import thesis_density, thesis_token_efficiency
from .s2_design import (
    claim_tool_minimality,
    claim_hierarchical_memory,
    claim_self_evolution,
    claim_context_compression,
    def_hallucination_free_length,
)

# ── Experimental setup settings ───────────────────────────────────────────────

setup_baselines = setting(
    "Baseline systems evaluated: (1) Claude Code — industry-leading proprietary agent "
    "with 53 source-level built-in tools; (2) OpenClaw — open-source multi-tool "
    "framework with 18 source-level tool factories; (3) CodeX — widely adopted "
    "execution baseline. Backbone LLMs used: Claude Sonnet 4.6, Claude Opus 4.6, "
    "Minimax M2.7, GPT-5.4, covering different architectural paradigms.",
    title="Experimental baselines and backbone LLMs",
)

setup_efficiency_metric = setting(
    "Efficiency metric: Efficiency = Accuracy / Total Tokens (M). "
    "Measures the accuracy achieved per million total tokens consumed. "
    "Because token scales differ across benchmarks, efficiency values are only "
    "comparable within the same benchmark block.",
    title="Efficiency metric definition",
)

setup_memory_ablation = setting(
    "Memory ablation configurations on SOP-Bench dangerous_goods subset (backbone: GPT-5.4): "
    "(1) No-Memory: task inputs and tool descriptions only; "
    "(2) Full-Memory: complete unedited SOP injected; "
    "(3) Redundant-Memory: Condensed Memory extended with background, definitions, "
    "weakly relevant content (288 tokens); "
    "(4) Condensed Memory: only high-density, action-guiding rules (165 tokens).",
    title="Memory ablation experimental configurations",
)

setup_locomo = setting(
    "LoCoMo factual memory evaluation: first subset of LoCoMo with Category 5 "
    "(summarization) removed. Embedding-based baselines: Mem0 and A-MEM with "
    "text-embedding-3-small. Non-embedding baselines: OpenClaw and GA. "
    "Backbone: GPT-5.4. Metrics: F1 (correctness/completeness), BLEU-1 (lexical similarity).",
    title="LoCoMo factual memory evaluation setup",
)

setup_self_evolution = setting(
    "Self-evolution longitudinal study: nine sequential rounds of a GitHub research "
    "task, each on a new task instance. Stages: Round 1 (initial run), "
    "Rounds 2-5 (SOP optimization), Rounds 6-9 (codified SOP). "
    "Backbone: Claude Opus 4.6 for GA and OpenClaw comparison.",
    title="Self-evolution longitudinal study setup",
)

setup_web_browsing = setting(
    "Web browsing evaluation: GA vs. OpenClaw (both using Claude Opus 4.6). "
    "Three benchmarks: WebCanvas (12 tasks, automatic evaluation), "
    "BrowseComp-ZH (10 tasks, LLM-as-judge), Custom Tasks (22 tasks, human + LLM). "
    "Metric: Score (0-1). Also reports Avg. Tokens (M) per task.",
    title="Web browsing evaluation setup",
)

# ── 4.1 Task Completion Results ───────────────────────────────────────────────

result_sop_bench_ga_claude = claim(
    "On SOP-Bench (multi-step SOP execution benchmark) with Claude Sonnet 4.6 backbone: "
    "GA achieves 100% accuracy, consuming 2.02M input tokens, 53k output tokens, "
    "2.08M total tokens, efficiency 0.48. "
    "OpenClaw achieves 100% accuracy, consuming 2.60M input tokens, 2.64M total, "
    "efficiency 0.38. "
    "Claude Code achieves 85% accuracy, consuming 1.23M input tokens, 1.25M total, "
    "efficiency 0.68.",
    title="SOP-Bench results with Claude Sonnet 4.6",
    metadata={"source_table": "artifacts/2604-17091.pdf, Table 2"},
)

result_lifelong_ga_claude = claim(
    "On Lifelong AgentBench (sequential tasks with cross-task dependencies) with "
    "Claude Sonnet 4.6 backbone: "
    "GA achieves 100% accuracy, consuming only 222k input tokens, 20k output, "
    "241k total tokens, efficiency 4.15. "
    "OpenClaw achieves 70% accuracy, consuming 1.43M input tokens, 1.45M total, "
    "efficiency 0.48. "
    "Claude Code achieves 75% accuracy, consuming 800k input tokens, 814k total, "
    "efficiency 0.92. "
    "GA uses 27.7% of Claude Code's input tokens and 15.5% of OpenClaw's input tokens "
    "while achieving higher task completion.",
    title="Lifelong AgentBench results with Claude Sonnet 4.6",
    metadata={"source_table": "artifacts/2604-17091.pdf, Table 2"},
)

result_realfin_ga = claim(
    "On RealFin-Benchmark (financial workflows with implicit user intent) with mixed backbones: "
    "GA (Claude Sonnet 4.6) achieves 65% accuracy, 102k input tokens, 114k total, "
    "efficiency 5.70. "
    "Claude Code (Claude Opus 4.6): 60% accuracy, 290k input, 307k total, efficiency 1.95. "
    "Claude Code (Claude Sonnet 4.6): 55% accuracy, 226k input, 238k total, efficiency 2.31. "
    "OpenClaw (Claude Sonnet 4.6): 35% accuracy, 249k input, 251k total, efficiency 1.39. "
    "CodeX (GPT-5.4): 60% accuracy, 838k input, 892k total, efficiency 0.67. "
    "GA achieves the highest accuracy and efficiency on this benchmark.",
    title="RealFin-Benchmark results",
    metadata={"source_table": "artifacts/2604-17091.pdf, Table 2"},
)

result_long_horizon_tool = claim(
    "On five long-horizon complex tasks (document generation, SQL copilot, experiment "
    "analysis report, procurement decision-making, research paper feasibility analysis) "
    "using Claude Sonnet 4.6: "
    "GA: 100% success, 188,829 total tokens (35.1% of Claude Code's), 220.8s, "
    "11.0 requests, 12.8 tool calls. "
    "Claude Code: 100% success, 537,413 total tokens, 320.8s, 32.6 requests, 22.6 tool calls. "
    "OpenClaw: 80% success, 633,101 total tokens, 183.1s, 15.0 requests, 16.6 tool calls.",
    title="Long-horizon complex task results",
    metadata={"source_table": "artifacts/2604-17091.pdf, Table 4"},
)

# ── Alternative explanation for task completion ───────────────────────────────

alt_model_advantage = claim(
    "GA's superior performance on task completion benchmarks could be primarily due "
    "to better backbone model selection or model-specific optimizations rather than "
    "architectural innovations in context density management.",
    title="Alternative: GA performance from model selection rather than architecture",
)

# ── 4.2 Tool Use Efficiency ───────────────────────────────────────────────────

result_tool_distribution = claim(
    "Tool usage is highly concentrated in a small subset even in systems with many tools. "
    "In Claude Code: AgentTool accounts for 50.4% of calls, WebFetchTool 22.1%, "
    "FileReadTool 10.6%, FileWriteTool 8.9%; many tools appear only in the tail. "
    "OpenClaw shows similar concentration. "
    "In GA: code_run (34.4%), web_execute_js (17.2%), file_read (10.9%), "
    "file_write (3.1%), web_scan (3.1%), update_working_checkpoint (31.2%). "
    "A substantial fraction of low-frequency tools in large-toolset systems still "
    "occupy prompt context despite contributing little to execution.",
    title="Tool usage concentration analysis",
    metadata={"source_figure": "artifacts/2604-17091.pdf, Figure 3"},
)

# ── 4.3 Memory System Results ─────────────────────────────────────────────────

result_continuous_improvement = claim(
    "GA shows continuous efficiency improvement across repeated runs of the same "
    "task type. Using GPT-5.4 backbone on a HuggingFace dataset download task: "
    "GA's operation time decreased from 102 seconds (Run 1) to approximately 66 "
    "seconds (Run 5). Token consumption dropped from 200,439 (Run 1) to approximately "
    "100,000 (Run 5). "
    "CodeX, Claude Code, and OpenClaw remained largely stable across runs, "
    "with OpenClaw's token usage fluctuating (1,370k to 2,330k to 2,130k). "
    "GA's gain comes from converting task experience into reusable L3 SOPs.",
    title="Continuous efficiency improvement through repeated task execution",
    metadata={"source_figure": "artifacts/2604-17091.pdf, Figure 4"},
)

result_condensed_memory_ablation = claim(
    "Memory ablation on SOP-Bench dangerous_goods (GPT-5.4 backbone): "
    "No-Memory: TSR = 13.87%, memory size = 0 tokens. "
    "Full-Memory: TSR = 52.44%, memory size = 575 tokens. "
    "Redundant-Memory: TSR = 66.48%, memory size = 288 tokens. "
    "Condensed Memory: TSR = 66.48%, memory size = 165 tokens. "
    "Condensed memory achieves the same highest TSR (Task Success Rate) as "
    "Redundant-Memory while using 42.7% fewer tokens (165 vs 288), and outperforms "
    "Full-Memory (52.44%) while using 71.3% fewer tokens.",
    title="Condensed vs Full vs Redundant memory ablation results",
    metadata={"source_table": "artifacts/2604-17091.pdf, Table 5"},
)

result_factual_memory = claim(
    "Long-term factual memory evaluation on LoCoMo (GPT-5.4 backbone): "
    "GA achieves highest scores across all four categories: "
    "Multi-Hop: F1=43.33, BLEU=39.96 (vs Mem0 F1=39.32, A-MEM F1=29.03, OpenClaw F1=21.43). "
    "Temporal: F1=52.23, BLEU=51.11 (vs Mem0 F1=50.03, A-MEM F1=46.83, OpenClaw F1=22.56). "
    "Open-Domain: F1=20.41, BLEU=15.31 (vs Mem0 F1=18.32, A-MEM F1=13.11, OpenClaw F1=9.56). "
    "Single-Hop: F1=45.69, BLEU=40.66 (vs Mem0 F1=40.32, A-MEM F1=44.68, OpenClaw F1=23.44). "
    "GA does not use an embedding model or vector database.",
    title="Long-term factual memory evaluation results (LoCoMo)",
    metadata={"source_table": "artifacts/2604-17091.pdf, Table 6"},
)

result_context_explosion = claim(
    "Context explosion prevention after installing 20 skills with intensive use. "
    "Full prompt length on minimal 'Hello' request: "
    "GA: 2,298 tokens. Claude Code: 22,821 tokens. CodeX: 23,932 tokens. "
    "OpenClaw: 43,321 tokens. "
    "GA's prompt is 10.1x smaller than Claude Code, 10.4x smaller than CodeX, "
    "and 18.9x smaller than OpenClaw.",
    title="Context explosion prevention results",
    metadata={"source_table": "artifacts/2604-17091.pdf, Table 7"},
)

# ── 4.4 Self-Evolution Results ────────────────────────────────────────────────

result_evolution_trajectory = claim(
    "Nine-round evolution trajectory on LangChain GitHub research task (Claude Opus 4.6): "
    "Round 1 (initial): 7m30s, 32 LLM calls, 15,581 input tokens, 222,203 total. "
    "Round 2-5 (SOP optimization): time decreases from 4m19s to 2m50s; "
    "calls decrease from 12 to 7; total tokens from 66,341 to 35,536. "
    "Round 6-9 (codified SOP): converges to ~23k +/- 1k total tokens; "
    "5 LLM calls; time ~1m35s to 1m41s. "
    "Token reduction from Round 1 to Round 9: 89.6% (222,203 to 23,010). "
    "Cache-read tokens collapse from 183,375 (Round 1) to 19,034 (Round 9). "
    "Input tokens collapse from 15,581 to 1,323.",
    title="Nine-round evolution trajectory results",
    metadata={"source_table": "artifacts/2604-17091.pdf, Table 8"},
)

result_cross_task_evolution = claim(
    "Cross-task evolution on 8-task web benchmark (GA vs OpenClaw, Claude Opus 4.6): "
    "GA shows consistent token convergence across repeated runs on all 8 tasks. "
    "High-complexity tasks (OpenClaw average >1,000k tokens, e.g., A1, B2, D1) "
    "achieve 83.5% average token saving in Run 3 vs Run 1. "
    "Mid-complexity tasks achieve 72.5% average saving. "
    "D2 achieves 90.1% saving despite low absolute cost, due to long-horizon structure. "
    "OpenClaw shows no convergence (e.g., A1 tokens: 1,370k to 2,330k to 2,130k). "
    "SOP self-evolution benefit scales with task complexity.",
    title="Cross-task evolution convergence results",
    metadata={"source_figure": "artifacts/2604-17091.pdf, Figure 5"},
)

# ── 4.5 Web Browsing Results ──────────────────────────────────────────────────

result_web_browsing = claim(
    "Web browsing evaluation (GA and OpenClaw both using Claude Opus 4.6): "
    "WebCanvas (12 tasks, automatic): GA score 0.834, 0.18M tokens; "
    "OpenClaw score 0.722, 0.71M tokens. GA uses 25.4% of OpenClaw's tokens. "
    "BrowseComp-ZH (10 tasks, LLM judge): GA score 0.600, 0.47M tokens; "
    "OpenClaw score 0.200, 1.31M tokens. GA triples OpenClaw's score "
    "at one-third the token cost. "
    "Custom Tasks (22 tasks, human + LLM): GA score 0.577, 0.26M tokens; "
    "OpenClaw score 0.500, 0.76M tokens. "
    "Structural token reduction: 2.9x to 3.9x across all benchmarks.",
    title="Web browsing evaluation results",
    metadata={"source_table": "artifacts/2604-17091.pdf, Table 9"},
)

# ── Strategies: connecting results to claims ──────────────────────────────────

# Connect orphaned benchmark results to hypothesis claims
strat_sop_bench = support(
    [claim_tool_minimality],
    result_sop_bench_ga_claude,
    reason=(
        "@claim_tool_minimality predicts GA can achieve competitive accuracy with "
        "fewer token overheads from tool descriptions. On SOP-Bench, GA achieves "
        "100% accuracy at 2.08M tokens, matching OpenClaw (100%, 2.64M) and "
        "outperforming Claude Code (85%, 1.25M). The accuracy advantage over "
        "Claude Code is consistent with lower context overhead [@GenericAgent2026]."
    ),
    prior=0.84,
)

strat_realfin = support(
    [claim_context_compression],
    result_realfin_ga,
    reason=(
        "@claim_context_compression predicts better handling of complex, multi-step "
        "financial workflows where context accumulates. GA achieves 65% on "
        "RealFin-Benchmark, outperforming Claude Code Opus (60%), CodeX (60%), "
        "and OpenClaw (35%), while using 35% of CodeX's tokens. "
        "Financial workflows have long implicit-intent chains that benefit from "
        "compression [@GenericAgent2026]."
    ),
    prior=0.80,
)

strat_long_horizon = support(
    [claim_tool_minimality, claim_context_compression],
    result_long_horizon_tool,
    reason=(
        "@claim_tool_minimality predicts reduced tool call overhead; "
        "@claim_context_compression predicts lower accumulated context cost. "
        "Together they predict GA should match success rates with fewer tokens "
        "on long-horizon tasks. Observed: GA achieves 100% success with 188,829 "
        "tokens (35.1% of Claude Code's 537,413) and 11.0 requests vs 32.6 "
        "[@GenericAgent2026]."
    ),
    prior=0.86,
)

strat_tool_distribution = support(
    [claim_tool_minimality],
    result_tool_distribution,
    reason=(
        "@claim_tool_minimality claims that even rich-toolset systems concentrate "
        "execution in a few tools. The observed distribution confirms: Claude Code's "
        "top 4 tools account for 92% of calls (AgentTool 50.4%, WebFetchTool 22.1%, "
        "FileReadTool 10.6%, FileWriteTool 8.9%). This validates the atomicity "
        "principle — broad tool inventories add prompt overhead without proportional "
        "execution benefit [@GenericAgent2026]."
    ),
    prior=0.85,
)

strat_continuous_improvement = support(
    [claim_self_evolution],
    result_continuous_improvement,
    reason=(
        "@claim_self_evolution predicts repeated task execution converts experience "
        "into L3 SOPs, reducing per-task cost over time. Observed: GA's operation "
        "time drops from 102s to ~66s and token consumption from 200,439 to ~100,000 "
        "across 5 runs, while CodeX, Claude Code, and OpenClaw remain stable. "
        "The reduction indicates high-value rule extraction, not mere history caching "
        "[@GenericAgent2026]."
    ),
    prior=0.87,
)

strat_cross_task_evolution = support(
    [claim_self_evolution],
    result_cross_task_evolution,
    reason=(
        "@claim_self_evolution predicts SOP crystallization transfers across similar "
        "task structures. Observed on 8-task web benchmark: GA converges to lower "
        "token usage by Run 3 for all 8 tasks (72.5%-90.1% savings). High-complexity "
        "tasks benefit most (83.5% savings for tasks with OpenClaw average >1,000k tokens). "
        "OpenClaw shows no convergence (A1: 1,370k to 2,330k), confirming "
        "the advantage is from self-evolution, not the backbone model [@GenericAgent2026]."
    ),
    prior=0.86,
)

# Abduction for task completion: density-design vs model-selection hypothesis
# The observation is result_lifelong_ga_claude (GA's high accuracy + low token use)

ga_density_architecture = claim(
    "GA's context density architecture (hierarchical memory, minimal tools, context "
    "compression) is the primary driver of its accuracy-efficiency advantage across "
    "benchmarks and backbone LLMs.",
    title="Density architecture hypothesis for GA advantage",
)

strat_density_explains_obs = support(
    [ga_density_architecture],
    result_lifelong_ga_claude,
    reason=(
        "@ga_density_architecture predicts GA should achieve high accuracy with fewer "
        "tokens. The density mechanisms reduce per-step context cost (hierarchical memory), "
        "tool overhead (minimal tools), and history growth (context compression). "
        "This predicts the observed 100% accuracy at 222k tokens vs Claude Code 75% "
        "at 800k and OpenClaw 70% at 1.45M — a structural efficiency advantage."
    ),
    prior=0.85,
)

strat_model_explains_obs = support(
    [alt_model_advantage],
    result_lifelong_ga_claude,
    reason=(
        "@alt_model_advantage suggests model selection drives GA's advantage. "
        "If so, using a weaker backbone (Minimax M2.7) should degrade GA's advantage "
        "relative to Claude Code or OpenClaw. The observation shows GA still achieves "
        "90% at 423k with Minimax M2.7 vs OpenClaw 70% at 1.22M — some advantage "
        "persists across LLMs, suggesting architecture rather than just model quality."
    ),
    prior=0.30,
)

comp_task_completion = compare(
    ga_density_architecture, alt_model_advantage,
    result_lifelong_ga_claude,
    reason=(
        "GA achieves 100% accuracy at 241k total tokens on Lifelong AgentBench "
        "with Claude Sonnet 4.6, and 90% at 423k with Minimax M2.7. Both "
        "consistently outperform OpenClaw (70%/1.45M and 70%/1.22M) and Claude Code "
        "(75%/814k). Cross-LLM advantage persistence is inconsistent with a pure "
        "model-selection explanation and consistent with architectural density design."
    ),
    prior=0.82,
)

abd_task_completion = abduction(
    strat_density_explains_obs, strat_model_explains_obs, comp_task_completion,
    reason=(
        "Both density-design and model-selection hypotheses attempt to explain "
        "GA's superior accuracy and efficiency on Lifelong AgentBench. "
        "The cross-LLM consistency (advantage persists with both Claude Sonnet 4.6 "
        "and Minimax M2.7) favors the architectural density explanation."
    ),
)

# Memory ablation support
strat_condensed_memory = support(
    [claim_hierarchical_memory],
    result_condensed_memory_ablation,
    reason=(
        "@claim_hierarchical_memory predicts that high-density, action-guiding "
        "memory outperforms verbose memory. The ablation confirms: Condensed Memory "
        "(165 tokens) matches Redundant-Memory TSR (66.48%) at 42.7% lower token cost, "
        "and outperforms Full-Memory (52.44%) at 71.3% fewer tokens. "
        "Background descriptions add contextual cost without behavioral value."
    ),
    prior=0.88,
)

# Self-evolution support
strat_evolution_trajectory = support(
    [claim_self_evolution],
    result_evolution_trajectory,
    reason=(
        "@claim_self_evolution predicts that textual SOP then codified SOP conversion "
        "reduces per-task token cost. The nine-round study shows: total tokens collapse "
        "from 222,203 (Round 1) to 23,010 (Round 9), an 89.6% reduction. "
        "The dominant contribution is call count reduction (32 to 5), eliminating "
        "entire understand-reason-generate loops. The convergence band ~23k+/-1k "
        "in Rounds 6-9 indicates deterministic codified execution."
    ),
    prior=0.90,
)

# Factual memory: induction across categories

obs_multihop = claim(
    "GA achieves best Multi-Hop factual memory performance on LoCoMo: F1=43.33, "
    "BLEU=39.96, exceeding Mem0 (F1=39.32), A-MEM (F1=29.03), OpenClaw (F1=21.43).",
    title="GA best on Multi-Hop factual recall",
)

obs_temporal = claim(
    "GA achieves best Temporal factual memory performance on LoCoMo: F1=52.23, "
    "BLEU=51.11, exceeding Mem0 (F1=50.03), A-MEM (F1=46.83), OpenClaw (F1=22.56).",
    title="GA best on Temporal factual recall",
)

obs_open_domain = claim(
    "GA achieves best Open-Domain factual memory performance on LoCoMo: F1=20.41, "
    "BLEU=15.31, exceeding Mem0 (F1=18.32), A-MEM (F1=13.11), OpenClaw (F1=9.56). "
    "Open-Domain is the hardest category for all systems.",
    title="GA best on Open-Domain factual recall",
)

law_hierarchical_memory_factual = claim(
    "GA's hierarchical memory with validated commit and L1 routing achieves superior "
    "long-term factual retention across multi-hop, temporal, open-domain, and "
    "single-hop categories without requiring an embedding model or vector database.",
    title="Hierarchical memory law: superior factual retention across categories",
)

s_mem_multihop = support(
    [law_hierarchical_memory_factual], obs_multihop,
    reason=(
        "@law_hierarchical_memory_factual predicts GA performs best at factual recall. "
        "Multi-hop tasks require reasoning across fact chains — GA's L1/L2 routing "
        "and validated commit prevent stale facts from degrading multi-step reasoning."
    ),
    prior=0.88,
)

s_mem_temporal = support(
    [law_hierarchical_memory_factual], obs_temporal,
    reason=(
        "@law_hierarchical_memory_factual predicts GA performs best at factual recall. "
        "Temporal tasks require time-ordered fact retrieval — hierarchical memory "
        "preserves temporal structure better than raw log storage."
    ),
    prior=0.85,
)

s_mem_open = support(
    [law_hierarchical_memory_factual], obs_open_domain,
    reason=(
        "@law_hierarchical_memory_factual predicts GA performs best at factual recall. "
        "Open-Domain is hardest because structural cues are weak — GA's categorical "
        "L1 index still provides routing even without strong retrieval signals."
    ),
    prior=0.78,
)

ind_mem_12 = induction(
    s_mem_multihop, s_mem_temporal,
    law=law_hierarchical_memory_factual,
    reason=(
        "Multi-Hop and Temporal categories involve different reasoning demands "
        "(cross-fact chains vs. time-ordered sequences) and are independently "
        "evaluated. Both confirming @law_hierarchical_memory_factual provides "
        "independent corroboration of the memory architecture's generality."
    ),
)

ind_mem_123 = induction(
    ind_mem_12, s_mem_open,
    law=law_hierarchical_memory_factual,
    reason=(
        "Open-Domain adds a third independent category (no structural cues) "
        "confirming @law_hierarchical_memory_factual. Three independent task "
        "categories converging supports the law's generality across memory challenges."
    ),
)

strat_factual_memory_summary = support(
    [law_hierarchical_memory_factual],
    result_factual_memory,
    reason=(
        "@law_hierarchical_memory_factual predicts GA outperforms embedding-based "
        "systems across factual recall categories. The summary LoCoMo results confirm: "
        "GA leads on all four categories (Multi-Hop F1=43.33, Temporal F1=52.23, "
        "Open-Domain F1=20.41, Single-Hop F1=45.69) without embedding model or "
        "vector database. The categorical L1 routing provides effective navigation "
        "without vector similarity search [@GenericAgent2026]."
    ),
    prior=0.87,
)

# Web browsing: abduction
# H = density design explains web results
# Alt = specialized browser tools advantage

alt_web_tools = claim(
    "OpenClaw's more specialized browser tools and richer action space could "
    "outperform GA's atomic web_scan and web_execute_js on tasks requiring "
    "fine-grained browser interaction.",
    title="Alternative: specialized browser tools outperform atomic tools",
)

web_density_design = claim(
    "GA's context compression and web_scan DOM optimization maintain information "
    "density on web pages, enabling GA to outperform systems with specialized "
    "browser tools, especially on multi-hop reasoning tasks.",
    title="Web density design hypothesis",
)

strat_density_explains_web = support(
    [web_density_design],
    result_web_browsing,
    reason=(
        "@web_density_design predicts lower token usage and better multi-hop "
        "handling via DOM compression. Observed: GA uses 25.4% of OpenClaw's "
        "tokens on WebCanvas, 35.9% on BrowseComp-ZH, and 34.2% on Custom Tasks — "
        "consistent structural compression across all three benchmarks. "
        "BrowseComp-ZH (multi-hop) shows the largest score gap (0.600 vs 0.200), "
        "consistent with compounding context management benefit."
    ),
    prior=0.82,
)

strat_tools_explains_web = support(
    [alt_web_tools],
    result_web_browsing,
    reason=(
        "@alt_web_tools predicts specialized tools outperform atomic primitives "
        "on web tasks. OpenClaw has dedicated browser tools vs GA's web_scan + "
        "web_execute_js. If specialized tools win, OpenClaw should score higher on "
        "standard WebCanvas interactions (atomic element clicking, navigation). "
        "Observed: OpenClaw scores 0.722 vs GA's 0.834 on WebCanvas — specialized "
        "tools do not yield higher accuracy even on standard interactions."
    ),
    prior=0.30,
)

comp_web = compare(
    web_density_design, alt_web_tools,
    result_web_browsing,
    reason=(
        "GA outperforms OpenClaw on all three web benchmarks. BrowseComp-ZH "
        "(most multi-hop) shows the largest gap: GA 0.600 vs OpenClaw 0.200 at "
        "one-third the tokens. GA also wins WebCanvas (0.834 vs 0.722) at 25.4% "
        "of the token cost. The specialized-tools hypothesis is inconsistent with "
        "OpenClaw losing even on standard WebCanvas interactions."
    ),
    prior=0.82,
)

abd_web = abduction(
    strat_density_explains_web, strat_tools_explains_web, comp_web,
    reason=(
        "Both density-design and specialized-tools hypotheses attempt to explain "
        "web browsing performance differences. GA's advantage being largest on "
        "BrowseComp-ZH (most multi-hop, most context-sensitive) and persisting even "
        "on standard WebCanvas interactions favors the density-design explanation."
    ),
)

# Token efficiency as summary conclusion
strat_token_efficiency_evidence = support(
    [result_lifelong_ga_claude, result_context_explosion, result_evolution_trajectory],
    thesis_token_efficiency,
    reason=(
        "@result_lifelong_ga_claude shows GA using 27.7% of Claude Code's tokens "
        "while achieving higher accuracy (100% vs 75%). @result_context_explosion "
        "shows GA's prompt 10x smaller than Claude Code after extensive use. "
        "@result_evolution_trajectory shows 89.6% token reduction with maintained "
        "performance after self-evolution. Together, these systematically demonstrate "
        "that lower token consumption correlates with better task performance."
    ),
    prior=0.87,
)
