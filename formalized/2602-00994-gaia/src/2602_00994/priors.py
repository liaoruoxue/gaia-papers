"""Priors for independent (leaf) claims in the 2602-00994 package.

All other (derived) claims have their belief computed by Belief Propagation
from these leaves and from the in-DSL ``prior=`` warrants on strategies.

Prior-assignment rationale:

* **Direct empirical observations** quoted from a peer-reviewed table or
  figure of the paper get high priors (0.90+). The data themselves are not
  in dispute (we read them off Tables 1-3, Fig. 2-10); the question of
  whether they support the higher-level conclusions is what BP propagates.
* **Structural / definitional claims** about DART's architecture
  (disjoint adapters, frozen backbone) get very high priors (0.95+) -- they
  are matters of design that follow from the architecture description.
* **Architectural claims about prior work** (Multi-LoRA cannot disentangle,
  task-LoRA too coarse) get high priors (0.85-0.92) -- they are well-known
  properties of those methods.
* **The implicit ARL assumption** (joint training improves performance)
  is the proposition the paper sets out to refute. Its prior is set
  moderately (0.5-0.6) -- it is a reasonable default belief without
  evidence, but the contradiction operator with the LEAS finding will
  drive it down sharply during BP.
* **Theoretical efficiency claims** (8x memory, O(L^2) recompute) follow
  from straightforward complexity arguments and get high priors (0.95+).
* **Citations to peer-reviewed prior findings** (LoRA matches full
  fine-tuning, RL tunes sparse subnetworks) get high priors (0.85+).
"""

from . import (
    # ----- Tables (direct empirical observations) -----
    table1_qwen3b,
    table2_qwen7b,
    table3_hybrid,
    # ----- Figures: per-cell observations -----
    obs_lambda23_distribution,
    obs_arl_succeeds_in_interference_region,
    obs_gradient_angles,
    obs_dart_better_reasoning_3b,
    obs_dart_better_reasoning_7b,
    obs_lora_equals_searchr1,
    obs_2agent_strongest,
    obs_dart_approaches_2agent,
    obs_rank_insensitive,
    obs_dart_retrieval_acc,
    # ----- Structural / architectural claims -----
    claim_dart_zero_interaction,
    claim_design_matrix_invertible,
    claim_freeze_backbone_necessary,
    claim_freeze_no_performance_loss,
    claim_hybrid_no_interaction,
    # ----- Multi-LoRA characterization (related work) -----
    claim_multi_lora_cannot_disentangle,
    claim_task_lora_too_coarse,
    claim_prior_arl_no_interference_study,
    # ----- Theoretical efficiency (Appendix F) -----
    claim_2agent_memory_8x,
    claim_2agent_kv_recompute,
    claim_dart_simpler_stack,
    # ----- Implicit ARL assumption (refuted by LEAS) -----
    claim_joint_training_helps_assumed,
)


