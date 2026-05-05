"""Section 5 (Conclusion) + Limitations.

Synthesis claims, abduction-alternative scaffolding, and the three named
limitations. Source: Lin et al. 2026 [@Lin2026AHE], Section 5 + Limitations.
"""

from gaia.lang import claim

# ===========================================================================
# Synthesis: closing argument that observability-driven evolution works
# ===========================================================================

claim_observability_driven_evolution_works = claim(
    "**Synthesis: observability-driven harness evolution is a practical "
    "pathway to keep coding-agent harnesses continually improving "
    "alongside their base models.** The combination of (i) the +7.3 pp "
    "Terminal-Bench 2 main result, (ii) the +0.4 pp aggregate / -12% "
    "tokens cross-benchmark transfer to SWE-bench-verified, (iii) the "
    "+5.1 to +10.1 pp cross-family transfer across three alternate "
    "model families, and (iv) the component-localization finding that "
    "tools / middleware / memory carry the gain shows that AHE's three "
    "observability pillars provide a working substrate for autonomous "
    "harness evolution under a fixed base model.",
    title="Synthesis: observability-driven harness evolution is a practical pathway",
)

claim_complementary_to_model_training = claim(
    "**AHE positions harness-level evolution as a complementary axis to "
    "model-side training.** Model-side training updates the weights; "
    "harness-level evolution updates the externalized, auditable "
    "interface around the weights. The two axes need not compete: "
    "harness evolution provides an externalized surface where coding-"
    "agent experience can accumulate while base models are retrained "
    "or replaced.",
    title="Synthesis: harness-level evolution is complementary, not competing, with model-side training",
)

# ===========================================================================
# Foil claims for contradictions / abduction (Pass 2)
# ===========================================================================

claim_alt_manual_only = claim(
    "**Foil position 1: harness engineering must remain manual.** Under "
    "this position, the editorial judgment required to read failure "
    "patterns and craft component-level fixes is uniquely human, and "
    "any autonomous evolution loop would either (i) fail to converge "
    "(trial-and-error degenerates) or (ii) converge to a local optimum "
    "that a human-engineered harness still beats. This is the "
    "prevailing assumption that motivates manual harness practices "
    "[@OpenClaw; @Trivedy].",
    title="Foil 1: harness engineering must remain manual (autonomous evolution cannot converge stably)",
)

claim_alt_prompt_is_main_lever = claim(
    "**Foil position 2: the system prompt is the main lever in coding-"
    "agent design.** Under this position, careful prompt engineering "
    "(including evolved playbooks like ACE [@ACE]) captures most of "
    "the available gain in a coding agent's harness, and tool / "
    "middleware / memory edits are second-order. This view is "
    "implicit in the design of single-surface optimizers (ACE, "
    "TF-GRPO, GEPA, MIPRO, DSPy [@ACE; @TFGRPO; @GEPA; @MIPRO; "
    "@DSPy]).",
    title="Foil 2: system prompt is the main lever (tool/middleware/memory are second-order)",
)

# ===========================================================================
# Abduction structure: AHE's 3-pillar design vs. trivial alternatives
# ===========================================================================

claim_obs_3pillar_pattern = claim(
    "**Discriminating observation pattern.** Three observable patterns "
    "co-occur in the AHE experiments: (a) the **+7.3 pp main result** "
    "on the optimization target (Terminal-Bench 2 with GPT-5.4 high), "
    "(b) **transfer without re-evolution** -- +0.4 pp aggregate / "
    "-12% tokens to SWE-bench-verified plus +5.1 to +10.1 pp on three "
    "cross-family bases, and (c) the **component-localization "
    "ablation** showing tools / middleware / memory each carry the "
    "gain alone while the system prompt regresses. The conjunction is "
    "the observation any explanation must account for.",
    title="Observation pattern: main result + transfer + component-localized ablation, all together",
)

claim_pred_3pillar_explains = claim(
    "**Prediction under the 3-pillar hypothesis.** Under the "
    "hypothesis that AHE's three observability pillars (component / "
    "experience / decision) cause the gain, we expect (a) the "
    "Evolve Agent to converge to better harnesses on the optimization "
    "target (component-observability action space + decision-"
    "observability rollback are sufficient signal), (b) frozen "
    "components to transfer because the gains live in factual "
    "structure rather than benchmark-specific tuning (Pillar 1's "
    "decoupling exposes structure), and (c) the gain to localize to "
    "tools / middleware / memory (factual structure) rather than the "
    "system prompt (prose-level strategy). The conjunction of (a), "
    "(b), and (c) is the unique fingerprint of the 3-pillar design.",
    title="Prediction (H): 3-pillar design predicts main result + transfer + factual-structure localization",
)

