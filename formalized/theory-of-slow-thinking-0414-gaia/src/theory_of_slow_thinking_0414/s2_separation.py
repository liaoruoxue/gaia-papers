"""Section 2: Separation of Approximation Ability and the Representation Hierarchy"""

from gaia.lang import claim, setting, deduction, support, complement

# ── Background settings ──────────────────────────────────────────────────────

approx_ability_setting = setting(
    "Given a data space X, a distribution parametrization f -> P_f maps a function space F "
    "(with norm ||·||_F) to the space of probability measures P(X). The complexity "
    "||P*||_F := inf{||f||_F | P_f = P*} measures the difficulty of fitting a target P*. "
    "If ||P*||_F = infinity then P* cannot be represented. If finite, the training loss "
    "satisfies KL(P*||P_t) ≲ ||P*||_F / t^a and the generalization error satisfies "
    "KL(P*||P_t^(n)) ≲ ||P*||_F * n^{-a/(2(a+b))} with early stopping, for constants a,b > 0.",
    title="Approximation ability framework",
)

transformer_setting = setting(
    "TF(L, H, d_h, p) denotes the set of Transformer networks with L blocks, H attention heads, "
    "head dimension d_h, and floating-point precision p bits. These Transformers can be modeled "
    "as DLOGTIME-uniform TC0 circuit families (bounded-depth polynomial-size threshold circuits). "
    "TC0 is strictly contained in NC1 under the widely-believed assumption TC0 ⊊ NC1 "
    "(analogous to the famous conjecture P ⊊ NP).",
    title="Transformer as TC0 circuit",
)

sequence_space_setting = setting(
    "For any finite alphabet Sigma, Sigma^omega denotes the space of infinite sequences, "
    "equipped with the product topology (metrized by d_omega(x,y) = 2^{-inf{t | x_t != y_t}}). "
    "Sigma^* denotes finite sequences. A 'lifting' Proj^{-1}_{<omega}: Sigma^* -> 2^{Omega^*} "
    "is derived from any continuous surjective partial function Proj: Omega^omega -> Sigma^omega "
    "with closed domain, and expresses the finite-length inverse of the projection.",
    title="Sequence space and lifting definition",
)

hmm_setting = setting(
    "A Hidden Markov Model (HMM) is a tuple (A, B, lambda) where A is a |Omega|x|Omega| "
    "stochastic transition matrix, B is a |Omega|x|Sigma| emission matrix, and lambda is "
    "an initial state distribution. The observable distribution P_{A,B,lambda} is the "
    "marginal law of the observations (X_t), obtained by marginalizing out the hidden states (Z_t). "
    "Despite having a memoryless (Markov) latent process, the observable dependency can have "
    "arbitrarily long range.",
    title="Hidden Markov Model (HMM)",
)

tc0_nc1_conjecture = setting(
    "The computational complexity assumption TC0 ⊊ NC1 is widely believed to be true in "
    "theoretical computer science, analogous to P ⊊ NP. TC0 circuits have bounded depth and "
    "polynomial size with threshold gates; NC1 circuits have O(log n) depth. The assumption "
    "implies that certain problems (e.g., the cups-and-ball tracking problem based on the "
    "symmetric group S5 via Barrington's theorem [@Barrington1986]) require unbounded depth "
    "when restricted to polynomial size.",
    title="TC0 ⊊ NC1 assumption",
)

semi_divergence_setting = setting(
    "The semi-divergence D(P*, P) is a modified divergence that tolerates small pointwise "
    "numerical errors (of magnitude epsilon ~ 0.01, consistent with floating-point arithmetic "
    "like bfloat16). It is used to define the representation hierarchy: P1 can 'approximate' "
    "P2 if sup_{P*inP2} inf_{P in P1} D(P*, P) = 0, and P1 'contains' P2 if the infimum "
    "is also attained (min instead of inf).",
    title="Semi-divergence D and representation hierarchy",
)

