"""Section 6-7: Limitations and conclusion.

Sections 6 (Limitations) and 7 (Conclusion) of [@Kaddour2026].

Limitations the author surfaces:
* Candidate quality and group-based costs -- TPO can only redistribute
  over the candidates given; in sequence settings without a critic, it
  still requires K rollouts per context just like GRPO.
* Score standardization helpful but not free -- it can amplify small
  numerical differences when within-group variance is tiny (the same
  difficulty-bias mechanism Dr.GRPO addresses).
* Scale of evaluation -- 1.5-1.7B parameter LLMs on three tasks; 7B+
  models and harder benchmarks (MATH, AIME) are future work.

The Conclusion restates the headline: TPO replaces scalar-weighted PG
with a single design choice (build a target on the scored candidate
set; fit by cross-entropy), matches PG/PPO/DG/GRPO on dense-reward
tasks, and substantially outperforms them under sparse reward.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Sec. 6: Limitations
# ---------------------------------------------------------------------------

claim_lim_candidate_quality = claim(
    "**Limitation 1 -- TPO can only redistribute over the given "
    "candidates.** If the sampled set is low-diversity or uniformly "
    "poor, the target $q$ is correspondingly uninformative. In "
    "discrete-action settings where all actions can be scored in a "
    "single forward pass, the $K$-candidate group adds no extra "
    "environment interactions; in sequence settings *without* a "
    "critic, TPO requires $K$ rollouts per context just as GRPO "
    "does. TPO 'may use those rollouts better, but does not remove "
    "the cost' [@Kaddour2026, Sec. 6]. More aggressive rollout "
    "reuse would move TPO into a genuinely off-policy regime where "
    "Retrace- or V-trace-style corrections [@Munos2016Retrace; "
    "@Espeholt2018IMPALA] may become necessary.",
    title="Limitation: TPO is bounded by sampled candidate quality; needs $K$ rollouts per context",
)

claim_lim_low_variance_groups = claim(
    "**Limitation 2 -- standardization can amplify tiny within-group "
    "differences.** Score standardization gives TPO a stable scale "
    "across tasks and largely removes the need to tune temperature, "
    "but in low-variance groups (e.g. one candidate scores 0.001 and "
    "the rest score 0) it produces a very sharp target after "
    "$z$-scoring. This is the same difficulty-bias mechanism "
    "identified for GRPO [@Liu2025DrGRPO; @Murphy2025RL]. A more "
    "robust treatment of low-variance groups would help in practice "
    "[@Kaddour2026, Sec. 6].",
    title="Limitation: low-variance groups can amplify tiny score differences post-$z$-scoring",
)

claim_lim_scale_of_evaluation = claim(
    "**Limitation 3 -- LLM-scale results limited to 1.5-1.7B params "
    "on three tasks.** The Section 3.8 LLM RLVR experiments use "
    "1.5-1.7B parameter models on GSM8K, graph coloring, and "
    "Knights & Knaves. Testing on larger models (7B+) and harder "
    "benchmarks (MATH, AIME) remains future work; the main open "
    "question is whether TPO's relative gains persist at larger "
    "scale [@Kaddour2026, Sec. 6].",
    title="Limitation: LLM-scale evaluation is 1.5-1.7B params on 3 tasks; 7B+ untested",
)

# ---------------------------------------------------------------------------
# Sec. 7: Conclusion
# ---------------------------------------------------------------------------

claim_conclusion_restated = claim(
    "**Conclusion (restated).** TPO replaces scalar-weighted policy "
    "gradients with a single design choice: build a target "
    "distribution on the scored candidate set and fit the policy to "
    "it by cross-entropy. Across every setting tested -- tabular "
    "bandits (Sec. 3.1-3.2), neural bandits (Sec. 3.3), dense- and "
    "sparse-reward transformers (Sec. 3.4-3.7), and billion-"
    "parameter LLM RLVR (Sec. 3.8) -- TPO matches PG, PPO, DG, and "
    "GRPO on dense-reward tasks and substantially outperforms them "
    "under sparse reward. The conceptual takeaway is that "
    "*separating what redistribution is desired from how the "
    "optimizer realizes it can make the update more robust* "
    "[@Kaddour2026, Sec. 7].",
    title="Conclusion: TPO is a single design choice (target + cross-entropy) that decouples Q1 from Q2",
)

# ---------------------------------------------------------------------------
# Counterposed view: the prevailing PG perspective
# ---------------------------------------------------------------------------

claim_pg_view_entanglement_unavoidable = claim(
    "**Implicit prevailing view -- entanglement of Q1/Q2 is "
    "fundamental to policy gradients and must be tamed via clipping, "
    "trust regions, or KL penalties.** This is the implicit position "
    "of the dominant PG/PPO/GRPO literature: rather than decouple, "
    "the field has spent years adding stabilising machinery (importance "
    "ratios, clip ranges, KL anchors, advantage normalisation, "
    "entropy bonuses, sigmoid gates) on top of an entangled update. "
    "TPO's empirical demonstration -- that explicit decoupling "
    "*solves* sparse-reward tasks where these mechanisms only "
    "stabilize -- contradicts this prevailing view at the empirical "
    "level. The paper does not state this contradiction in so many "
    "words but the framing of Sec. 1 ('learning fragile, especially "
    "when reward is sparse') and the Figure 1(b) gap make it the "
    "implicit foil.",
    title="Foil: prevailing PG view treats entanglement as unavoidable; TPO's results contradict that",
)

__all__ = [
    "claim_lim_candidate_quality",
    "claim_lim_low_variance_groups",
    "claim_lim_scale_of_evaluation",
    "claim_conclusion_restated",
    "claim_pg_view_entanglement_unavoidable",
]
