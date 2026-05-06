"""Section 7 + Appendix K + H.3: Qualitative observations and connections.

Combines:

* Section 7 (Related work): credit assignment in RLVR, token-level
  advantage reshaping, latent-representation-based methods.

* Appendix H.3: Connection to Process Reward Models -- the SHEAR
  weight omega_t qualitatively tracks 1 - PRM(t) for incorrect rollouts
  (small when reasoning is on track, large after errors).

* Appendix K: case study on AIME-style 4-tuples problem comparing
  Wasserstein matrices for correct vs. incorrect cases.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Section 7 related work characterizations
# ---------------------------------------------------------------------------

claim_related_credit_assignment = claim(
    "**Related work: credit assignment in RLVR.** GRPO [@Shao2024GRPO] "
    "assigns uniform advantages across all tokens, which is coarse-"
    "grained [@Li2026OutcomeGrounded]. Process reward models (PRMs) "
    "[@Lightman2023PRM; @Cui2025PRIME; @Cheng2025PURE] provide finer-"
    "grained step-level supervision and have shown clear benefits "
    "over outcome-level feedback. However, PRMs require either "
    "human-annotated intermediate labels or an auxiliary reward "
    "model -- introducing both annotation cost and a *transfer gap* "
    "when the policy model's capacity exceeds the PRM's. Cui et al. "
    "[@Cui2025PRIME] proposed learning process rewards through "
    "implicit signals; Cheng et al. [@Cheng2025PURE] introduced "
    "min-form credit assignment to mitigate reward hacking. SHEAR "
    "*departs from the PRM paradigm entirely* by extracting process-"
    "level credit from the policy model's own hidden states, "
    "requiring no additional annotation or reward model.",
    title="Related: PRMs need step-level supervision; SHEAR doesn't (different paradigm)",
)

claim_related_token_reshaping = claim(
    "**Related work: token-level advantage reshaping.** Several "
    "recent methods differentiate token-level advantages within "
    "GRPO using *internal* signals. [@Cheng2025EntropyAdv; "
    "@Zhang2025EDGEGRPO] exploit per-token *entropy* to reshape "
    "advantages, improving credit granularity and exploration. A "
    "shared limitation: a *scalar* entropy metric cannot reliably "
    "distinguish between productive reasoning pivots and genuine "
    "erroneous steps. To overcome this representational bottleneck, "
    "recent methods leverage *continuous latent representations* to "
    "model and optimize reasoning [@Kang2026Ladir; @Du2026LTO; "
    "@Yue2025HybridLatent]. These works share a core insight: "
    "high-dimensional latent spaces inherently capture *richer "
    "semantic signals* that separate correct from erroneous reasoning. "
    "SHEAR builds on this insight but directly computes the span-"
    "level Wasserstein distance between the model's *native* hidden "
    "states -- rather than designing complex latent generation "
    "architectures or training auxiliary latent reward models -- "
    "extracting an expressive self-supervised credit signal while "
    "eliminating reliance on auxiliary models.",
    title="Related: entropy-reshaping (scalar) vs. latent-reasoning (auxiliary models); SHEAR uses native hidden states",
)

# ---------------------------------------------------------------------------
# Appendix H.3: Connection to PRMs (interpretive)
# ---------------------------------------------------------------------------

claim_appendix_h3_prm_connection = claim(
    "**Appendix H.3 -- SHEAR weight tracks $1 - \\text{PRM}(t)$ for "
    "incorrect rollouts (interpretive connection).** Let "
    "$\\text{PRM}(t) = P[\\text{correct} \\mid \\text{reasoning up to "
    "step } t]$ in the divergence model: $\\text{PRM}(t)$ is high "
    "for $t \\leq \\tau$ and decreases for $t > \\tau$. The token-"
    "level weight $\\omega^{(i)}_t$ (Algorithm 1, line 13) "
    "qualitatively tracks $1 - \\text{PRM}(t)$ for incorrect "
    "rollouts: small when reasoning is on track, large after errors. "
    "This connection is *interpretive*; the key practical advantage "
    "is that $\\omega^{(i)}_t$ requires *no step-level supervision*. "
    "SHEAR can therefore be read as recovering the PRM signal from "
    "hidden-state distributional structure alone.",
    title="Appendix H.3: $\\omega^{(i)}_t$ qualitatively tracks $1 - \\text{PRM}(t)$ for incorrect rollouts",
)

# ---------------------------------------------------------------------------
# Appendix K: case study
# ---------------------------------------------------------------------------

claim_appendix_k_case_study = claim(
    "**Appendix K -- case study on a 4-tuples competition problem.** "
    "On the problem 'How many ordered 4-tuples $(a, b, c, d)$ with "
    "$0 < a < b < c < d < 500$ satisfy (1) $a + d = b + c$ and (2) "
    "$bc - ad = 93$?' (correct answer: 870), the paper compares three "
    "rollouts: Case 1 (correct, 870), Case 2 (incorrect, 2450), "
    "Case 3 (correct, 870). The Wasserstein-distance heatmap (Figure "
    "11) shows clear visual contrast: Case 1 vs. Case 2 (correct vs. "
    "incorrect) shows pronounced high-discrepancy regions in the "
    "post-divergence span indices, whereas Case 1 vs. Case 3 (both "
    "correct) shows a more uniform, lower-magnitude pattern. The "
    "qualitative pattern in this single case study is consistent with "
    "the population-level finding from Section 5.1 (AUC 0.99 at high "
    "$W$): high-$W$ regions are reliably post-divergence.",
    title="Appendix K: case study (4-tuples problem) shows visible high-W regions in correct-vs-incorrect comparison",
    metadata={
        "figure": "artifacts/2604.23318.pdf, Figure 11",
    },
)

# ---------------------------------------------------------------------------
# Section 8: conclusion
# ---------------------------------------------------------------------------

claim_section8_conclusion = claim(
    "**Section 8 -- conclusion.** SHEAR is a self-supervised credit "
    "assignment method for RLVR that exploits the model's own hidden-"
    "state representations to provide fine-grained, token-level "
    "training signals. The paper (i) identifies the empirical "
    "phenomenon (span-level Wasserstein distance tracks local "
    "reasoning quality), (ii) formalizes it via a separation theorem "
    "(post-divergence spans have *provably larger* Wasserstein "
    "distances than pre-divergence spans, conditional on $D(S) > "
    "2\\eta$), and (iii) translates the insight into a practical "
    "algorithm requiring only minimal modifications to existing "
    "training pipelines. Experiments on five mathematical reasoning "
    "and five code generation benchmarks demonstrate consistent "
    "improvements over standard GRPO and competitive or superior "
    "performance vs. PRM-based methods that rely on a separately "
    "trained 7B reward model -- while incurring less than 16% "
    "computational overhead.",
    title="Section 8: SHEAR = self-supervised PRM-substitute via hidden-state Wasserstein distance",
)

# ---------------------------------------------------------------------------
# Limitations and scope (gathered from various sections)
# ---------------------------------------------------------------------------

setup_scope_limitations = setting(
    "**Scope and acknowledged limitations.** (i) The diagnostic in "
    "Section 2 and the Section 5.1 verification both require *mixed-"
    "outcome* groups; on uniformly-correct or uniformly-incorrect "
    "groups SHEAR falls back to GRPO (Eq. 4). (ii) The separation "
    "theorem (Theorems 1, 2) is *conditional* on the population-level "
    "gap $D(S) > 2\\eta(n, d)$; spans with small $D(S)$ are correctly "
    "down-weighted but the method does not claim *all* post-"
    "divergence spans are separable. (iii) The single-divergence "
    "model (A1) is a stylized approximation; real chains may have "
    "multiple divergences, addressed conceptually in Appendix G "
    "(Proposition G.1) but not formally verified. (iv) The Sinkhorn "
    "approximation $W_\\epsilon$ is used in practice; ranking "
    "robustness requires the true separation gap to exceed "
    "$\\epsilon \\log n \\approx 20.8$ -- empirically satisfied "
    "(Section 5.1) but adds an asterisk to the formal guarantee. "
    "(v) The empirical evaluation is limited to 7B-14B-scale models "
    "trained on math/code; transfer to larger reasoning models or "
    "different task families is open.",
    title="Scope: mixed-outcome groups required; conditional theorem; single-divergence stylization; 7-14B model scale",
)

claim_pure_bottom_line = claim(
    "**Bottom-line claim of the paper.** Hidden-state distributional "
    "divergence between correct and incorrect rollouts in a GRPO "
    "group is a *practically operational, theoretically justified* "
    "self-supervised signal for fine-grained credit assignment in "
    "RLVR. The signal can be extracted with $W_1$ (Sinkhorn) on "
    "fixed-size spans, normalized by global mean hidden-state norm, "
    "and applied as a token-advantage *multiplier* in GRPO. The "
    "result improves over vanilla GRPO and competes with / beats "
    "supervised PRM baselines without requiring step-level labels "
    "or a separately trained reward model.",
    title="Bottom line: $W$-on-hidden-states is a viable PRM substitute, label-free, theory-justified",
)

__all__ = [
    "claim_related_credit_assignment",
    "claim_related_token_reshaping",
    "claim_appendix_h3_prm_connection",
    "claim_appendix_k_case_study",
    "claim_section8_conclusion",
    "setup_scope_limitations",
    "claim_pure_bottom_line",
]
