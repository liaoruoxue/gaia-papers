"""Section 6 — Experimental Results"""

from gaia.lang import claim, setting
from .motivation import (
    existing_verifiers_inadequate,
    gains_are_architectural,
    auto_research_70pct,
    human_expert_complementary_to_auto,
)
from .s3_principles import (
    rubric_quality_critical,
    process_outcome_separation,
    relevance_matrix_approach,
    controllable_vs_uncontrollable,
)
from .s5_experiments import (
    internal_dataset_setting,
    browserbase_dataset_setting,
    cuaverifierbench_novel,
    auto_research_setup,
)

# --- Main quantitative results ---

uv_outcome_kappa_internal = claim(
    "On the internal dataset ($n=140$), the Universal Verifier (GPT-5.2) achieves "
    "Cohen's $\\kappa = 0.64$ on outcome labels, compared to $\\kappa = 0.44$ for "
    "WebJudge (o4-mini) and $\\kappa = 0.31$ for WebVoyager (GPT-4o). "
    "The UV achieves FPR = 0.01 and FNR = 0.32.",
    title="UV outcome Cohen's kappa = 0.64 on internal dataset vs. 0.44/0.31 for baselines",
    background=[internal_dataset_setting],
    metadata={"source_table": "artifacts/2604.06240.pdf, Table 2"},
)

uv_outcome_kappa_browserbase = claim(
    "On the Browserbase OM2W dataset ($n=106$), the Universal Verifier (GPT-5.2) achieves "
    "Cohen's $\\kappa = 0.58$ on outcome labels, compared to $\\kappa = 0.31$ for "
    "WebJudge (o4-mini) and $\\kappa = 0.13$ for WebVoyager (GPT-4o). "
    "The UV achieves FPR = 0.08 on outcome labels.",
    title="UV outcome Cohen's kappa = 0.58 on Browserbase vs. 0.31/0.13 for baselines",
    background=[browserbase_dataset_setting],
    metadata={"source_table": "artifacts/2604.06240.pdf, Table 2"},
)

uv_process_kappa_internal = claim(
    "On the internal dataset ($n=140$), the Universal Verifier achieves Cohen's $\\kappa = 0.59$ "
    "on process labels, FPR = 0.04, and FNR = 0.24.",
    title="UV process Cohen's kappa = 0.59 on internal dataset",
    background=[internal_dataset_setting],
    metadata={"source_table": "artifacts/2604.06240.pdf, Table 2"},
)

uv_fpr_near_zero = claim(
    "The Universal Verifier achieves a false positive rate near zero on outcome labels: "
    "FPR = 0.01 on the internal dataset and FPR = 0.08 on the Browserbase dataset, "
    "meaning it almost never credits a trajectory with success when a human annotator "
    "would mark it as failure. This compares to FPR $\\geq 0.45$ for WebVoyager "
    "and FPR $\\geq 0.22$ for WebJudge.",
    title="UV reduces false positive rate to near zero (0.01-0.08 vs. 0.45+/0.22+ for baselines)",
    metadata={"source_table": "artifacts/2604.06240.pdf, Table 2"},
)

# Alternative hypothesis for architectural abduction
alt_fpr_reduction_is_model = claim(
    "The UV's lower false positive rate is primarily due to using a stronger backbone LLM "
    "(GPT-5.2) rather than its architectural design choices.",
    title="Alternative: UV advantage is from stronger LLM, not architecture",
)

uv_matches_human_interannotator = claim(
    "The Universal Verifier's outcome $\\kappa$ with human labels (0.58 on Browserbase) "
    "slightly exceeds the inter-annotator outcome $\\kappa$ range (0.53–0.57), "
    "and the UV's process $\\kappa$ (0.43) falls within the inter-annotator process $\\kappa$ "
    "range (0.36–0.45), indicating that the UV agrees with humans about as well as "
    "humans agree with each other on both dimensions.",
    title="UV agrees with humans as well as humans agree with each other",
    metadata={"source_table": "artifacts/2604.06240.pdf, Table 14"},
)

