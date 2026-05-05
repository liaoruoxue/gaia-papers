"""Section 4: Linear Effect Attribution System (LEAS).

LEAS is a diagnostic framework that decomposes question-level correctness into
per-capability and pairwise-interaction effects, then identifies the sign of
the reasoning-tool interaction term $\\lambda_{23}$. A negative sign means
the two capabilities **interfere** under joint optimization. The section
contains: 4.1 the formalism (Defs. 4.1-4.2, Assumption 4.3, Eqs. 4-7);
4.2 the construction of six model variants populating the design matrix;
4.3 the empirical analysis on NQ + HotpotQA showing that interference
dominates and is driven by gradient conflict.
"""

from gaia.lang import claim, setting, support, deduction

from .motivation import (
    claim_capabilities_are_heterogeneous,
    claim_seesaw_phenomenon,
    claim_contribution_leas,
    claim_joint_assumption_unexamined,
)
from .s3_preliminaries import (
    setup_role_router,
    setup_token_partition,
    setup_masked_objective,
    setup_policy_gradient,
)

# ---------------------------------------------------------------------------
# 4.1 Formalism (Definitions and assumption are settings)
# ---------------------------------------------------------------------------

setup_capability_indicators = setting(
    "**Definition 4.1 (capability indicators).** An agent's capabilities are "
    "encoded by three binary indicators: base capability $x_1$, tool-use "
    "$x_2$, and reasoning $x_3$. Each $x_i \\in \\{0,1\\}$.",
    title="Definition 4.1: capability indicators $x_1, x_2, x_3$",
)

setup_interaction_indicators = setting(
    "**Definition 4.2 (interaction indicators).** Pairwise interaction "
    "indicators $x_{ij} \\in \\{0,1\\}$ are set to 1 if and only if "
    "capabilities $i$ and $j$ are *jointly optimized in the same parameter "
    "subspace*, and 0 otherwise. Hybrid inference (composing separately "
    "trained models at decoding time) does **not** activate any "
    "interaction indicator.",
    title="Definition 4.2: pairwise interaction indicators $x_{12}, x_{13}, x_{23}$",
)

setup_capability_vector = setting(
    "**Capability indicator vector.** Each model $\\mathcal{M}$ is "
    "associated with a fixed binary vector "
    "$x_\\mathcal{M} = [x_1, x_2, x_3, x_{12}, x_{13}, x_{23}] "
    "\\in \\{0,1\\}^6$ (Eq. 4).",
    title="Capability vector $x_\\mathcal{M}$ (Eq. 4)",
)

setup_logit_model = setting(
    "**Assumption 4.3 (logit model).** The expected correctness of model "
    "$\\mathcal{M}$ on question $q$ is modeled as "
    "$$s^q_\\mathcal{M} = \\sigma(x_\\mathcal{M}^\\top \\lambda^q),"
    "\\qquad \\lambda^q = [\\lambda_1^q, \\lambda_2^q, \\lambda_3^q, "
    "\\lambda_{12}^q, \\lambda_{13}^q, \\lambda_{23}^q]$$ (Eq. 5), where "
    "$\\sigma$ is the sigmoid. $\\lambda_i^q$ are *main effects*, "
    "$\\lambda_{ij}^q$ are *interaction effects*. The model is used for "
    "**attribution** (sign of $\\lambda_{ij}^q$), not for prediction.",
    title="Assumption 4.3: logit-additive correctness model (Eq. 5)",
)

setup_logit_transform = setting(
    "Applying the logit transform to Eq. 5 gives a linear equation "
    "$z^q_\\mathcal{M} = \\log \\frac{s^q_\\mathcal{M}}{1-s^q_\\mathcal{M}} "
    "= x_\\mathcal{M}^\\top \\lambda^q$ (Eq. 6). Stacking six such equations "
    "yields the linear system $z^q = X \\lambda^q$ (Eq. 7), where $X$ is "
    "the **design matrix** whose rows are the six capability vectors.",
    title="Linear system $z^q = X \\lambda^q$ (Eqs. 6-7)",
)

setup_identifiability_condition = setting(
    "To uniquely identify $\\lambda^q \\in \\mathbb{R}^6$, the six rows of "
    "$X$ must be **linearly independent**. The six model variants in "
    "Section 4.2 are constructed to satisfy this.",
    title="Identifiability requires six linearly-independent capability vectors",
)

