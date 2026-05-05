"""Section 4.2 (RQ1): main results on Terminal-Bench 2.

AHE outperforms human-designed and self-evolving baselines.

Source: Lin et al. 2026 [@Lin2026AHE], Section 4.2 + Table 1 + Fig. 1.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# Headline panel: per-method scores from Table 1
# ---------------------------------------------------------------------------

claim_terminal_results_table = claim(
    "**Table 1: pass@1 on Terminal-Bench 2 (89 tasks).** Per-method "
    "results by official difficulty bucket; bold marks per-column "
    "best (ties all bold).\n\n"
    "| Method | All (89) | Easy (4) | Med (55) | Hard (30) |\n"
    "|---|---:|---:|---:|---:|\n"
    "| **Human-designed harness** | | | | |\n"
    "| opencode | 47.2% | 75.0% | 52.7% | 33.3% |\n"
    "| terminus-2 | 62.9% | 75.0% | 74.5% | 40.0% |\n"
    "| Codex CLI | 71.9% | 75.0% | 80.0% | **56.7%** |\n"
    "| **Self-evolved from NexAU0** | | | | |\n"
    "| NexAU0 (seed) | 69.7% | 87.5% | 78.2% | 51.7% |\n"
    "| ACE | 68.9% | 91.7% | 78.2% | 48.9% |\n"
    "| TF-GRPO | 72.3% | **100.0%** | 79.4% | 55.6% |\n"
    "| **AHE** | **77.0%** | **100.0%** | **88.2%** | 53.3% |\n",
    title="Table 1: Terminal-Bench 2 pass@1 per method per difficulty",
    metadata={
        "figure": "artifacts/2604.25850.pdf, Table 1",
        "caption": "Table 1: pass@1 on Terminal-Bench 2 across 89 tasks by official difficulty.",
    },
)

# ---------------------------------------------------------------------------
# Per-baseline comparison numbers (atomic claims for downstream reasoning)
# ---------------------------------------------------------------------------

claim_ahe_pass1 = claim(
    "**AHE achieves pass@1 = 77.0% on Terminal-Bench 2 (89 tasks, "
    "GPT-5.4 high).** This is the best result obtained by the AHE "
    "campaign of 10 iterations starting from the bash-only NexAU0 "
    "seed, with $k=2$ rollouts per task per iteration. Per-difficulty: "
    "100.0% (4 easy), 88.2% (55 medium), 53.3% (30 hard).",
    title="Result: AHE pass@1 = 77.0% on Terminal-Bench 2",
)

claim_seed_pass1 = claim(
    "**The bash-only NexAU0 seed achieves pass@1 = 69.7% on Terminal-"
    "Bench 2.** This is the common starting point for all three self-"
    "evolution loops (ACE, TF-GRPO, AHE). Per-difficulty: 87.5% "
    "(easy), 78.2% (medium), 51.7% (hard).",
    title="Result: NexAU0 seed pass@1 = 69.7% on Terminal-Bench 2",
)

claim_codex_pass1 = claim(
    "**Codex CLI [@CodexCLI] (human-designed) achieves pass@1 = 71.9% "
    "on Terminal-Bench 2.** Codex CLI is the strongest of three "
    "human-designed harnesses on the AHE comparison panel. Per-"
    "difficulty: 75.0% (easy), 80.0% (medium), 56.7% (hard, the panel "
    "leader on Hard).",
    title="Result: Codex CLI pass@1 = 71.9% on Terminal-Bench 2",
)

claim_ace_pass1 = claim(
    "**ACE [@ACE] (self-evolved from NexAU0) achieves pass@1 = 68.9% "
    "on Terminal-Bench 2.** ACE evolves only the in-context playbook; "
    "it regresses 0.8 pp below the seed NexAU0 (69.7%). Per-"
    "difficulty: 91.7% (easy), 78.2% (medium), 48.9% (hard).",
    title="Result: ACE pass@1 = 68.9% on Terminal-Bench 2 (regresses below seed)",
)

claim_tfgrpo_pass1 = claim(
    "**TF-GRPO [@TFGRPO] (self-evolved from NexAU0) achieves pass@1 = "
    "72.3% on Terminal-Bench 2.** TF-GRPO reinforces successful tool "
    "sequences via prompt-injected priors. Per-difficulty: 100.0% "
    "(easy), 79.4% (medium), 55.6% (hard).",
    title="Result: TF-GRPO pass@1 = 72.3% on Terminal-Bench 2",
)

claim_other_human_baselines = claim(
    "**Other human-designed baselines on Terminal-Bench 2.** opencode "
    "[@Opencode] achieves pass@1 = 47.2% and terminus-2 [@Terminus2] "
    "achieves pass@1 = 62.9%; both are well below the bash-only "
    "NexAU0 seed (69.7%) and below Codex CLI (71.9%). Per-difficulty: "
    "opencode 75.0%/52.7%/33.3%; terminus-2 75.0%/74.5%/40.0%.",
    title="Result: opencode 47.2% / terminus-2 62.9% on Terminal-Bench 2",
)

# ---------------------------------------------------------------------------
# Iteration trajectory (Fig. 1): the per-iteration AHE panel
# ---------------------------------------------------------------------------

claim_iteration_trajectory = claim(
    "**Iteration trajectory (Fig. 1): pass@1 climbs across 10 "
    "iterations, with four named peaks at iterations 2, 5, 6, 8.** The "
    "best-so-far curve shows the gain accumulating across iterations: "
    "starting from the seed at 69.7% (iteration 0), pass@1 rises with "
    "AHE evolutions, hitting four named peaks corresponding to four "
    "winning rounds: peak 1 at iteration 2 (contract-first prompt + "
    "tunable shell timeout, prompt + tool), peak 2 at iteration 5 "
    "(publish-state guard, prompt + tool), peak 3 at iteration 6 "
    "(cross-step risk monitor, middleware), peak 4 at iteration 8 "
    "(post-success hard-block + pre-turn risk salience, tool + "
    "middleware). Final iteration-8 best-so-far peaks at 76.97%.",
    title="Result: 10-iteration trajectory has 4 named peaks at iter 2, 5, 6, 8",
    metadata={
        "figure": "artifacts/2604.25850.pdf, Fig. 1",
        "caption": "Fig. 1: AHE evolves a bash-only seed past every human-designed and self-evolving baseline on Terminal-Bench 2.",
    },
)

# Per-iteration evidence -- semantically distinct events used for the
# induction over the trajectory.
claim_iter2_peak = claim(
    "**Iteration-2 peak (commit `c0b8a05` + `169c34c`, level: prompt + "
    "tool implementation).** Two changes: a 68-line append to "
    "`workspace/systemprompt.md` containing eight numbered rules "
    "(contract-first workflow), and a tunable shell timeout argument "
    "added to `run_shell_command`. Lift on Terminal-Bench 2: above "
    "seed 69.7%; this is the contract-first peak. Sample beneficiary: "
    "`db-wal-recovery` flips from 1/2 to 2/2 (verifier asserts every "
    "row's value, contract-first rule reroutes the agent off the "
    "cached-stdout shortcut).",
    title="Iter-2 peak: contract-first prompt + tunable shell timeout (prompt + tool)",
    metadata={
        "figure": "artifacts/2604.25850.pdf, Fig. 7 + Fig. 5",
        "caption": "Fig. 7: chg-1 + chg-2 manifest entries shipped at iteration 2. Fig. 5: db-wal-recovery before/after chg-1.",
    },
)

claim_iter5_peak = claim(
    "**Iteration-5 peak (commit `3ba3a90` + `4e0aab9`, level: prompt + "
    "tool descriptor + tool implementation).** Two changes: append "
    "publish-state + scratch-directory + literal-output rules to "
    "system prompt and tool descriptor; install a stateful publish-"
    "state guard inside the shell tool (parses the acceptance command "
    "for protected paths, blocks later destructive commands, accepts "
    "explicit `ALLOW_POST_SUCCESS_RESET` override). Sample beneficiary: "
    "`path-tracing` flips from 0/2 to 2/2 because the guard "
    "intercepts `rm -rf /app/reconstructed.ppm` after the self-check.",
    title="Iter-5 peak: publish-state mechanism (prompt rules + shell-tool guard)",
    metadata={
        "figure": "artifacts/2604.25850.pdf, Fig. 8",
        "caption": "Fig. 8: chg-7 + chg-8 manifest entries shipped at iteration 5.",
    },
)

claim_iter6_peak = claim(
    "**Iteration-6 peak (commit `ff0cf3d` + `9651986`, level: tool "
    "implementation + middleware).** Two changes: extend the publish-"
    "state guard to script entrypoints (any script tied to a passing "
    "evaluator becomes protected); register "
    "`ExecutionRiskHintsMiddleware` that scans live shell commands for "
    "seven risk patterns (shallow validation, localhost-only validation, "
    "inline proxy validator, low-level model API, missing comparator, "
    "repeated long timeouts, repeated retries). Sample beneficiary: "
    "`mcmc-sampling-stan` flips from 0/2 to 2/2 after 5 failed "
    "iterations (the middleware flags grid-integration as a proxy "
    "validator; the extended guard protects `analysis.R`).",
    title="Iter-6 peak: protected entrypoints + execution-risk middleware (tool + middleware)",
    metadata={
        "figure": "artifacts/2604.25850.pdf, Fig. 9 + Fig. 6",
        "caption": "Fig. 9: chg-1 + chg-2 manifest entries shipped at iteration 6. Fig. 6: mcmc-sampling-stan before/after.",
    },
)

claim_iter8_peak = claim(
    "**Iteration-8 peak (commit `ca35f53` + `a4a4a29`, level: tool "
    "implementation + middleware).** Two changes: upgrade two soft "
    "reasons in the publish-state guard to *hard blocks* (deletion of "
    "non-/tmp protected output; reset of non-/tmp protected root) -- "
    "the override token can no longer wipe verified live deliverables; "
    "add `BeforeModelHook` to the ExecutionRiskHintsMiddleware that "
    "promotes execution-risk notes into FRAMEWORK reminders visible "
    "in the next model turn. Beneficiaries: `configure-git-webserver` "
    "and `git-multibranch` flip via the hard-block path; "
    "`polyglot-c-py`, `polyglot-rust-c`, `pytorch-model-recovery`, "
    "`mteb-retrieve` flip via the salience-promotion path. Iteration "
    "8's overall score lands at **76.97%**, the run's high-water mark "
    "and the single biggest jump.",
    title="Iter-8 peak: hard blocks + FRAMEWORK reminders (tool + middleware); 76.97% high-water mark",
    metadata={
        "figure": "artifacts/2604.25850.pdf, Fig. 10",
        "caption": "Fig. 10: chg-1 + chg-2 manifest entries shipped at iteration 8.",
    },
)

# ---------------------------------------------------------------------------
# Aggregate margin claims (atomic differences)
# ---------------------------------------------------------------------------

claim_margin_vs_seed = claim(
    "**AHE margin vs seed: +7.3 pp.** Aggregate Terminal-Bench 2 "
    "pass@1: AHE 77.0% - NexAU0 69.7% = +7.3 pp. This is the headline "
    "AHE gain over its own starting point.",
    title="Margin: AHE - NexAU0 = +7.3 pp on Terminal-Bench 2",
)

claim_margin_vs_codex = claim(
    "**AHE margin vs Codex CLI: +5.1 pp.** Aggregate Terminal-Bench 2 "
    "pass@1: AHE 77.0% - Codex CLI 71.9% = +5.1 pp. AHE surpasses the "
    "best human-designed harness in the comparison panel.",
    title="Margin: AHE - Codex CLI = +5.1 pp on Terminal-Bench 2",
)

claim_margin_vs_ace = claim(
    "**AHE margin vs ACE: +8.1 pp.** Aggregate Terminal-Bench 2 "
    "pass@1: AHE 77.0% - ACE 68.9% = +8.1 pp.",
    title="Margin: AHE - ACE = +8.1 pp on Terminal-Bench 2",
)

claim_margin_vs_tfgrpo = claim(
    "**AHE margin vs TF-GRPO: +4.7 pp.** Aggregate Terminal-Bench 2 "
    "pass@1: AHE 77.0% - TF-GRPO 72.3% = +4.7 pp.",
    title="Margin: AHE - TF-GRPO = +4.7 pp on Terminal-Bench 2",
)

claim_hard_tier_exception = claim(
    "**Hard-tier exception: AHE marginally trails Codex CLI on Hard "
    "(53.3% vs 56.7%).** The only cell where AHE is not at the panel "
    "best is the Hard column (30 tasks): AHE 53.3% vs Codex CLI "
    "56.7%, a 3.4 pp deficit. The paper traces this gap to "
    "interference between AHE's components on long-horizon tasks "
    "rather than a missing capability: ablation Section 4.4 shows "
    "that swapping AHE's long-term memory alone into the NexAU0 seed "
    "(without the other AHE components) achieves 63.3% on Hard, "
    "which exceeds Codex CLI on Hard.",
    title="Result: Hard-tier exception (AHE 53.3% vs Codex CLI 56.7%); attributed to component interference",
)

# ---------------------------------------------------------------------------
# Synthesis claims
# ---------------------------------------------------------------------------

claim_ahe_beats_human_baselines = claim(
    "**AHE outperforms every human-designed harness on the panel.** On "
    "Terminal-Bench 2 aggregate pass@1: AHE 77.0% > Codex CLI 71.9% > "
    "terminus-2 62.9% > opencode 47.2%. AHE achieves this without any "
    "manual harness engineering, starting from a single-bash-tool seed.",
    title="Synthesis: AHE > all human-designed harnesses on Terminal-Bench 2 aggregate",
)

claim_ahe_beats_self_evolution_baselines = claim(
    "**AHE outperforms both self-evolving baselines starting from the "
    "same seed.** On Terminal-Bench 2 aggregate: AHE 77.0% > "
    "TF-GRPO 72.3% > NexAU0 69.7% > ACE 68.9%. ACE and TF-GRPO both "
    "edit only one harness component (in-context playbook / "
    "trajectory-distribution prior); AHE's joint multi-component "
    "evolution captures gains they cannot reach.",
    title="Synthesis: AHE > both self-evolving baselines (ACE, TF-GRPO) from same seed",
)

claim_layer_mismatch_explanation = claim(
    "**The gap to ACE and TF-GRPO traces to a layer mismatch.** ACE "
    "distills natural-language playbooks the agent reads in-context, "
    "and TF-GRPO is a trajectory-feedback variant of GRPO that "
    "reinforces successful tool sequences; starting from the same "
    "NexAU0 seed as AHE, neither method opens the surrounding "
    "scaffolding (tools, middleware, long-term memory) to edits. AHE "
    "jointly evolves system prompt, tools, middleware, and long-term "
    "memory across iterations -- precisely the components Section "
    "4.4 quantifies as carrying the gain.",
    title="Synthesis: ACE/TF-GRPO gap = layer mismatch (they cannot edit tools/middleware/memory; AHE can)",
)

__all__ = [
    "claim_terminal_results_table",
    "claim_ahe_pass1",
    "claim_seed_pass1",
    "claim_codex_pass1",
    "claim_ace_pass1",
    "claim_tfgrpo_pass1",
    "claim_other_human_baselines",
    "claim_iteration_trajectory",
    "claim_iter2_peak",
    "claim_iter5_peak",
    "claim_iter6_peak",
    "claim_iter8_peak",
    "claim_margin_vs_seed",
    "claim_margin_vs_codex",
    "claim_margin_vs_ace",
    "claim_margin_vs_tfgrpo",
    "claim_hard_tier_exception",
    "claim_ahe_beats_human_baselines",
    "claim_ahe_beats_self_evolution_baselines",
    "claim_layer_mismatch_explanation",
]
