"""Section 5 & 7.2: Test-Time Scaling with Reflection and Feedback"""

from gaia.lang import (
    claim, setting,
    support, induction,
)

from .motivation import alternative_paradigm_claim, dra_unreliability
from .s3_taxonomy import rubrics_from_taxonomy
from .s4_deepverifier import (
    deepverifier_superiority,
    three_stage_architecture,
    judge_scoring_rubric,
    full_deepverifier_performance,
)


# ── Scaling protocol settings ─────────────────────────────────────────────────

scaling_protocol = setting(
    "Reflective test-time scaling integrates DeepVerifier into the DRA loop: after completing each "
    "task, the agent verifies its own outputs using DeepVerifier, collects feedback, and uses it to "
    "guide further retries. The feedback loop repeats until the verifier judges the answer correct "
    "(score ≥ 3) or a predefined retry limit (10 rounds) is exceeded.",
    title="Reflective test-time scaling protocol",
)

corrective_feedback_design = setting(
    "The corrective feedback prompt instructs the judge to: (1) provide a brief reflection on why "
    "the previous answer was wrong, (2) give up to three actionable retry instructions specifying "
    "necessary sources and actions, and (3) suggest the correct answer if derivable from available "
    "information. Instructions are concise to avoid confusing the agent.",
    title="Corrective feedback prompt design",
)

gaia_web_subset = setting(
    "The GAIA-Web subset of the GAIA benchmark [@Mialon2023] filters for tasks requiring web "
    "browsing. The GAIA dataset has three difficulty levels (Level 1 easiest, Level 3 hardest). "
    "The GAIA-Full split includes 165 development examples.",
    title="GAIA benchmark: Web subset and full split",
)

evaluation_models = setting(
    "Main backbone model for scaling experiments: Claude-3.7-Sonnet. Generalization also tested "
    "on GPT-4.1 and the fine-tuned DeepVerifier-8B (Qwen3-8B base).",
    title="Backbone models evaluated",
)

# ── Scaling result claims ─────────────────────────────────────────────────────

gaia_full_scaling = claim(
    "On GAIA-Full (n = 165), DeepVerifier with Claude-3.7-Sonnet backbone improves accuracy from "
    "52.22% (0 feedback rounds) to a peak of 60.12% at round 4 (+7.90 points), ending at 58.93% "
    "after 10 rounds (+6.71 points final gain). The GAIA-Web subset shows the greatest improvement, "
    "rising from 51.11% to a peak of 63.33% at round 4 (+12.22 points), ending at 62.22% "
    "(+11.11 points final gain).",
    title="GAIA accuracy gains with DeepVerifier scaling (Claude-3.7-Sonnet)",
    background=[scaling_protocol, gaia_web_subset, evaluation_models],
    metadata={"source_table": "artifacts/2601.15808.pdf, Table 3"},
)

gaia_gpt41_scaling = claim(
    "On GAIA-Full with GPT-4.1 backbone, DeepVerifier improves accuracy from 29.51% (0 rounds) "
    "to a peak of 32.53% at rounds 2 and 6 (+3.01 points), ending at 31.92% after 10 rounds "
    "(+2.41 points). On GAIA-Web, accuracy rises from 28.89% to a peak of 32.22% (+3.33 points), "
    "ending at 31.11% (+2.22 points).",
    title="GAIA accuracy gains with DeepVerifier scaling (GPT-4.1)",
    background=[scaling_protocol, gaia_web_subset, evaluation_models],
    metadata={"source_table": "artifacts/2601.15808.pdf, Table 3"},
)

gaia_dv8b_scaling = claim(
    "On GAIA-Full with DeepVerifier-8B backbone, accuracy improves from 26.73% (0 rounds) to "
    "32.21% after 10 rounds (+5.48 points). On GAIA-Web, accuracy rises from 26.67% to 33.33% "
    "(+6.67 points). File/Reasoning/Others subset gains 4.04 points.",
    title="GAIA accuracy gains with DeepVerifier-8B scaling",
    background=[scaling_protocol, gaia_web_subset, evaluation_models],
    metadata={"source_table": "artifacts/2601.15808.pdf, Table 3"},
)

peak_at_round_four = claim(
    "Performance typically peaks around the fourth feedback round across all models and subsets. "
    "This is explained by the interplay of two competing transition rates: the incorrect→correct "
    "transition (strong early: 18.99% at round 1, decaying to 0% by round 5) dominates the "
    "correct→incorrect regression rate (weaker but persistent: 12.79% at round 1, declining "
    "thereafter). Their crossover produces the observed peak around round 4.",
    title="Scaling peak at round 4 explained by transition rates",
    background=[scaling_protocol, judge_scoring_rubric],
    metadata={"source_table": "artifacts/2601.15808.pdf, Table 5"},
)

transition_rates = claim(
    "Transition rates between consecutive feedback rounds on GAIA-Full (Claude-3.7-Sonnet):\n\n"
    "| Round | Incorrect→Correct (%) | Correct→Incorrect (%) |\n"
    "|-------|----------------------|----------------------|\n"
    "| 1     | 18.99               | 12.79               |\n"
    "| 2     | 9.33                | 4.44                |\n"
    "| 3     | 6.94                | 4.30                |\n"
    "| 4     | 8.45                | 1.06                |\n"
    "| 5     | 0.00                | 3.03                |\n"
    "| 6     | 1.45                | 0.00                |\n"
    "| 7–10  | ≤1.45               | ≤1.03               |\n\n"
    "The incorrect→correct rate is stronger but decays; the correct→incorrect rate is weaker but persists.",
    title="Feedback round transition rates",
    background=[scaling_protocol, judge_scoring_rubric],
    metadata={"source_table": "artifacts/2601.15808.pdf, Table 5"},
)