setup_attribution_only = setting(
    "**Remark 4.4.** Although Eq. 5 superficially resembles logistic "
    "regression, LEAS uses it for **attribution rather than prediction**: "
    "the goal is to identify the *sign* of $\\lambda_{ij}^q$ "
    "($\\lambda_{ij}^q > 0$ = synergy; $\\lambda_{ij}^q < 0$ = "
    "interference) -- not to model absolute correctness probabilities.",
    title="Remark 4.4: LEAS does attribution, not prediction",
)

# ---------------------------------------------------------------------------
# Definitional setup of the closed-form contrast (Appendix C)
# ---------------------------------------------------------------------------

setup_contrast_formula = setting(
    "**Closed-form contrast (Appendix C, Eq. 19).** Plugging the four "
    "capability vectors $x_\\text{Uni}, x_\\text{Tool}, x_\\text{Reas}, "
    "x_\\text{Base}$ (defined in Section 4.2) into Eq. 5 gives "
    "$\\lambda_{23}^q = z^q_\\text{Uni} - z^q_\\text{Tool} - z^q_\\text{Reas} "
    "+ z^q_\\text{Base}$. Equivalently (Eq. 20), "
    "$\\lambda_{23}^q = (z^q_\\text{Uni} - z^q_\\text{Base}) - "
    "[(z^q_\\text{Tool} - z^q_\\text{Base}) + (z^q_\\text{Reas} - "
    "z^q_\\text{Base})]$ -- the joint improvement minus the sum of the "
    "individual improvements.",
    title="Contrast: $\\lambda_{23}^q = z_\\text{Uni} - z_\\text{Tool} - z_\\text{Reas} + z_\\text{Base}$",
)

# ---------------------------------------------------------------------------
# 4.2 Six model variants (definitional)
# ---------------------------------------------------------------------------

setup_base_model = setting(
    "**Model 1 -- $\\mathcal{M}_\\text{Base}$.** The off-the-shelf "
    "pretrained Qwen2.5-Instruct model with no tool-use or reasoning "
    "post-training. Capability vector $x_\\text{Base} = [1,0,0,0,0,0]$.",
    title="$\\mathcal{M}_\\text{Base}$: pretrained backbone, $x = [1,0,0,0,0,0]$",
)

setup_reas_model = setting(
    "**Model 2 -- $\\mathcal{M}_\\text{Reas}$ (reasoning-specialized).** "
    "Trained from $\\mathcal{M}_\\text{Base}$ using the gradient mask "
    "$m_t^{(\\text{Reas})} = \\mathbb{1}(t \\in \\mathcal{T}_\\text{reas})$ "
    "in Eq. 8. Only reasoning-token gradients update the parameters; "
    "tool-use is unaltered. Capability vector "
    "$x_\\text{Reas} = [1,0,1,0,1,0]$.",
    title="$\\mathcal{M}_\\text{Reas}$: reasoning-only update, $x = [1,0,1,0,1,0]$",
)

setup_tool_model = setting(
    "**Model 3 -- $\\mathcal{M}_\\text{Tool}$ (tool-specialized).** Same "
    "construction but with mask $m_t^{(\\text{Tool})} = \\mathbb{1}(t \\in "
    "\\mathcal{T}_\\text{tool})$. Only tool-use-token gradients update the "
    "parameters; reasoning behaviour is unaltered. Capability vector "
    "$x_\\text{Tool} = [1,1,0,1,0,0]$.",
    title="$\\mathcal{M}_\\text{Tool}$: tool-only update, $x = [1,1,0,1,0,0]$",
)

setup_unified_model = setting(
    "**Model 4 -- $\\mathcal{M}_\\text{Unified}$.** Standard joint ARL "
    "training: mask $m_t^{(\\text{Uni})} \\equiv 1$. Both reasoning and "
    "tool-use gradients update the same parameters. Capability vector "
    "$x_\\text{Unified} = [1,1,1,1,1,1]$ -- all individual and pairwise "
    "interaction terms active.",
    title="$\\mathcal{M}_\\text{Unified}$: standard ARL, $x = [1,1,1,1,1,1]$",
)

setup_htool_model = setting(
    "**Model 5 -- $\\mathcal{H}_\\text{Tool}$ (tool-hybrid inference).** "
    "Composed at inference only: $\\mathcal{M}_\\text{Base}$ produces "
    "reasoning tokens, $\\mathcal{M}_\\text{Tool}$ produces tool-use "
    "tokens. No joint optimization, so all tool-use interaction indicators "
    "are zero. Capability vector $x_{\\mathcal{H}_\\text{Tool}} = "
    "[1,1,0,0,0,0]$.",
    title="$\\mathcal{H}_\\text{Tool}$: hybrid inference, $x = [1,1,0,0,0,0]$",
)

