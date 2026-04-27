"""Gaia formalization of Irie, Yau & Gershman (2025): Blending Complementary
Memory Systems in Hybrid Quadratic-Linear Transformers (NeurIPS 2025)."""

from .motivation import *
from .s2_background import *
from .s3_methods import *
from .s4_experiments import *
from .s5_discussion import *

# Top-level exports — the paper's main external interface
__all__ = [
    # Definitions other packages may reference
    "def_quadratic_transformer",
    "def_linear_transformer",
    "def_deltanet",
    "def_hqlt",
    # Core complementarity claim
    "claim_complementarity_table",
    # The three blending designs
    "def_delayed_stream",
    "def_delayed_chunk",
    "def_synchronous",
    # Main theoretical predictions
    "claim_synchronous_keeps_expressivity",
    "claim_delayed_lose_expressivity",
    # Main experimental conclusions
    "claim_lm_baselines_comparable",
    "claim_hqlts_match_or_beat",
    "claim_lambada_synchronous_best",
    "claim_fw_choice_matters",
    "claim_window_drives_retrieval",
    "claim_hqlt_beats_matched_window",
    "claim_rl_supports_synchronous",
    # The synthesised design principle
    "claim_design_principle",
    "proposal_synchronous_best",
    # Limitations
    "claim_long_window_unavoidable",
    "claim_future_revival_mechanism",
]
