"""From Procedural Skills to Strategy Genes: Towards Experience-Driven Test-Time Evolution"""

from .motivation import *
from .s4_skill_probe import *
from .s4_gene_probe import *
from .s4_evolution_probe import *
from .s4_evolution_results import *

__all__ = [
    # CritPt baseline observations
    "obs_critpt_baseline_feb",
    "obs_critpt_baseline_mar",
    # Core thesis claims (exported cross-package interface)
    "thesis_form_over_content",
    "thesis_skill_misaligned",
    "thesis_gene_superior",
    # Primary empirical findings
    "obs_gene_passrate",
    "obs_skill_passrate",
    "obs_baseline_passrate",
    "gene_evolution_persistent_improvement",
    "law_gene_evolution_improves",
    # Key mechanistic findings
    "strategy_layer_critical",
    "gene_sensitive_to_content_not_structure",
    "documentation_dilution",
    "failure_distillation_principle",
    "structure_independent_value",
    "gene_reuse_scope_bounded",
    # Evolution results
    "obs_evolver_feb",
    "obs_evolver_mar",
    "gene_enables_accumulation",
]
