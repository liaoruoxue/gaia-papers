"""Test-Time Training with KV Binding Is Secretly Linear Attention.

Formalization of Liu, Elflein, Litany, Gojcic, Li (2026) [@Liu2026];
arXiv:2602.21204v2.

Three contributions:
  - Empirical analysis revealing four anomalies that contradict the
    storage-and-retrieval (memorization) interpretation of TTT-with-KV-binding.
  - Theoretical equivalence: a broad class of TTT-KVB architectures
    (multi-layer MLP inner loops, momentum) can be analytically rewritten
    as a learned linear attention operator (Theorems 5.1-5.3).
  - Practical consequences: principled architectural simplifications
    (six-step ablation reducing TTT to standard linear attention), a
    fully parallel formulation of TTT preserving performance and yielding
    up to 4.0x throughput, and a unified reduction of diverse TTT variants.
"""

from .motivation import *  # noqa: F401,F403
from .s2_related_work import *  # noqa: F401,F403
from .s3_preliminaries import *  # noqa: F401,F403
from .s4_anomalies import *  # noqa: F401,F403
from .s5_linear_attention_equivalence import *  # noqa: F401,F403
from .s6_simplifications_and_parallelization import *  # noqa: F401,F403
from .s7_experiments import *  # noqa: F401,F403

__all__ = [
    # core contributions (cross-package interface)
    "claim_contribution_anomalies",
    "claim_contribution_equivalence",
    "claim_contribution_practical",
    # central findings
    "claim_memorization_view_falsified",
    "claim_ttt_is_linear_attention",
    "claim_simplifications_preserve_performance",
    "claim_parallel_form_speedup",
    "claim_anomalies_explained_by_la_view",
]
