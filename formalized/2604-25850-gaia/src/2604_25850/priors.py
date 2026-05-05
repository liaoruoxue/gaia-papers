"""Priors for independent (leaf) claims in the 2604.25850 AHE formalization.

Calibration philosophy
----------------------

* **Numerical readouts from the paper's own tables and figures**
  (Table 1 per-method pass@1, Table 2 per-repo SWE numbers, Table 3
  ablation deltas, Fig. 3 cross-model deltas, Fig. 4 self-attribution
  metrics) -- 0.92-0.95. Each is a directly measured benchmark value
  with the per-difficulty / per-repo / per-base breakdown reproduced
  exactly from the source.
* **Method-description claims** (ACE, TF-GRPO, Codex CLI,
  Meta-Harness, related-work category descriptions) -- 0.9-0.94.
  Author-stated characterizations of competing methods drawn from
  those papers / blog posts directly.
* **Foundational coding-agent literature observations** (harness
  engineering as a research practice, evaluation-horizon coverage,
  reproducible-execution infrastructure) -- 0.88-0.92. Established
  practitioner / academic claims with broad support.
* **Foundational design principle** (every loop phase must be
  observable) -- 0.88. Author's stated design principle, not
  empirically falsifiable per se but well-grounded in the broader
  observability literature.
"""

from .motivation import (
    claim_main_terminal_headline,
)
from .s2_related_work import (
    claim_ace_method,
    claim_codex_human_baseline,
    claim_eval_infrastructure,
    claim_evaluation_horizons,
    claim_harness_engineering_definition,
    claim_meta_harness,
    claim_program_structure_methods,
    claim_prompt_instruction_methods,
    claim_self_critique_methods,
    claim_tfgrpo_method,
)
from .s3_setup import (
    claim_design_principle_observability,
)
from .s6_decision_observability import (
    claim_fix_attribution_quantitative,
    claim_per_round_regression_breakdown,
    claim_regression_attribution_quantitative,
)
from .s7_main_results import (
    claim_ace_pass1,
    claim_ahe_pass1,
    claim_codex_pass1,
    claim_iter2_peak,
    claim_iter5_peak,
    claim_iter6_peak,
    claim_iter8_peak,
    claim_other_human_baselines,
    claim_seed_pass1,
    claim_tfgrpo_pass1,
)
from .s8_transfer import (
    claim_deepseek_transfer,
    claim_gemini_transfer,
    claim_gpt54_med_transfer,
    claim_gpt54_xhigh_transfer,
    claim_qwen_transfer,
    claim_swe_aggregate_success,
    claim_swe_aggregate_tokens,
    claim_swe_table_tokens,
)
from .s9_ablations import (
    claim_memory_only_delta,
    claim_middleware_only_delta,
    claim_prompt_only_regression,
    claim_tool_only_delta,
)


