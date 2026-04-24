"""Section 4: Multi-Agent Co-Evolution — Coordination, Ablations, and Trajectory Analysis"""

from gaia.lang import (
    claim, setting, support, induction, contradiction, abduction, compare,
)

from .motivation import (
    evaluation_budget_setting,
    claim_multi_agent_gains,
    claim_knowledge_causal,
    claim_agents_adaptable,
    claim_coral_outperforms_fixed,
)
from .s2_framework import (
    claim_persistent_memory_design,
    claim_async_execution,
    claim_heartbeat_mechanism,
)
from .s3_single_agent import (
    claim_sota_8_tasks,
    claim_improvement_rate,
    benchmark_tasks_setting,
)

# =============================================================================
# Multi-agent experimental setup
# =============================================================================

multi_agent_setup_setting = setting(
    "Multi-agent co-evolution experiments use 4 agents running simultaneously on the "
    "hardest benchmark tasks (Kernel Engineering and Polyominoes packing stress tests, "
    "plus Transaction Scheduling). Each agent has its own isolated workspace but shares "
    "the persistent memory store. The comparison baseline is 'independent best-of-4': "
    "4 independent single-agent runs where agents do not share memory, taking the best "
    "result across all 4. This controls for additional compute.",
    title="Multi-agent experimental setup",
)

kernel_engineering_setting = setting(
    "Kernel Engineering stress-test: optimize the cycle count of a computational kernel "
    "(lower is better). Starting score used for normalization. The task involves "
    "low-level code optimization requiring specialized knowledge of CPU architecture, "
    "memory access patterns, SIMD instructions, and compiler optimization flags. "
    "Scores reported in CPU cycles (lower = better).",
    title="Kernel Engineering task description",
)

polyominoes_setting = setting(
    "Polyominoes packing stress-test: pack the maximum number of polyominoes into a "
    "fixed grid (higher coverage percentage is better). The task requires combinatorial "
    "search over placement strategies and shape selection, with a known optimal upper "
    "bound. Scores reported as coverage percentage (higher = better).",
    title="Polyominoes packing task description",
)

# =============================================================================
# Core multi-agent performance claims (from Table 2)
# =============================================================================

claim_kernel_4agent = claim(
    "Four co-evolving CORAL agents achieve a Kernel Engineering score of 1,103 cycles, "
    "compared to 1,350 cycles for the single-agent baseline and 1,363 cycles as the "
    "starting score—a 18.3% improvement over single-agent CORAL and 19.1% over the "
    "initial score. The 4-agent result establishes a new best-known score for this task.",
    title="4-agent Kernel Engineering: 1103 cycles",
    metadata={"source": "artifacts/2604-01658.pdf, Table 2, Section 4.2"},
)

claim_polyominoes_4agent = claim(
    "Four co-evolving CORAL agents achieve 84.2% Polyominoes coverage, compared to "
    "80.2% for the single-agent baseline—a 4.99 percentage point improvement. "
    "The 4-agent result exceeds all single-agent baselines including the best-of-4 "
    "independent runs.",
    title="4-agent Polyominoes: 84.2% coverage",
    metadata={"source": "artifacts/2604-01658.pdf, Table 2, Section 4.2"},
)

claim_transaction_4agent = claim(
    "Four co-evolving CORAL agents achieve a Transaction Scheduling score of 4,694 "
    "(higher is better), compared to 4,566 for the single-agent CORAL—a 1.89% "
    "improvement over single-agent performance.",
    title="4-agent Transaction Scheduling: 4694",
    metadata={"source": "artifacts/2604-01658.pdf, Table 2, Section 4.2"},
)

# =============================================================================
# Multi-agent vs independent compute baseline (the key counterfactual)
# =============================================================================

claim_coevolution_beats_independent = claim(
    "4-agent co-evolution (with shared memory) outperforms independent best-of-4 "
    "(without shared memory) on the hardest tasks. On Kernel Engineering, co-evolution "
    "achieves 1,103 cycles versus 1,180 cycles for independent best-of-4—a 6.5% "
    "advantage. This confirms that multi-agent gains derive from coordination (knowledge "
    "sharing) rather than simply from running more independent agents.",
    title="Co-evolution beats independent best-of-4",
    metadata={"source": "artifacts/2604-01658.pdf, Table 2, Section 4.2"},
)

alt_additional_compute_explains = claim(
    "The performance advantage of 4-agent CORAL over single-agent CORAL is fully "
    "explained by the additional compute (4× more evaluations), and knowledge sharing "
    "between agents provides no additional benefit beyond what independent parallel "
    "search would achieve.",
    title="Alternative: additional compute explains multi-agent gains",
    metadata={"source": "artifacts/2604-01658.pdf, Section 4.2 (counterfactual baseline)"},
)

