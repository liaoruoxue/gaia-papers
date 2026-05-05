"""Section 7 + Appendix C: Related works -- LLM-based MAS, recursive
language-model scaling, latent-space collaboration, and the positioning
of RecursiveMAS as the first system-level extension of recursive
scaling to multi-agent systems.

Source: Yang et al. 2026 [@Yang2026RecursiveMAS], Section 7 + Appendix C.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# Related work category claims
# ---------------------------------------------------------------------------

claim_mas_topology_literature = claim(
    "**Existing MAS topology literature.** Standard multi-agent system "
    "topologies extend single-LLM solving to a collaborative setting "
    "[@MASsurvey; @AutoGen]. The most widely studied topologies are "
    "(i) **sequential** pipelines [@CAMEL; @ChatDev], where role-"
    "specialized agents are arranged linearly to decompose and "
    "resolve problems in order, and (ii) **mixture** pipelines "
    "[@MoA; @GraphOfAgents], where multiple domain-expert agents "
    "reason in parallel and aggregate.",
    title="Related work: MAS topologies (sequential pipelines + mixture-of-agents)",
)

claim_textual_feedback_optimization_literature = claim(
    "**Existing MAS optimization via textual feedback.** One line of "
    "MAS work improves systems through *textual feedback* signals: "
    "TextGrad [@TextGrad] propagates natural-language feedback as "
    "textual gradients to refine each agent's contextual prompt; "
    "other methods iteratively refine shared context to elicit "
    "more aligned responses. These methods optimize the inter-"
    "agent text channel rather than the agent parameters or the "
    "system as a whole.",
    title="Related work: textual-feedback MAS optimization (TextGrad)",
)

claim_per_agent_training_literature = claim(
    "**Existing MAS optimization via per-agent training.** A more "
    "principled line trains each MAS agent separately with role-"
    "specific responses (MALT [@MALT]). This improves individual "
    "agents but does not co-evolve cross-agent collaboration as a "
    "unified system, and it requires updating all model parameters "
    "of every agent.",
    title="Related work: per-agent training (MALT) -- improves agents in isolation, not the system",
)

claim_recursive_lm_literature = claim(
    "**Existing recursive (looped) language-model literature.** "
    "Recent studies explore **recursion as an alternative scaling "
    "axis** for LLMs [@MoR; @Geiping2025; @LoopRPT], where the same "
    "computation blocks are reused across multiple rounds to "
    "increase reasoning depth and iteratively refine hidden "
    "representations. Recursive language models include LoopLM "
    "[@LoopLM] (pre-trained looped LMs with iterative latent "
    "computation), tiny recursive networks [@TinyRecursive], the "
    "Hierarchical Reasoning Model [@HRM], and recursive self-calling "
    "schemes for long-context inference [@RecursiveLM2025]. **All "
    "existing methods focus on recursion *inside* a single language "
    "model.**",
    title="Related work: recursive LMs scale within one model -- no system-level recursion before RecursiveMAS",
)

claim_first_system_level_recursion = claim(
    "**RecursiveMAS is the first system-level extension of recursive "
    "scaling.** While prior recursion-as-scaling work [@LoopLM; "
    "@TinyRecursive; @MoR; @Geiping2025; @HRM; @LoopRPT] applies "
    "recursion only *within* a single language model, RecursiveMAS "
    "is the first to extend the recursive scaling paradigm to "
    "**system level** -- treating an entire heterogeneous LLM-based "
    "MAS as one recursive computation. This is the conceptual "
    "extension claimed by contribution C1.",
    title="Positioning: RecursiveMAS = first system-level extension of recursive scaling to MAS",
)

# ---------------------------------------------------------------------------
# Appendix C: latent-space collaboration related work
# ---------------------------------------------------------------------------

claim_latent_space_communication_literature = claim(
    "**Existing latent-space LLM communication literature** "
    "(Appendix C). Beyond text-based interaction, recent studies "
    "explore the latent space as an alternative medium for LLM "
    "communication: (a) transferring hidden embeddings for cross-"
    "model communication [@DuLatentComm; @C2C], (b) reusing "
    "internal states to share information across LLMs [@KVcomm], "
    "and (c) latent interfaces for coordinating multiple agents "
    "[@ThoughtComm; @ZouLatentMAS]. These works treat latent "
    "exchanges as one-shot or pairwise. RecursiveMAS differs by "
    "treating latent information as part of a **system-level "
    "*recursive* information flow**, enabling heterogeneous agents "
    "to recursively collaborate and improve as a unified MAS.",
    title="Related work: prior latent-space LLM comm. is one-shot / pairwise; RecursiveMAS makes it recursive system-level",
)

# ---------------------------------------------------------------------------
# Positioning summary
# ---------------------------------------------------------------------------

claim_positioning_summary = claim(
    "**Positioning summary.** RecursiveMAS sits at the intersection "
    "of three existing axes: "
    "(P1) *MAS topology* -- it is structure-agnostic and runs under "
    "Sequential / Mixture / Distillation / Deliberation patterns; "
    "(P2) *Recursive scaling* -- it generalizes RLM-style latent "
    "recursion from a single model to a heterogeneous N-agent "
    "system; and "
    "(P3) *Latent-space collaboration* -- it treats latent "
    "embeddings as the communication medium across recursion rounds "
    "rather than text. The conjunction of these three is novel; "
    "no prior work covers all three simultaneously.",
    title="Positioning: RecursiveMAS = MAS topology x recursive scaling x latent-space collaboration",
)

__all__ = [
    "claim_mas_topology_literature",
    "claim_textual_feedback_optimization_literature",
    "claim_per_agent_training_literature",
    "claim_recursive_lm_literature",
    "claim_first_system_level_recursion",
    "claim_latent_space_communication_literature",
    "claim_positioning_summary",
]
