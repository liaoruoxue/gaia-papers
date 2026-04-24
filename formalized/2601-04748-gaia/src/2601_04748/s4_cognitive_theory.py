"""
Section 4: Cognitive Foundations and Scaling Hypotheses
========================================================

Establishes the cognitive science theoretical framework grounding the skill selection scaling
hypothesis. Presents four foundational theories (F1-F4) and derives four testable predictions (H1-H4).
"""

from gaia.lang import claim, setting, question, support

from .motivation import q_skill_scaling, sas_definition

# --- Cognitive science foundations ---

f1_hicks_law = setting(
    "**Hick's Law (F1):** Human choice reaction time scales logarithmically with the number of "
    "alternatives: $RT = a + b \\cdot \\log_2(n+1)$, where $n$ is the number of equally probable options. "
    "Critically, Longstreth (1988) demonstrated that this relationship breaks down beyond approximately "
    "8 choices ($\\sim$3 bits), becoming curvilinear as the binary subdivision strategy fails [@Hick1952; @Longstreth1988].",
    title="F1: Hick's Law — decision time vs. alternatives",
    metadata={"source": "artifacts/2601.04748.pdf, Section 4.1"},
)

f2_cognitive_load = setting(
    "**Cognitive Load Theory (F2):** Miller's 'magical number seven' identified fundamental limits on "
    "immediate memory span (approximately 7 ± 2 items) [@Miller1956]. Sweller's Cognitive Load Theory "
    "extends this to complex tasks, distinguishing intrinsic load (inherent task complexity) from "
    "extraneous load (unnecessary processing demands). When total cognitive load exceeds working memory "
    "capacity, performance degrades sharply — a threshold effect rather than gradual decline [@Sweller1988].",
    title="F2: Cognitive Load Theory — working memory capacity limits",
    metadata={"source": "artifacts/2601.04748.pdf, Section 4.1"},
)

f3_similarity_interference = setting(
    "**Similarity-Based Interference (F3):** Shepard's Universal Law of Generalization establishes that "
    "confusion probability decays exponentially with psychological distance: $g(d) = e^{-d/\\lambda}$ [@Shepard1987]. "
    "Anderson's ACT-R model provides a mechanistic account through the fan effect: as more facts share a "
    "retrieval cue, associative strength to each fact decreases, leading to slower retrieval and reduced "
    "accuracy [@Anderson1974]. The Generalized Context Model formalizes how classification errors increase "
    "with both option count and inter-option similarity [@Nosofsky1986].",
    title="F3: Similarity-based interference — fan effect and confusability",
    metadata={"source": "artifacts/2601.04748.pdf, Section 4.1"},
)

f4_hierarchical_chunking = setting(
    "**Hierarchical Processing and Chunking (F4):** Chase and Simon's chunking theory demonstrates that "
    "experts manage complexity through hierarchical organization — chess masters perceive board positions "
    "as approximately 7 chunks rather than 32 individual pieces [@Chase1973]. Menu design research finds "
    "optimal breadth of 4–8 items per level, matching working memory capacity. Tversky's "
    "Elimination-by-Aspects model formalizes how stepwise narrowing of options makes large choice sets "
    "more manageable [@Tversky1972].",
    title="F4: Hierarchical processing — chunking and menu design",
    metadata={"source": "artifacts/2601.04748.pdf, Section 4.1"},
)

# --- Formal scaling model ---

scaling_model = setting(
    "The proposed functional form for skill selection accuracy as a function of library size $|S|$ "
    "and semantic interference $I(S)$ is: "
    "$$ACC(\\sigma, S) \\approx \\frac{\\alpha}{1 + (|S|/\\kappa)^\\gamma} - \\epsilon \\cdot I(S)$$ "
    "where: $\\alpha \\leq 1$ is asymptotic accuracy at small $|S|$; "
    "$\\kappa$ is the capacity threshold (library size at which accuracy drops to $\\alpha/2$); "
    "$\\gamma > 1$ controls sharpness of the phase transition (super-linear); "
    "$\\epsilon > 0$ is sensitivity to semantic interference $I(S)$.",
    title="Scaling model: accuracy vs. library size and interference",
    metadata={"source": "artifacts/2601.04748.pdf, Section 4.3, Eq. 10"},
)

# --- Hypotheses (claims, to be tested) ---

h1_phase_transition = claim(
    "**H1 (Non-linear Phase Transition):** LLM skill selection accuracy exhibits a phase transition: "
    "accuracy remains high when $|S| < \\kappa$ but suffers sharp, non-linear degradation once library "
    "size exceeds the capacity threshold $\\kappa$. The transition is phase-like rather than gradual — "
    "accuracy is relatively stable until $|S| \\approx \\kappa$, then drops precipitously. "
    "This mirrors the breakdown of Hick's Law beyond ~8 choices (F1) and threshold effects in "
    "Cognitive Load Theory when working memory is exceeded (F2).",
    title="H1: Non-linear phase transition in skill selection",
    metadata={"source": "artifacts/2601.04748.pdf, Section 4.4"},
)

h2_confusability = claim(
    "**H2 (Confusability-Driven Errors):** Selection degradation is driven primarily by semantic "
    "confusability among skills, not mere library size. Adding semantically similar 'competitor' skills "
    "degrades accuracy more than adding an equivalent number of distinct skills. This follows from "
    "the interference term $\\epsilon \\cdot I(S)$ in the scaling model and similarity-based "
    "interference in cognitive science (F3).",
    title="H2: Confusability-driven degradation",
    metadata={"source": "artifacts/2601.04748.pdf, Section 4.4"},
)

h3_instructional_saturation = claim(
    "**H3 (Instructional Saturation):** Skills with more complex execution policies $\\pi$ "
    "(verbose, detailed instructions) consume additional processing bandwidth, reducing effective "
    "capacity $\\kappa$ by increasing extraneous cognitive load. Including full execution policies "
    "in the selection prompt should degrade accuracy more than using only skill descriptors (F2).",
    title="H3: Policy complexity reduces effective capacity",
    metadata={"source": "artifacts/2601.04748.pdf, Section 4.4"},
)

h4_hierarchy_mitigation = claim(
    "**H4 (Mitigation via Hierarchy):** When flat selection fails ($|S| > \\kappa$), hierarchical "
    "organization can restore reliable scaling by ensuring each decision point involves fewer than "
    "$\\kappa$ options. This transforms an intractable single decision into a sequence of tractable "
    "sub-decisions, mirroring chunking (F4) and menu design principles.",
    title="H4: Hierarchical routing mitigates scaling limits",
    metadata={"source": "artifacts/2601.04748.pdf, Section 4.4"},
)

# --- Support strategies linking cognitive theory to hypotheses ---

# Note: H1-H4 are theoretical hypotheses grounded in cognitive science (F1-F4).
# Their initial plausibility comes from cognitive theory (background settings),
# and their confirmation comes from experimental results in s5_experiments.py.
# We set priors on H1-H4 in priors.py to reflect the cognitive-theory prior probability.
# No strategies here since the premises would all be settings (background only).

__all__ = [
    "f1_hicks_law",
    "f2_cognitive_load",
    "f3_similarity_interference",
    "f4_hierarchical_chunking",
    "scaling_model",
    "h1_phase_transition",
    "h2_confusability",
    "h3_instructional_saturation",
    "h4_hierarchy_mitigation",
]
