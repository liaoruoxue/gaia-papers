"""Section 3: Building a Recursive Multi-Agent System.

Defines the inner and outer RecursiveLink modules and the chained-loop
architecture, then states Proposition 3.1 (runtime complexity advantage).

Source: Yang et al. 2026 [@Yang2026RecursiveMAS], Section 3 + Appendix A.1.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Section 3.1: RecursiveLink module definition
# ---------------------------------------------------------------------------

setup_recursive_link_intent = setting(
    "**RecursiveLink design intent.** A language model's last-layer "
    "hidden states carry a natural representation of the model's "
    "generated semantics. The RecursiveLink module $\\mathcal{R}$ is "
    "designed to *preserve and transmit* this last-layer information "
    "from one embedding space to another. Two transitions arise inside "
    "RecursiveMAS: (i) **Dense-to-Shallow transition** -- the previous "
    "step's last-layer embeddings are fed back as the next-step input "
    "embeddings during latent thoughts generation within a single agent; "
    "and (ii) **Cross-Model transition** -- one model's newly generated "
    "latent representation is passed as conditioning input to another "
    "model. The inner and outer links handle the two cases respectively.",
    title="Setup: RecursiveLink R bridges (i) dense-to-shallow and (ii) cross-model embedding transitions",
    metadata={
        "figure": "artifacts/2604.25917.pdf, Fig. 3",
        "caption": "Fig. 3: Inner and outer RecursiveLink design (2-layer GELU MLP + residual; outer adds W_3 to bridge hidden dimensions).",
    },
)

setup_inner_link = setting(
    "**Inner RecursiveLink $\\mathcal{R}_{in}$ (Eq. 3).** Each agent "
    "$A_i$ is paired with an inner link $\\mathcal{R}_{in}$. Given a "
    "new last-layer embedding vector $h$, the inner link transforms "
    "it as:\n\n"
    "$$\\mathcal{R}_{in}(h) = h + W_2 \\, \\sigma(W_1 h),$$\n\n"
    "where $W_1, W_2$ are two standard linear layers, $\\sigma(\\cdot)$ "
    "is the GELU activation, and the residual term $h$ preserves the "
    "original latent semantics. The transformed embedding is then used "
    "as input to the next forward pass of agent $A_i$ during latent "
    "thoughts generation.",
    title="Setup: inner link R_in(h) = h + W_2 sigma(W_1 h) (Eq. 3)",
)

setup_outer_link = setting(
    "**Outer RecursiveLink $\\mathcal{R}_{out}$ (Eq. 4).** The outer "
    "link connects heterogeneous agents that may have different hidden "
    "dimensions. An additional linear layer $W_3$ maps the source "
    "embedding from agent $A_i$'s space into agent $A_j$'s embedding "
    "space:\n\n"
    "$$\\mathcal{R}_{out}(h) = W_3 h + W_2 \\, \\sigma(W_1 h).$$\n\n"
    "The residual branch is now $W_3 h$ (a learned projection rather "
    "than identity) so that the link can change embedding dimensions; "
    "the GELU branch $W_2 \\sigma(W_1 h)$ handles the distributional "
    "shift between source and target spaces.",
    title="Setup: outer link R_out(h) = W_3 h + W_2 sigma(W_1 h) (Eq. 4)",
)

claim_residual_design_motivation = claim(
    "**Why a residual connection?** The residual branch ($h$ inside "
    "$\\mathcal{R}_{in}$ and $W_3 h$ inside $\\mathcal{R}_{out}$) "
    "largely preserves the original semantics of the input, so the "
    "RecursiveLink network only needs to learn the *distributional "
    "shift* between embedding spaces rather than the full projection "
    "from scratch. This leads to more stable and efficient training "
    "and is empirically validated against three alternative designs "
    "(1-layer, 1-layer + residual, 2-layer no-residual) in Section 6.",
    title="Design rationale: residual = preserve semantics, only learn distributional shift",
)

# ---------------------------------------------------------------------------
# Section 3.2: chaining all agents as a loop
# ---------------------------------------------------------------------------

setup_latent_thoughts_generation = setting(
    "**Latent thoughts generation inside an agent.** Given input "
    "context embeddings $E_{A_1} = [e_1, e_2, \\dots, e_t]$ (the "
    "question plus agent-specific instructions), agent $A_1$ first "
    "passes $E_{A_1}$ through its Transformer to compute the last-"
    "layer hidden representation $h_t$ at step $t$. The state $h_t$ "
    "is then fed into the inner link $\\mathcal{R}_{in}$ to map it "
    "back into the input embedding space, yielding "
    "$e_{t+1} = \\mathcal{R}_{in}(h_t)$. Agent $A_1$ repeats this "
    "auto-regressively for $m$ forward steps, producing a continuous "
    "sequence of latent thoughts "
    "$H_{A_1} = [h_t, h_{t+1}, \\dots, h_{t+m}]$.",
    title="Setup: each agent emits m latent thoughts via inner link, no decoding",
)

setup_cross_agent_interaction = setting(
    "**Cross-agent interaction via the outer link.** Once agent $A_1$ "
    "completes latent reasoning, its latent thoughts $H_{A_1}$ are "
    "passed through the outer link $\\mathcal{R}_{out}$ to be aligned "
    "with agent $A_2$'s embedding space. Agent $A_2$ then performs "
    "latent thoughts generation conditioned on both its own input "
    "context and the transferred information, "
    "$E_{A_2} \\oplus \\mathcal{R}_{out}(H_{A_1})$, where $\\oplus$ "
    "denotes concatenation along the sequence dimension. This process "
    "continues sequentially through all agents.",
    title="Setup: cross-agent transfer -- A_2 conditions on E_{A_2} concat R_out(H_{A_1})",
)

setup_loop_closure = setting(
    "**Loop closure across recursion rounds.** After the final agent "
    "$A_N$ completes latent thoughts generation in a given recursion "
    "round, its latent outputs (representing the system's latent "
    "answer for that round) are fed back to the first agent $A_1$ "
    "through the inner-outer RecursiveLink, closing the recursive "
    "loop. Each new round therefore conditions on information "
    "produced in previous rounds, so each agent iteratively reflects "
    "on earlier system outputs and refines its current generation. "
    "Throughout intermediate recursion rounds, all agents collaborate "
    "*entirely in latent space*. Only after the final recursion round "
    "does the last agent $A_N$ decode its hidden state to a textual "
    "answer.",
    title="Setup: loop closure -- A_N's latent output feeds A_1 in next round; only final round decodes",
)

# ---------------------------------------------------------------------------
# Proposition 3.1: runtime complexity (with proof from Appendix A.1)
# ---------------------------------------------------------------------------

claim_per_agent_shared_cost = claim(
    "**Per-agent shared Transformer cost.** For a single agent with "
    "context length at most $t$ and generation length at most $m$, the "
    "Transformer processes a sequence of length at most $t + m$, "
    "incurring $\\Theta((t+m) d_h^2)$ time for the feed-forward layers "
    "and $\\Theta((t+m)^2 d_h)$ time for self-attention. This standard "
    "Transformer cost is shared by both RecursiveMAS and text-based "
    "Recursive MAS.",
    title="Lemma: per-agent shared Transformer cost = Theta((t+m) d_h^2 + (t+m)^2 d_h)",
)

claim_recursivemas_extra_cost = claim(
    "**RecursiveMAS extra cost = $\\Theta(m d_h^2)$.** In RecursiveMAS, "
    "each of the $m$ generated latent embeddings is transformed by the "
    "RecursiveLink (a 2-layer GELU MLP applied to a $d_h$-vector), "
    "incurring an additional cost of $\\Theta(m d_h^2)$ per agent.",
    title="Lemma: RecursiveMAS adds Theta(m d_h^2) per agent for latent transformation",
)

claim_textmas_extra_cost = claim(
    "**Text-based MAS extra cost = $\\Theta(m |V| d_h)$.** In text-"
    "based Recursive MAS, each generated embedding must be decoded "
    "into an explicit token by projecting it to vocabulary space and "
    "computing logits over $|V|$ tokens, incurring an additional cost "
    "of $\\Theta(m |V| d_h)$ per agent.",
    title="Lemma: text-based MAS adds Theta(m |V| d_h) per agent for vocabulary projection",
)

claim_proposition_3_1 = claim(
    "**Proposition 3.1 (RecursiveMAS Runtime Complexity).** Without "
    "RecursiveLink, a text-based Recursive MAS with the same "
    "collaboration structure requires runtime complexity\n"
    "$$\\Theta\\bigl(N(m|V| d_h + (t+m) d_h^2 + (t+m)^2 d_h)\\bigr).$$\n"
    "In contrast, with RecursiveLink-enabled collaboration, "
    "RecursiveMAS achieves\n"
    "$$\\Theta\\bigl(N(m d_h^2 + (t+m) d_h^2 + (t+m)^2 d_h)\\bigr).$$\n"
    "The improvement comes from replacing the $m|V| d_h$ vocabulary-"
    "projection term with the much cheaper $m d_h^2$ latent-"
    "transformation term across all $N$ agents.",
    title="Theorem: Proposition 3.1 -- end-to-end runtime complexity of RecursiveMAS vs text-based MAS",
    metadata={
        "figure": "artifacts/2604.25917.pdf, Section 3 + Appendix A.1",
    },
)

claim_remark_3_2 = claim(
    "**Remark 3.2.** Since $d_h \\ll |V|$ in practice (typical "
    "$d_h \\sim 10^3$, $|V| \\sim 10^5$), RecursiveMAS replaces the "
    "expensive per-step vocabulary-space decoding cost $m|V| d_h$ "
    "with a much more efficient latent-space transformation $m d_h^2$, "
    "yielding a constant-factor saving per generated latent token "
    "that compounds over recursion rounds and across $N$ agents.",
    title="Remark 3.2: m|V|d_h -> m d_h^2 yields a substantial per-token saving since d_h << |V|",
)

__all__ = [
    "setup_recursive_link_intent",
    "setup_inner_link",
    "setup_outer_link",
    "claim_residual_design_motivation",
    "setup_latent_thoughts_generation",
    "setup_cross_agent_interaction",
    "setup_loop_closure",
    "claim_per_agent_shared_cost",
    "claim_recursivemas_extra_cost",
    "claim_textmas_extra_cost",
    "claim_proposition_3_1",
    "claim_remark_3_2",
]
