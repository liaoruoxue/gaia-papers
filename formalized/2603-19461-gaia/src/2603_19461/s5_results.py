"""Section 5: Results — Task Performance, Transfer, and Compounding"""

from gaia.lang import (
    claim, setting,
    support, compare, abduction, induction,
    contradiction,
)

from .motivation import (
    setup_dgm,
    setup_hyperagent_def,
    dgm_limitation,
    hyperagent_advantage,
)
from .s3_methods import (
    setup_initial_agent,
    setup_evaluation_protocol,
    setup_statistical,
    dgmh_extends_dgm,
    dgmh_no_domain_alignment,
    open_ended_mitigates_convergence,
)

# ─── Section 5.1: Improving Task Performance ─────────────────────────────────

# Coding
coding_initial_score = claim(
    "On the Polyglot coding benchmark (50-task training subset), the initial agent achieves "
    "a training score of 0.140 and a full-benchmark score of 0.084.",
    title="Coding initial agent score",
    metadata={"source_figure": "artifacts/2603.19461.pdf, Section 5.1"},
)

dgmh_coding_result = claim(
    "On the Polyglot coding benchmark, DGM-H improves its training score on the 50-task "
    "subset from 0.140 (initial agent) to 0.340 (CI: 0.300–0.380) over 80 iterations. "
    "On the full Polyglot benchmark (largely unseen tasks), performance increases from "
    "0.084 (initial) to 0.267 (CI: 0.231–0.280).",
    title="DGM-H coding benchmark performance",
    background=[setup_evaluation_protocol, setup_statistical],
    metadata={"source_figure": "artifacts/2603.19461.pdf, Section 5.1"},
)

dgm_coding_result = claim(
    "The original DGM (Zhang et al., 2025) achieves coding improvements from 0.140 to 0.380 "
    "on the 50-task Polyglot training subset and from 0.142 to 0.307 on the full Polyglot "
    "benchmark, using a handcrafted instruction-generation mechanism specifically designed "
    "for coding.",
    title="Original DGM coding benchmark performance",
    background=[setup_dgm, setup_evaluation_protocol],
    metadata={"source_figure": "artifacts/2603.19461.pdf, Section 5.1"},
)

dgmh_coding_comparable_to_dgm = claim(
    "DGM-H achieves coding improvement comparable to the original DGM (DGM-H: 0.084→0.267 "
    "on full benchmark; DGM: 0.142→0.307), despite DGM-H not being handcrafted specifically "
    "for coding tasks.",
    title="DGM-H coding performance comparable to DGM",
)

strat_coding_comparable = support(
    [dgmh_coding_result, dgm_coding_result, coding_initial_score],
    dgmh_coding_comparable_to_dgm,
    reason=(
        "Both DGM-H and DGM start from the same initial coding performance (@coding_initial_score). "
        "The full-benchmark scores are similar in magnitude: DGM-H reaches 0.267 vs DGM's 0.307 "
        "(@dgmh_coding_result, @dgm_coding_result). The DGM is purpose-built for coding, "
        "while DGM-H uses a general self-modification framework. Near-parity indicates DGM-H "
        "has not sacrificed coding ability for generality."
    ),
    prior=0.8,
)

# Paper review
paper_review_initial = claim(
    "On paper review (test set), the initial agent achieves a score of 0.0, because it fails "
    "to produce outputs in the required format due to the absence of task-specific parsing "
    "or post-processing.",
    title="Paper review initial agent score",
    background=[setup_initial_agent],
)

dgmh_paper_review_result = claim(
    "On paper review (test set), DGM-H improves performance from 0.0 (initial agent) to "
    "0.710 (CI: 0.590–0.750) over 100 iterations. Several top-performing agents outperform "
    "the open-sourced static baseline (Yamada et al., 2025) which achieves 0.630.",
    title="DGM-H paper review test performance",
    background=[setup_evaluation_protocol, setup_statistical],
    metadata={"source_figure": "artifacts/2603.19461.pdf, Figure 2"},
)

dgm_paper_review_result = claim(
    "The original DGM (designed for coding), when applied without domain customization, achieves "
    "paper review test-set performance of 0.0 (CI: 0.0–0.510). When manually customized "
    "(DGM-custom), it achieves 0.590 (CI: 0.570–0.650).",
    title="Original DGM paper review performance",
    background=[setup_dgm, dgm_limitation],
    metadata={"source_figure": "artifacts/2603.19461.pdf, Figure 2"},
)

pred_dgmh_paper = claim(
    "DGM-H (metacognitive self-modification) predicts paper review performance of ~0.710 on test.",
    title="DGM-H prediction for paper review",
)