PRIORS: dict = {
    # ---------------------------------------------------------------------
    # Per-method Terminal-Bench 2 pass@1 measurements (Table 1)
    # ---------------------------------------------------------------------
    claim_ahe_pass1: (
        0.93,
        "Table 1: AHE pass@1 = 77.0% on 89 Terminal-Bench 2 tasks "
        "with k=2 rollouts. Per-difficulty: 100/88.2/53.3 on "
        "easy/medium/hard. Direct measurement; modest discount for "
        "k=2 rollout variance and infrastructure-aborted-as-failure "
        "convention.",
    ),
    claim_seed_pass1: (
        0.94,
        "Table 1: NexAU0 seed = 69.7% on 89 Terminal-Bench 2 tasks. "
        "Per-difficulty: 87.5/78.2/51.7. Same measurement protocol; "
        "the seed is shared across ACE/TF-GRPO/AHE so this number is "
        "well-anchored across runs.",
    ),
    claim_codex_pass1: (
        0.92,
        "Table 1: Codex CLI = 71.9%. Per-difficulty: 75.0/80.0/56.7. "
        "Codex CLI is human-designed; the AHE paper measures it on "
        "the same 89-task panel.",
    ),
    claim_ace_pass1: (
        0.92,
        "Table 1: ACE = 68.9% (regresses below seed). Per-difficulty: "
        "91.7/78.2/48.9. Self-evolved from NexAU0 via the published "
        "ACE method.",
    ),
    claim_tfgrpo_pass1: (
        0.92,
        "Table 1: TF-GRPO = 72.3%. Per-difficulty: 100/79.4/55.6. "
        "Self-evolved from NexAU0 via the published TF-GRPO method.",
    ),
    claim_other_human_baselines: (
        0.92,
        "Table 1: opencode 47.2%, terminus-2 62.9%; both well below "
        "the seed and Codex CLI.",
    ),

    # ---------------------------------------------------------------------
    # SWE-bench-verified measurements (Table 2)
    # ---------------------------------------------------------------------
    claim_swe_aggregate_success: (
        0.93,
        "Table 2 first row: AHE 75.6% beats seed 75.2% (and ACE 74.6%, "
        "TF-GRPO 74.2%) on aggregate over 500 SWE-bench-verified tasks. "
        "n=500 is large; the per-repo concentrations support the "
        "aggregate.",
    ),
    claim_swe_aggregate_tokens: (
        0.94,
        "Table 2 first row tokens: AHE 461k vs seed 526k = -12.4% "
        "tokens. Same n=500; tokens-per-trial means are tightly "
        "measured (excluding only infrastructure-aborted trials per "
        "the Setup convention).",
    ),
    claim_swe_table_tokens: (
        0.93,
        "Table 2 right columns: per-repo Tokens_k means (461k "
        "aggregate; per-repo from 257k to 656k for AHE).",
    ),

    # ---------------------------------------------------------------------
    # Cross-model transfer (Fig. 3) -- the within-family points
    # (the cross-family points feed into the induction directly)
    # ---------------------------------------------------------------------
    claim_gpt54_med_transfer: (
        0.92,
        "Fig. 3: GPT-5.4 medium 65.7% -> 68.0%, +2.3 pp. Same model "
        "family, lower reasoning tier; transfer measured after "
        "applying the AHE harness without re-evolution.",
    ),
    claim_gpt54_xhigh_transfer: (
        0.92,
        "Fig. 3: GPT-5.4 xhigh 72.5% -> 74.7%, +2.3 pp. Same model "
        "family, higher reasoning tier with timeout-pressure caveat.",
    ),
    # NOTE: Cross-family transfers are observations -- they are also
    # conclusions of the induction's generative-direction supports, but
    # the source publishes their measured values directly. Setting priors
    # anchors them as data so the induction can lift the cross-family law.
    claim_qwen_transfer: (
        0.92,
        "Fig. 3: qwen-3.6-plus 56.2% -> 62.5%, +6.3 pp. Direct "
        "Terminal-Bench 2 measurement on the alternate base, no "
        "re-evolution.",
    ),
    claim_gemini_transfer: (
        0.92,
        "Fig. 3: gemini-3.1-flash-lite-preview 36.5% -> 41.6%, "
        "+5.1 pp. Direct Terminal-Bench 2 measurement.",
    ),
    claim_deepseek_transfer: (
        0.92,
        "Fig. 3: deepseek-v4-flash 51.7% -> 61.8%, +10.1 pp. "
        "Direct Terminal-Bench 2 measurement, the largest cross-"
        "family gain.",
    ),

    # NOTE: Per-iteration AHE peaks are observations from the case study
    # (Section C); they are also conclusions of the iteration-trajectory
    # induction's generative-direction supports. Setting priors anchors
    # them as observed peaks of the AHE iteration trajectory.
    claim_iter2_peak: (
        0.93,
        "Section C.2.1 + Fig. 7: iteration-2 winning round at commit "
        "c0b8a05 (prompt) + 169c34c (tool); flips db-wal-recovery; "
        "documented case study.",
    ),
    claim_iter5_peak: (
        0.93,
        "Section C.2.2 + Fig. 8: iteration-5 winning round at commit "
        "3ba3a90 (prompt + tool descriptor) + 4e0aab9 (tool impl); "
        "flips path-tracing; documented case study.",
    ),
    claim_iter6_peak: (
        0.93,
        "Section C.2.3 + Fig. 9: iteration-6 winning round at commit "
        "ff0cf3d (tool impl) + 9651986 (middleware); flips "
        "mcmc-sampling-stan; documented case study.",
    ),
    claim_iter8_peak: (
        0.94,
        "Section C.2.4 + Fig. 10: iteration-8 winning round at "
        "commit ca35f53 (tool impl) + a4a4a29 (middleware); flips "
        "configure-git-webserver / git-multibranch / polyglot-c-py "
        "/ polyglot-rust-c / pytorch-model-recovery / mteb-retrieve; "
        "lands at the run's high-water mark of 76.97%.",
    ),

    # ---------------------------------------------------------------------
    # Component ablation deltas (Table 3)
    # ---------------------------------------------------------------------
    claim_memory_only_delta: (
        0.92,
        "Table 3: + memory only = 75.3% (+5.6 pp aggregate). Hard +11.6 "
        "pp -- exceeds full AHE on Hard. Largest single-component "
        "lift; the Easy regression (-37.5 pp) is consistent with "
        "re-verification overhead.",
    ),
    claim_tool_only_delta: (
        0.92,
        "Table 3: + tools only = 73.0% (+3.3 pp aggregate). Medium "
        "+9.1 pp lands within 0.9 pp of full AHE on Medium.",
    ),
    claim_middleware_only_delta: (
        0.92,
        "Table 3: + middleware only = 71.9% (+2.2 pp aggregate). "
        "Easy +12.5 pp ties full AHE on Easy.",
    ),
    claim_prompt_only_regression: (
        0.93,
        "Table 3: + system_prompt only = 67.4% (-2.3 pp aggregate). "
        "The unambiguous regression here is the load-bearing piece "
        "of the factual-structure-transfers headline; the negative "
        "delta is what discriminates from the prompt-is-main-lever "
        "foil.",
    ),

    # ---------------------------------------------------------------------
    # Self-attribution metrics (Fig. 4 cross-iteration mean)
    # ---------------------------------------------------------------------
    claim_fix_attribution_quantitative: (
        0.93,
        "Fig. 4 left: cross-iteration fix-precision 33.7% / fix-recall "
        "51.4% (vs random baselines 6.5% / 10.6%, both 5x random).",
    ),
    claim_regression_attribution_quantitative: (
        0.93,
        "Fig. 4 right: cross-iteration regression-precision 11.8% / "
        "regression-recall 11.1% (vs random baselines 5.6% / 5.4%, "
        "both ~2x random).",
    ),
    claim_per_round_regression_breakdown: (
        0.92,
        "Appendix D: 43 regression predictions across 9 rounds, only "
        "5 landed; 40 unforeseen actual regressions. Cumulative P = "
        "11.6%, R = 11.1%.",
    ),

    # ---------------------------------------------------------------------
    # Method-description claims for related-work baselines
    # ---------------------------------------------------------------------
    claim_ace_method: (
        0.93,
        "ACE [@ACE]: prompt-context playbook self-evolution, "
        "documented in the original ACE paper (ICLR 2025).",
    ),
    claim_tfgrpo_method: (
        0.93,
        "TF-GRPO [@TFGRPO]: training-free trajectory-feedback policy "
        "optimization, documented in the original paper (Oct 2025).",
    ),
    claim_codex_human_baseline: (
        0.94,
        "Codex CLI is OpenAI's published human-designed coding-"
        "agent harness [@CodexCLI]; its design is documented in "
        "OpenAI's developer materials.",
    ),
    claim_meta_harness: (
        0.9,
        "Meta-Harness [@MetaHarness] is a recent (March 2026) end-"
        "to-end joint harness optimization approach; concurrent and "
        "the only prior work that targets multi-component harness "
        "evolution.",
    ),
    claim_self_critique_methods: (
        0.93,
        "Self-Refine / Reflexion / Critiq are documented self-"
        "critique optimizers in the literature; the AHE paper "
        "characterizes their editable surface as the agent's "
        "behavior at inference.",
    ),
    claim_prompt_instruction_methods: (
        0.93,
        "DSPy / ACE / TF-GRPO / MIPRO / GEPA are documented "
        "prompt-instruction optimizers; the AHE paper characterizes "
        "their editable surface as the system prompt or in-context "
        "playbook.",
    ),
    claim_program_structure_methods: (
        0.93,
        "Voyager / AlphaEvolve / ADAS / AFlow / Symbolic Learning "
        "are documented program-structure optimizers; the AHE paper "
        "characterizes their editable surface as the program graph "
        "or agent archive.",
    ),

    # ---------------------------------------------------------------------
    # Foundational coding-agent literature observations
    # ---------------------------------------------------------------------
    claim_harness_engineering_definition: (
        0.92,
        "Harness engineering as a research / engineering practice is "
        "extensively documented across [@RajasekaranHarness; "
        "@Lopopolo; @Trivedy; @ClaudeCode; @OpenClaw; @SWEAgent; "
        "@OpenHands]. The definition is consensus-level.",
    ),
    claim_evaluation_horizons: (
        0.92,
        "Coding-agent benchmark coverage spans function-level "
        "[@LiveCodeBench; @BigCodeBench], repo-scale [@SWEbench; "
        "@SWEbenchMM; @SWEbenchPro], and terminal multi-hour "
        "[@SWELancer; @MLEbench; @TerminalBench2]. Established.",
    ),
    claim_eval_infrastructure: (
        0.9,
        "Reproducible-execution infrastructure ([@SWEGym; @R2EGym; "
        "@SWEHub]) packages executable runtimes and verifiers; "
        "documented in those papers and repos.",
    ),

    # ---------------------------------------------------------------------
    # Design principle (motivation)
    # ---------------------------------------------------------------------
    claim_design_principle_observability: (
        0.88,
        "Design principle that every loop phase must produce "
        "structured agent-readable artifacts. Author-stated "
        "principle; well-grounded in broader observability and "
        "context-engineering literature [@ContextEngineering; "
        "@AgentDebugger]; not empirically falsifiable per se but "
        "the entire AHE design rests on it.",
    ),

    # ---------------------------------------------------------------------
    # Motivation-section main headline (also a leaf because the wiring
    # also derives it from arithmetic; we keep a moderate prior since
    # it is also a primary author-stated empirical claim)
    # ---------------------------------------------------------------------
    # NOTE: claim_main_terminal_headline is *derived* in the wiring -- the
    # arithmetic strategy strat_main_terminal_headline derives it from
    # the per-method scores. So we do NOT set its prior here.
}