simple_projection_setting = setting(
    "A 'simple projection' is a continuous surjective partial function Proj: Omega^omega -> Sigma^omega "
    "with closed domain whose lifting Proj^{-1}_{<omega} is a DLOGTIME-uniform TC0 nondeterministic "
    "circuit family. Examples include: (1) identity Proj = id; (2) product space Proj((x_t, y_t)) = (x_t) "
    "with latent vocabulary Omega = Sigma x Gamma; (3) 'pause-to-think' Proj stripping inserted "
    "thought tokens <s>y</s> before each observable token x_t.",
    title="Simple projection and examples",
)

projection_distribution_setting = setting(
    "For any simple projection Proj and latent distribution P over Omega^omega, the projected "
    "distribution Proj#P over Sigma^omega is computed via: (Proj#P)^{<=|x|}(x) = "
    "sum_{z in Proj^{-1}_{<omega}(x)} P^{<=|z|}(z). This summation is generally exponential in |x|, "
    "making exact computation infeasible. Monte-Carlo sampling is used to estimate it.",
    title="Projected distribution formula",
)

# ── Claims ────────────────────────────────────────────────────────────────────

claim_transformer_cannot_approximate_hmm = claim(
    "Under the assumption TC0 ⊊ NC1, there exists an HMM (A, B, lambda) that no Transformer "
    "can approximate: for any configuration (L, H, d_h, p), the semi-divergence D(P_{A,B,lambda}, P_f) "
    "cannot be reduced to zero by any f in TF(L, H, d_h, p). "
    "The proof embeds the 'cups-and-ball' function based on the symmetric group S5 into an HMM; "
    "tracking the ball requires O(t) sequential steps, which bounded-depth Transformers cannot replicate.",
    title="Theorem 3: Transformers cannot approximate all HMMs",
)

claim_simple_proj_can_model_hmm = claim(
    "For any HMM (A, B, lambda), there exist a finite set Omega, a simple projection Proj, "
    "and constants d_h*, p* such that for any d_h >= d_h* and p >= p*, "
    "the zero-layer Transformer (L=0) achieves min_{f in TF(0,1,d_h,p)} D(P_{A,B,lambda}, Proj#P_f) = 0. "
    "The key insight is that the latent distribution of an HMM is already Markov (memoryless), "
    "so no Transformer depth is needed to model it.",
    title="Theorem 9: Simple projections can model all HMMs",
)

claim_poly_simple_proj_insufficient = claim(
    "Under the assumption TC0 ⊊ NC1, there exists an HMM (A, B, lambda) such that for any "
    "finite set Omega, any polynomially-simple projection Proj (whose lifting has at most "
    "O(log t) auxiliary bits, giving |Proj^{-1}_{<omega}(x)| = O(poly(|x|))), and any "
    "Transformer configuration, the semi-divergence cannot be reduced to zero. "
    "This means at least superpolynomially many latent sequences are required for full expressivity.",
    title="Theorem 10: Polynomially-simple projections cannot model all HMMs",
)

claim_psimple_contains_phmm = claim(
    "The family P_simple = {Proj#P_f | simple proj Proj, f in TF_{<omega}(Omega)} "
    "strictly contains the HMM family P_HMM, and strictly contains the plain Transformer family "
    "P_plain = {P_f | f in TF_{<omega}(Sigma)}. Moreover, P_poly (polynomially-simple projections) "
    "and P_plain are incomparable — neither contains P_HMM.",
    title="Representation hierarchy: P_plain ⊊ P_simple ⊃ P_HMM",
)

claim_projection_reduces_norm = claim(
    "For any target distribution P* and simple projection Proj, the projected parametrization "
    "satisfies ||P*||_{F,Proj} << ||P*||_F, often with the projected norm being finite even "
    "when ||P*||_F = infinity (e.g., P* is an HMM). This reduction in complexity norm implies "
    "smaller training error and generalization error by the estimates (2) and (4).",
    title="Projection reduces complexity norm, improving learning",
)

