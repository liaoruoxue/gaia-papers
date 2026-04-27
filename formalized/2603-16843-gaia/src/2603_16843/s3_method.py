"""Section 3: LEAFE — Tree-Based Experience Generation + Experience Distillation."""

from gaia.lang import claim, setting, support

from .motivation import (
    setup_agent,
    setup_rlvr,
    setup_passk,
    claim_rich_feedback,
    claim_rlvr_underuses_feedback,
    claim_distribution_sharpening,
    claim_agency_internalization,
)

# ── Settings: method definitions ─────────────────────────────────────────────

setup_step_dynamics = setting(
    "Environment dynamics are defined by $\\mathrm{Step}(\\cdot)$: "
    "$E_{t+1}, o_{t+1} \\leftarrow \\mathrm{Step}(E_t, a_t)$. Executing action "
    "$a_t$ in environment state $E_t$ transitions to $E_{t+1}$ and yields "
    "observation $o_{t+1}$. Rollouts terminate at horizon $T$ or upon a terminal "
    "condition (success or irreversible failure).",
    title="Environment transition dynamics"
)

setup_reflection = setting(
    "Every $K$ steps or upon failure, the policy is invoked with the interaction "
    "history $h_t$ and a reflection prompt $p_{\\mathrm{refl}}$ to produce a "
    "rollback target $\\tau \\in \\{1, \\dots, t\\}$ and a natural-language "
    "experience summary $e$: $(\\tau, e) \\sim \\pi_\\theta(\\cdot | h_t, "
    "p_{\\mathrm{refl}})$. $\\tau$ marks the step where the trajectory deviated; "
    "$e$ is a brief diagnosis-and-fix instruction.",
    title="Periodic reflection procedure"
)

setup_branching = setting(
    "**Branching via rollback:** Given $(\\tau, e)$, the environment is reset and "
    "the original action prefix $a_{1:\\tau-1}$ is replayed to reach state "
    "$E_\\tau$ and history $h_\\tau$. The policy then samples a revised action "
    "$a'_\\tau \\sim \\pi_\\theta(\\cdot | h_\\tau, q, e)$ conditioned on the "
    "experience summary, and the new branch continues from "
    "$E'_{\\tau+1} \\leftarrow \\mathrm{Step}(E_\\tau, a'_\\tau)$. Branch "
    "requests are managed with a queue-based BFS strategy until a maximum tree "
    "depth or attempt budget is reached.",
    title="Rollback + BFS branching"
)

setup_rehearsal_loss = setting(
    "**Behavior rehearsal loss.** For each successful trajectory in the "
    "rehearsal dataset $\\mathcal{D}_{\\mathrm{reh}}$ (rejection-sampled from "
    "successful rollouts including branched ones), state-action pairs $(h_t, a_t)$ "
    "are extracted and the loss "
    "$\\mathcal{L}_{\\mathrm{reh}}(\\theta') = -\\mathbb{E}_{(h,a) \\sim "
    "\\mathcal{D}_{\\mathrm{reh}}}[\\log \\pi_{\\theta'}(a | h, q)]$ is "
    "minimized. This preserves the agent's baseline competence.",
    title="Rehearsal loss (Lreh)"
)

setup_cf_loss = setting(
    "**Counterfactual (experience-to-policy) distillation loss.** For each "
    "branching event in $\\mathcal{D}_{\\mathrm{refl}}$ at round $\\tau$ with "
    "experience-improved action $a'_\\tau$, the model is trained to produce "
    "$a'_\\tau$ from the **original** experience-free history $h_\\tau$: "
    "$\\mathcal{L}_{\\mathrm{cf}}(\\theta') = -\\mathbb{E}_{(h_\\tau, a'_\\tau) "
    "\\sim \\mathcal{D}_{\\mathrm{refl}}}[\\log \\pi_{\\theta'}(a'_\\tau | "
    "h_\\tau, q)]$. The natural-language experience $e$ is dropped at training "
    "time so that recovery becomes intrinsic at test time.",
    title="Counterfactual loss (Lcf)"
)

setup_total_loss = setting(
    "The LEAFE training objective is the sum "
    "$\\mathcal{L}(\\theta') = \\mathcal{L}_{\\mathrm{cf}}(\\theta') + \\beta "
    "\\mathcal{L}_{\\mathrm{reh}}(\\theta')$, where $\\beta$ is a "
    "hyperparameter scaling rehearsal strength.",
    title="LEAFE total objective"
)