pred_dgm_paper = claim(
    "DGM without domain customization predicts paper review performance ~0.0 on test, because "
    "its fixed instruction-generation mechanism is not suited to non-coding tasks.",
    title="DGM prediction for paper review",
)

comp_paper = compare(
    pred_dgmh_paper, pred_dgm_paper, dgmh_paper_review_result,
    reason=(
        "DGM-H achieves 0.710 on test (CI: 0.590–0.750), substantially outperforming "
        "DGM-without-customization (0.0, starting from @paper_review_initial) and "
        "matching or exceeding DGM-custom (0.590) (@dgm_paper_review_result). "
        "The deviation from DGM (non-customized) is statistically significant (p < 0.05)."
    ),
    prior=0.9,
)

s_h_paper = support(
    [pred_dgmh_paper], dgmh_paper_review_result,
    reason="DGM-H's metacognitive self-modification enables domain adaptation without manual engineering, predicting high paper review performance.",
    prior=0.9,
)
s_alt_paper = support(
    [pred_dgm_paper], dgmh_paper_review_result,
    reason="DGM without customization predicts near-zero performance; this does not explain 0.710.",
    prior=0.2,
)

abd_paper = abduction(
    s_h_paper, s_alt_paper, comp_paper,
    reason=(
        "Both DGM-H and baseline DGM attempt to solve the same paper review task from the "
        "same initial agent. The outcome (DGM-H: 0.710 vs DGM: 0.0) provides evidence about "
        "which approach better explains the observed performance gains."
    ),
)

# Robotics reward design
robotics_initial = claim(
    "On robotics reward design (test set), the initial agent achieves a score of 0.060, "
    "because the initial agent occasionally produces a minimally functional reward function.",
    title="Robotics reward design initial agent score",
    background=[setup_initial_agent],
)

dgmh_robotics_result = claim(
    "On robotics reward design (test set), DGM-H improves performance from 0.060 (initial) "
    "to 0.372 (CI: 0.355–0.436) over 100 iterations, surpassing the default reward function "
    "that directly optimizes the evaluation metric (0.348). DGM-H almost always generates "
    "agents that induce jumping behaviors (optimal) rather than getting stuck at standing tall "
    "(local optimum).",
    title="DGM-H robotics reward design test performance",
    background=[setup_evaluation_protocol, setup_statistical],
    metadata={"source_figure": "artifacts/2603.19461.pdf, Figure 2"},
)

dgm_robotics_result = claim(
    "The original DGM (without domain customization) achieves robotics reward design test "
    "performance of 0.0 (CI: 0.0–0.090). DGM-custom achieves 0.348 (CI: 0.305–0.385).",
    title="Original DGM robotics reward design performance",
    background=[setup_dgm, dgm_limitation],
    metadata={"source_figure": "artifacts/2603.19461.pdf, Figure 2"},
)

dgmh_outperforms_dgm_robotics = claim(
    "DGM-H significantly outperforms the original DGM on robotics reward design test tasks "
    "(p < 0.05). DGM-H achieves higher median performance (0.372) than DGM-custom (0.348) "
    "on test tasks, though the difference is not statistically significant (p > 0.05).",
    title="DGM-H vs DGM on robotics",
)

strat_robotics_outperforms = support(
    [dgmh_robotics_result, dgm_robotics_result, robotics_initial],
    dgmh_outperforms_dgm_robotics,
    reason=(
        "DGM-H reaches 0.372 vs DGM's 0.0 on test (@dgmh_robotics_result, @dgm_robotics_result), "
        "both starting from the same initial score of 0.060 (@robotics_initial). "
        "The difference between DGM-H and DGM (non-customized) is statistically significant "
        "(p < 0.05, Wilcoxon signed-rank test). DGM-H also outperforms DGM-custom (0.348) in "
        "median but not significantly. The qualitative difference (DGM-H escapes the local "
        "optimum of standing vs. jumping) further differentiates the methods."
    ),
    prior=0.85,
)

# Both metacognition and open-ended exploration are necessary
dgmh_wout_self_improve = claim(
    "DGM-H without self-improving meta agents (DGM-H w/o self-improve), which fixes the meta "
    "agent throughout the run (replicating the ADAS approach), achieves test-set performance of "
    "0.0 (CI: 0.0–0.130) on paper review and 0.213 (CI: 0.180–0.348) on robotics reward design. "
    "DGM-H significantly outperforms this baseline (p < 0.05) in both domains.",
    title="DGM-H w/o self-improve baseline performance",
    background=[setup_statistical],
    metadata={"source_figure": "artifacts/2603.19461.pdf, Figure 2"},
)

metacognition_necessary = claim(
    "Metacognitive self-modification (the ability to improve the meta agent) is necessary for "
    "the observed performance gains of DGM-H. The gains are not solely due to task-level "
    "optimization under a fixed meta agent.",
    title="Metacognition is necessary for DGM-H gains",
)

