"""Section 3: Latent Sampling, Optimal Samplers, and the Sampler Hierarchy"""

from gaia.lang import claim, setting, support, deduction, contradiction, complement

from .s2_separation import (
    simple_projection_setting,
    projection_distribution_setting,
    claim_lifting_intractable,
    claim_psimple_contains_phmm,
)

# ── Background settings ──────────────────────────────────────────────────────

monte_carlo_setting = setting(
    "Monte-Carlo estimation of the projected likelihood: given any conditional distribution "
    "Q(·|x) whose support equals Proj^{-1}_{<omega}(x), the likelihood is estimated as "
    "p_n = (1/n) * sum_{i=1}^{n} P^{<=|Z^(i)|}(Z^(i)) / Q(Z^(i)|x), with {Z^(i)} i.i.d. ~ Q(·|x). "
    "This estimator is strongly consistent (p_n -> p* a.s.) and unbiased (E[p_n] = p*). "
    "Convergence rate is O(chi^2(Q*(·|x) || Q(·|x)) / n), where Q* is the posterior sampler.",
    title="Monte-Carlo estimation of projected likelihood",
)

posterior_sampler_setting = setting(
    "The posterior sampler Q*(·|x) is the Bayesian posterior distribution of latent sequences "
    "given an observed prefix x: Q*(z|x) := P^{<=|z|}(z) / (Proj#P)^{<=|x|}(x) for z in "
    "Proj^{-1}_{<omega}(x). It is the variance-minimizing sampler for estimating the "
    "projected likelihood. It is generally non-causal (depends on future observations).",
    title="Posterior sampler Q* defined",
)

identity_sampler_setting = setting(
    "The identity sampler Q_id(·|x) is defined for disentangled projections by autoregressively "
    "sampling the latent model P conditioned only on past tokens (no future context). "
    "For the 'pause-to-think' projection (Example 6), Q_id samples thoughts y^(t) from P "
    "conditioned on prior observable and latent tokens, without seeing x_t or future tokens. "
    "All existing reasoning models (e.g., DeepSeek-R1, Quiet-STaR) use the identity sampler.",
    title="Identity sampler Q_id for existing models",
)

sampler_classes_setting = setting(
    "The sampler hierarchy is: {Q_id} ⊆ Q_hat_Proj (predictive samplers: strictly causal, "
    "depend only on past observations) ⊆ Q_check_Proj (causal samplers: can also see current "
    "token x_t) ⊆ Q_Proj (explanatory samplers: full non-causal access to entire input x). "
    "In general, each containment is strict.",
    title="Sampler hierarchy: identity ⊆ predictive ⊆ causal ⊆ explanatory",
)

chi_square_scaling_setting = setting(
    "The slow thinking scaling laws from Table 2 show that all performance errors scale as "
    "O(chi^2 / n) where chi^2 is the chi-squared divergence between the implemented sampler "
    "and the optimal sampler, and n is the sampling size. Specifically:\n\n"
    "| Task | Scaling Law |\n"
    "|------|-------------|\n"
    "| Encoding (likelihood) | (Proj#P_f)^{<=|x|}(x)^2 * chi^2(Q*(·|x) || Q(·|x)) / n |\n"
    "| Decoding (TV distance) | sqrt(6*chi^2(Q*(·|x)||Q(·|x))+2) / n |\n"
    "| Training (gradient) | [chi^2 terms involving Q and Q-tilde] / n + O(n^{-2}) |\n"
    "| Multi-choice error | 4/n * sum ... chi^2_i / n + O(n^{-2}) |",
    title="Slow thinking scaling laws (Table 2)",
)

inquisitive_sampler_setting = setting(
    "The inquisitive sampler Q-tilde is the variance-minimizing sampler for estimating the "
    "training gradient (not the likelihood). It is defined as: "
    "Q-tilde(z|x) proportional to P_f^{<=|z|}(z) * ||grad_theta log P_f^{<=|z|}(z)||, "
    "normalized over z in Proj^{-1}_{<omega}(x). Unlike the posterior Q*, the inquisitive "
    "sampler is parametrization-dependent and tends to explore novel latent sequences "
    "('exploration' vs Q*'s 'exploitation').",
    title="Inquisitive sampler Q-tilde: exploration-focused",
)

