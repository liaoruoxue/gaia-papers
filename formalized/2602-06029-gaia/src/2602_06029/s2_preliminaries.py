"""Section 2: Preliminaries (Bayesian Optimization and Bayesian Experimental Design)."""

from gaia.lang import claim, setting

# --- BO formal setup ---

setup_bo_problem = setting(
    "**Bayesian Optimization (BO) formal setup.** Given an unknown objective function "
    "$f:\\mathcal{X}\\to\\mathbb{R}$, BO seeks the input "
    "$x^* = \\arg\\max_{x\\in\\mathcal{X}} f(x)$ over an admissible query set "
    "$\\mathcal{X}$, by combining a probabilistic surrogate model of $f$ with an "
    "acquisition function that selects the next query.",
    title="BO problem definition",
)

setup_dataset = setting(
    "**Observation dataset.** At iteration $t$ the available data is "
    "$D_t := \\{(x_1,y_1),\\ldots,(x_t,y_t)\\}$, where each observation is "
    "$y_t \\sim \\mathcal{N}(f(x_t), \\sigma^2(x_t))$—zero-mean Gaussian noise "
    "with standard deviation $\\sigma$ around the true function value.",
    title="Observation model",
)

setup_gp_surrogate = setting(
    "**Gaussian Process (GP) surrogate.** The surrogate model is a GP with "
    "joint normal posterior $p(f(x)|D_t) = \\mathcal{N}(\\mu_t(x), \\kappa_t(x,x'))$, "
    "where $\\mu_t(x)$ is the predictive mean and $\\kappa_t(x,x')$ is the kernel "
    "(predictive uncertainty). Bayesian inference combines a prior $p(f(x))$ with "
    "the likelihood $p(D_t|f(x))$ to yield the posterior.",
    title="Gaussian Process surrogate model",
)

setup_acquisition = setting(
    "**Acquisition function.** The next query is "
    "$x_{t+1} = \\arg\\max_{x\\in\\mathcal{X}} \\alpha(x|D_t)$, where "
    "$\\alpha:\\mathcal{X}\\to\\mathbb{R}$ measures the improvement that the next "
    "query is expected to provide. Examples include probability of improvement, "
    "expected improvement, upper confidence bound, and entropy search variants.",
    title="Acquisition function definition",
)

# --- BED formal setup ---

setup_bed_problem = setting(
    "**Bayesian Experimental Design (BED) formal setup.** Given a parameter of "
    "interest $\\theta$ (which can be explicit model parameters or any implicitly "
    "defined quantity such as a function optimum), BED sequentially selects "
    "experimental designs $x\\in\\mathcal{X}$ to maximize the *expected information "
    "gain* (EIG) [@Chaloner1995] about $\\theta$:\n\n"
    "$$\\mathrm{EIG}(x|D_t) = H[p(\\theta|D_t)] - "
    "\\mathbb{E}_{p(y|x,D_t)}[H[p(\\theta|D_t \\cup (x,y))]] = I(\\theta;(x,y)|D_t),$$\n\n"
    "i.e., the expected reduction in posterior entropy of $\\theta$, equivalently "
    "the conditional mutual information between $\\theta$ and the next observation pair.",
    title="BED objective: expected information gain",
)

# --- Bridge claim: BO + BED unification by AIF ---

claim_bo_bed_complementary = claim(
    "BO is *predominantly goal-seeking* (locating an optimizer with few "
    "evaluations) while BED is *predominantly information-seeking* (selecting "
    "experiments to maximize expected information gain about latent parameters). "
    "Although developed historically as separate paradigms, both are responses to "
    "the same imperative: act under uncertainty to improve outcomes while reducing "
    "uncertainty.",
    title="BO and BED are complementary",
)

claim_aif_unifies_bo_bed = claim(
    "**Active Inference unifies BO and BED.** Minimizing the Expected Free Energy "
    "yields a single decision objective whose two summands are the pragmatic term "
    "(favoring actions that produce preferred outcomes—exploitation) and the "
    "epistemic term (favoring actions that reduce uncertainty about latent "
    "quantities—exploration). Under this view, exploration and exploitation are "
    "not separate heuristics but two aspects of one principle.",
    title="AIF unifies goal-seeking and information-seeking",
)