strat_metacognition_necessary = support(
    [dgmh_wout_self_improve, paper_review_initial, dgm_paper_review_result],
    metacognition_necessary,
    reason=(
        "DGM-H w/o self-improve fixes the meta agent and still allows task-level optimization. "
        "Its substantially lower performance (0.0 on paper review, 0.213 on robotics) compared "
        "to full DGM-H (0.710 and 0.372), both starting from the same initial agent "
        "(@paper_review_initial), indicates that the meta-level improvement is not "
        "redundant. Even DGM-custom (@dgm_paper_review_result, 0.590) does not achieve DGM-H's "
        "performance, showing manual engineering is also not sufficient."
    ),
    prior=0.85,
)

# ─── Section 5.2: Transferable Meta-Level Improvements ───────────────────────

imp50_metric = setting(
    "imp@50 measures an agent's ability to generate improved agents. Starting from a given "
    "initial agent, a generation algorithm is run for 50 iterations; imp@50 is the performance "
    "gain of the best generated agent over the starting agent on the task.",
    title="imp@50 metric definition",
)

dgmh_transfer_agents_score = claim(
    "Transfer hyperagents from prior DGM-H runs on paper review + robotics reward design "
    "achieve initial test-set score of 0.0 (CI: 0.0–0.0) on Olympiad-level math grading, "
    "reflecting the domain shift.",
    title="Transfer hyperagent initial score on math grading",
    background=[imp50_metric],
)

dgmh_transfer_imp50 = claim(
    "After 50 iterations of DGM-H w/o self-improve starting from transfer hyperagents, "
    "the best generated agents achieve a test-set score of 0.630 (CI: 0.540–0.630) on "
    "Olympiad-level math grading. This corresponds to imp@50 = 0.630 (CI: 0.540–0.630). "
    "The transfer agents are significantly more effective at generating improved agents "
    "than the initial agent (p < 0.05).",
    title="DGM-H transfer imp@50 on math grading",
    background=[imp50_metric, setup_statistical],
    metadata={"source_figure": "artifacts/2603.19461.pdf, Figure 3"},
)

dgm_transfer_imp50 = claim(
    "Transfer agents from DGM-custom runs achieve imp@50 ≈ 0.0 (CI: 0.0–0.010) on Olympiad-"
    "level math grading when using DGM w/o self-improve as the generation algorithm. "
    "This shows DGM-custom does not learn transferable meta-level improvements.",
    title="DGM-custom transfer imp@50 on math grading",
    background=[imp50_metric, setup_statistical],
    metadata={"source_figure": "artifacts/2603.19461.pdf, Figure 3"},
)

meta_improvements_transfer = claim(
    "Meta-level improvements learned by DGM-H transfer across domains. Hyperagents acquire "
    "general-purpose meta-level capabilities (e.g., performance tracking, persistent memory) "
    "that enable rapid self-adaptation to previously unseen tasks.",
    title="DGM-H meta-improvements are transferable",
)

pred_dgmh_transfer = claim(
    "DGM-H predicts that hyperagents encode transferable self-improvement mechanisms enabling "
    "imp@50 > 0 in a new domain when starting from transfer hyperagents.",
    title="DGM-H prediction for transfer",
)

pred_dgm_transfer = claim(
    "DGM-custom predicts that task-level improvements transfer, but meta-level improvements "
    "do not, so imp@50 ≈ 0 when starting from DGM-custom transfer agents.",
    title="DGM prediction for transfer",
)

comp_transfer = compare(
    pred_dgmh_transfer, pred_dgm_transfer, dgmh_transfer_imp50,
    reason=(
        "DGM-H achieves imp@50 = 0.630 starting from transfer hyperagents (which had initial "
        "score 0.0, @dgmh_transfer_agents_score) vs. imp@50 ≈ 0 "
        "for DGM-custom transfer agents (@dgmh_transfer_imp50, @dgm_transfer_imp50). "
        "The difference is statistically significant (p < 0.05). DGM-H's prediction is "
        "confirmed; DGM-custom's prediction is also confirmed (their transfers don't work)."
    ),
    prior=0.9,
)

s_h_transfer = support(
    [pred_dgmh_transfer], dgmh_transfer_imp50,
    reason=(
        "DGM-H predicts hyperagents encode transferable self-improvement mechanisms (@pred_dgmh_transfer), "
        "directly predicting that a transfer hyperagent can generate improved agents in a new domain "
        "with imp@50 > 0."
    ),
    prior=0.85,
)
s_alt_transfer = support(
    [pred_dgm_transfer], dgmh_transfer_imp50,
    reason=(
        "DGM-custom's prediction (@pred_dgm_transfer) is that meta-level improvements do not transfer, "
        "so imp@50 ≈ 0. This alternative cannot explain the observed DGM-H imp@50 of 0.630."
    ),
    prior=0.1,
)

