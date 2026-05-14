"""Priors for independent (leaf) claims in the 2512.04388 Conductor
formalization.

Calibration philosophy
----------------------

* **Numerical readouts from the paper's own tables** (Tables 1, 2, 5, 6,
  7, 8 -- per-benchmark per-model accuracy, token / cost columns, plus
  Tables 9, 10, 11 ablation rows) -- 0.92-0.95. Each cell is a directly
  measured value with multi-seed mean +/- SE. The prior is high but not
  0.97 because (a) the multi-column breadth gives more chances for
  transcription error and (b) some leaderboard columns aggregate the
  best-of-multiple-implementation runs which adds a small subjective
  judgment component.
* **Related-work characterizations** (RL-with-tools, multi-agent
  coordination literature summaries) -- 0.90. Author-stated descriptions
  of competing methods drawn from the cited papers directly.
* **Background framework result** (GRPO recipe yields thinking) -- 0.93.
  Replicated across DeepSeek-R1, o1, Gemini 2.5, Qwen3, Llama 4 -- broad
  cross-organization confirmation.
* **Abduction component prediction claims** (learned-coordination vs
  trivial alternatives) -- H at 0.55, Alt at 0.18. pi(Alt) is the
  probability that the trivial alternative *alone* explains the 5-fact
  fingerprint, NOT whether trivial alternatives correctly characterize
  any single isolated fact. Since trivial alternatives predict OPPOSITE
  signs for cost (more compute -> more tokens), agent diversity (no
  diversity should mean no gain), and untrained-LLM-as-Conductor (any
  LLM should suffice), pi(Alt) is held substantially below pi(H).
"""

# No leaf claims in motivation -- all motivation claims are derived
# from downstream evidence via the wiring strategies.
from .s2_rl_reasoning import (
    claim_grpo_yields_thinking,
)
from .s6_main_results import (
    claim_table1_full,
)
from .s7_controlled_eval import (
    claim_table5_efficiency_consensus,
    claim_table6_efficiency_baselines,
    claim_table7_full,
)
from .s8_user_recursion import (
    claim_table2_recursion_full,
)
from .s9_analysis_ablations import (
    claim_table9_ablations,
    claim_table10_agent_selection_ablation,
    claim_table11_conductor_replacement,
)
from .s10_related_work import (
    claim_rl_with_tools_literature,
    claim_multi_agent_coord_literature,
)
from .s12_wiring import (
    claim_pred_learned_coord_explains,
    claim_pred_alt_trivial_explains,
)


