"""Section 5: Theoretical Analysis -- convergence (Theorem 5.1), basin
quality (Theorem 5.2), basin separation (Theorem 5.3), linear scaling
(Theorem 5.4), parallel convergence (Theorem 5.5), and the comparison-
to-alternatives table.

Source: Rodriguez 2026 [@Rodriguez2026PressureField], Section 5 +
Appendix C (full proofs).
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Theorem 5.1: convergence
# ---------------------------------------------------------------------------

claim_per_tick_pressure_drop = claim(
    "**Per-tick pressure-drop lemma (intermediate step in Theorem "
    "5.1 proof).** Under $\\epsilon$-bounded coupling, when a patch "
    "reduces local pressure $P_i$ by $\\delta_i$, global pressure "
    "changes by $P_{t+1} - P_t = -\\delta_i + \\sum_{j \\ne i} "
    "(P_j(s_{t+1}) - P_j(s_t))$. By bounded coupling "
    "$|P_j(s_{t+1}) - P_j(s_t)| \\le \\epsilon$ for each $j \\ne i$, "
    "so with $n$ regions, $P_{t+1} - P_t \\le -\\delta_i + "
    "(n-1)\\epsilon$. If $\\delta_i \\ge \\delta_{\\min}$ and "
    "$\\delta_{\\min} > (n-1)\\epsilon$, then "
    "$P_{t+1} - P_t \\le -\\delta_{\\min} + (n-1)\\epsilon < 0$.",
    title="Lemma: per-tick pressure drop is at least delta_min - (n-1)*eps > 0",
)

claim_theorem_5_1_convergence = claim(
    "**Theorem 5.1 (Convergence).** Let the pressure system be "
    "aligned with $\\epsilon$-bounded coupling. Let "
    "$\\delta_{\\min} > 0$ be the minimum *local* pressure "
    "reduction $P_i(s) - P_i(s')$ from any applied patch, and "
    "assume $\\delta_{\\min} > (n-1)\\epsilon$ where $n$ is the "
    "number of regions. Then from any initial state $s_0$ with "
    "pressure $P_0 = P(s_0)$, the system reaches a stable basin "
    "within: $T \\le P_0 / (\\delta_{\\min} - (n-1)\\epsilon)$ "
    "ticks, provided the fitness boost $\\Delta_f$ from successful "
    "patches exceeds decay during inhibition: $\\Delta_f > 1 - "
    "e^{-\\lambda_f \\cdot \\tau_{inh}}$.",
    title="Theorem 5.1 (Convergence): T <= P_0 / (delta_min - (n-1)*eps) ticks under alignment + epsilon-bounded coupling",
    metadata={
        "figure": "artifacts/2601.08129.pdf, Theorem 5.1 (page 19) and Appendix C.1",
    },
)

claim_convergence_bound_implication = claim(
    "**Implication of Theorem 5.1's bound.** The convergence-time "
    "bound is loose but establishes that **convergence time scales "
    "with initial pressure $P_0$, not with state-space size or "
    "number of possible actions**. This is the crucial property: "
    "the tick budget required to reach a stable basin grows linearly "
    "with how 'bad' the initial artifact is, not exponentially with "
    "the artifact's representational complexity.",
    title="Implication: convergence time scales with initial pressure P_0, not with state-space or action-space size",
)

# ---------------------------------------------------------------------------
# Theorem 5.2: basin quality
# ---------------------------------------------------------------------------

claim_theorem_5_2_basin_quality = claim(
    "**Theorem 5.2 (Basin Quality).** In any stable basin $s^*$, "
    "the artifact pressure satisfies $P(s^*) < n \\cdot \\tau_{act}$, "
    "where $n$ is the number of regions and $\\tau_{act}$ is the "
    "activation threshold. **Proof:** by definition of stability, "
    "$P_i(s^*) < \\tau_{act}$ for all $i$. Summing over regions: "
    "$P(s^*) = \\sum_i P_i(s^*) < n \\cdot \\tau_{act}$. The bound "
    "is tight: adversarial initial conditions can place the system "
    "in a basin where each region has pressure just below "
    "threshold. In practice, however, actors typically reduce "
    "pressure well below $\\tau_{act}$, yielding much lower basin "
    "pressures.",
    title="Theorem 5.2 (Basin Quality): P(s*) < n * tau_act in any stable basin (tight in adversarial worst case)",
)

# ---------------------------------------------------------------------------
# Theorem 5.3: basin separation -- decay necessity
# ---------------------------------------------------------------------------

claim_theorem_5_3_basin_separation = claim(
    "**Theorem 5.3 (Basin Separation).** Under separable pressure "
    "(zero coupling), distinct stable basins are separated by "
    "pressure barriers of height at least $\\tau_{act}$. **Proof "
    "sketch:** moving from one basin $B_1$ to another $B_2$ "
    "requires some region to exceed $\\tau_{act}$ -- otherwise, by "
    "continuity under separable pressure, the state would still be "
    "in $B_1$. The minimum such exceedance defines the barrier "
    "height.",
    title="Theorem 5.3 (Basin Separation): distinct stable basins are separated by barriers of height >= tau_act",
    metadata={
        "figure": "artifacts/2601.08129.pdf, Theorem 5.3 (page 20) and Appendix C.2",
    },
)

claim_decay_necessity_argument = claim(
    "**Decay-necessity argument from Theorem 5.3.** Without decay, "
    "once the system enters a basin, fitness remains high "
    "indefinitely, preventing any region's pressure from exceeding "
    "$\\tau_{act}$ even if a *better* (lower-pressure) basin "
    "exists. Decay erodes fitness over time, eventually allowing "
    "pressure to exceed $\\tau_{act}$ and enabling transition to a "
    "potentially lower-pressure basin. **This is the formal "
    "rationale for why temporal decay is part of the architecture: "
    "Theorem 5.3 implies decay is necessary to escape suboptimal "
    "stable basins.**",
    title="Theory: decay is necessary to escape suboptimal stable basins (corollary of Theorem 5.3)",
)

# ---------------------------------------------------------------------------
# Theorem 5.4: linear scaling
# ---------------------------------------------------------------------------

claim_theorem_5_4_linear_scaling = claim(
    "**Theorem 5.4 (Linear Scaling).** Per-tick complexity is "
    "$O(m \\cdot (d + k + a \\cdot \\log(ma)))$, where $m$ is the "
    "number of regions, $d$ is signal dimension, $k$ is the number "
    "of pressure axes, and $a$ is the number of actors. **Crucially, "
    "this is independent of agent count $n$.** Coordination "
    "overhead is $O(1)$ (no inter-agent communication; the fork "
    "pool is $O(K)$ for fixed $K$). **Adding agents increases "
    "throughput (more patches proposed per tick) without increasing "
    "coordination cost.**",
    title="Theorem 5.4 (Linear Scaling): per-tick complexity = O(m*(d+k+a*log(ma))), independent of agent count n",
    metadata={
        "figure": "artifacts/2601.08129.pdf, Theorem 5.4 (page 21) and Appendix C.3",
    },
)

# ---------------------------------------------------------------------------
# Theorem 5.5: parallel convergence
# ---------------------------------------------------------------------------

claim_theorem_5_5_parallel_convergence = claim(
    "**Theorem 5.5 (Parallel Convergence).** Under the same "
    "alignment conditions as Theorem 5.1, with $K$ patches "
    "validated in parallel per tick where patches affect *disjoint* "
    "regions, the system reaches a stable basin within "
    "$T \\le P_0 / (K \\cdot (\\delta_{\\min} - (n-1)\\epsilon))$ "
    "ticks. **This improves convergence time by factor $K$ while "
    "maintaining guarantees.** When patches conflict (target the "
    "same region), only one is selected per region and effective "
    "speedup is reduced.",
    title="Theorem 5.5 (Parallel Convergence): T <= P_0 / (K * (delta_min - (n-1)*eps)) with K parallel non-conflicting patches",
    metadata={
        "figure": "artifacts/2601.08129.pdf, Theorem 5.5 (page 21) and Appendix C.4",
    },
)

# ---------------------------------------------------------------------------
# 5.4 Comparison-to-alternatives table
# ---------------------------------------------------------------------------

claim_table_1_coordination_comparison = claim(
    "**Table 1: Coordination-overhead comparison across paradigms.**\n\n"
    "| Paradigm | Coordination | Parallelism | Fault tolerance |\n"
    "|---|---|---|---|\n"
    "| Centralized | $O(m \\cdot a)$ | None | Single point of failure |\n"
    "| Hierarchical | $O(n \\log n)$ | Limited by tree | Manager failure cascades |\n"
    "| Message-passing | $O(n^2)$ | Consensus-bound | Partition-sensitive |\n"
    "| **Pressure-field** | **$O(1)$** | **Full ($\\min(n, m, K)$)** | **Graceful degradation** |\n\n"
    "$K$ denotes the fork-pool size for parallel validation. "
    "Pressure-field's $O(1)$ coordination overhead reflects "
    "agents sharing state only through the artifact itself (a form "
    "of stigmergy); agents can fail, join, or leave without "
    "protocol overhead.",
    title="Table 1: coordination-overhead comparison across paradigms (centralized / hierarchical / message-passing / pressure-field)",
    metadata={
        "figure": "artifacts/2601.08129.pdf, Table 1 (page 22)",
        "caption": "Table 1: Coordination overhead comparison. K denotes the fork pool size for parallel validation.",
    },
)

# ---------------------------------------------------------------------------
# Centralized / hierarchical / message-passing complexity claims
# (used as comparison anchors for Table 1)
# ---------------------------------------------------------------------------

claim_centralized_complexity = claim(
    "**Centralized planning complexity.** A global planner "
    "evaluates all $m \\cdot a$ possible actions and selects an "
    "optimal subset. Per-step complexity: $O(m \\cdot a)$ "
    "evaluations, but the planner requires global state access. The "
    "sequential bottleneck prevents parallelization.",
    title="Centralized planning: O(m*a) evaluations + sequential bottleneck (single point of failure)",
)

claim_hierarchical_complexity = claim(
    "**Hierarchical delegation complexity.** Manager agents "
    "decompose tasks and delegate to workers. Communication "
    "complexity: $O(n \\log n)$ for tree-structured delegation with "
    "$n$ agents. Latency scales with tree depth. Manager failure "
    "blocks all descendants.",
    title="Hierarchical delegation: O(n log n) communication + tree-depth latency + manager-failure cascades",
)

claim_message_passing_complexity = claim(
    "**Message-passing coordination complexity.** Agents negotiate "
    "actions through pairwise communication. Convergence requires "
    "$O(n^2)$ messages in the worst case for $n$ agents. Consensus "
    "protocols add latency. The system is partition-sensitive: "
    "network partitions break consensus and stall coordination.",
    title="Message-passing: O(n^2) messages worst case + consensus latency + partition-sensitive",
)

__all__ = [
    "claim_per_tick_pressure_drop",
    "claim_theorem_5_1_convergence",
    "claim_convergence_bound_implication",
    "claim_theorem_5_2_basin_quality",
    "claim_theorem_5_3_basin_separation",
    "claim_decay_necessity_argument",
    "claim_theorem_5_4_linear_scaling",
    "claim_theorem_5_5_parallel_convergence",
    "claim_table_1_coordination_comparison",
    "claim_centralized_complexity",
    "claim_hierarchical_complexity",
    "claim_message_passing_complexity",
]