claim_lifting_intractable = claim(
    "The size of the set Proj^{-1}_{<omega}(x) is in general exponential in |x|, making "
    "exact computation of the projected likelihood (Proj#P_f)^{<=|x|}(x) infeasible by "
    "direct enumeration. Monte-Carlo estimation via importance sampling is the only "
    "theoretically-correct approach that does not require additional Markov assumptions.",
    title="Lifting set is exponential; exact computation infeasible",
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_sep1 = support(
    [claim_lifting_intractable],
    claim_transformer_cannot_approximate_hmm,
    reason=(
        "By @transformer_setting, every Transformer f in TF(L,H,d_h,p) is implementable as "
        "a DLOGTIME-uniform TC0 circuit. By @tc0_nc1_conjecture (TC0 ⊊ NC1), the cups-and-ball "
        "function on the symmetric group S5 (which is NC1-complete by Barrington's theorem) "
        "cannot be computed by any TC0 circuit of polynomial size. By embedding this function "
        "into an @hmm_setting, the resulting HMM has an observable distribution that requires "
        "sequential processing of arbitrary depth, beyond any Transformer's capability."
    ),
    prior=0.9,
    background=[transformer_setting, tc0_nc1_conjecture, hmm_setting],
)

strat_sep2 = support(
    [claim_projection_reduces_norm],
    claim_simple_proj_can_model_hmm,
    reason=(
        "Given an HMM (A,B,lambda) with latent state space Omega, construct a simple "
        "@simple_projection_setting that maps latent-observable pairs back to observables. "
        "Then Proj#P_f matches the HMM's latent Markov chain: P_f is set to model the "
        "Markov transitions A, so no Transformer depth (L=0) is needed. The @projection_distribution_setting "
        "formula then recovers the HMM observable distribution exactly."
    ),
    prior=0.92,
    background=[simple_projection_setting, hmm_setting, projection_distribution_setting],
)

strat_sep3 = support(
    [claim_transformer_cannot_approximate_hmm],
    claim_poly_simple_proj_insufficient,
    reason=(
        "A 'meta' TC0 circuit composed of TC0 gates (with uniform depth and polynomial size) "
        "remains TC0. Since polynomially-simple projections have TC0 liftings with O(log t) "
        "auxiliary bits, any combined circuit for Proj#P_f remains TC0. By @tc0_nc1_conjecture, "
        "the same HMM embedding from Theorem 3 cannot be captured, establishing the lower bound."
    ),
    prior=0.88,
    background=[tc0_nc1_conjecture, transformer_setting],
)

strat_hierarchy = deduction(
    [claim_transformer_cannot_approximate_hmm, claim_simple_proj_can_model_hmm,
     claim_poly_simple_proj_insufficient],
    claim_psimple_contains_phmm,
    reason=(
        "By @claim_transformer_cannot_approximate_hmm, P_plain and P_poly cannot contain P_HMM. "
        "By @claim_simple_proj_can_model_hmm, P_simple contains P_HMM. "
        "By @claim_poly_simple_proj_insufficient, P_poly ⊊ P_simple. "
        "Together these establish the strict containment hierarchy P_plain ⊊ P_simple ⊃ P_HMM, "
        "with P_poly and P_plain both failing to capture P_HMM."
    ),
    prior=0.99,
)

strat_norm_reduction = support(
    [claim_simple_proj_can_model_hmm],
    claim_projection_reduces_norm,
    reason=(
        "Since @claim_simple_proj_can_model_hmm shows that the projected parametrization can "
        "exactly represent HMMs that P_plain cannot (||P_HMM||_F = infinity but "
        "||P_HMM||_{F,Proj} < infinity), the @projection_distribution_setting's formula for "
        "projected distributions implies that the norm is dramatically reduced. The training "
        "error and generalization error estimates then both benefit from the smaller norm."
    ),
    prior=0.93,
    background=[projection_distribution_setting],
)