claim_pred_alt_explains = claim(
    "**Prediction under the trivial alternatives.** Each trivial "
    "alternative explanation predicts only a strict subset of the "
    "observed pattern: "
    "(Alt-A) **Bigger LM / more compute**: predicts the main result "
    "(stronger model converges to better harness via bigger context "
    "window) but does NOT predict component-localization to tools / "
    "middleware / memory specifically -- a bigger LM should help all "
    "components equally. "
    "(Alt-B) **More iterations**: predicts incremental gain on the "
    "optimization target but does NOT predict cross-family transfer "
    "of +5.1 to +10.1 pp -- iteration count cannot create general "
    "structure. "
    "(Alt-C) **Benchmark-specific overfitting**: predicts the +7.3 pp "
    "Terminal-Bench 2 gain but predicts the *opposite* of cross-"
    "benchmark transfer (overfitting should regress on SWE-bench-"
    "verified) and the *opposite* of cross-family transfer "
    "(overfitting should regress on alternate base models).",
    title="Prediction (Alt): trivial alternatives explain only subsets, predict opposite of transfer",
)

# ===========================================================================
# Limitations
# ===========================================================================

claim_lim_benchmark_scope = claim(
    "**Limitation 1: benchmark scope.** Evaluation drives evolution on "
    "Terminal-Bench 2 and probes transfer on SWE-bench-verified. Even "
    "though the frozen harness transfers to a second task surface and "
    "to three alternate base-model families, broader programming "
    "languages, repository-scale deployments, and human-in-the-loop "
    "workflows remain untested.",
    title="Limitation 1: benchmark scope (terminal + SWE-Python only; broader languages/repos/human workflows untested)",
)

claim_lim_operating_point = claim(
    "**Limitation 2: evolution operating point.** AHE's step budget "
    "and per-task timeout were fitted to GPT-5.4 high during "
    "evolution, so cross-model transfer numbers conflate harness "
    "portability with operating-point coupling. Within one family the "
    "gain is non-monotone across reasoning tiers (medium +2.3, high "
    "+7.3, xhigh +2.3). Untangling these factors will require re-"
    "running the loop under multiple operating points.",
    title="Limitation 2: operating-point coupling (timeout/budget fitted to GPT-5.4 high; non-monotone within family)",
)

claim_lim_self_modification_governance = claim(
    "**Limitation 3: self-modification governance is incomplete.** "
    "AHE bounds edits to a workspace, attributes every change in a "
    "versioned manifest, and rolls back ineffective edits at file "
    "granularity, but it does not provide a complete guardrail "
    "stack. Long-horizon harness cleanup and stronger misuse "
    "prevention remain incomplete, and AHE should be viewed as a "
    "controlled research prototype rather than a fully mature "
    "autonomous self-improvement system.",
    title="Limitation 3: self-modification governance is incomplete (research prototype, not mature)",
)

claim_lim_two_evolution_limits = claim(
    "**Limitation 4 (stated in the contributions): two limits of "
    "agent-driven evolution.** (i) Harness components interact non-"
    "additively, so stacking effective edits *caps* the aggregate "
    "gain (sum of single-component gains 11.1 > full AHE 7.3, see "
    "Section 4.4). (ii) The loop's self-attribution is reliable for "
    "fixes (5x random) but blind to regressions (only 2x random), "
    "pinpointing regression foresight as the clearest direction for "
    "future self-evolution loops (Section 4.4.2).",
    title="Limitation 4: non-additive component interactions cap aggregate gain; regression foresight is blind",
)

__all__ = [
    "claim_observability_driven_evolution_works",
    "claim_complementary_to_model_training",
    "claim_alt_manual_only",
    "claim_alt_prompt_is_main_lever",
    "claim_obs_3pillar_pattern",
    "claim_pred_3pillar_explains",
    "claim_pred_alt_explains",
    "claim_lim_benchmark_scope",
    "claim_lim_operating_point",
    "claim_lim_self_modification_governance",
    "claim_lim_two_evolution_limits",
]