not_both_coordination = contradiction(
    claim_coevolution_beats_independent,
    alt_additional_compute_explains,
    reason=(
        "If co-evolution beats independent best-of-4 by 6.5% on Kernel Engineering, "
        "while both use the same total compute, then the additional compute explanation "
        "is falsified. These two claims cannot both be true: coordination matters implies "
        "additional compute does not fully explain the gains."
    ),
    prior=0.95,
)

# Abduction: coordination vs compute
# The observation is claim_coevolution_beats_independent (co-evolution beats independent compute)
# Both support strategies must conclude this observation
s_coordination_h = support(
    [claim_multi_agent_gains],
    claim_coevolution_beats_independent,
    reason=(
        "If multi-agent collaboration provides genuine gains (@claim_multi_agent_gains), "
        "then co-evolution with shared memory should outperform independent best-of-4 "
        "under identical compute, because coordination enables agents to avoid duplicating "
        "failed approaches and to build on each other's successes. This predicts the "
        "observed 6.5% advantage of co-evolution over independent best-of-4."
    ),
    prior=0.88,
)

s_compute_alt = support(
    [alt_additional_compute_explains],
    claim_coevolution_beats_independent,
    reason=(
        "If additional compute alone (@alt_additional_compute_explains) explains performance "
        "gains, then co-evolution (4 agents × shared memory) should match independent "
        "best-of-4 (4 agents × independent). The alternative predicts that the co-evolution "
        "vs. independent comparison would show approximately no gap—contradicted by the "
        "observed 6.5% advantage."
    ),
    prior=0.25,
)

pred_coordination = claim(
    "Co-evolution with shared memory will outperform independent best-of-4 on hard tasks "
    "where knowledge transfer is possible, showing a measurable gap.",
    title="Prediction: coordination beats independent compute",
)

pred_compute = claim(
    "Independent best-of-4 will match or nearly match co-evolution performance since "
    "additional compute is the main driver, showing approximately no gap.",
    title="Prediction: independent compute matches co-evolution",
)

comp_coordination = compare(
    pred_coordination, pred_compute, claim_coevolution_beats_independent,
    reason=(
        "The observed 6.5% gap between co-evolution (1,103 cycles) and independent best-of-4 "
        "(1,180 cycles) on Kernel Engineering matches the coordination hypothesis's prediction "
        "of a measurable gap, and contradicts the compute-only hypothesis's prediction of "
        "approximately no gap."
    ),
    prior=0.90,
)

abd_coordination = abduction(
    s_coordination_h, s_compute_alt, comp_coordination,
    reason=(
        "Both hypotheses (coordination vs. additional compute) attempt to explain why "
        "4-agent CORAL outperforms single-agent CORAL (@claim_multi_agent_gains). The "
        "decisive test is the co-evolution vs. independent best-of-4 comparison "
        "(@claim_coevolution_beats_independent): if co-evolution wins under identical "
        "compute, coordination explains the gains; if not, compute explains them."
    ),
)

# =============================================================================
# Ablation study: knowledge accumulation
# =============================================================================

claim_ablation_knowledge_kernel = claim(
    "Ablating knowledge accumulation (disabling the shared notes/ and skills/ directories "
    "so agents cannot write or read shared knowledge) degrades Kernel Engineering "
    "performance from 1,350 cycles to 1,601 cycles—an 18.6% regression. This establishes "
    "that knowledge accumulation is causally responsible for a substantial performance gain, "
    "not merely correlated with agent capability.",
    title="Knowledge ablation: 18.6% regression on Kernel Engineering",
    metadata={"source": "artifacts/2604-01658.pdf, Table 3, Section 4.3"},
)

claim_ablation_knowledge_polyominoes = claim(
    "Ablating knowledge accumulation degrades Polyominoes coverage from 80.2% to 77.3%—"
    "a 3.6 percentage point regression (4.5% relative). The effect is smaller than on "
    "Kernel Engineering, consistent with Polyominoes requiring less specialized domain "
    "knowledge that agents would record and reuse.",
    title="Knowledge ablation: 3.6pp regression on Polyominoes",
    metadata={"source": "artifacts/2604-01658.pdf, Table 3, Section 4.3"},
)

# Induction over two ablation observations
s_ablation_kernel = support(
    [claim_knowledge_causal],
    claim_ablation_knowledge_kernel,
    reason=(
        "If knowledge accumulation is causally important (@claim_knowledge_causal), then "
        "disabling it should produce a regression. The Kernel Engineering task requires "
        "specialized low-level optimization knowledge (CPU architecture, SIMD, compiler "
        "flags) that agents accumulate over iterations. Removing this accumulation "
        "forces each attempt to start from scratch, predicting the observed 18.6% regression."
    ),
    prior=0.90,
)