# ── Claims ────────────────────────────────────────────────────────────────────

claim_posterior_is_noncausal = claim(
    "The posterior sampler Q*(·|x) is generically non-causal: for almost all latent "
    "distributions P (in measure-theoretic sense), Q* is NOT a causal sampler. "
    "More precisely, the set of P for which Q* is causal has Lebesgue measure zero in "
    "the simplex of all distributions. Furthermore, no causal sampler can approximate "
    "Q* with respect to chi^2 divergence for general non-causal P.",
    title="Theorem 15 + Prop 16: Posterior sampler is generically non-causal",
)

claim_causal_samplers_inadequate = claim(
    "Causal samplers (including all predictive samplers and the identity sampler Qid) are "
    "inadequate for slow thinking because they cannot approximate the optimal samplers Q* "
    "and Q-tilde in chi^2 divergence for generic distributions. This directly implies, "
    "via the scaling laws in Table 2, that all slow thinking operations (encoding, decoding, "
    "training) of models using causal samplers are suboptimal compared to those using "
    "explanatory samplers.",
    title="Causal/predictive samplers are suboptimal for slow thinking",
)

claim_explanatory_sampler_advantage = claim(
    "Explanatory samplers (which can access the full observable sequence x including future "
    "tokens during latent sequence sampling) are generally more efficient than predictive "
    "or causal samplers. Their advantage manifests in: better understanding of prompts during "
    "prefill, more efficient extraction of training signal from data, and lower chi^2 "
    "divergence from the optimal posterior sampler Q*.",
    title="Explanatory samplers are more efficient than causal/predictive samplers",
)

claim_two_samplers_needed = claim(
    "Optimal training requires two distinct samplers: (1) the inference sampler Q (= posterior Q*) "
    "for importance-weighted likelihood estimation, and (2) the train sampler Q-tilde (= inquisitive sampler) "
    "for gradient estimation. The inference sampler exploits known high-probability latent sequences, "
    "while the train sampler explores novel latent sequences that maximally shift the gradient. "
    "Using only one sampler (as in current models) is suboptimal for training.",
    title="Two samplers needed: posterior Q* for inference, inquisitive Q-tilde for training",
)

claim_policy_collapse_mechanism = claim(
    "When a slow thinking model trains using only the identity sampler (fitting only the posterior Q*), "
    "a positive feedback cycle develops: since Q fits Q* which concentrates at modes of P_f, "
    "samples Z^(i) concentrate near those modes, training P_f on these samples further concentrates "
    "P_f at those modes, until total entropy collapse (policy collapse). Implementing the inquisitive "
    "sampler Q-tilde for training breaks this cycle by ensuring exploration of the latent space.",
    title="Policy collapse mechanism: identity sampler creates feedback cycle",
)

