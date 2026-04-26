"""Section 5: Derivation and Improvement of DeepSeek-R1 Slow Thinking Models"""

from gaia.lang import claim, setting, support, deduction, abduction, compare

from .motivation import (
    claim_three_stage_improvement_roadmap,
    claim_policy_collapse_cause,
)
from .s2_separation import simple_projection_setting, claim_lifting_intractable
from .s3_samplers import (
    claim_causal_samplers_inadequate,
    claim_explanatory_sampler_advantage,
    claim_two_samplers_needed,
    claim_policy_collapse_mechanism,
    identity_sampler_setting,
    inquisitive_sampler_setting,
    chi_square_scaling_setting,
)

# ── Background settings ──────────────────────────────────────────────────────

deepseek_r1_setting = setting(
    "DeepSeek-R1 [@DeepSeekR1] is a slow thinking LLM whose representation uses: "
    "(1) Observable vocabulary Sigma = DeepSeek-V3 vocabulary; "
    "(2) Latent vocabulary Omega = Sigma + {<s>, </s>} (thought start/end tokens); "
    "(3) Projection Proj: strips thought tokens, mapping latent sequences to observable ones; "
    "(4) Thought bound c = 2^15 = 32768 tokens maximum per thought; "
    "(5) Identity sampler Q_id (no future context); "
    "(6) Forgetful latent representation (defined below).",
    title="DeepSeek-R1 configuration",
)

forgetful_latent_setting = setting(
    "A latent distribution P is 'forgetful' if its next-token distribution P(y_t+1 | y_{<=t}) "
    "is the same whether conditioned on the full history y_{<=t} or only the current observed "
    "segment y_{>s_t} (tokens after the most recent thought boundary). This means P 'forgets' "
    "all content before the current thought when deciding the next latent token. "
    "This is the key structural property that allows the existing inference pipeline.",
    title="Forgetful latent: P forgets prior thoughts",
)

grpo_training_setting = setting(
    "DeepSeek-R1 training uses the Group Relative Policy Optimization (GRPO) objective: "
    "for n sampled thought-response pairs (Y^(i), X_r^(i)), reward r_i = 1 if response is correct, "
    "advantage A_i = (r_i - mean(r_1,...,r_n)) / std(r_1,...,r_n), and the loss minimizes "
    "-E[A_i * log P_f(Y^(i) X_r^(i) | x)]. With clipping and KL regularization, this "
    "is equivalent to fitting the posterior sampler Q_TR* (specialized to the training projection).",
    title="GRPO training objective of DeepSeek-R1",
)

explanatory_sampler_stage1_setting = setting(
    "Stage 1 improvement: replace the identity sampler with an explanatory sampler during training. "
    "The explanatory sampler uses a prompt that includes both the query x and response x_r, "
    "so it can generate thoughts Y that bridge the two. The loss becomes: "
    "L_n(theta) = -log(1/n * sum_i P_f(Y^(i) x_r | x) / Q(Y^(i) | x x_r)). "
    "Optionally, a separate train sampler Q-tilde(·|x x_r) is used for gradient estimation.",
    title="Stage 1: explanatory sampler replaces identity sampler",
)

# ── Claims ────────────────────────────────────────────────────────────────────

claim_deepseek_is_derived = claim(
    "DeepSeek-R1's design (representation, training, and inference) is fully derivable from "
    "the active lifting static theory as a specific instance of the general (Sigma, Omega, Proj, P, Q) "
    "tuple. Specifically: the forgetful latent corresponds to the lowest level of the representation "
    "hierarchy; the identity sampler corresponds to the lowest level of the sampler hierarchy; "
    "GRPO training corresponds to fitting the posterior sampler Q*.",
    title="DeepSeek-R1 derived as a special case of static theory",
)

