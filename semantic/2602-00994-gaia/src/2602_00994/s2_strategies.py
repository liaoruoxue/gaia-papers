"""Layer 2 strategies — semantically meaningful reasoning chains.

Replaces Layer 1's compiler-generated __implication_* glue with
human-reviewed strategy types: induction (generalization), abduction
(alternative explanation), support (direct evidence), contradiction.
"""

from gaia.lang import support, induction, abduction, contradiction
from 2602_00994.motivation import (
    seesaw_phenomenon, gradient_conflict_is_root_cause,
    dart_solves_gradient_conflict, dart_vs_alternatives,
    leas_diagnostic_framework, no_llama_validation, single_turn_scope,
)


# ── Core evidential chain ──

strat_seesaw_to_conflict = support(
    [seesaw_phenomenon],
    gradient_conflict_is_root_cause,
    reason=(
        "The seesaw pattern alone shows capability trade-off exists. "
        "The jump to 'gradient conflict is the cause' requires excluding "
        "alternative mechanisms. The data-mixture experiment (varying "
        "reasoning/tool-use ratio fails to resolve interference) rules "
        "out data imbalance. LEAS's negative λ23 interaction coefficients "
        "directly measure gradient-level interference. Excluding data "
        "imbalance as a cause strengthens the gradient-conflict "
        "explanation from post-hoc to diagnostic."
    ),
    prior=0.88,
)

strat_conflict_to_dart = support(
    [gradient_conflict_is_root_cause],
    dart_solves_gradient_conflict,
    reason=(
        "If gradient conflict is the root cause, then isolating gradients "
        "per capability should resolve it. DART structurally guarantees "
        "zero interaction term (x23=0) via hard token-level routing. The "
        "stronger the gradient-conflict diagnosis, the stronger the case "
        "that DART works for the right mechanistic reason rather than by "
        "accident. The remaining gap is whether gradient conflict is the "
        "ONLY interference mechanism — the paper doesn't test for others."
    ),
    prior=0.85,
)


# ── Generalization via induction ──

strat_dart_cross_backbone = induction(
    [
        "obs_dart_better_reasoning_3b",   # Qwen3-8B: +4.91 MATH
        "obs_dart_better_reasoning_7b",   # Qwen3-7B: +3.82
        "obs_dart_better_reasoning_2_5",  # Qwen2.5-7B: +3.15
        "obs_rank_insensitive",           # Robust to LoRA rank
    ],
    dart_solves_gradient_conflict,
    reason=(
        "DART improvement is consistent (+3.15 to +4.91) across three "
        "backbone/model-size combinations. Rank insensitivity (Fig 5) "
        "suggests the routing mechanism, not adapter capacity, drives "
        "the gain. However: no Llama-series validation, no >7B evidence."
    ),
    prior=0.85,
)


# ── Alternative explanation check ──

alt_data_mix = claim(
    "The observed DART improvement could be explained by the specific "
    "data mixture rather than the architectural change to gradient "
    "isolation.",
    title="Alternative: data mixture explains DART improvement",
)

alt_2agent_capacity = claim(
    "2-agent baselines' slight edge (~1.2pp) over DART could indicate "
    "that DART's single-model architecture imposes a small but real "
    "capacity ceiling compared to independent models.",
    title="Alternative: residual 2-agent gap suggests capacity ceiling",
)

strat_dart_abduction = abduction(
    dart_solves_gradient_conflict,
    [dart_solves_gradient_conflict, alt_data_mix],
    reason=(
        "Three evidence points favor DART's gradient-isolation mechanism "
        "over the data-mixture alternative: (1) 2-agent baseline uses "
        "identical data and performs worse than DART on some benchmarks, "
        "(2) the rank sweep (Fig 5) shows improvement is independent of "
        "adapter capacity, which a data-mixture account cannot explain, "
        "(3) LEAS's λ23 measure reverses sign under DART, providing a "
        "mechanism-level confirmation. However the 2-agent gap (~1.2pp) "
        "warrants treating alt_2agent_capacity as a live alternative."
    ),
    prior=0.78,
)


# ── Boundary condition marking ──

strat_boundary_contradiction = contradiction(
    dart_solves_gradient_conflict,
    alt_2agent_capacity,
    reason=(
        "DART structurally guarantees zero gradient interaction, but the "
        "residual ~1.2pp gap to 2-agent baselines is consistent with a "
        "small capacity ceiling in the single-model design. This tension "
        "— perfect gradient isolation but imperfect performance parity — "
        "is the paper's most interesting unresolved question. It may "
        "indicate that gradient conflict is the dominant but not the only "
        "interference mechanism in multi-capability ARL."
    ),
)
