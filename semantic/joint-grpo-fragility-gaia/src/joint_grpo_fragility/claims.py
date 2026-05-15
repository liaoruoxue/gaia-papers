"""Joint claims across 3 RL papers — GRPO fragility + counter-evidence.

Three papers, two opposing framings:

  PRO (GRPO has systemic weakness):
    - DART (2602.00994): seesaw under multi-capability GRPO training
    - TPO (2604.06159): GRPO fails on sparse-reward tasks

  CON (GRPO is fine, baselines were broken):
    - SFT-then-RL (2604.23747): published mixed-policy gains over GRPO/SFT
      were artifacts of two framework bugs; corrected SFT+GRPO matches or
      beats all mixed-policy methods.

The joint conclusion accepts the "systemic weakness" framing but qualifies
it: weakness is real on certain axes (sparse reward, multi-capability)
yet does not extend to standard math-reasoning where corrected baselines
plus GRPO already win. The skeptical paper acts as a boundary premise
inside the joint deduction — it scopes the systemic-weakness claim.
"""

import importlib
from gaia.lang import claim, support, deduction

_dart_mot = importlib.import_module("2602_00994.motivation")
_tpo_mot = importlib.import_module("2604_06159.motivation")
_sft_mot = importlib.import_module("2604_23747.motivation")

seesaw_phenomenon = _dart_mot.seesaw_phenomenon
tpo_excels_on_sparse_reward = _tpo_mot.tpo_excels_on_sparse_reward
mixed_policy_gains_are_artifact = _sft_mot.mixed_policy_gains_are_artifact
sft_then_rl_sufficient = _sft_mot.sft_then_rl_sufficient


# ── Counter-evidence as boundary premise (in scope of the joint claim) ──

bdry_grpo_fine_on_corrected_math = claim(
    "On standard math reasoning at 7-8B with framework bugs corrected, "
    "simple SFT-then-RL using GRPO matches or beats all mixed-policy "
    "methods. So the GRPO-fragility claim does not extend to this domain.",
    title="Boundary: GRPO is sufficient on math + corrected baselines",
    aggregated_from=[
        "2604_23747::mixed_policy_gains_are_artifact",
        "2604_23747::sft_then_rl_sufficient",
    ],
    semantic_refs=["grpo_has_systemic_weakness"],
    boundary_type="scope",
    stated_explicitly=False,
)


# ── Joint conclusion ──

grpo_has_systemic_weakness = claim(
    "GRPO-based agent RL exhibits structural failures on multi-capability "
    "training (seesaw) and sparse-reward tasks (policy-gradient vanishing). "
    "These are independent failure modes on different axes, so the "
    "fragility is not bug-induced. However, on standard math reasoning at "
    "7-8B with corrected baselines, GRPO is sufficient — so the systemic "
    "weakness is *axis-specific*, not universal.",
    title="Joint: GRPO has axis-specific systemic weakness",
    aggregated_from=[
        "2602_00994::seesaw_phenomenon",
        "2604_06159::tpo_excels_on_sparse_reward",
        "2604_23747::mixed_policy_gains_are_artifact",
    ],
)


# ── Strategies ──
# Use deduction: weakness claim depends on (positive evidence + boundary).
# If counter-evidence (bdry_grpo_fine_on_corrected_math) gets stronger,
# BP reverse-flow penalises the boundary premise — i.e., we'd flag that
# the weakness claim's scope must shrink.

strat_joint_grpo_fragility = deduction(
    [
        seesaw_phenomenon,
        tpo_excels_on_sparse_reward,
        bdry_grpo_fine_on_corrected_math,
        # Reference SFT's claims directly so BP threads through SFT's subgraph
        mixed_policy_gains_are_artifact,
        sft_then_rl_sufficient,
    ],
    grpo_has_systemic_weakness,
    reason=(
        "Two independent failure modes (capability axis + reward axis) "
        "support a systemic-weakness reading; the SFT-then-RL boundary "
        "premise + the actual SFT findings (mixed_policy_gains_are_artifact, "
        "sft_then_rl_sufficient) scope that weakness to 'not on standard "
        "math'. If a fourth paper extended the failure to math (e.g., "
        "corrected SFT+GRPO breaking on a new math benchmark), BP would "
        "reverse-pressure the boundary premise."
    ),
    prior=0.82,
)