setup_hreas_model = setting(
    "**Model 6 -- $\\mathcal{H}_\\text{Reas}$ (reasoning-hybrid "
    "inference).** Composed at inference only: $\\mathcal{M}_\\text{Reas}$ "
    "produces reasoning tokens, $\\mathcal{M}_\\text{Base}$ produces "
    "tool-use tokens. Capability vector $x_{\\mathcal{H}_\\text{Reas}} = "
    "[1,0,1,0,0,0]$.",
    title="$\\mathcal{H}_\\text{Reas}$: hybrid inference, $x = [1,0,1,0,0,0]$",
)

# ---------------------------------------------------------------------------
# Theoretical claims about the construction
# ---------------------------------------------------------------------------

claim_design_matrix_invertible = claim(
    "The 6 capability vectors of $\\mathcal{M}_\\text{Base}, "
    "\\mathcal{M}_\\text{Reas}, \\mathcal{M}_\\text{Tool}, "
    "\\mathcal{M}_\\text{Unified}, \\mathcal{H}_\\text{Tool}, "
    "\\mathcal{H}_\\text{Reas}$ are **linearly independent**, so the "
    "design matrix $X \\in \\{0,1\\}^{6 \\times 6}$ is invertible and "
    "$\\lambda^q = X^{-1} z^q$ is uniquely identified for every question.",
    title="The six capability vectors are linearly independent",
    background=[
        setup_base_model,
        setup_reas_model,
        setup_tool_model,
        setup_unified_model,
        setup_htool_model,
        setup_hreas_model,
        setup_identifiability_condition,
    ],
)

claim_hybrid_no_interaction = claim(
    "Hybrid models ($\\mathcal{H}_\\text{Tool}, \\mathcal{H}_\\text{Reas}$) "
    "compose two **separately trained** models at inference time. Because "
    "no parameter is updated by gradients from both capabilities, no "
    "joint-parameter interaction is induced -- so all interaction "
    "indicators involving the hybridized pair are zero by construction.",
    title="Hybrid composition induces no joint-parameter interaction",
    background=[setup_htool_model, setup_hreas_model, setup_interaction_indicators],
)

claim_contrast_isolates_lambda23 = claim(
    "From Appendix C: substituting the four capability vectors "
    "$x_\\text{Uni}, x_\\text{Tool}, x_\\text{Reas}, x_\\text{Base}$ into "
    "$z^q_\\mathcal{M} = x_\\mathcal{M}^\\top \\lambda^q$ and forming the "
    "alternating sum $z^q_\\text{Uni} - z^q_\\text{Tool} - z^q_\\text{Reas} "
    "+ z^q_\\text{Base}$ leaves only the $\\lambda_{23}^q$ term: every "
    "main effect and every other interaction effect cancels by "
    "construction. Hence $\\lambda_{23}^q$ is identified by a 4-model "
    "contrast that does not require the hybrid models.",
    title="The 4-model contrast identifies $\\lambda_{23}^q$ alone",
    background=[
        setup_contrast_formula,
        setup_logit_model,
        setup_capability_vector,
        setup_base_model,
        setup_reas_model,
        setup_tool_model,
        setup_unified_model,
    ],
)

# ---------------------------------------------------------------------------
# Reasoning connections (Pass 2 -- using infer / support drafts)
# ---------------------------------------------------------------------------

# The contrast formula (Appendix C) is a pure algebraic deduction from the
# capability-vector design. The conclusion is the contrast claim. We feed
# the design-matrix invertibility claim as a real premise (it's logically
# what allows the contrast to be solved).
strat_contrast_derivation = deduction(
    [claim_design_matrix_invertible],
    claim_contrast_isolates_lambda23,
    reason=(
        "Once the six capability vectors are linearly independent "
        "(@claim_design_matrix_invertible), $\\lambda^q$ is uniquely "
        "determined by $X^{-1} z^q$. Substituting "
        "$x_\\text{Uni}, x_\\text{Tool}, x_\\text{Reas}, x_\\text{Base}$ "
        "into Eq. 5 (@setup_logit_model) gives four logit values, each a "
        "specific linear combination of the six $\\lambda$ components "
        "with coefficients read from the capability vectors "
        "(@setup_capability_vector, @setup_base_model, @setup_reas_model, "
        "@setup_tool_model, @setup_unified_model). Forming the "
        "alternating sum $z^q_\\text{Uni} - z^q_\\text{Tool} - "
        "z^q_\\text{Reas} + z^q_\\text{Base}$ cancels every $\\lambda$ "
        "component except $\\lambda_{23}^q$, because only $x_{23}$ has "
        "the parity pattern $+1, 0, 0, 0$ across the four vectors. This "
        "is purely algebraic and exact: the derivation of Eq. 19 in "
        "Appendix C (@setup_contrast_formula)."
    ),
    prior=0.99,
    background=[
        setup_logit_model,
        setup_capability_vector,
        setup_contrast_formula,
        setup_base_model,
        setup_reas_model,
        setup_tool_model,
        setup_unified_model,
    ],
)

