"""Section IV.A-IV.B: Experimental setup and the five-stage progressive
ablation study.

Section IV of [@Abtahi2026Memanto] presents Memanto's empirical evaluation
on LongMemEval and LoCoMo. Subsection IV.A defines the evaluation
protocol; IV.B walks through five sequential ablation stages, each
isolating one architectural decision.

Each stage is extracted as separate atomic claims for the *configuration*
and the *measured outcome* (so theory and observation can be cleanly
related in Pass 2). The five Stage tables (III, IV, V, VI, plus the
Stage-5 final) are transcribed verbatim into claim content.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# IV.A Evaluation protocol
# ---------------------------------------------------------------------------

setup_evaluation_protocol = setting(
    "**Evaluation protocol.** All experiments employ Memanto's vector-"
    "only architecture with the Moorcheh ITS engine as the sole "
    "retrieval backend [@Abtahi2026Memanto, Sec. IV.A; Appendix A]. "
    "LongMemEval is run on the standard $S$ setting (full 500-question "
    "suite, approximately 115K tokens / approximately 50 sessions). "
    "LoCoMo is run on its standard split. Claude Sonnet 4 serves as "
    "the LLM judge throughout all stages; it also serves as the "
    "*inference model* for Stages 1-4, with Gemini 3 used at Stage 5. "
    "Answer-generation and judge prompts are adapted from the Hindsight "
    "repository [@Hindsight] to mitigate two systematic evaluation "
    "artefacts: answerer refusal on ambiguous questions, and rigid "
    "judge rejection of responses that are semantically correct but "
    "lexically divergent.",
    title="Setup: evaluation protocol -- vector-only Memanto + Moorcheh ITS, Hindsight-adapted prompts, Sonnet 4 judge",
)

# ---------------------------------------------------------------------------
# IV.B Stage 1 -- Naive baseline
# ---------------------------------------------------------------------------

setup_stage1_config = setting(
    "**Stage 1 configuration.** Standard semantic search with retrieval "
    "limit $k = 10$, ITS similarity threshold = 0.15, Claude Sonnet 4 "
    "as inference model [@Abtahi2026Memanto, Sec. IV.B.1; Table III].",
    title="Setup: Stage 1 config -- $k=10$, threshold=0.15, Sonnet 4",
)

claim_stage1_results = claim(
    "**Stage 1 result -- naive baseline establishes the floor.** "
    "Stage 1 yields the following accuracies, establishing a "
    "performance floor for a minimally parameterised RAG implementation "
    "on Memanto:\n\n"
    "| Benchmark | Accuracy |\n"
    "|-----------|---------:|\n"
    "| LongMemEval | 56.6% |\n"
    "| LoCoMo | 76.2% |\n\n"
    "The 19.6 percentage-point (pp) gap is *not* a session-length "
    "difference (the two datasets are comparable on session length); it "
    "reflects question structure and information accessibility. "
    "LongMemEval queries are longer and span multiple topics, "
    "distributing the semantic signal across a broader embedding space "
    "and reducing similarity scores for relevant chunks; under "
    "threshold 0.15 this information often falls below the cutoff "
    "[@Abtahi2026Memanto, Table III; Sec. IV.B.1].",
    title="Stage 1: 56.6% LongMemEval / 76.2% LoCoMo (baseline floor)",
    metadata={
        "figure": "artifacts/2604.22085.pdf, Table III",
        "caption": "Stage 1 naive baseline. k=10, threshold=0.15, Claude Sonnet 4.",
    },
)

# ---------------------------------------------------------------------------
# IV.B Stage 2 -- Recall expansion
# ---------------------------------------------------------------------------

setup_stage2_config = setting(
    "**Stage 2 configuration -- recall expansion.** Retrieval limit "
    "increased to $k = 40$ chunks; ITS similarity threshold relaxed to "
    "0.10 [@Abtahi2026Memanto, Sec. IV.B.2; Table IV].",
    title="Setup: Stage 2 config -- $k=40$, threshold=0.10",
)

claim_stage2_results = claim(
    "**Stage 2 result -- single largest gain across all five stages.** "
    "Recall expansion yields:\n\n"
    "| Benchmark | Accuracy | Delta vs Stage 1 |\n"
    "|-----------|---------:|-----------------:|\n"
    "| LongMemEval | 77.0% | +20.4 pp |\n"
    "| LoCoMo | 82.8% | +6.6 pp |\n\n"
    "This single parameter adjustment ($k=10 \\to 40$, threshold "
    "$0.15 \\to 0.10$) constitutes the largest single improvement "
    "observed across all five stages [@Abtahi2026Memanto, Table IV; "
    "Sec. IV.B.2].",
    title="Stage 2: +20.4 pp on LongMemEval (largest single-stage gain)",
    metadata={
        "figure": "artifacts/2604.22085.pdf, Table IV",
        "caption": "Stage 2 recall expansion. k=40, threshold=0.10.",
    },
)

claim_stage2_finding = claim(
    "**Stage 2 finding: the precision-recall tradeoff in agentic memory "
    "skews decisively toward recall.** Providing the LLM a broader, "
    "noisier candidate set and relying on its in-context reasoning to "
    "filter irrelevant content is substantially more effective than "
    "constraining retrieval to a narrow, high-precision window that "
    "risks excluding critical fragments. Multi-session questions "
    "frequently require synthesis of facts distributed across "
    "temporally disjoint sessions [@LongMemEval], so a fixed top-$k=10$ "
    "is a *critical architectural bottleneck* for agentic memory "
    "[@Abtahi2026Memanto, Sec. IV.B.2].",
    title="Stage 2 finding: agentic memory needs recall, not precision",
)

# ---------------------------------------------------------------------------
# IV.B Stage 3 -- Prompt optimisation
# ---------------------------------------------------------------------------

setup_stage3_config = setting(
    "**Stage 3 configuration -- prompt optimisation.** Retrieval "
    "parameters unchanged from Stage 2 ($k=40$, threshold=0.10); answer-"
    "generation and judge prompts replaced with optimised variants from "
    "the Hindsight repository [@Hindsight; @Abtahi2026Memanto, "
    "Sec. IV.B.3; Table V].",
    title="Setup: Stage 3 config -- Stage 2 retrieval + Hindsight-style prompts",
)

claim_stage3_results = claim(
    "**Stage 3 result -- prompt optimisation contributes only marginal "
    "gains.** Replacing the prompts yields:\n\n"
    "| Benchmark | Accuracy | Delta vs Stage 2 |\n"
    "|-----------|---------:|-----------------:|\n"
    "| LongMemEval | 79.2% | +2.2 pp |\n"
    "| LoCoMo | 82.9% | +0.1 pp |\n\n"
    "[@Abtahi2026Memanto, Table V; Sec. IV.B.3].",
    title="Stage 3: +2.2 pp / +0.1 pp (marginal prompt-optimisation gain)",
    metadata={
        "figure": "artifacts/2604.22085.pdf, Table V",
        "caption": "Stage 3 prompt optimisation. Hindsight-style answer + judge prompts.",
    },
)

claim_stage3_finding = claim(
    "**Stage 3 finding: prompt engineering yields only marginal "
    "improvements when retrieval is the bottleneck.** When the retrieval "
    "layer fails to surface relevant content, no degree of prompt "
    "refinement compensates for the resulting structural deficit. As "
    "foundation-model capabilities continue to advance, the relative "
    "contribution of prompt design diminishes in proportion to the "
    "quality of the underlying retrieval mechanism "
    "[@Abtahi2026Memanto, Sec. IV.B.3].",
    title="Stage 3 finding: prompts cannot compensate for retrieval failure",
)

# ---------------------------------------------------------------------------
# IV.B Stage 4 -- Maximum recall
# ---------------------------------------------------------------------------

setup_stage4_config = setting(
    "**Stage 4 configuration -- maximum recall.** Dynamic retrieval "
    "limit expanded to a maximum of $k = 100$ chunks, governed by "
    "ITS-threshold gating rather than a fixed-$k$ constraint; "
    "similarity threshold lowered to 0.05 [@Abtahi2026Memanto, "
    "Sec. IV.B.4; Table VI].",
    title="Setup: Stage 4 config -- dynamic $k$ up to 100 governed by ITS, threshold=0.05",
)

claim_stage4_motivation = claim(
    "**Stage 4 motivation: error analysis traced Stage 3 failures to "
    "missed retrievals, not LLM confusion.** Error analysis of Stage 3 "
    "failures established that incorrect answers were attributable not "
    "to LLM confusion arising from expanded context [@LostMiddle], but "
    "to semantic search consistently failing to retrieve critical "
    "sentences embedded within otherwise largely irrelevant chunks "
    "[@Abtahi2026Memanto, Sec. IV.B.4].",
    title="Stage 4 motivation: errors are missed retrievals, not LLM long-context degradation",
)

claim_stage4_results = claim(
    "**Stage 4 result -- maximum-recall yields large gains on both "
    "benchmarks.** Dynamic $k=100$ + threshold=0.05 yields:\n\n"
    "| Benchmark | Accuracy | Delta vs Stage 3 |\n"
    "|-----------|---------:|-----------------:|\n"
    "| LongMemEval | 85.0% | +5.8 pp |\n"
    "| LoCoMo | 86.3% | +3.4 pp |\n\n"
    "[@Abtahi2026Memanto, Table VI; Sec. IV.B.4].",
    title="Stage 4: +5.8 pp / +3.4 pp (maximum recall)",
    metadata={
        "figure": "artifacts/2604.22085.pdf, Table VI",
        "caption": "Stage 4 maximum recall. Dynamic k=100, threshold=0.05.",
    },
)

claim_stage4_finding = claim(
    "**Stage 4 finding: modern LLMs tolerate noisy retrieval context; "
    "extending retrieval budget consistently outperforms engineering for "
    "retrieval precision.** High-dimensional vector search is "
    "susceptible to distortion by multi-topic chunks in which a single "
    "critical detail is co-located with predominantly irrelevant "
    "content. Extending the retrieval budget to accommodate such cases "
    "consistently outperforms engineering for retrieval precision, "
    "confirming that *recall is the dominant lever for agentic memory "
    "performance* [@Abtahi2026Memanto, Sec. IV.B.4].",
    title="Stage 4 finding: recall is the dominant lever; LLMs tolerate noise",
)

# ---------------------------------------------------------------------------
# IV.B Stage 5 -- Inference model upgrade
# ---------------------------------------------------------------------------

setup_stage5_config = setting(
    "**Stage 5 configuration -- inference-model upgrade.** Retrieval "
    "parameters unchanged from Stage 4; inference model upgraded from "
    "Claude Sonnet 4 to Gemini 3 to establish parity with leading "
    "competing systems [@Abtahi2026Memanto, Sec. IV.B.5].",
    title="Setup: Stage 5 config -- Stage 4 retrieval + Gemini 3 inference",
)

claim_stage5_results = claim(
    "**Stage 5 result -- Memanto's final SOTA configuration.** The "
    "inference-model upgrade contributes:\n\n"
    "| Benchmark | Accuracy | Delta vs Stage 4 |\n"
    "|-----------|---------:|-----------------:|\n"
    "| LongMemEval | 89.8% | +4.8 pp |\n"
    "| LoCoMo | 87.1% | +0.8 pp |\n\n"
    "These are Memanto's final reported scores [@Abtahi2026Memanto, "
    "Fig. 5; Sec. IV.B.5].",
    title="Stage 5: 89.8% LongMemEval / 87.1% LoCoMo (final config, Gemini 3)",
    metadata={
        "figure": "artifacts/2604.22085.pdf, Fig. 5",
        "caption": "Progressive ablation waterfall across all 5 stages.",
    },
)

# ---------------------------------------------------------------------------
# Cumulative ablation summary
# ---------------------------------------------------------------------------

claim_ablation_waterfall = claim(
    "**Cumulative ablation waterfall (Fig. 5).** Stage-by-stage "
    "accuracies on both benchmarks:\n\n"
    "| Stage | Description | LongMemEval | LoCoMo |\n"
    "|-------|-------------|------------:|-------:|\n"
    "| S1 | Baseline (k=10, thr=0.15, Sonnet 4) | 56.6% | 76.2% |\n"
    "| S2 | Recall expansion (k=40, thr=0.10) | 77.0% | 82.8% |\n"
    "| S3 | Prompt optimisation | 79.2% | 82.9% |\n"
    "| S4 | Maximum recall (k=100, thr=0.05) | 85.0% | 86.3% |\n"
    "| S5 | Gemini 3 inference | 89.8% | 87.1% |\n\n"
    "Stage 2 (recall expansion) delivers the largest single gain "
    "(+20.4 pp on LongMemEval), confirming that retrieval tuning rather "
    "than architectural complexity is the dominant performance driver. "
    "Stage 3 (prompt optimisation) contributes only +2.2 pp; Stages 4 "
    "and 5 contribute +5.8 and +4.8 pp respectively "
    "[@Abtahi2026Memanto, Fig. 5].",
    title="Cumulative ablation waterfall: retrieval tuning >> prompt + model upgrades",
    metadata={
        "figure": "artifacts/2604.22085.pdf, Fig. 5",
        "caption": "Progressive ablation waterfall across S1-S5 on LongMemEval and LoCoMo.",
    },
)

claim_recall_tokencost_tradeoff = claim(
    "**Accuracy-vs-$k$ inflection at $k=40$, with token cost rising "
    "approximately fourfold (Fig. 6).** Both LongMemEval and LoCoMo "
    "accuracy curves plateau above $k=60$ with a clear inflection at "
    "$k=40$. The accuracy gain from $k = 10 \\to 40$ (+20.4 pp on "
    "LongMemEval) far outweighs the approximately fourfold token-cost "
    "increase, validating the *recall over precision* principle "
    "quantitatively [@Abtahi2026Memanto, Fig. 6].",
    title="Fig. 6: accuracy plateau above k=60, inflection at k=40; +20.4 pp >> 4x token cost",
    metadata={
        "figure": "artifacts/2604.22085.pdf, Fig. 6",
        "caption": "Accuracy vs k (left axis) and avg tokens/query (right axis dotted).",
    },
)

# ---------------------------------------------------------------------------
# Synthesis: stages support population finding
# ---------------------------------------------------------------------------

claim_recall_dominates = claim(
    "**Synthesis: recall, not architectural complexity, is the dominant "
    "performance driver for agentic memory.** The five-stage ablation "
    "decomposes Memanto's 33.2 pp LongMemEval gain (S1 -> S5) into: "
    "+20.4 pp recall expansion (S2) > +5.8 pp maximum recall (S4) > "
    "+4.8 pp model upgrade (S5) > +2.2 pp prompt optimisation (S3). "
    "Two of the three largest gains (S2 and S4) come from the same "
    "lever -- expanding the retrieval budget. Combined, retrieval "
    "tuning explains 26.2 / 33.2 = 79% of the total gain "
    "[@Abtahi2026Memanto, Sec. IV.B; Sec. V.B].",
    title="Synthesis: 79% of total gain comes from retrieval tuning; recall is the dominant lever",
)

__all__ = [
    "setup_evaluation_protocol",
    "setup_stage1_config",
    "claim_stage1_results",
    "setup_stage2_config",
    "claim_stage2_results",
    "claim_stage2_finding",
    "setup_stage3_config",
    "claim_stage3_results",
    "claim_stage3_finding",
    "setup_stage4_config",
    "claim_stage4_motivation",
    "claim_stage4_results",
    "claim_stage4_finding",
    "setup_stage5_config",
    "claim_stage5_results",
    "claim_ablation_waterfall",
    "claim_recall_tokencost_tradeoff",
    "claim_recall_dominates",
]
