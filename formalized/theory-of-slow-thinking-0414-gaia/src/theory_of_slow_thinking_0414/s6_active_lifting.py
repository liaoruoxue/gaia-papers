"""Section 6: The Agency of Perceptual Representation — Active Lifting"""

from gaia.lang import claim, setting, support, deduction

from .motivation import (
    claim_active_lifting_derives_language,
    claim_unified_encoder_approach,
    claim_linguistic_coupling_generative,
)
from .s2_separation import (
    simple_projection_setting,
    projection_distribution_setting,
    claim_psimple_contains_phmm,
)
from .s3_samplers import (
    claim_explanatory_sampler_advantage,
    inquisitive_sampler_setting,
    posterior_sampler_setting,
)

# ── Background settings ──────────────────────────────────────────────────────

active_lifting_problem_setting = setting(
    "Problem 3 (active lifting): Let P* be a target distribution over X = Sigma^*. "
    "Find a latent vocabulary Omega (finite set), a latent distribution P over Omega^omega, "
    "and a sampler Q over Proj^{-1}_{<omega} (where Proj is implicitly determined by the "
    "training objective) such that the unified objective (62) is minimized. "
    "Unlike the static theory (Problem 2), the projection Proj is NOT prescribed — "
    "it emerges from the optimization.",
    title="Active lifting problem (Problem 3): projection emerges from training",
)

active_lifting_training_setting = setting(
    "The active lifting training objective: for each step t, minimize "
    "C_t = KL(Q^{<=t}_*(·) || P^{<=t}) = E_{Z~Q^{<=t}_*}[-log P^{<=t}(Z) + log Q^{<=t}_*(Z)]. "
    "This corresponds to training P to approximate the marginal of the posterior sampler Q^{<=t}_*. "
    "The overall objective is sum_t C_t (or the time-weighted version from Section 4). "
    "The posterior Q^{<=t}_* is implicitly defined as the optimal sampler at step t.",
    title="Active lifting training objective",
)

minimum_length_coding_setting = setting(
    "Minimum-length coding (source coding / Huffman coding): for a distribution P* over a "
    "countable set X, assigns codewords c(x) in {0,1}* to minimize E_{X~P*}[|c(X)|]. "
    "The optimal code satisfies |c(x)| = -log_2 P*(x) (Shannon entropy bound). "
    "Active lifting training objective (99) resembles minimum-length coding: "
    "the sampled latent sequence Z plays the role of the codeword, and the training "
    "tries to minimize E[|Z|] subject to the sampler being learnable by P.",
    title="Minimum-length coding analogy",
)

# ── Claims ────────────────────────────────────────────────────────────────────

claim_active_lifting_generalizes_static = claim(
    "Active lifting is strictly more general than the static theory: the static theory "
    "corresponds to the special case of active lifting where the projection function Proj "
    "is prescribed and fixed. Any static theory solution (Sigma, Omega, Proj, P, Q) is "
    "a feasible solution to the active lifting problem. The active lifting optimal solution "
    "implicitly develops a deterministic projection function from the training data.",
    title="Active lifting generalizes static theory (Proj emerges implicitly)",
)

claim_training_resembles_min_length_coding = claim(
    "The active lifting training objective (99) highly resembles minimum-length coding: "
    "the sampled latent sequence Z(x) plays the role of a code for the observation x, "
    "and the training simultaneously optimizes compression efficiency (P learns to match "
    "the marginal Q^omega_*) and regularity (the coding must be learnable by P). "
    "Specifically, E_{X~P*}[|c(X)|] ≈ E_{X~P*}[E_{Z~Q(·|X)}[sum_t -log Q^{<=t}_*(Z_{<=t})]]. "
    "This resemblance means a well-trained model invents a descriptive language for its data.",
    title="Training objective resembles minimum-length coding",
)

claim_concept_induction_emerges = claim(
    "When trained on a distribution P* of photographs via the active lifting objective, "
    "the optimal sampler Q*^omega spontaneously develops latent tokens z_t that encode "
    "recurring perceptual objects and their parts, attributes, and relations. This occurs "
    "because objects are the most distinctive features from a minimum-length coding perspective "
    "(they reduce uncertainty most efficiently). This is a form of unsupervised concept induction.",
    title="Concept induction emerges from active lifting training",
)

claim_linguistic_regularity_emerges = claim(
    "The active lifting training objective forces the sampler Q to arrange latent concepts "
    "in a learnable format (grammar/schema) so that the latent distribution P can model them "
    "with bounded-depth circuits. For image data, concepts might appear in SVO format; "
    "for text, the linear reading order is most learnable. Thus, training not only induces "
    "perceptual concepts but also organizes them into a learnable language.",
    title="Linguistic regularity emerges: latent sequences form a learnable language",
)