# ---------------------------------------------------------------------------
# 4.3 Empirical findings -- INTERFERENCE
# ---------------------------------------------------------------------------

setup_leas_protocol = setting(
    "**Empirical protocol (Sec. 4.3, Appendix D).** LEAS is instantiated "
    "on Natural Questions (NQ) and HotpotQA following the splits and "
    "training protocol of Search-R1 [@Jin2025]. Each model-question pair "
    "is evaluated with $N=50$ stochastic decoding samples; "
    "$\\hat{s}_\\mathcal{M}^q = \\frac{1}{N}\\sum_n "
    "\\mathrm{EM}(a_q^{(n)}, a_\\text{gold})$. Per-question "
    "$\\hat{\\lambda}^q$ is obtained by solving $z^q = X \\hat{\\lambda}^q$ "
    "in logit space. Only questions where at least one of the six models "
    "produces at least one correct prediction are retained. Both "
    "Qwen2.5-3B and Qwen2.5-7B backbones are used.",
    title="LEAS empirical protocol (50 samples / model-question pair)",
)

obs_lambda23_distribution = claim(
    "**Observation (Fig. 2).** The histogram of question-level "
    "$\\lambda_{23}^q$ across NQ and HotpotQA, for both Qwen2.5-3B and "
    "Qwen2.5-7B, shows that interference dominates synergy. Specifically:\n\n"
    "| Model      | Dataset   | % $\\lambda_{23}^q < 0$ (interference) | % $\\lambda_{23}^q > 0$ (synergy) |\n"
    "|------------|-----------|---------------------------------------:|----------------------------------:|\n"
    "| Qwen2.5-7B | NQ        | 66.10%                                 | 33.90%                            |\n"
    "| Qwen2.5-3B | NQ        | 61.84%                                 | 38.16%                            |\n"
    "| Qwen2.5-7B | HotpotQA  | 67.24%                                 | 32.76%                            |\n"
    "| Qwen2.5-3B | HotpotQA  | 42.30%                                 | 57.70%                            |\n\n"
    "On three of the four (model, dataset) combinations the interference "
    "share is roughly two-thirds; only Qwen2.5-3B on HotpotQA is "
    "synergy-dominant.",
    title="Empirical $\\lambda_{23}^q$ histograms: interference dominates 3/4 settings",
    metadata={
        "source_figure": "artifacts/2602.00994.pdf, Figure 2",
        "caption": "Fig. 2 | Histograms of question-level interaction coefficient lambda_23 on NQ and HotpotQA using Qwen2.5-Instruct (3B and 7B). Negative values (blue) = interference; positive (red) = synergy.",
    },
    background=[setup_leas_protocol],
)

obs_arl_succeeds_in_interference_region = claim(
    "**Observation (Fig. 2 overlay curve).** The ARL accuracy curve "
    "overlaid on the $\\lambda_{23}^q$ histogram shows that questions in "
    "the interference region ($\\lambda_{23}^q < 0$) consistently achieve "
    "**markedly higher** average correctness than questions in the synergy "
    "region. ARL therefore predominantly succeeds on the very questions "
    "where capabilities interfere -- i.e. the model is forced to use both "
    "skills simultaneously precisely when they compete for the same "
    "shared parameters.",
    title="ARL succeeds in the interference region (Fig. 2 overlay)",
    metadata={
        "source_figure": "artifacts/2602.00994.pdf, Figure 2 (overlaid accuracy curve)"
    },
    background=[setup_leas_protocol],
)

# ---------------------------------------------------------------------------
# Synthesis claims drawn from the empirical observations
# ---------------------------------------------------------------------------