claim_stage1_explanatory_improves = claim(
    "In a preliminary experiment on pretraining data (GPT-2 Small, 128-token query/response pairs, "
    "n=8 sampling), replacing the predictive (identity) sampler with an explanatory sampler "
    "improved the test loss by approximately 264% relative to the gap between the fast-thinking "
    "baseline and the predictive sampler baseline: (L_fast - L_expl) / (L_fast - L_pred) - 1 ≈ 264%. "
    "Specifically: L_fast = 1.7345, L_pred = 1.7331, L_expl = 1.7294.",
    title="Experimental result: explanatory sampler shows 264% relative improvement",
)

claim_stage1_explanatory_prediction = claim(
    "Theory predicts that replacing the identity (predictive) sampler with an explanatory sampler "
    "should reduce the chi^2 divergence from the optimal posterior sampler Q* and thus improve "
    "training efficiency, because the explanatory sampler can produce thoughts that are relevant "
    "to the response x_r (the 'causal gap' r_i > 0 more often) rather than guessing blindly.",
    title="Theoretical prediction: explanatory sampler reduces chi^2, improves training",
)

claim_stage2_persistent_ubiquitous = claim(
    "Stage 2 improvement: replace the forgetful latent with 'persistent and ubiquitous thinking'. "
    "Persistent thinking: allow the latent model to carry information across thought boundaries "
    "(remove the forgetfulness constraint). Ubiquitous thinking: allow thought insertion anywhere "
    "in the text during pretraining (not only after user queries). "
    "This ascends the representation hierarchy, enabling more expressive distributions.",
    title="Stage 2: persistent and ubiquitous thinking improves approximation ability",
)

claim_stage3_active_lifting = claim(
    "Stage 3 improvement: transcend the static theory (fixed projection Proj) and adopt active "
    "lifting with unconstrained latent sequence sampling. The latent vocabulary, thought length, "
    "and thought insertion frequency are no longer prescribed but emerge from training. "
    "This is the most general improvement and is analyzed in Section 6.",
    title="Stage 3: active lifting enables free-form slow thinking",
)