abd_transfer = abduction(
    s_h_transfer, s_alt_transfer, comp_transfer,
    reason=(
        "Both DGM-H and DGM-custom attempt transfer to math grading from paper-review and "
        "robotics-optimized agents. The large difference in imp@50 (0.630 vs. ~0) disambiguates "
        "whether observed gains arise from general meta-level skill or domain-specific tuning."
    ),
)

strat_transfer = support(
    [dgmh_transfer_imp50, dgm_transfer_imp50, dgmh_transfer_agents_score],
    meta_improvements_transfer,
    reason=(
        "DGM-H's transfer imp@50 of 0.630 vs. DGM-custom's 0.0 (@dgmh_transfer_imp50, "
        "@dgm_transfer_imp50) directly shows that DGM-H learns something that transfers while "
        "DGM-custom does not. Critically, both started from agents with similar initial scores "
        "in the new domain (near 0.0, @dgmh_transfer_agents_score), controlling for initial "
        "advantage. The qualitative analysis attributes this to general capabilities such as "
        "performance tracking and persistent memory that the hyperagents autonomously acquired."
    ),
    prior=0.85,
)

# ─── Section 5.3: Compounding Self-Improvements ──────────────────────────────

dgmh_compound_faster = claim(
    "DGM-H run on Olympiad-level math grading, initialized from transfer hyperagents, achieves "
    "faster progress and higher final performance compared to DGM-H initialized from the initial "
    "agent, indicating previously learned self-improvements remain useful and compound in a "
    "new domain.",
    title="Transfer hyperagents enable faster compounding progress",
    metadata={"source_figure": "artifacts/2603.19461.pdf, Figure 4"},
)

dgmh_proofautograder_result = claim(
    "DGM-H initialized with ProofAutoGrader as the task agent and a transfer meta agent from "
    "prior DGM-H runs achieves a test-set score of 0.700 on Olympiad-level math grading after "
    "200 iterations, compared to ProofAutoGrader's score of 0.670. On the full IMO-GradingBench, "
    "DGM-H improves accuracy from 0.561 to 0.601 and reduces mean absolute error from 0.178 "
    "to 0.175.",
    title="DGM-H improves ProofAutoGrader on IMO-GradingBench",
    background=[setup_statistical],
    metadata={"source_figure": "artifacts/2603.19461.pdf, Figure 4"},
)

self_improvements_compound = claim(
    "Self-improvements learned by DGM-H in one setting can accumulate and compound across runs. "
    "The system can build on strong existing solutions (like ProofAutoGrader) and further improve "
    "their performance in a new domain.",
    title="DGM-H self-improvements compound across runs",
)

strat_compound = support(
    [dgmh_compound_faster, dgmh_proofautograder_result],
    self_improvements_compound,
    reason=(
        "Two pieces of evidence jointly support compounding: (1) transfer hyperagents lead to "
        "faster progress and higher ceiling vs. initial-agent initialization (@dgmh_compound_faster), "
        "showing prior meta-improvements are reusable; (2) starting from a strong artifact "
        "(ProofAutoGrader) and a transfer meta agent yields further improvement (0.561→0.601) "
        "(@dgmh_proofautograder_result), showing the system can build on strong existing solutions."
    ),
    prior=0.8,
)

# Induction: multiple independent domains support the generality of DGM-H
law_dgmh_improves = claim(
    "DGM-H achieves substantial and generalizable task-performance gains across diverse computable "
    "tasks, without domain-specific engineering of the self-improvement mechanism.",
    title="DGM-H general self-improvement law",
)

s_coding = support(
    [law_dgmh_improves], dgmh_coding_comparable_to_dgm,
    reason="The general law predicts coding improvement; DGM-H achieves comparable coding gains.",
    prior=0.85,
)

s_paper = support(
    [law_dgmh_improves], dgmh_paper_review_result,
    reason="The general law predicts paper review improvement; DGM-H achieves 0.710 from 0.0.",
    prior=0.85,
)

s_robotics = support(
    [law_dgmh_improves], dgmh_robotics_result,
    reason="The general law predicts robotics improvement; DGM-H achieves 0.372 from 0.060.",
    prior=0.85,
)

ind_coding_paper = induction(
    s_coding, s_paper,
    law=law_dgmh_improves,
    reason="Coding and paper review are independent domains with different skill requirements.",
)

ind_all_domains = induction(
    ind_coding_paper, s_robotics,
    law=law_dgmh_improves,
    reason="Robotics reward design adds an independent domain requiring interaction with a physics simulator.",
)