claim_interference_dominates = claim(
    "**Synthesis.** Across NQ and HotpotQA on Qwen2.5-3B/7B, joint ARL "
    "training of reasoning and tool-use induces a *systematic negative "
    "interaction* between the two capabilities: the average sign of "
    "$\\lambda_{23}^q$ is negative on three of four (model, dataset) "
    "settings, and the interference is concentrated on the questions ARL "
    "actually solves. This is direct quantitative evidence for the seesaw "
    "phenomenon hypothesized in Section 1 (@claim_seesaw_phenomenon).",
    title="LEAS finding: joint ARL induces systematic interference",
)

strat_interference_synthesis = support(
    [obs_lambda23_distribution, obs_arl_succeeds_in_interference_region],
    claim_interference_dominates,
    reason=(
        "The histogram measurement (@obs_lambda23_distribution) shows that "
        "$\\lambda_{23}^q < 0$ on the majority of questions in three of "
        "the four (model, dataset) cells (66.10%, 61.84%, 67.24%). The "
        "overlay accuracy curve (@obs_arl_succeeds_in_interference_region) "
        "shows that the questions where ARL is most successful are "
        "concentrated in the interference region. Together these two "
        "empirical observations directly substantiate the seesaw / "
        "competition hypothesis (@claim_seesaw_phenomenon) -- in the "
        "regime where ARL is operationally relevant, the two capabilities "
        "exhibit competition rather than synergy."
    ),
    prior=0.9,
    background=[setup_leas_protocol],
)

# Motivation -> seesaw and capability heterogeneity become consequences of
# the LEAS interference finding (the paper's quantitative conclusion).
strat_seesaw_from_interference = support(
    [claim_interference_dominates],
    claim_seesaw_phenomenon,
    reason=(
        "The LEAS finding that joint training induces systematic "
        "$\\lambda_{23}^q < 0$ across most questions "
        "(@claim_interference_dominates) is the quantitative "
        "instantiation of the qualitative seesaw phenomenon "
        "(@claim_seesaw_phenomenon) -- improving one capability degrades "
        "the other [@Yu2020]. The empirical interference finding directly "
        "supports the seesaw description."
    ),
    prior=0.92,
)

# strat_heterogeneous_from_gradients is defined after obs_gradient_angles
# (declared further down in the same module).

# ---------------------------------------------------------------------------
# Gradient-conflict explanation
# ---------------------------------------------------------------------------

setup_gradient_protocol = setting(
    "**Gradient-conflict protocol (Sec. 4.3, Appendix E).** Following the "
    "training settings of Search-R1 [@Jin2025], for each query the policy "
    "is rolled out $N=16$ times, yielding trajectories "
    "$\\{\\tau_i\\}_{i=1}^{16}$. For each trajectory $\\tau_i$ and each "
    "token role $b \\in \\{r, a\\}$, the partial gradient $g_{\\tau_i}^{(b)}$ "
    "is computed by backpropagating only through the tokens of role $b$ "
    "(separate backward pass per role, gradients zeroed between passes). "
    "Two angle distributions are then compared: (i) **same-role across "
    "trajectories** "
    "$\\mathbb{E}_{i \\ne j}[\\angle(g^{(b)}_{\\tau_i}, g^{(b)}_{\\tau_j})]$, "
    "and (ii) **different-role within trajectory** "
    "$\\mathbb{E}_i [\\angle(g^{(r)}_{\\tau_i}, g^{(a)}_{\\tau_i})]$. "
    "Angles obtained via cosine similarity in BF16 with FlashAttention-2.",
    title="Gradient-angle protocol (16 rollouts, two angle distributions)",
)

obs_gradient_angles = claim(
    "**Observation (Fig. 3A and Fig. 7A).** On Qwen2.5-3B (NQ + HotpotQA) "
    "and Qwen2.5-7B (NQ + HotpotQA), the *same-role* gradient angle "
    "distribution is concentrated near small angles (typically below "
    "$30^\\circ$), while the *different-role* distribution is concentrated "
    "near $90^\\circ$ -- i.e. reasoning-token gradients and tool-use-token "
    "gradients are *near-orthogonal* on average. The 7B model exhibits a "
    "more dispersed same-role distribution (more parameters, more degrees "
    "of freedom), but the inter-role orthogonality is preserved.",
    title="Gradient angles: same-role aligned, different-role near-orthogonal",
    metadata={
        "source_figure": "artifacts/2602.00994.pdf, Figure 3A and Figure 7A",
        "caption": "Fig. 3A | Gradient angle distributions on NQ under Qwen2.5-3B; same-capability gradients are aligned, reasoning vs tool-use gradients are nearly orthogonal. Fig. 7A confirms across Qwen2.5-3B/7B and NQ/HotpotQA.",
    },
    background=[setup_gradient_protocol],
)