PRIORS: dict = {
    # -----------------------------------------------------------------
    # Background framework result: GRPO yields self-emergent thinking
    # -----------------------------------------------------------------
    claim_grpo_yields_thinking: (
        0.93,
        "Replicated cross-organizationally: DeepSeek-R1 "
        "[@Guo2025DeepSeekR1] introduced the GRPO + format/correctness "
        "recipe; OpenAI o1 [@Jaech2024OpenAIO1], Gemini 2.5 "
        "[@Comanici2025Gemini25], Qwen3 [@Yang2025Qwen3], Llama 4 "
        "[@MetaAI2025Llama4] all use related recipes that elicit "
        "self-emergent thinking. The high prior reflects broad "
        "cross-organization confirmation. Modest discount from 0.97 "
        "reflects that the 'self-emergent thinking' characterization "
        "involves some interpretive judgment about whether scratch-pad "
        "reasoning constitutes thinking.",
    ),

    # -----------------------------------------------------------------
    # Table 1: per-benchmark unconstrained accuracy
    # -----------------------------------------------------------------
    claim_table1_full: (
        0.93,
        "Table 1 reports per-task per-model unconstrained-setting "
        "accuracy for 7 baselines + Conductor across 7 benchmarks. "
        "Numbers are reported as the best of own re-evaluation, "
        "private implementation, and online leaderboard scores at "
        "matched precision (1 decimal for AIME25/GPQA-D, 2 decimals "
        "for BCB, etc.). The prior is 0.93 to reflect the multi-"
        "source aggregation (some cells take leaderboard best, others "
        "take re-evaluation), which adds modest uncertainty over a "
        "single-source-direct-measurement reading.",
    ),

    # -----------------------------------------------------------------
    # Table 2: recursion result on AIME25 / BCB / GPQA-D (constrained)
    # -----------------------------------------------------------------
    claim_table2_recursion_full: (
        0.94,
        "Table 2 reports Conductor and Conductor-Recursive performance "
        "across AIME25 / BCB / GPQA-D under the constrained setting "
        "in which the Conductor was originally trained. Single-source "
        "direct measurement; higher prior than Table 1 because the "
        "constrained setting uses uniform 4096-token / minimal-"
        "reasoning configuration without leaderboard aggregation.",
    ),

    # -----------------------------------------------------------------
    # Table 5: 5x consensus vs Conductor MMLU efficiency
    # -----------------------------------------------------------------
    claim_table5_efficiency_consensus: (
        0.93,
        "Table 5 reports per-method performance, token usage, USD "
        "cost, and cost-adjusted performance on MMLU under a 5x "
        "consensus / reflect setup. Direct measurement; cost-adjusted "
        "performance is derived arithmetic. Prior reflects the multi-"
        "column / multi-method breadth.",
    ),

    # -----------------------------------------------------------------
    # Table 6: efficiency across multi-agent baselines
    # -----------------------------------------------------------------
    claim_table6_efficiency_baselines: (
        0.93,
        "Table 6 reports per-method performance, token usage, and "
        "cost averaged across the 4 training tasks (MMLU/RLPR/LCB/"
        "MATH500). Direct measurement; the per-task disaggregation "
        "is in Table 7.",
    ),

    # -----------------------------------------------------------------
    # Table 7: full controlled-setting results
    # -----------------------------------------------------------------
    claim_table7_full: (
        0.94,
        "Table 7 reports the full per-task per-method controlled-"
        "setting comparison (4K-context / minimal-reasoning matching "
        "Conductor training-time config). All numbers are mean +/- "
        "standard error from up-to-16-run evaluations. Single-source "
        "direct measurement; higher prior than Table 1 because the "
        "controlled setting eliminates leaderboard-aggregation "
        "subjectivity.",
    ),

    # -----------------------------------------------------------------
    # Table 9: subtask / few-shot / fine-grained ablation
    # -----------------------------------------------------------------
    claim_table9_ablations: (
        0.93,
        "Table 9 reports 4 model variants (fine-grained / w/o "
        "few-shot / w/o subtasks / Conductor) on 4 in-domain "
        "benchmarks. Each ablation is a separate training run "
        "evaluated on the same test sets. Direct measurement; prior "
        "0.93 reflects the multi-cell breadth.",
    ),

    # -----------------------------------------------------------------
    # Table 10: agent-selection ablation (all-GPT-5)
    # -----------------------------------------------------------------
    claim_table10_agent_selection_ablation: (
        0.94,
        "Table 10 reports Conductor with all agents fixed to GPT-5 vs "
        "individual frontier workers vs full-pool Conductor across "
        "AIME / BCB / GPQA-D. Single-source direct measurement, "
        "small (3) per-row count, low transcription risk.",
    ),

    # -----------------------------------------------------------------
    # Table 11: frontier-LLM-as-Conductor ablation
    # -----------------------------------------------------------------
    claim_table11_conductor_replacement: (
        0.93,
        "Table 11 reports GPT-5/Gemini-as-Conductor variants (7-model "
        "and 3-model versions) vs trained 7B Conductor on LCB / AIME / "
        "BCB / GPQA-D. Includes automatic resampling on format "
        "failure and doubled output-token limit for fairness. Direct "
        "measurement; slight discount because of the per-baseline "
        "fairness adjustment.",
    ),

    # -----------------------------------------------------------------
    # Related-work category descriptions
    # -----------------------------------------------------------------
    claim_rl_with_tools_literature: (
        0.92,
        "The RL-with-tools literature characterization "
        "(RLEF [@Gehring2024RLEF], ReTool [@Feng2025ReTool], "
        "StepTool [@Yu2024StepTool], CodeRL [@Le2022CodeRL], "
        "WebGPT [@Nakano2021WebGPT]) is the literal scope of each "
        "cited work -- single-model RL + external deterministic tool. "
        "Consensus-level characterization.",
    ),
    claim_multi_agent_coord_literature: (
        0.91,
        "The MAS-coordination literature characterization (MASRouter "
        "[@Yue2025MASRouter], RouterDC [@Chen2024RouterDC], Smoothie "
        "[@Guha2024Smoothie], MoA [@Wang2024MoA], multi-agent debate "
        "[@Du2023MultiAgentDebate], GPTSwarm [@Zhuge2024GPTSwarm], "
        "evolving orchestration [@Dang2025EvolvingOrchestration]) -- "
        "the 'fixed-vocabulary topology + pre-specified options' "
        "framing is the literal stated approach of each cited work.",
    ),

    # -----------------------------------------------------------------
    # Abduction component prediction claims
    # -----------------------------------------------------------------
    claim_pred_learned_coord_explains: (
        0.55,
        "Hypothesis prediction: learned coordination (topology + "
        "prompt-engineering jointly via RL) predicts the 5-fact "
        "fingerprint (avg gain over best worker, low cost, all-GPT-5 "
        "Conductor lift, trained-vs-untrained gap, open-pool "
        "generalization). The prediction is precise and follows from "
        "the Conductor framework + emergent-skills observation; we "
        "hold the prior moderate (0.55) because the prediction itself "
        "is a claim about which mechanisms produce which fingerprints, "
        "not the underlying emergent-skills observation.",
    ),
    claim_pred_alt_trivial_explains: (
        0.18,
        "Alternative prediction: trivial confounds (pick-best-worker "
        "/ more-compute / cherry-picked-pools / any-LLM-as-Conductor) "
        "predict at most a single fact each in isolation. CRUCIALLY, "
        "pi(Alt) = 'can the trivial alternative alone explain the "
        "OBSERVED 5-fact pattern?' -- not 'can it explain any single "
        "isolated fact?'. Since trivial alternatives predict the "
        "OPPOSITE sign for fact (ii) compute (more compute = more "
        "tokens, but Conductor uses 1820 < MoA's 11203), and the "
        "OPPOSITE behavior for fact (iv) trained-vs-untrained "
        "Conductor (any LLM should work, but untrained falls -4 to "
        "-16 pp short), they cannot jointly explain the observed "
        "fingerprint. pi(Alt) is held low (0.18) because the "
        "alternative's explanatory power for the FULL fingerprint "
        "is poor, regardless of how correctly any individual "
        "confound description is.",
    ),
}


__all__ = ["PRIORS"]