alt_identity_sampler_sufficient = claim(
    "The identity sampler may be sufficient for training if the training data contains strong "
    "enough supervision signal that predictive thoughts are reliably useful. In this alternative, "
    "the overhead of implementing an explanatory sampler outweighs its benefit.",
    title="Alternative: identity sampler may be sufficient for training",
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_deepseek_derivation = support(
    [claim_explanatory_sampler_advantage],
    claim_deepseek_is_derived,
    reason=(
        "The @deepseek_r1_setting specifies the exact (Sigma, Omega, Proj, P, Q) tuple for DeepSeek-R1. "
        "Its projection matches @simple_projection_setting (Example 6 type). "
        "The @forgetful_latent_setting corresponds to the lowest level of the representation "
        "hierarchy (Pforgetful ⊊ Ppersistent ⊊ Pubiquitous). The @identity_sampler_setting "
        "corresponds to the lowest level of the sampler hierarchy. "
        "The @grpo_training_setting is shown to be equivalent to fitting Q* under the "
        "one-sampler training loss (44), completing the derivation."
    ),
    prior=0.92,
    background=[deepseek_r1_setting, grpo_training_setting, simple_projection_setting,
                forgetful_latent_setting, identity_sampler_setting],
)

strat_stage1_pred = support(
    [claim_causal_samplers_inadequate],
    claim_stage1_explanatory_prediction,
    reason=(
        "By @claim_causal_samplers_inadequate, the identity sampler (predictive) has large "
        "chi^2(Q*(·|x) || Q_id(·|x)). The explanatory sampler in @explanatory_sampler_stage1_setting "
        "can see the response x_r, so it generates thoughts Y that are posterior-conditioned, "
        "reducing chi^2. By @chi_square_scaling_setting, lower chi^2 directly reduces training "
        "gradient estimation error, leading to better parameter updates."
    ),
    prior=0.88,
    background=[chi_square_scaling_setting, explanatory_sampler_stage1_setting],
)

# Abduction: theory prediction vs experimental observation
pred_explanatory_better = claim(
    "Theory predicts that explanatory samplers significantly improve training efficiency, "
    "with relative improvement much larger than predictive samplers (many times larger gap).",
    title="Theory prediction: large improvement from explanatory samplers",
)
pred_alt_marginal = claim(
    "An alternative view predicts only marginal improvement from explanatory samplers, "
    "since the information bottleneck from thought-token length limits usefulness.",
    title="Alternative prediction: marginal improvement only",
)
obs_experiment = claim(
    "Observed experimental result: explanatory sampler achieves test loss 1.7294, "
    "vs predictive sampler 1.7331 and fast-thinking baseline 1.7345. "
    "Relative improvement: (1.7345 - 1.7294) / (1.7345 - 1.7331) - 1 ≈ 264%.",
    title="Observed: 264% relative improvement in preliminary experiment",
)

s_expl_h = support(
    [pred_explanatory_better],
    obs_experiment,
    reason="Theory predicts large improvement; the 264% relative gain confirms a large, not marginal, effect",
    prior=0.82,
)
s_expl_alt = support(
    [pred_alt_marginal],
    obs_experiment,
    reason="Marginal improvement hypothesis cannot explain the 264% relative gain observed",
    prior=0.25,
)
comp_expl = compare(
    pred_explanatory_better,
    pred_alt_marginal,
    obs_experiment,
    reason="Theory prediction of large improvement matches observation far better than the marginal-improvement alternative",
    prior=0.88,
)
abd_stage1 = abduction(
    s_expl_h, s_expl_alt, comp_expl,
    reason="Both theory and alternative attempt to explain the observed training improvement",
)

claim_persistent_more_expressive = claim(
    "P_persistent and P_ubiquitous are strictly more expressive than P_forgetful within "
    "the static theory's representation hierarchy: they can model distributions that "
    "require information flow across thought boundaries or during pretraining.",
    title="Persistent/ubiquitous thinking more expressive than forgetful",
)

strat_stage2 = support(
    [claim_deepseek_is_derived, claim_persistent_more_expressive],
    claim_stage2_persistent_ubiquitous,
    reason=(
        "By @claim_deepseek_is_derived, DeepSeek-R1 uses a forgetful latent, the lowest level "
        "of the representation hierarchy. The @claim_persistent_more_expressive confirms "
        "that ascending the hierarchy strictly expands the modeled distribution family. "
        "Removing the forgetfulness constraint (persistent thinking) and applying thinking during "
        "pretraining (ubiquitous thinking) are concrete steps up this hierarchy."
    ),
    prior=0.82,
    background=[deepseek_r1_setting],
)

strat_three_stage_completion = deduction(
    [claim_stage1_explanatory_improves, claim_stage2_persistent_ubiquitous, claim_stage3_active_lifting],
    claim_three_stage_improvement_roadmap,
    reason=(
        "The three-stage roadmap from @claim_three_stage_improvement_roadmap is instantiated by: "
        "Stage 1 = @claim_stage1_explanatory_improves (sampler hierarchy), "
        "Stage 2 = @claim_stage2_persistent_ubiquitous (representation hierarchy), "
        "Stage 3 = @claim_stage3_active_lifting (transcending static theory). "
        "Together they form the complete roadmap."
    ),
    prior=0.99,
)

# Bring in the policy collapse claim
strat_policy_collapse_ref = support(
    [claim_policy_collapse_mechanism],
    claim_policy_collapse_cause,
    reason=(
        "The mechanism described in @claim_policy_collapse_mechanism (identity sampler creating "
        "a mode-concentration feedback loop) is the specific cause identified in Remark 17 of "
        "the paper, explaining @claim_policy_collapse_cause. The fix is implementing the "
        "inquisitive sampler to break the feedback."
    ),
    prior=0.82,
)


# Avoid using undefined name
from .s2_separation import claim_psimple_contains_phmm