# ── Claims: method properties / design rationale ─────────────────────────────

claim_experience_as_intervention = claim(
    "Linguistic feedback is qualitative and unstructured, making it hard to "
    "internalize via standard token-level optimization. LEAFE addresses this by "
    "treating experience as a **contextual intervention**: the experience "
    "summary $e$ is concatenated to the prompt and induces a policy shift via "
    "the input context, rather than entering the loss directly during exploration.",
    title="Experience as a contextual intervention"
)

claim_branching_targets_failures = claim(
    "Stage 1 branching produces trajectories with the structure "
    "**failure → rollback → fix → success**, explicitly targeting the critical "
    "decision points where the original rollout went wrong. Successful branches "
    "supply paired $(h_\\tau, a_\\tau)$ vs. $(h_\\tau, a'_\\tau)$ examples that "
    "are unavailable to outcome-driven RL [@LiGARollback2025; @WangHOPE].",
    title="Branching produces failure → fix → success traces"
)

claim_cf_internalizes_recovery = claim(
    "By training $\\pi_{\\theta'}$ to produce the corrected action $a'_\\tau$ "
    "from the **experience-free** history $h_\\tau$, the counterfactual loss "
    "$\\mathcal{L}_{\\mathrm{cf}}$ maps the experience-augmented decision back "
    "into the original context. This expands the policy's intrinsic action "
    "distribution with experience-induced alternatives, making corrected actions "
    "more probable without requiring an explicit reflection step at inference.",
    title="Lcf internalizes corrective revisions into model weights"
)

claim_lreh_stabilizes = claim(
    "The rehearsal loss $\\mathcal{L}_{\\mathrm{reh}}$ acts as an "
    "anti-forgetting regularizer: by maximizing the likelihood of action "
    "sequences from successful trajectories, it preserves baseline task "
    "competence while $\\mathcal{L}_{\\mathrm{cf}}$ adapts the model toward "
    "corrective behaviors [@Ahn2024].",
    title="Lreh preserves baseline competence"
)

claim_initialization_grpo = claim(
    "LEAFE is initialized from a GRPO-trained checkpoint and further optimized "
    "with $\\mathcal{L}_{\\mathrm{cf}} + \\beta \\mathcal{L}_{\\mathrm{reh}}$. "
    "It therefore composes with — rather than replaces — outcome-driven RL.",
    title="LEAFE composes on top of GRPO checkpoints"
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_branching_targets = support(
    [claim_rich_feedback, claim_experience_as_intervention],
    claim_branching_targets_failures,
    reason=(
        "Because environments emit diagnostic feedback that pinpoints failure "
        "causes (@claim_rich_feedback), the reflection step can identify a "
        "specific failure point $\\tau$ and synthesize a targeted fix $e$. "
        "Treating $e$ as a context intervention (@claim_experience_as_intervention) "
        "lets the policy explore the alternative branch $a'_\\tau$ directly "
        "from $h_\\tau$, producing the failure → rollback → fix → success "
        "structure that outcome-only methods cannot generate."
    ),
    prior=0.85,
    background=[setup_reflection, setup_branching, setup_step_dynamics]
)

strat_cf_internalizes = support(
    [claim_branching_targets_failures, claim_experience_as_intervention],
    claim_cf_internalizes_recovery,
    reason=(
        "The branching procedure (@claim_branching_targets_failures) yields "
        "$(h_\\tau, a'_\\tau)$ pairs in which the corrected action was elicited "
        "by the experience $e$. Training the model to reproduce $a'_\\tau$ from "
        "$h_\\tau$ alone (with $e$ removed, see @setup_cf_loss) is exactly the "
        "operation of distilling the contextual intervention "
        "(@claim_experience_as_intervention) into the parameters of "
        "$\\pi_{\\theta'}$. After distillation the corrected action carries "
        "intrinsic probability under the experience-free policy, so recovery "
        "no longer requires an explicit reflection turn at inference."
    ),
    prior=0.82,
    background=[setup_cf_loss]
)

# Note: claim_lreh_stabilizes is treated as a leaf claim — the regularizing
# role of an imitation-learning loss on successful trajectories is a standard
# property of supervised learning, not a derivation in this paper. The reason
# above is stated in setup_rehearsal_loss and the textbook fact [@Ahn2024].
