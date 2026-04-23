from .motivation import *
from .s2_values_principles import *
from .s3_architecture import *
from .s4_query_loop import *
from .s5_permissions import *
from .s6_extensibility import *
from .s7_context_memory import *
from .s8_subagents import *
from .s9_persistence import *
from .s10_openclaw import *
from .s11_discussion import *
from .s12_future import *

__all__ = [
    # Motivation (Introduction)
    "qualitatively_new_workflows",
    "agentic_shift_introduces_new_requirements",
    # Section 2: Values and Principles
    "five_values_motivate_architecture",
    "design_principles_distinguish_from_alternatives",
    "long_term_capability_preservation_lens",
    # Section 3: Architecture
    "reasoning_separation_claim",
    "single_query_loop_claim",
    "deny_first_safety_posture",
    "context_window_as_binding_constraint",
    "seven_independent_safety_layers",
    "architecture_coherence",
    # Section 4: Query Loop
    "react_orchestration_claim",
    "graduated_compaction_claim",
    "concurrent_serial_tool_execution",
    "recovery_mechanisms_claim",
    # Section 5: Permissions
    "approval_fatigue_observation",
    "deny_first_motivated_by_approval_fatigue",
    "graduated_trust_spectrum_claim",
    "defense_in_depth_shared_failure_modes",
    "pre_trust_ordering_vulnerability",
    # Section 6: Extensibility
    "four_mechanisms_justified",
    "agent_tool_vs_skill_tool",
    "tool_pool_pre_filtering",
    # Section 7: Context and Memory
    "file_based_memory_vs_alternatives",
    "claudemd_probabilistic_compliance",
    # Section 8: Subagents
    "isolated_context_boundaries",
    "summary_only_return",
    "worktree_isolation_design",
    "two_tier_permission_scoping",
    # Section 9: Persistence
    "append_only_auditability",
    "no_permission_restore_on_resume",
    "compact_boundary_read_time_patching",
    # Section 10: OpenClaw comparison
    "different_trust_boundaries",
    "loop_vs_control_plane",
    "composable_layered_design_space",
    # Section 11: Discussion
    "infrastructure_over_decision_scaffolding",
    "value_tensions_are_structural",
    "bounded_context_code_quality_prediction",
    "long_term_sustainability_gap",
    # Section 12: Future directions
    "architecture_as_snapshot",
    "memory_experiential_tier_gap",
    "sustainability_as_first_class_design",
    "governance_external_constraint",
]