claim_time_axis_inference = claim(
    "Under active lifting, inference (encoding) is endowed with an internal time axis indexed "
    "by t = 0, 1, ..., omega. At each step t, the estimator p_{t,n} for P*(x) uses t latent "
    "tokens per sample (sampled sequentially by Q). The estimation improves as t increases "
    "(better generator G^{<=t}(x|z) as P^{<=t}_*(x|z) becomes more deterministic), creating "
    "a speed-accuracy tradeoff: more observation steps increase both compute and accuracy.",
    title="Inference has internal time axis: perception is iterative",
)

claim_visual_representation_emerges = claim(
    "For image data, the active lifting framework predicts that a model trained on the "
    "unified objective may spontaneously develop a human-like multiscale compositional "
    "visual representation — encoding coarse features (mammal/rodent/capybara) before fine "
    "details — without any architectural or training prior for this structure. "
    "The representation might unify three common computer vision representations: "
    "patch auto-regression, diffusion (score matching), and part-based modeling.",
    title="Human-like visual representation emerges from active lifting",
)

claim_linguistic_coupling_derivation = claim(
    "The active lifting framework provides a principled derivation of the 'linguistic coupling' "
    "approach to generative modeling: the posterior data distribution P^{<=t}_*(x|z) provides "
    "a non-trivial yet tractable regression target for the generator G. Training G on this target "
    "is described by loss (104): E_{X~P*} E_{Z~Q^{<=t}(·|X)}[-log G^{<=t}(X|Z)]. "
    "This offers an alternative to free coupling (GAN, VAE) and product coupling (diffusion, flow matching).",
    title="Linguistic coupling derived from active lifting",
)

claim_active_lifting_conditional_decoding = claim(
    "For text data, active lifting enables conditional decoding (given prompt x, sample P*(·|[x])) "
    "by training the sampler Q to approximate the conditional sampler Q^omega_{<omega}(·|x) = "
    "integral Q^omega(·|x') dP*(x'|[x]). Since P*'s support is prefix-free, Q^omega(·|x) and "
    "Q^omega_{<omega}(·|x) coincide at sequence boundaries, making it natural to reuse the "
    "unconditional sampler for conditional decoding.",
    title="Active lifting enables conditional decoding for text via shared sampler",
)

# ── Strategies ────────────────────────────────────────────────────────────────

strat_generalizes_static = support(
    [claim_training_resembles_min_length_coding],
    claim_active_lifting_generalizes_static,
    reason=(
        "The @active_lifting_problem_setting does not constrain the projection Proj, "
        "while @simple_projection_setting is a specific choice of Proj. Any feasible solution "
        "to the static problem (Problem 2) with a fixed Proj is also feasible for the active "
        "lifting problem — the projection just becomes one free variable. The active lifting "
        "optimizer can always choose to fix Proj = any specific simple projection, recovering "
        "the static theory as a special case."
    ),
    prior=0.95,
    background=[active_lifting_problem_setting, simple_projection_setting],
)

strat_min_length_coding = support(
    [claim_active_lifting_generalizes_static],
    claim_training_resembles_min_length_coding,
    reason=(
        "The @active_lifting_training_setting objective sum_t C_t = sum_t E[log Q^{<=t}_*(Z) - "
        "log P^{<=t}(Z)] can be reorganized (equation 99 in the paper) as "
        "E_{X~P*}[sum_t -log P*(X | z(X)_{<=t})] where z(X) = Q^omega_*(X) is the optimal "
        "latent sequence for X. This closely parallels @minimum_length_coding_setting's "
        "E[|c(X)|] = E[-log_2 P*(X)]. The approximation is tight when P*(X|z(X)_{<=t}) is "
        "close to 1 for t >= |c(X)|, as illustrated in Figure 16 of the paper."
    ),
    prior=0.87,
    background=[active_lifting_training_setting, minimum_length_coding_setting],
)

strat_concept_induction = support(
    [claim_training_resembles_min_length_coding],
    claim_concept_induction_emerges,
    reason=(
        "By @claim_training_resembles_min_length_coding, the training objective induces efficient "
        "coding of observations. For photographic data, recurring objects and their attributes "
        "are the most information-rich patterns (they reduce posterior entropy fastest per latent token). "
        "The @active_lifting_training_setting's minimization of C_t therefore rewards encoding "
        "these objects as latent tokens z_t, leading to spontaneous concept formation without "
        "any supervision about object identity."
    ),
    prior=0.78,
    background=[active_lifting_training_setting],
)