s_ablation_poly = support(
    [claim_knowledge_causal],
    claim_ablation_knowledge_polyominoes,
    reason=(
        "If knowledge accumulation is causally important (@claim_knowledge_causal), "
        "Polyominoes should also regress without knowledge, but less so than Kernel "
        "Engineering because combinatorial packing requires less specialized technical "
        "knowledge. The observed 3.6pp regression is consistent with this prediction."
    ),
    prior=0.85,
)

ind_ablation = induction(
    s_ablation_kernel, s_ablation_poly,
    law=claim_knowledge_causal,
    reason=(
        "Two independent ablation observations on structurally different tasks "
        "(Kernel Engineering: code optimization; Polyominoes: combinatorial packing) both "
        "confirm the causal role of knowledge accumulation, providing inductive support "
        "for the general law (@claim_knowledge_causal). The tasks are independent: "
        "different solution spaces, different evaluation functions, different agent behaviors."
    ),
)

# =============================================================================
# Trajectory analysis claims (from Table 4)
# =============================================================================

claim_local_verification_benefit = claim(
    "Agents that perform local verification (running their own tests before submitting "
    "to the evaluator) have significantly higher improvement rates than agents that "
    "do not. On tasks involving compiled code, local verification rates reach 57–61% "
    "(Kernel Engineering: 57%, Transaction Scheduling: 61%), and agents using local "
    "testing show improvement rates of approximately 43% versus 24% for agents without "
    "local verification on standard tasks.",
    title="Local verification correlates with improvement rate",
    metadata={"source": "artifacts/2604-01658.pdf, Table 4, Section 4.4"},
)

claim_knowledge_access_correlates = claim(
    "Knowledge access frequency (fraction of attempts where the agent reads from shared "
    "memory before attempting a solution) correlates positively with improvement rate. "
    "Advanced tasks show 17–30% knowledge access rates, with knowledge-accessing attempts "
    "improving at 55% (Kernel Engineering) and 38% (Polyominoes) versus 26% and 18% "
    "for non-knowledge-accessing attempts.",
    title="Knowledge access correlates with improvement",
    metadata={"source": "artifacts/2604-01658.pdf, Table 4, Section 4.4"},
)

claim_knowledge_creation_differential = claim(
    "Knowledge creation rates differ dramatically between standard and advanced tasks. "
    "On standard tasks, agents create only 0.05 knowledge artifacts per attempt (notes, "
    "skills). On advanced tasks, knowledge creation rates are 0.55 (Kernel Engineering) "
    "and 0.68 (Polyominoes) artifacts per attempt—approximately 10× higher. This "
    "suggests agents recognize and record more insights on harder problems.",
    title="Advanced tasks generate 10x more knowledge artifacts",
    metadata={"source": "artifacts/2604-01658.pdf, Section 4.4"},
)

# =============================================================================
# Cross-agent knowledge transfer claims
# =============================================================================

claim_cross_agent_transfer_kernel = claim(
    "On Kernel Engineering, 36% of attempts explicitly leverage another agent's prior "
    "work (by reading and building on another agent's code or notes from shared memory). "
    "These cross-agent attempts improve at a 17% rate versus 9% for attempts without "
    "cross-agent transfer. Furthermore, 66% of new best-known records on Kernel "
    "Engineering originate from cross-agent parentage.",
    title="Kernel Engineering: 36% cross-agent transfer, 66% of records from cross-agent",
    metadata={"source": "artifacts/2604-01658.pdf, Section 4.4"},
)

claim_cross_agent_transfer_poly = claim(
    "On Polyominoes, 87% of agent rounds reference knowledge from other agents "
    "(reading shared notes or skills before attempting). This extremely high cross-agent "
    "reading rate indicates that the shared memory store becomes the primary information "
    "source for agent strategy on hard combinatorial problems.",
    title="Polyominoes: 87% of rounds reference cross-agent knowledge",
    metadata={"source": "artifacts/2604-01658.pdf, Section 4.4"},
)

claim_strategy_diversity = claim(
    "Co-evolving agents maintain diverse strategies despite sharing memory: average "
    "Jaccard similarity between any two agents' strategy vocabularies is 0.43 (Kernel "
    "Engineering) and 0.31 (Polyominoes). This means more than half of each agent's "
    "strategy vocabulary is unique to that agent, indicating that memory sharing promotes "
    "knowledge diffusion without eliminating strategic diversity.",
    title="Co-evolving agents maintain strategic diversity",
    metadata={"source": "artifacts/2604-01658.pdf, Section 4.4"},
)

# =============================================================================
# Strategies
# =============================================================================