PRIORS: dict = {
    # =====================================================================
    # Tables 1-3: directly read from the paper's tables.
    # =====================================================================
    table1_qwen3b: (
        0.95,
        "Per-cell EM scores transcribed verbatim from Table 1 of the "
        "paper [@Li2026]. The numbers themselves are reported (and "
        "reproducible from the released setup). Slight uncertainty "
        "(<5%) is allowed for transcription / single-seed-run variance "
        "(no error bars are reported in the table).",
    ),
    table2_qwen7b: (
        0.95,
        "Per-cell EM scores transcribed verbatim from Table 2 [@Li2026]. "
        "Same reasoning as Table 1: directly read off, slight uncertainty "
        "for the lack of reported variance estimates.",
    ),
    table3_hybrid: (
        0.92,
        "Single-ability vs hybrid EM scores transcribed from Table 3 "
        "[@Li2026]. Lower than the main tables because Table 3 mixes "
        "two distinct evaluation regimes (DART_Reas / DART_Tool); the "
        "single-ability evaluation protocol is described less explicitly "
        "than the main protocol.",
    ),
    # =====================================================================
    # Figure-derived observations: directly read from Fig. 2-10.
    # =====================================================================
    obs_lambda23_distribution: (
        0.92,
        "The four percentages (66.10 / 61.84 / 67.24 / 42.30) are "
        "explicitly displayed in Fig. 2 [@Li2026]. The numbers depend "
        "on the 50-sample-per-question stochastic estimator and on the "
        "filtering rule (drop questions with all six models scoring 0); "
        "both sources of estimation noise leave residual uncertainty.",
    ),
    obs_arl_succeeds_in_interference_region: (
        0.85,
        "The overlay accuracy curve in Fig. 2 visibly rises in the "
        "$\\lambda_{23}^q < 0$ region. The qualitative claim is read "
        "from the figure, not from a numeric table; somewhat lower "
        "confidence because the per-bin accuracy values are not "
        "tabulated and the visual trend is the primary evidence.",
    ),
    obs_gradient_angles: (
        0.92,
        "Fig. 3A and Fig. 7A clearly show the bimodal angle distribution "
        "(same-role peaks below 30 degrees, different-role peaks near 90 "
        "degrees) across four (model, dataset) settings. The qualitative "
        "near-orthogonality conclusion is directly read off the "
        "histograms; quantitative averages are not tabulated.",
    ),
    obs_dart_better_reasoning_3b: (
        0.93,
        "Fig. 5 left panel directly displays the four EM bars (44.0, "
        "26.5, 44.6, 37.6) for Qwen2.5-3B-Base under fixed retrieval. "
        "Single-seed results, no variance reported.",
    ),
    obs_dart_better_reasoning_7b: (
        0.93,
        "Fig. 5 right panel directly displays the four EM bars (39.5, "
        "32.6, 46.0, 40.9) for Qwen2.5-7B-Base under fixed retrieval. "
        "Same reasoning as 3B case.",
    ),
    obs_lora_equals_searchr1: (
        0.88,
        "Fig. 6 radar plots show LoRA and Search-R1 traces nearly "
        "overlapping across all four backbones. The qualitative "
        "'nearly identical' claim is supported but the figure reports "
        "only the radar averages (30.3 / 33.6 / 38.9 / 39.6 for LoRA "
        "vs 31.6 / 36.6 / 39.6 / 38.9 for Search-R1) -- per-benchmark "
        "deltas are not separately tabulated, so confidence is high "
        "but not maximal.",
    ),
    obs_2agent_strongest: (
        0.93,
        "Fig. 6 shows 2-Agent achieving 40.6 / 40.4 / 41.9 / 42.0 -- the "
        "highest or near-highest on every backbone. Direct read-off.",
    ),
    obs_dart_approaches_2agent: (
        0.93,
        "Fig. 6 shows DART (40.5 / 39.9 / 41.6 / 41.9) within ~1 EM of "
        "2-Agent (40.6 / 40.4 / 41.9 / 42.0) on every backbone. Direct "
        "arithmetic comparison of the radar-average values reported in "
        "the figure.",
    ),
    obs_rank_insensitive: (
        0.92,
        "Appendix G Fig. 9 directly tabulates EM at ranks 8/16/32 plus "
        "the 2-agent reference. The variation across ranks is <1 EM "
        "and DART stays close to 2-agent at every rank. Direct read.",
    ),
    obs_dart_retrieval_acc: (
        0.93,
        "Fig. 10 (Appendix H) directly displays the eight retrieval "
        "accuracy bars (45.6, 64.1 on NQ-3B; 45.0, 63.3 on NQ-7B; 40.9, "
        "52.5 on HotpotQA-3B; 45.0, 47.9 on HotpotQA-7B). DART beats "
        "Search-R1 in every cell.",
    ),
    # =====================================================================
    # Structural / definitional claims: design facts about DART.
    # =====================================================================
    claim_dart_zero_interaction: (
        0.97,
        "Pure structural fact: the routing rule (each token -> exactly "
        "one of two disjoint adapters) plus backbone freezing implies "
        "that no parameter is updated by gradients of both roles. Hence "
        "$x_{23} \\equiv 0$ at every token. This is a definitional "
        "consequence of the DART architecture (Eq. 10 + Sec. 3.1's role "
        "router).",
    ),
    claim_design_matrix_invertible: (
        0.97,
        "Direct linear-algebra check: the six 6-dim binary capability "
        "vectors of the LEAS construction are visibly independent (the "
        "design matrix can be exhibited and its determinant computed). "
        "The author asserts identifiability and the construction is "
        "explicit; very high prior.",
    ),
    claim_freeze_backbone_necessary: (
        0.95,
        "Necessary-condition reasoning: if $W$ were trainable, gradients "
        "of both reasoning and tool-use tokens would write to $W$ -- "
        "exactly the situation LEAS shows produces interference. So "
        "freezing $W$ is required to maintain disentanglement. This is "
        "a definitional consequence of the LEAS interaction-indicator "
        "model.",
    ),
    claim_freeze_no_performance_loss: (
        0.85,
        "Two prior peer-reviewed findings cited [@Mukherjee2025; "
        "@Schulman2025] support that freezing the backbone with LoRA "
        "adapters does not sacrifice performance. The empirical "
        "near-2-Agent EM in Fig. 6 corroborates this. Lower than 0.9 "
        "because (i) the cited results are general and may not perfectly "
        "transfer to the ARL+QA setting; (ii) the 2-Agent gap is small "
        "but non-zero (~1 EM) in some cells.",
    ),
    claim_hybrid_no_interaction: (
        0.95,
        "Definitional: hybrid models are constructed by composing two "
        "*separately trained* models at inference time. By the LEAS "
        "interaction-indicator definition (Def. 4.2), $x_{ij} = 1$ "
        "requires *joint optimization* in shared parameter space; "
        "inference-time composition does not satisfy this, so the "
        "indicator is 0 by construction.",
    ),
    # =====================================================================
    # Multi-LoRA characterization: well-known properties of prior methods.
    # =====================================================================
    claim_multi_lora_cannot_disentangle: (
        0.88,
        "The soft-mixing property of router-driven Multi-LoRA (gradients "
        "flow through every active adapter) is well-documented in the "
        "MoELoRA / MixLoRA / MoLE literature. The conclusion that this "
        "*cannot* disentangle interfering capabilities is a slightly "
        "stronger claim than the architectural fact, so prior is 0.88 "
        "rather than 0.95. The DART paper supports it indirectly via "
        "the LoRA = Search-R1 ablation in Fig. 6.",
    ),
    claim_task_lora_too_coarse: (
        0.92,
        "Architectural fact: task-specific Multi-LoRA methods (LoRAHub, "
        "Modula) by design assign one adapter per task, so within a "
        "single task all token roles share one adapter. This is "
        "definitionally true for these methods.",
    ),
    claim_prior_arl_no_interference_study: (
        0.85,
        "A negative-existence claim about the prior literature. The "
        "authors review the major ARL systems (Toolformer, DeepSeekMath, "
        "Search-R1, AgentTuning) and confirm none target interference. "
        "Lower than 0.95 because exhaustive negative claims about the "
        "literature are inherently subject to revision (some niche prior "
        "work might address it).",
    ),
    # =====================================================================
    # Theoretical efficiency claims (Appendix F): complexity arguments.
    # =====================================================================
    claim_2agent_memory_8x: (
        0.95,
        "Standard memory-accounting under BF16 weights/grads + FP32 Adam "
        "states: each trainable backbone needs ~4P bytes; two backbones "
        "need ~8P. DART uses one frozen backbone + tiny adapters. The "
        "author also reports empirical 8x. Very high prior.",
    ),
    claim_2agent_kv_recompute: (
        0.95,
        "Standard transformer-inference complexity: a fresh model must "
        "build its own KV-cache from scratch for the entire history, "
        "$O(L^2)$ in self-attention. DART's adapter swap leaves the "
        "shared backbone's KV-cache valid, $O(1)$ extra. Standard fact.",
    ),
    claim_dart_simpler_stack: (
        0.95,
        "Engineering observation: a 2-Agent system requires an external "
        "orchestrator to format prompts and synchronize state between "
        "models; DART's single inference pipeline does not. This is a "
        "factual property of the deployment topologies.",
    ),
    # =====================================================================
    # Implicit ARL assumption: the proposition the paper refutes.
    # =====================================================================
    claim_joint_training_helps_assumed: (
        0.55,
        "Set just above 0.5 to reflect that prior to LEAS the assumption "
        "*was the prevailing view* in the ARL community (every major "
        "framework adopted it). The contradiction operator with "
        "@claim_interference_dominates will pull the posterior sharply "
        "down once the LEAS evidence flows through BP. NOT set higher "
        "because by the time of this paper the assumption is already "
        "questioned in [@Wu2025a; @Su2025] and the paper's whole purpose "
        "is to falsify it.",
    ),
}
