"""Knowledge package for Diera, Galke, Scherp 2024 (arXiv:2411.17538).

"Isotropy Matters: Soft-ZCA Whitening of Embeddings for Semantic Code Search"
"""

from .motivation import *  # noqa: F401,F403
from .s2_whitening import *  # noqa: F401,F403
from .s3_apparatus import *  # noqa: F401,F403
from .s4_results import *  # noqa: F401,F403
from .s5_conclusion import *  # noqa: F401,F403
from .s6_appendix import *  # noqa: F401,F403

# Cross-package exports: the paper's headline conclusions and the methodological
# contribution claim are the most reusable units of knowledge.
__all__ = [
    # Section 4 -- empirical findings
    "finding_code_lms_anisotropic",
    "finding_finetuning_weak_on_isotropy",
    "finding_iso_mrr_relationship_nonlinear",
    "finding_code_vs_comment_iso_similar",
    "finding_softzca_improves_code_search",
    "finding_optimal_isotropy_depends_on_finetuning",
    # Section 5 -- conclusions
    "conclusion_geometry_matters",
    "conclusion_softzca_practical",
    # Section 6 -- appendix findings
    "finding_separate_whitening_better",
    # Section 1 -- contributions (interface for downstream packages)
    "contribution_softzca_method",
]