upgrading_backbone_insufficient = claim(
    "Upgrading WebVoyager from GPT-4o to GPT-5.2 reduces outcome FPR from 0.45 to 0.10 "
    "on the internal dataset, but simultaneously increases outcome FNR from 0.24 to 0.44, "
    "and improves Cohen's $\\kappa$ only modestly (0.31 → 0.43). WebJudge with GPT-5.2 "
    "also shows similarly modest $\\kappa$ improvement. These results confirm that the UV's "
    "advantage comes from its architectural design, not from using GPT-5.2.",
    title="Upgrading baseline backbone to GPT-5.2 yields only modest kappa improvement with higher FNR",
    metadata={"source_table": "artifacts/2604.06240.pdf, Table 2"},
)

# --- UV-informed annotation results ---

uv_reasoning_improves_human_labels = claim(
    "When Browserbase annotators are shown the Universal Verifier's verdict and reasoning "
    "(UV-informed stage), outcome Cohen's $\\kappa$ rises from 0.39 to 0.63, and outcome "
    "FNR drops from 0.62 to 0.35, while FPR remains near zero (0.04). For process labels, "
    "FNR drops sharply from 0.32 to 0.09. Only 16.6% of annotator outcome judgments "
    "flipped, of which 31 of 34 flips moved from success to failure — agreeing with "
    "UV-identified failures the annotators had initially missed.",
    title="UV reasoning improves human annotation: kappa rises 0.39→0.63 and FNR drops 0.62→0.35",
    background=[browserbase_dataset_setting],
    metadata={"source_table": "artifacts/2604.06240.pdf, Table 13"},
)

rubric_score_correlation = claim(
    "The Pearson correlation between UV rubric scores and human annotator rubric scores "
    "on the Browserbase OM2W dataset (215 annotator-task pairs, $\\sim$2 annotators per task) "
    "is $r = 0.61$ ($p < 10^{-22}$) and Spearman $\\rho = 0.58$ ($p < 10^{-20}$), "
    "confirming strong monotonic agreement between the two continuous scores.",
    title="UV and human rubric scores correlate at r=0.61 (Pearson), rho=0.58 (Spearman)",
    background=[browserbase_dataset_setting],
    metadata={"figure": "artifacts/2604.06240.pdf, Figure 11"},
)

process_more_subjective_than_outcome = claim(
    "Process evaluation is inherently more subjective than outcome evaluation: "
    "inter-annotator agreement on outcome labels ($\\kappa = 0.57$) is substantially "
    "higher than on process labels ($\\kappa = 0.45$ binary, $\\kappa = 0.36$ via "
    "rubric score binarized at 0.8). The continuous process scores correlate at "
    "Pearson $r = 0.62$ with mean absolute difference 0.21, indicating that annotators "
    "often assign directionally similar scores but differ enough near the 0.8 threshold "
    "to flip the binary label.",
    title="Process evaluation is more subjective than outcome evaluation",
    metadata={"source_table": "artifacts/2604.06240.pdf, Table 14"},
)

# --- Native benchmark verifier agreement ---

native_verifiers_overcount_success = claim(
    "Native verifiers shipped with CUA benchmarks (WebVoyager, Online-Mind2Web, WebTailBench) "
    "substantially disagree with the Universal Verifier: false positive rates relative to UV "
    "outcome labels are consistently above 20%, with WebVoyager (GPT-4o) having the highest "
    "FPR (0.60 for Fara-7B, 0.72 for GPT-5) and lowest Cohen's $\\kappa$. "
    "For example, on WebVoyager with Fara-7B: native verifier success rate = 74.6%, "
    "UV Process = 49.0%, UV Outcome = 37.9%.",
    title="Native benchmark verifiers over-count success by 20%+ vs. Universal Verifier",
    metadata={"source_table": "artifacts/2604.06240.pdf, Table 3"},
)

