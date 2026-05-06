"""Section 3: Problem Formulation.

Formalizes artifact refinement as a dynamical system over a pressure
landscape: state space, pressure landscape (signals + pressure
functions), four-phase tick dynamics (decay -> proposal -> validation
-> reinforcement), stable basins, locality constraint.

Source: Rodriguez 2026 [@Rodriguez2026PressureField], Section 3.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# 3.1 State space
# ---------------------------------------------------------------------------

setup_artifact_state_space = setting(
    "**Artifact state space.** An *artifact* consists of $n$ "
    "regions, where each region $i \\in \\{1, \\dots, n\\}$ has "
    "content $c_i \\in \\mathcal{C}$ (an arbitrary content space "
    "such as strings or Abstract Syntax Tree (AST) nodes) and "
    "auxiliary state $h_i \\in \\mathcal{H}$ representing "
    "confidence, fitness, and history. Regions are passive "
    "subdivisions of the artifact; agents are active proposers "
    "that observe regions and generate patches. The full system "
    "state is $s = ((c_1, h_1), \\dots, (c_n, h_n)) \\in "
    "(\\mathcal{C} \\times \\mathcal{H})^n$.",
    title="Setup: artifact state space (n regions, each with content c_i and auxiliary state h_i)",
)

# ---------------------------------------------------------------------------
# 3.2 Pressure landscape
# ---------------------------------------------------------------------------

setup_signal_function = setting(
    "**Signal function and locality.** A *signal function* "
    "$\\sigma: \\mathcal{C} \\to \\mathbb{R}^d$ maps a region's "
    "content to measurable features. Signals are *local*: "
    "$\\sigma(c_i)$ depends only on region $i$ -- not on other "
    "regions' content $c_j$ for $j \\ne i$.",
    title="Setup: signal function sigma : C -> R^d (local -- depends only on region i's content)",
)

setup_pressure_function = setting(
    "**Pressure function and pressure decomposition.** A *pressure "
    "function* $\\phi: \\mathbb{R}^d \\to \\mathbb{R}_{\\ge 0}$ maps "
    "signals to a scalar 'badness'. With $k$ pressure axes weighted "
    "by $w \\in \\mathbb{R}^k_{>0}$, the *region pressure* is "
    "$P_i(s) = \\sum_{j=1}^{k} w_j \\phi_j(\\sigma(c_i))$ and the "
    "*artifact pressure* is $P(s) = \\sum_{i=1}^{n} P_i(s)$. Low-"
    "pressure regions are 'valleys' where the artifact satisfies "
    "quality constraints.",
    title="Setup: pressure decomposition (P_i = sum_j w_j phi_j(sigma(c_i)); P(s) = sum_i P_i(s))",
)

# ---------------------------------------------------------------------------
# 3.3 System dynamics: four phases per tick
# ---------------------------------------------------------------------------

setup_phase_1_decay = setting(
    "**Phase 1: Decay.** Auxiliary state erodes toward a baseline "
    "each tick. Fitness $f_i$ and confidence $\\gamma_i$ components "
    "of $h_i$ obey: $f_i^{t+1} = f_i^t \\cdot e^{-\\lambda_f}$ and "
    "$\\gamma_i^{t+1} = \\gamma_i^t \\cdot e^{-\\lambda_\\gamma}$, "
    "with decay rates $\\lambda_f, \\lambda_\\gamma > 0$. Decay "
    "ensures that stability requires continuous reinforcement -- no "
    "region can become permanently 'solved'.",
    title="Setup: Phase 1 decay (exponential erosion of fitness and confidence)",
)

setup_phase_2_proposal = setting(
    "**Phase 2: Proposal.** For each region $i$ where pressure "
    "exceeds activation threshold ($P_i > \\tau_{act}$) and the "
    "region is *not inhibited*, each actor $a_k: \\mathcal{C} "
    "\\times \\mathcal{H} \\times \\mathbb{R}^d \\to \\mathcal{C}$ "
    "proposes a content transformation in parallel. **Each actor "
    "observes only local state $(c_i, h_i, \\sigma(c_i))$ -- actors "
    "do not communicate or coordinate their proposals.**",
    title="Setup: Phase 2 proposal (each actor sees only local state, proposes a patch in parallel)",
)

setup_phase_3_validation = setting(
    "**Phase 3: Validation.** When multiple patches are proposed, "
    "each is validated on an *independent fork* of the artifact. "
    "Forks are created by cloning artifact state; validation "
    "proceeds in parallel across forks. This addresses a "
    "fundamental resource constraint: a single artifact cannot be "
    "used to test multiple patches simultaneously without cloning.",
    title="Setup: Phase 3 validation (each patch tested on an independent fork)",
)

setup_phase_4_reinforcement = setting(
    "**Phase 4: Reinforcement.** Regions where actions were applied "
    "receive fitness and confidence boosts and enter an inhibition "
    "period preventing immediate re-modification: "
    "$f_i^{t+1} = \\min(f_i^t + \\Delta_f, 1)$ and "
    "$\\gamma_i^{t+1} = \\min(\\gamma_i^t + \\Delta_\\gamma, 1)$. "
    "Inhibition allows changes to propagate through the artifact "
    "and forces agents to address other high-pressure regions, "
    "preventing oscillation around local fixes.",
    title="Setup: Phase 4 reinforcement (fitness/confidence boost, inhibition cooldown)",
)

# ---------------------------------------------------------------------------
# 3.4 Stability and central questions
# ---------------------------------------------------------------------------

setup_stability_definition = setting(
    "**Definition 3.1 (Stability).** A state $s^*$ is *stable* if, "
    "under the system dynamics with no external perturbation, both "
    "(i) all region pressures are below activation threshold "
    "($P_i(s^*) < \\tau_{act}$ for all $i$), and (ii) decay is "
    "balanced by residual fitness, so the system remains in a "
    "neighborhood of $s^*$.",
    title="Setup: Definition 3.1 stability (all P_i < tau_act AND decay balanced by residual fitness)",
)

# ---------------------------------------------------------------------------
# 3.5 Locality constraint
# ---------------------------------------------------------------------------

setup_locality_constraint = setting(
    "**Locality constraint.** The constraint distinguishing this "
    "setting from centralized optimization: agents observe only "
    "local state. An actor at region $i$ sees only "
    "$(c_i, h_i, \\sigma(c_i))$ -- it does **not** see other "
    "regions' content $c_j$ for $j \\ne i$, the global pressure "
    "$P(s)$, or other agents' actions. Coordinated planning is "
    "ruled out; stability must emerge from local incentives aligned "
    "with global pressure reduction.",
    title="Setup: locality constraint (actors see only (c_i, h_i, sigma(c_i)) -- no global state, no peer actions)",
)

# ---------------------------------------------------------------------------
# Central design questions raised at the end of Section 3.4
# ---------------------------------------------------------------------------

claim_central_design_questions = claim(
    "**Central design questions raised by the formalism.** Four "
    "questions: (Q1) *Existence* -- under what conditions do stable "
    "basins exist? (Q2) *Quality* -- what is the pressure $P(s^*)$ "
    "of states in stable basins? (Q3) *Convergence* -- from initial "
    "state $s_0$, does the system reach a stable basin, and how "
    "quickly? (Q4) *Decentralization* -- can stability be achieved "
    "with purely local decisions? Sections 4-5 answer these "
    "questions: Q4 is answered by pressure alignment, Q1 / Q3 by "
    "Theorem 5.1 (convergence), Q2 by Theorem 5.2 (basin quality).",
    title="Setup: four central design questions (existence / quality / convergence / decentralization)",
)

__all__ = [
    "setup_artifact_state_space",
    "setup_signal_function",
    "setup_pressure_function",
    "setup_phase_1_decay",
    "setup_phase_2_proposal",
    "setup_phase_3_validation",
    "setup_phase_4_reinforcement",
    "setup_stability_definition",
    "setup_locality_constraint",
    "claim_central_design_questions",
]
