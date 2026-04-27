"""Section 5: Conclusion.

Synthesises the section-4 findings into the paper's headline conclusion
about Soft-ZCA whitening as a practical post-processing technique for
semantic code search.
"""

from gaia.lang import claim, support

from .motivation import code_search_anisotropy_problem, isotropy_benefits
from .s4_results import (
    finding_softzca_improves_code_search,
    finding_optimal_isotropy_depends_on_finetuning,
    finding_iso_mrr_relationship_nonlinear,
    obs_low_resource_r_helped,
)

# --- Conclusion claims ---

conclusion_geometry_matters = claim(
    "Embedding-space geometry (specifically the degree of isotropy) plays "
    "a crucial role in semantic code-search performance: consistently "
    "across model architectures and programming languages, the MRR "
    "improvement obtained by reshaping the embedding space via Soft-ZCA "
    "is non-trivial.",
    title="Conclusion: embedding-space geometry crucially affects code search",
)

conclusion_softzca_practical = claim(
    "Soft-ZCA whitening with an appropriately tuned eigenvalue regularizer "
    "$\\epsilon$ is a simple, lightweight post-processing technique that "
    "reliably improves the semantic code-search performance of code "
    "language models -- both pre-trained and contrastively fine-tuned -- "
    "across multiple programming languages, including held-out "
    "low-resource languages. It is therefore a practical solution for "
    "production code-search systems.",
    title="Conclusion: Soft-ZCA is a practical, robust post-processing tool",
)

# --- Strategies ---

strat_geometry_matters = support(
    [finding_softzca_improves_code_search, finding_iso_mrr_relationship_nonlinear],
    conclusion_geometry_matters,
    background=[isotropy_benefits, code_search_anisotropy_problem],
    reason=(
        "@finding_softzca_improves_code_search shows that simply changing "
        "the isotropy of the embedding space via Soft-ZCA produces "
        "consistent positive $\\Delta$MRR across all four configurations "
        "and seven languages. @finding_iso_mrr_relationship_nonlinear "
        "shows the relation is non-trivially monotonic. Together, these "
        "two findings -- combined with the prior expectation in "
        "@isotropy_benefits and @code_search_anisotropy_problem that "
        "isotropy underlies retrieval quality -- support the conclusion "
        "that embedding-space geometry crucially affects code search."
    ),
    prior=0.9,
)

strat_softzca_practical = support(
    [
        finding_softzca_improves_code_search,
        finding_optimal_isotropy_depends_on_finetuning,
        obs_low_resource_r_helped,
    ],
    conclusion_softzca_practical,
    reason=(
        "@finding_softzca_improves_code_search establishes consistent "
        "positive $\\Delta$MRR across four configurations and seven "
        "languages. @finding_optimal_isotropy_depends_on_finetuning gives "
        "concrete operational guidance ($\\epsilon \\in \\{0.1, 0.01\\}$ "
        "for base models, $\\epsilon = 0.0001$ for fine-tuned models). "
        "@obs_low_resource_r_helped demonstrates generalisation to a "
        "held-out low-resource language. Together these warrant the "
        "practical-utility conclusion."
    ),
    prior=0.88,
)

__all__ = [
    "conclusion_geometry_matters",
    "conclusion_softzca_practical",
]