strat_transfer_drives_records = support(
    [claim_cross_agent_transfer_kernel, claim_persistent_memory_design],
    claim_kernel_4agent,
    reason=(
        "The 1,103-cycle Kernel Engineering result by 4-agent co-evolution is mechanistically "
        "explained by cross-agent knowledge transfer (@claim_cross_agent_transfer_kernel): "
        "66% of new records come from cross-agent parentage, meaning the best solutions "
        "build on insights from multiple agents. This transfer is enabled by shared "
        "persistent memory (@claim_persistent_memory_design) which stores agent-discovered "
        "techniques in the skills/ directory accessible to all agents."
    ),
    prior=0.85,
)

strat_diversity_prevents_collapse = support(
    [claim_strategy_diversity, claim_heartbeat_mechanism],
    claim_coevolution_beats_independent,
    reason=(
        "Strategic diversity (@claim_strategy_diversity) — Jaccard similarity 0.43, "
        "implying >50% unique strategy vocabulary per agent — ensures agents explore "
        "complementary regions of the solution space. Combined with heartbeat-triggered "
        "stagnation detection (@claim_heartbeat_mechanism), co-evolution avoids convergence "
        "to the same local optima that independent agents would each discover, producing "
        "the 6.5% advantage over independent best-of-4."
    ),
    prior=0.80,
)

strat_local_verify_from_adaptable = support(
    [claim_agents_adaptable],
    claim_local_verification_benefit,
    reason=(
        "Agent adaptability (@claim_agents_adaptable) is the mechanism behind local "
        "verification behavior: agents autonomously learn (through accumulated notes) that "
        "local testing before evaluation improves efficiency on compiled-code tasks. The "
        "57–61% local test rates on Kernel Engineering and Transaction Scheduling are "
        "emergent behaviors, not specified by the framework, consistent with agents adapting "
        "to task structure."
    ),
    prior=0.82,
)

strat_knowledge_access_causal = support(
    [claim_ablation_knowledge_kernel, claim_knowledge_access_correlates],
    claim_knowledge_causal,
    reason=(
        "Two converging lines of evidence support knowledge causality: (1) ablation "
        "(@claim_ablation_knowledge_kernel) shows that removing knowledge access produces "
        "18.6% regression, establishing counterfactual causality; (2) trajectory analysis "
        "(@claim_knowledge_access_correlates) shows knowledge-accessing attempts improve "
        "at 55% versus 26% for non-accessing attempts, establishing correlational evidence "
        "within the same experimental runs. Together they support @claim_knowledge_causal."
    ),
    prior=0.88,
)

strat_poly_transfer = support(
    [claim_persistent_memory_design],
    claim_cross_agent_transfer_poly,
    reason=(
        "Shared persistent memory (@claim_persistent_memory_design) is the mechanism enabling "
        "87% of Polyominoes rounds to reference cross-agent knowledge: the notes/ and skills/ "
        "directories provide the store from which agents read other agents' findings. Without "
        "this shared store, cross-agent knowledge transfer would be impossible."
    ),
    prior=0.90,
)

strat_poly_4agent = support(
    [claim_cross_agent_transfer_poly, claim_strategy_diversity],
    claim_polyominoes_4agent,
    reason=(
        "The 84.2% Polyominoes coverage by 4-agent co-evolution is explained by extremely "
        "high cross-agent knowledge transfer (87% of rounds reading cross-agent knowledge, "
        "@claim_cross_agent_transfer_poly) combined with strategic diversity (Jaccard "
        "similarity 0.31, @claim_strategy_diversity). Diverse strategies ensure agents "
        "discover complementary packing approaches, while high transfer ensures each agent "
        "builds on the best insights from all agents."
    ),
    prior=0.82,
)

strat_transaction_4agent = support(
    [claim_coevolution_beats_independent, claim_local_verification_benefit],
    claim_transaction_4agent,
    reason=(
        "The Transaction Scheduling improvement from 4,566 (single-agent) to 4,694 "
        "(4-agent) follows from co-evolution advantages (@claim_coevolution_beats_independent): "
        "shared memory allows agents to exchange successful local verification strategies "
        "@claim_local_verification_benefit. On Transaction Scheduling, agents achieve 61% "
        "local test rates, and sharing these verification discoveries accelerates improvement."
    ),
    prior=0.80,
)

strat_knowledge_creation_from_tasks = support(
    [claim_knowledge_causal],
    claim_knowledge_creation_differential,
    reason=(
        "If knowledge accumulation causally improves performance (@claim_knowledge_causal), "
        "then harder tasks—where knowledge matters more—should trigger higher knowledge "
        "creation rates. The 10× differential (0.05 vs. 0.55–0.68 artifacts per attempt) "
        "reflects that on harder tasks, agents recognize and record more useful insights, "
        "consistent with knowledge being genuinely valuable on those tasks."
    ),
    prior=0.78,
)