strat_linguistic_regularity = support(
    [claim_concept_induction_emerges, claim_psimple_contains_phmm],
    claim_linguistic_regularity_emerges,
    reason=(
        "By @claim_concept_induction_emerges, the sampler Q* induces perceptual concepts in latent "
        "tokens. However, the latent distribution P must model Q^omega_* with bounded-depth circuits "
        "(@simple_projection_setting context). By Theorem 3 (Transformers are TC0, from @claim_psimple_contains_phmm), "
        "P cannot model arbitrary sequential dependencies. Therefore, the optimal Q* must also arrange "
        "concepts in a format learnable by P (e.g., linear order, SVO grammar), spontaneously developing "
        "linguistic regularity."
    ),
    prior=0.78,
    background=[simple_projection_setting],
)

strat_visual_repr = support(
    [claim_concept_induction_emerges, claim_linguistic_regularity_emerges],
    claim_visual_representation_emerges,
    reason=(
        "For image data, @claim_concept_induction_emerges predicts spontaneous object encoding. "
        "By @claim_linguistic_regularity_emerges, these concepts must be arranged in a learnable "
        "format. The most uncertainty-efficient ordering for images is coarse-to-fine (consistent "
        "with how humans perceive as in Example 3 of the paper: mammal -> rodent -> capybara), "
        "yielding a multiscale compositional representation. The resulting latent codes "
        "correspond to patch auto-regression (spatial), diffusion (temporal refinement), "
        "and part-based modeling (compositional hierarchy)."
    ),
    prior=0.72,
)

strat_linguistic_coupling = support(
    [claim_training_resembles_min_length_coding],
    claim_linguistic_coupling_derivation,
    reason=(
        "The @active_lifting_training_setting shows that the posterior P^{<=t}_*(x|z) is "
        "approximately deterministic at large t (Remark 24 in the paper). This non-trivial "
        "target can be fit by a generator G via regression loss (103-104) in the paper. "
        "By @claim_training_resembles_min_length_coding, z acts as a description code for x, "
        "so G acts as an 'artist creating x from its description z' — this is linguistic coupling. "
        "Unlike free coupling (arbitrary G) or product coupling (trivial G = P*), linguistic "
        "coupling gives G a structured, learnable target."
    ),
    prior=0.82,
    background=[active_lifting_training_setting],
)

strat_time_axis = support(
    [claim_active_lifting_generalizes_static],
    claim_time_axis_inference,
    reason=(
        "Under @active_lifting_training_setting, the trained P ≈ Q^omega_* and G^{<=t} ≈ P^{<=t}_*. "
        "The estimator p_{t,n} in equation (106) uses n samples Z^(i) ~ Q^{<=t}(·|x) to estimate "
        "P*(x) via importance weighting. At t=0, posterior is trivial (P^{<=0}_*(·|x) = P*); "
        "at t=omega, posterior is deterministic. Increasing t improves generator accuracy but "
        "requires more sampler queries, creating the speed-accuracy tradeoff."
    ),
    prior=0.85,
    background=[active_lifting_training_setting, posterior_sampler_setting],
)

strat_active_lifting_language = deduction(
    [claim_concept_induction_emerges, claim_linguistic_regularity_emerges],
    claim_active_lifting_derives_language,
    reason=(
        "By @claim_concept_induction_emerges, active lifting induces perceptual concepts. "
        "By @claim_linguistic_regularity_emerges, these concepts are organized into a learnable "
        "format (grammar/schema). Together these constitute an efficient and regular 'language' "
        "as claimed in @claim_active_lifting_derives_language."
    ),
    prior=0.99,
)

strat_unified_encoder = deduction(
    [claim_time_axis_inference, claim_concept_induction_emerges],
    claim_unified_encoder_approach,
    reason=(
        "By @claim_time_axis_inference, active lifting provides a unified encoder architecture "
        "for any modality: train Q and P on the active lifting objective, then use Q for encoding "
        "via the iterative time-axis estimator. By @claim_concept_induction_emerges, the resulting "
        "representation spontaneously develops structure appropriate to each modality (visual concepts "
        "for images, linguistic concepts for text), without modality-specific architectural design."
    ),
    prior=0.99,
)

strat_linguistic_coupling_final = deduction(
    [claim_linguistic_coupling_derivation],
    claim_linguistic_coupling_generative,
    reason=(
        "By @claim_linguistic_coupling_derivation, active lifting directly derives the linguistic "
        "coupling approach, providing a principled target G for the generator. This resolves "
        "the non-uniqueness problem of @claim_linguistic_coupling_generative: the training "
        "objective (105) simultaneously optimizes the sampler Q and generator G to be consistent, "
        "making the solution more tractable than free coupling."
    ),
    prior=0.99,
)