claim_scaling_laws_chi2 = claim(
    "All slow thinking scaling laws are proportional to chi^2/n where chi^2 is the divergence "
    "between the implemented sampler and the optimal sampler, and n is sampling size. "
    "This means errors vanish as n → infinity (consistency), and the rate of convergence is "
    "determined entirely by how well the implemented sampler approximates the optimal one. "
    "Since existing models use the identity sampler (far from Q* in chi^2), their scaling laws "
    "are suboptimal.",
    title="Scaling laws are O(chi^2/n): sampler quality determines convergence",
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_causal_noncausal = support(
    [claim_lifting_intractable],
    claim_posterior_is_noncausal,
    reason=(
        "The posterior Q*(z|x) := P^{<=|z|}(z) / (Proj#P)^{<=|x|}(x) conditions on the entire "
        "observable sequence x. By @projection_distribution_setting and @simple_projection_setting, "
        "since |Proj^{-1}_{<omega}(x)| > 1 for non-trivial projections, the marginal Q*(·|x_{<=t}) "
        "and the restriction of Q*(·|x) to Proj^{-1}_{<omega}(x_{<=t}) are generically different "
        "(Theorem 15 and Proposition 16 in the paper), meaning Q* is not causal for almost all P."
    ),
    prior=0.88,
    background=[projection_distribution_setting, simple_projection_setting],
)

strat_causal_inadequate = deduction(
    [claim_posterior_is_noncausal, claim_scaling_laws_chi2],
    claim_causal_samplers_inadequate,
    reason=(
        "By @claim_posterior_is_noncausal, causal samplers cannot approximate Q* in chi^2. "
        "By @claim_scaling_laws_chi2, performance of all tasks scales as O(chi^2(Q*(·|x)||Q(·|x))/n). "
        "Therefore, using any causal sampler Q in place of Q* yields a chi^2 divergence "
        "bounded away from zero (Proposition 16), so the scaling laws cannot improve beyond "
        "some positive constant regardless of sampling size n."
    ),
    prior=0.99,
)

strat_two_samplers = support(
    [claim_posterior_is_noncausal],
    claim_two_samplers_needed,
    reason=(
        "The optimal sampler for likelihood estimation is Q* (the posterior, @posterior_sampler_setting) "
        "as it minimizes the chi^2 divergence in the Monte-Carlo estimator (@monte_carlo_setting). "
        "However, for gradient estimation, a different analysis (Proposition 33 in the paper) "
        "shows the optimal sampler is the @inquisitive_sampler_setting Q-tilde, which weights "
        "latent sequences by gradient norm rather than likelihood. These two objectives have "
        "distinct solutions, so two distinct samplers are required for jointly optimal training."
    ),
    prior=0.9,
    background=[monte_carlo_setting, inquisitive_sampler_setting, posterior_sampler_setting],
)

strat_policy_collapse = deduction(
    [claim_causal_samplers_inadequate, claim_two_samplers_needed],
    claim_policy_collapse_mechanism,
    reason=(
        "By @claim_causal_samplers_inadequate, the identity sampler (a causal sampler) is far "
        "from Q*. By @claim_two_samplers_needed, optimal training requires the inquisitive "
        "sampler Q-tilde for gradient estimation but existing models omit it. Training only "
        "with Q to fit Q* creates a self-reinforcing cycle: Q concentrates on modes of P_f, "
        "P_f is trained to concentrate further at those modes, leading to entropy collapse."
    ),
    prior=0.99,
)

strat_expl_advantage = support(
    [claim_causal_samplers_inadequate],
    claim_explanatory_sampler_advantage,
    reason=(
        "Since @claim_causal_samplers_inadequate establishes that causal samplers cannot approximate "
        "Q* in chi^2, and by @sampler_classes_setting explanatory samplers are strictly more "
        "expressive than causal samplers (they can access the full input x), explanatory samplers "
        "can achieve lower chi^2(Q*(·|x)||Q(·|x)). By the scaling laws, this directly translates "
        "to better performance in encoding, decoding, and training."
    ),
    prior=0.9,
    background=[sampler_classes_setting],
)

strat_scaling_laws = support(
    [claim_posterior_is_noncausal],
    claim_scaling_laws_chi2,
    reason=(
        "The @monte_carlo_setting gives p_n as a consistent estimator with convergence "
        "proportional to chi^2(Q*(·|x)||Q(·|x))/n. Analogous analyses for decoding, "
        "conditional encoding (Propositions 10, 11, 12 in the paper) and training gradient "
        "(Proposition 33) all yield the same O(chi^2/n) form, with appropriate chi^2 terms "
        "involving the posterior Q* and inquisitive @inquisitive_sampler_setting Q-tilde. "
        "The table in Section 3.5 summarizes all these scaling laws."
    ),
    prior=0.92,
    background=[monte_carlo_setting, posterior_sampler_setting, inquisitive_sampler_setting],
)
