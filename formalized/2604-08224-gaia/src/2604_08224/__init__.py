"""
Externalization in LLM Agents: A Unified Review of Memory, Skills, Protocols
and Harness Engineering (arXiv 2604.08224).

Formalized knowledge package covering the externalization framework for LLM
agent infrastructure — memory, skills, protocols, and harness coordination.
"""

from .motivation import *
from .s2_history import *
from .s3_memory import *
from .s4_skills import *
from .s5_protocols import *
from .s6_harness import *
from .s7_interactions import *
from .s8_future import *
from . import priors  # noqa: F401 — loads prior assignments

__all__ = [
    # Core thesis (cross-package exports)
    "externalization_thesis",
    "three_externalization_dimensions",
    "representational_transformation_claim",
    # Historical arc
    "historical_arc_claim",
    "era_progression_law",
    "design_question_shift",
    # Memory
    "memory_recall_recognition",
    "retrieval_quality_primacy",
    "memory_architectural_progression",
    "memory_as_managed_infrastructure",
    "episodic_to_skill_boundary",
    # Skills
    "generation_to_composition",
    "packaged_expertise_claim",
    "skill_distillation_coupling",
    # Protocols
    "adhoc_to_structured",
    "protocol_governance_benefits",
    "multi_agent_protocol_necessity",
    # Harness
    "harness_not_fourth_dimension",
    "harness_design_question_shift",
    "sandboxing_isolation",
    # Cross-cutting
    "dimensions_not_independent",
    "externalized_update_advantage",
    "externalized_auditability_advantage",
    # Future
    "self_evolving_harness_claim",
    "governance_scale_challenge",
    "externalization_limits_claim",
]
