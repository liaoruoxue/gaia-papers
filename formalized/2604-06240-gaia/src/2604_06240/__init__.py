"""The Art of Building Verifiers for Computer Use Agents (arXiv:2604.06240)

Rosset et al., 2026. Microsoft Research.

This package formalizes the knowledge in the Universal Verifier paper:
four design principles for building reliable CUA trajectory verifiers,
validated by CUAVerifierBench and an auto-research study.
"""

from .motivation import *
from .s3_principles import *
from .s4_system import *
from .s5_experiments import *
from .s6_results import *
from .strategies import *
from .priors import *

# Core contributions exported as the package interface
__all__ = [
    # Motivation
    "four_principles_sufficient",
    "gains_are_architectural",
    "verifier_errors_compound",
    "auto_research_70pct",
    "human_expert_complementary_to_auto",
    # Principles
    "rubric_quality_critical",
    "separate_generation_scoring",
    "conditional_criteria_design",
    "two_pass_hallucination_detection",
    "process_outcome_separation",
    "process_outcome_diverge_on_blockers",
    "outcome_label_primary_intent",
    "controllable_vs_uncontrollable",
    "cascading_error_free_scoring",
    "relevance_matrix_approach",
    # System
    "uv_design_invariant",
    "uv_richer_output",
    "verifier_needs_all_screenshots",
    # Results
    "uv_outcome_kappa_internal",
    "uv_outcome_kappa_browserbase",
    "uv_fpr_near_zero",
    "uv_matches_human_interannotator",
    "upgrading_backbone_insufficient",
    "native_verifiers_overcount_success",
    "cuaverifierbench_novel",
]