claim_gradient_conflict_explains_interference = claim(
    "**Mechanistic synthesis.** The near-orthogonality of reasoning vs "
    "tool-use gradients (@obs_gradient_angles) means each capability has "
    "its own distinct optimal update direction. In standard ARL, the "
    "policy gradient (@setup_policy_gradient) sums these orthogonal "
    "components, so the parameter update lies on a *compromise direction* "
    "that is sub-optimal for both reasoning and tool-use. This gradient "
    "compromise is the **mechanistic cause** of the LEAS-quantified "
    "interference (@claim_interference_dominates).",
    title="Gradient compromise mechanism explains the interference",
)

strat_heterogeneous_from_gradients = support(
    [obs_gradient_angles],
    claim_capabilities_are_heterogeneous,
    reason=(
        "The near-orthogonality of reasoning vs tool-use gradients "
        "(@obs_gradient_angles) is direct optimization-geometric "
        "evidence that the two capabilities require qualitatively "
        "different parameter updates -- i.e. the conditional next-token "
        "distributions they target differ substantially "
        "(@claim_capabilities_are_heterogeneous)."
    ),
    prior=0.85,
)

strat_gradient_explains_interference = support(
    [obs_gradient_angles, claim_interference_dominates],
    claim_gradient_conflict_explains_interference,
    reason=(
        "Gradient angles of $\\sim 90^\\circ$ between reasoning and "
        "tool-use components (@obs_gradient_angles) imply that, when both "
        "are summed in the unmasked policy gradient (Eq. 2, "
        "@setup_policy_gradient), the resulting update vector lies "
        "along a compromise direction whose projection onto either "
        "individual optimum is small. This geometric inefficiency is "
        "precisely what LEAS quantifies as a negative $\\lambda_{23}^q$ "
        "(@claim_interference_dominates). The two observations are "
        "consistent in sign and magnitude: same gradient pattern, "
        "consistent across both backbones and both datasets."
    ),
    prior=0.85,
    background=[setup_policy_gradient, setup_role_router],
)

# ---------------------------------------------------------------------------
# Top-level chain to the contribution claim
# ---------------------------------------------------------------------------

strat_leas_supports_contribution = support(
    [
        claim_design_matrix_invertible,
        claim_hybrid_no_interaction,
        claim_contrast_isolates_lambda23,
        claim_interference_dominates,
        claim_gradient_conflict_explains_interference,
    ],
    claim_contribution_leas,
    reason=(
        "The LEAS contribution rests on four pillars: (i) the design is "
        "**identifiable** (six linearly-independent capability vectors, "
        "@claim_design_matrix_invertible); (ii) hybrid inference "
        "**isolates** non-jointly-trained pairs (@claim_hybrid_no_interaction); "
        "(iii) the closed-form contrast (@claim_contrast_isolates_lambda23) "
        "shows that $\\lambda_{23}^q$ can be read directly from four "
        "model evaluations; (iv) the empirical instantiation reveals "
        "systematic interference (@claim_interference_dominates) with a "
        "concrete mechanistic explanation "
        "(@claim_gradient_conflict_explains_interference). Together they "
        "establish LEAS as a **quantitative diagnostic** for "
        "reasoning-tool interference in ARL [@Li2026]."
    ),
    prior=0.88,
)

__all__ = [
    # 4.1 settings
    "setup_capability_indicators",
    "setup_interaction_indicators",
    "setup_capability_vector",
    "setup_logit_model",
    "setup_logit_transform",
    "setup_identifiability_condition",
    "setup_attribution_only",
    "setup_contrast_formula",
    # 4.2 settings
    "setup_base_model",
    "setup_reas_model",
    "setup_tool_model",
    "setup_unified_model",
    "setup_htool_model",
    "setup_hreas_model",
    # claims
    "claim_design_matrix_invertible",
    "claim_hybrid_no_interaction",
    "claim_contrast_isolates_lambda23",
    # 4.3 protocol + observations + synthesis
    "setup_leas_protocol",
    "obs_lambda23_distribution",
    "obs_arl_succeeds_in_interference_region",
    "claim_interference_dominates",
    "setup_gradient_protocol",
    "obs_gradient_angles",
    "claim_gradient_conflict_explains_interference",
]
