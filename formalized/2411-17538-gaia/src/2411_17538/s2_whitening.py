"""Section 2: Whitening of the Embeddings.

Defines the whitening transformation framework, ZCA whitening as a specific
choice, and introduces Soft-ZCA as the paper's methodological contribution.
"""

from gaia.lang import claim, setting, deduction

from .motivation import zca_whitening_known_isotropy

# --- Mathematical definitions (settings; not questionable) ---

whitening_setup = setting(
    "Given a set of embeddings $Z \\in \\mathbb{R}^{N \\times d}$ (N samples, "
    "d features), a whitening transformation produces $H = W Z^{\\top}$, "
    "where $W \\in \\mathbb{R}^{d \\times d}$ is the whitening matrix and "
    "$H \\in \\mathbb{R}^{N \\times d}$ is the whitened embedding. The "
    "transformation is required to satisfy $W \\Sigma W^{\\top} = I$, where "
    "$\\Sigma$ is the covariance matrix of $Z$ and $I$ is the identity matrix.",
    title="Whitening transformation setup",
)

whitening_rotational_freedom = setting(
    "Because the only condition imposed on $W$ is $W \\Sigma W^{\\top} = I$, "
    "there are infinitely many valid whitening matrices (related to one "
    "another by an arbitrary orthogonal rotation). Common choices include "
    "Principal Component Analysis (PCA), Zero-phase Component Analysis "
    "(ZCA), and Cholesky-decomposition-based whitening, each with different "
    "tradeoffs [@Kessy2018].",
    title="Rotational freedom of whitening transformations",
)

zca_definition = setting(
    "The ZCA whitening matrix is defined as $W_{ZCA} = \\Sigma^{-1/2}$. "
    "Using singular value decomposition this can be rewritten as "
    "$W_{ZCA} = U \\Lambda^{-1/2} U^{\\top}$, where $U$ is the orthogonal "
    "matrix of eigenvectors of $\\Sigma$ and $\\Lambda$ is the diagonal "
    "matrix of $\\Sigma$'s eigenvalues.",
    title="ZCA whitening matrix definition",
)

soft_zca_definition = setting(
    "Soft-ZCA whitening adds an eigenvalue regularizer $\\epsilon \\geq 0$ "
    "to the eigenvalues before inverse square root, modifying the whitening "
    "matrix to $W_{ZCA} = U (\\Lambda + \\epsilon I)^{-1/2} U^{\\top}$, "
    "where $I$ is the identity matrix. Setting $\\epsilon = 0$ recovers "
    "standard ZCA whitening.",
    title="Soft-ZCA whitening matrix definition (with eigenvalue regularizer)",
)

# --- Claims about properties of the methods ---

zca_correlation_property = claim(
    "Among whitening transformations satisfying $W \\Sigma W^{\\top} = I$, "
    "ZCA whitening (i.e. $W_{ZCA} = \\Sigma^{-1/2}$) maintains the highest "
    "correlation between the whitened output $H$ and the original input $Z$ "
    "[@Kessy2018]. This property makes ZCA the most appropriate whitening "
    "transformation for embedding spaces, where preserving as much of the "
    "original semantic geometry as possible is desirable.",
    title="ZCA preserves the most correlation with the original embeddings",
)

zca_amplifies_noise_at_small_eigenvalues = claim(
    "When any eigenvalue $\\lambda_i$ of $\\Sigma$ is close to 0, the "
    "corresponding factor $\\lambda_i^{-1/2}$ in standard ZCA whitening "
    "becomes exceedingly large. As a result, the whitening transformation "
    "amplifies noise and insignificant components in the data, which "
    "degrades the resulting embedding quality.",
    title="Standard ZCA amplifies noise on small-eigenvalue directions",
)

soft_zca_controls_whitening = claim(
    "By placing a positive lower bound $\\epsilon$ on the regularized "
    "eigenvalues $(\\lambda_i + \\epsilon)$, Soft-ZCA bounds the magnitude "
    "of $(\\lambda_i + \\epsilon)^{-1/2}$ from above, retaining more of the "
    "original signal and variance. As $\\epsilon$ increases, the strength "
    "of the whitening transformation decreases, giving direct control over "
    "the whitening intensity (and therefore the isotropy) of the resulting "
    "embeddings.",
    title="Soft-ZCA's eigenvalue regularizer controls the strength of whitening",
)

# --- Strategies (mathematical derivations from definitions) ---

# Soft-ZCA's noise-control property follows mathematically from its definition
# combined with the noise-amplification problem of vanilla ZCA.
strat_soft_zca_controls = deduction(
    [zca_amplifies_noise_at_small_eigenvalues],
    soft_zca_controls_whitening,
    background=[soft_zca_definition, zca_definition],
    reason=(
        "By @soft_zca_definition the regularizer enters as "
        "$(\\Lambda + \\epsilon I)^{-1/2}$. Whenever some eigenvalue "
        "$\\lambda_i \\to 0$, @zca_amplifies_noise_at_small_eigenvalues "
        "shows that the unregularized ZCA factor $\\lambda_i^{-1/2}$ blows "
        "up. Adding $\\epsilon > 0$ caps the factor at "
        "$(\\lambda_i + \\epsilon)^{-1/2} \\leq \\epsilon^{-1/2}$, which "
        "monotonically decreases the magnitude of the whitening operator as "
        "$\\epsilon$ grows. This gives a direct, monotone knob on the "
        "whitening strength."
    ),
    prior=0.97,
)

# ZCA's preference over PCA/Cholesky for embeddings is the paper's
# justification for choosing ZCA as the base of Soft-ZCA. It is grounded in
# the cited Kessy et al. analysis but also reused as background motivating
# the contribution.
strat_zca_choice = deduction(
    [zca_correlation_property],
    zca_whitening_known_isotropy,
    background=[whitening_setup, whitening_rotational_freedom, zca_definition],
    reason=(
        "Within the family of valid whitening transformations described in "
        "@whitening_setup and @whitening_rotational_freedom, the explicit "
        "ZCA matrix from @zca_definition is selected because it maximizes "
        "correlation with the original embeddings (@zca_correlation_property "
        "[@Kessy2018]). The paper inherits the prior literature's finding "
        "that this choice yields effective isotropy improvement on text "
        "embeddings [@Su2021]."
    ),
    prior=0.92,
)

__all__ = [
    "whitening_setup",
    "whitening_rotational_freedom",
    "zca_definition",
    "soft_zca_definition",
    "zca_correlation_property",
    "zca_amplifies_noise_at_small_eigenvalues",
    "soft_zca_controls_whitening",
]