strat_peak_explanation = support(
    [transition_rates],
    peak_at_round_four,
    reason=(
        "@transition_rates shows that at round 1, incorrect→correct (18.99%) strongly dominates "
        "correct→incorrect (12.79%). By round 4, incorrect→correct (8.45%) still exceeds "
        "correct→incorrect (1.06%), but both are declining. Beyond round 4, incorrect→correct "
        "reaches 0% while correct→incorrect persists, causing the net improvement to saturate "
        "and then slightly reverse — producing the peak at @peak_at_round_four."
    ),
    prior=0.88,
)

# ── Cross-dataset generalization ──────────────────────────────────────────────

xbench_scaling = claim(
    "On XBench-DeepSearch (Chinese multilingual benchmark), DeepVerifier with Claude-3.7-Sonnet "
    "backbone improves accuracy from 41.0% (0 rounds) to a peak of 47.0% at round 2 (+6.0 points), "
    "ending at 44.0% after 10 rounds (+3.0 points final gain).",
    title="XBench-DeepSearch accuracy with DeepVerifier scaling",
    background=[scaling_protocol, evaluation_models],
    metadata={"source_table": "artifacts/2601.15808.pdf, Table 4"},
)

browsecomp_scaling = claim(
    "On BrowseComp (extremely hard information retrieval benchmark), DeepVerifier with "
    "Claude-3.7-Sonnet backbone improves accuracy from 5.0% (0 rounds) to a peak of 10.0% "
    "at rounds 2–3 (+5.0 points), ending at 9.0% after 10 rounds (+4.0 points final gain).",
    title="BrowseComp accuracy with DeepVerifier scaling",
    background=[scaling_protocol, evaluation_models],
    metadata={"source_table": "artifacts/2601.15808.pdf, Table 4"},
)

# ── Inference-time scaling law claim ─────────────────────────────────────────

scaling_generalizes = claim(
    "The inference-time scaling effect of DeepVerifier generalizes across: (1) model families "
    "(Claude-3.7-Sonnet, GPT-4.1, Qwen3-8B/DeepVerifier-8B), (2) dataset types (GAIA-Web for "
    "retrieval-heavy tasks; File/Reasoning for non-web tasks; XBench-DeepSearch for multilingual; "
    "BrowseComp for extremely hard browsing), confirming that structured rubric-based reflection "
    "is a broadly applicable improvement mechanism.",
    title="Scaling effect generalizes across models and datasets",
)

s1_claude = support(
    [scaling_generalizes],
    gaia_full_scaling,
    reason=(
        "@scaling_generalizes asserts broad generalization. @gaia_full_scaling (Claude-3.7-Sonnet, "
        "GAIA-Full +7.90 points peak) is the primary evidence confirming the law for the main model."
    ),
    prior=0.90,
)

s2_gpt41 = support(
    [scaling_generalizes],
    gaia_gpt41_scaling,
    reason=(
        "@scaling_generalizes predicts the improvement holds for GPT-4.1. @gaia_gpt41_scaling "
        "confirms +3.01 points on GAIA-Full, providing independent cross-model evidence."
    ),
    prior=0.85,
)

s3_xbench = support(
    [scaling_generalizes],
    xbench_scaling,
    reason=(
        "@scaling_generalizes predicts generalization to multilingual datasets. @xbench_scaling "
        "confirms +6.0 points on XBench-DeepSearch, providing cross-dataset evidence."
    ),
    prior=0.80,
)

ind_12 = induction(
    s1_claude,
    s2_gpt41,
    law=scaling_generalizes,
    reason="Claude-3.7-Sonnet and GPT-4.1 are independent model families from different organizations",
)

ind_123 = induction(
    ind_12,
    s3_xbench,
    law=scaling_generalizes,
    reason="XBench-DeepSearch is a different language/dataset from GAIA, providing independent cross-dataset evidence",
)

# ── Web-subset benefit claim ──────────────────────────────────────────────────

web_benefits_most = claim(
    "Web-based, retrieval-heavy tasks (GAIA-Web subset) benefit most from DeepVerifier's targeted "
    "verification and evidence-grounding process: +12.22 points peak gain (Claude-3.7-Sonnet), "
    "compared to +2.64 points peak for File/Reasoning/Others subset. This is consistent with "
    "Finding Sources being the dominant failure category.",
    title="GAIA-Web benefits most from verification scaling",
    background=[gaia_web_subset],
    metadata={"source_table": "artifacts/2601.15808.pdf, Table 3"},
)

strat_web_benefit = support(
    [gaia_full_scaling],
    web_benefits_most,
    reason=(
        "@gaia_full_scaling provides the comparative numbers: GAIA-Web peak gain (+12.22) vs "
        "File/Reasoning/Others peak gain (+2.64). @web_benefits_most follows because DeepVerifier's "
        "follow-up questions primarily target information-retrieval vulnerabilities (Finding Sources "
        "category from @rubrics_from_taxonomy), which are more prevalent in web tasks."
    ),
    prior=0.87,
)