agentrewardbench_fpr = claim(
    "On a sample of 30 high-quality trajectories from AgentRewardBench that terminated "
    "within the step budget and were labeled as successful by AgentRewardBench human annotators, "
    "an expert annotator judged 8/30 to be false positives according to Universal Verifier "
    "outcome guidelines (FPR $\\approx 0.27$).",
    title="AgentRewardBench has ~27% false positive rate by UV outcome guidelines",
)

# --- Auto-research results ---

auto_research_from_blank_result = claim(
    "The from-blank auto-research agent (starting with all ~2,000 prompt lines replaced "
    "by // TODO placeholders) reached approximately 70% of human expert verifier quality "
    "(Cohen's $\\kappa \\approx 0.55$ vs. human expert's $\\kappa \\approx 0.7$ at experiment 32) "
    "in roughly one day of iteration (~64 experiments) compared to three weeks of human expert work.",
    title="From-blank auto-research achieves kappa ~0.55 in 1 day vs. human expert kappa ~0.7 in 3 weeks",
    background=[auto_research_setup],
    metadata={"figure": "artifacts/2604.06240.pdf, Figure 1"},
)

auto_research_conservative = claim(
    "The auto-research agent's edits tended to be conservative and incremental — adjusting "
    "thresholds or tightening rubric language for individual failure cases — rather than "
    "making larger structural or conceptual changes. In contrast, the human expert derived "
    "general scoring rules (e.g., 'separate nitpicks from critical failures') from observing "
    "patterns across many trajectory failures, driving large step-function $\\kappa$ improvements.",
    title="Auto-research makes conservative incremental edits vs. human expert's structural leaps",
    background=[auto_research_setup],
)

auto_research_cont_expert_result = claim(
    "When initialized from the human expert's best verifier configuration (continuing-expert "
    "setting), the auto-research agent can still find improvements subject to the constraint "
    "of not increasing the false positive rate. Table 17 shows 4 of 11 iterations were "
    "committed (runs 2, 6, 10, 11), with the rubric score context injection (run 6) being "
    "the single most impactful change.",
    title="Auto-research initialized from expert best can still improve the verifier",
    background=[auto_research_setup],
    metadata={"source_table": "artifacts/2604.06240.pdf, Table 17"},
)

auto_research_stochastic_variance = claim(
    "LLM non-determinism in rubric generation causes large stochastic variance: across "
    "identical prompts, outcome $\\kappa$ ranged from 0.64 to 0.71 in different runs. "
    "This necessitates multiple runs to distinguish signal from noise when evaluating "
    "prompt changes.",
    title="LLM non-determinism causes kappa variance of 0.64-0.71 for identical prompts",
)

# --- Ablation: LLM backbone ---

gpt52_lowest_fpr = claim(
    "In end-to-end LLM ablations (each model generates and scores its own rubric), "
    "GPT-5.2 achieves the lowest false positive rate (FPR = 0.03/0.00 for process/outcome) "
    "while GPT-5 achieves the best balanced agreement (Cohen's $\\kappa = 0.63/0.72$ for "
    "process/outcome, highest accuracy 0.84/0.86). GPT-5.1 achieves the highest F1 "
    "on outcome (0.86) with $\\kappa = 0.68$.",
    title="GPT-5.2 has lowest FPR; GPT-5 has best balanced kappa in end-to-end ablation",
    metadata={"source_table": "artifacts/2604.06240.pdf, Table 11"},
)

fixed_rubric_ablation = claim(
    "When rubrics are fixed (generated by GPT-5.2) and only the scoring model varies, "
    "GPT-5.2 remains the most conservative scorer (FPR = 0.03/0.00) while GPT-5.1 achieves "
    "the highest overall Cohen's $\\kappa$ on outcome (0.74) with F1 = 0.89. "
    "This confirms GPT-5.2's conservatism is an intrinsic property of the scorer, "
    "not an artifact of self-generated rubrics.",
    title="Fixed-rubric ablation: GPT-5.1 achieves highest outcome kappa (0.74) while GPT-5.2 most conservative",
    metadata={"source_table": "artifacts/2604.06240.pdf, Table 12"},
)
