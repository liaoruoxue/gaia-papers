"""Prior assignments for independent (leaf) claims in the ABBEL package.

Only independent premises that are not the conclusion of any strategy receive
priors here. Derived claims get their belief from BP propagation.
"""

from . import (
    abbel_two_call_loop,
    alt_qa_just_better_rl,
    belief_prompting_definition,
    belief_prompting_helps,
    fm_belief_error_propagation,
    fm_hallucinated_memories,
    fm_uninformative_repeats,
    method_belief_grading,
    method_belief_length_penalty,
    natural_language_belief_capability,
    obs_belief_lengths_short,
    obs_belief_prompting_rarely_helps,
    obs_cb_table,
    obs_cl_bg_outperforms,
    obs_deepseek_abbel_worse,
    obs_gemini_abbel_competitive,
    obs_qa_abbel_outperforms_mem1,
    obs_qa_peak_tokens_table,
    pred_cl_abbel_no_bg,
    pred_cl_belief_grading_wins,
    pred_qa_isolation_helps,
    problem_long_horizon_context,
    vanilla_definition,
)

PRIORS = {
    # --- Background / framework definitions (high confidence, definitional) ---
    abbel_two_call_loop: (
        0.99,
        "This is the operational definition of the ABBEL framework as proposed "
        "by the authors. As a definition rather than an empirical claim, it is "
        "true by construction within the paper.",
    ),
    vanilla_definition: (
        0.99,
        "Operational definition of the standard multi-step paradigm. Standard "
        "and well-established framing of full-history multi-step LLM agents.",
    ),
    belief_prompting_definition: (
        0.99,
        "Operational definition of the BELIEF PROMPTING ablation. As a "
        "definition, holds by construction.",
    ),
    method_belief_grading: (
        0.97,
        "Operational definition of the belief-grading reward procedure (Fig. 3). "
        "Definition is precise and the size-2 GRPO trick is standard.",
    ),
    method_belief_length_penalty: (
        0.97,
        "Operational definition of the belief length penalty. The post-"
        "advantage-normalization detail is from Arora and Zanette (2025), a "
        "well-cited approach.",
    ),
    # --- Background context from the introduction ---
    problem_long_horizon_context: (
        0.95,
        "Empirically well-established: long-horizon agents (SWE-Agent, "
        "OpenHands, AutoGPT, AgentBench) routinely exceed practical context "
        "limits. Documented across multiple recent papers and standard "
        "industry experience.",
    ),
    natural_language_belief_capability: (
        0.85,
        "Established by Arumugam and Griffiths (2025) for environments with "
        "hand-crafted priors. Mild discount because the cited demonstration "
        "was on tailored bandit-like settings rather than the diverse "
        "environments evaluated here.",
    ),
    belief_prompting_helps: (
        0.80,
        "Established by Kim et al. (2025) ReflAct in goal-state reflection "
        "settings. Mild discount because the present paper actually finds in "
        "Section 4 that BELIEF PROMPTING rarely outperforms VANILLA on its "
        "six environments (so the prior literature claim does not "
        "universally generalize).",
    ),
    # --- Section 4 prompting-only observations ---
    obs_gemini_abbel_competitive: (
        0.92,
        "Direct empirical result from Fig. 2a, 40 instances per environment "
        "with reported standard error. The 'competitive or better in most "
        "tasks' phrasing leaves room for environment-specific exceptions, "
        "consistent with typical empirical robustness.",
    ),
    obs_deepseek_abbel_worse: (
        0.92,
        "Direct empirical result from Fig. 2a. DeepSeek V3 and R1 ABBEL bars "
        "are visibly lower than VANILLA across most environments. Standard "
        "errors reported, n = 40 per env.",
    ),
    obs_belief_prompting_rarely_helps: (
        0.88,
        "Direct empirical observation across Fig. 2a. The qualifier 'rarely "
        "outperforms VANILLA and sometimes substantially decreases "
        "performance' is consistent with the chart and conservative; small "
        "discount for the qualitative summary.",
    ),
    # --- Section 5 method-experiment observations ---
    obs_qa_peak_tokens_table: (
        0.95,
        "Table 1 reports concrete numerical EM scores and peak-token usage "
        "with standard errors. Internally consistent (LP < ABBEL on tokens, "
        "ABBEL > MEM1 Instruct on EM at 4+ objectives). External numbers for "
        "MEM1 Base and VANILLA 14B Zero come from Zhou et al. (2025b); the "
        "rest are the authors' own measurements.",
    ),
    obs_cb_table: (
        0.93,
        "Table 2 reports test pass rate, success rate, and peak tokens at "
        "training steps 0/50/100, with SEM over 2 ABBEL/ABBEL-BG seeds and "
        "over the test set for 1 VANILLA seed. The 1-seed VANILLA SEM means "
        "the trained-VANILLA numbers carry slightly more uncertainty, but the "
        "ABBEL/BG figures are reliable.",
    ),
    # --- Hypothesis predictions used inside contradiction operators ---
    pred_cl_belief_grading_wins: (
        0.85,
        "This is the authors' working hypothesis going into the Combination "
        "Lock experiment. The reasoning (dense shaping needed for complex "
        "belief-update reasoning) is plausible and is the standard intuition "
        "for shaping rewards. Confirmed by Fig. 4.",
    ),
    pred_cl_abbel_no_bg: (
        0.40,
        "The competing prediction that 'plain RL is sufficient on Combination "
        "Lock without belief grading'. The Fig. 10a ablation falsifies it: "
        "without BG, ABBEL only catches up rather than surpassing. Set as a "
        "below-50% prior reflecting that the alternative does not match the "
        "ablation outcome.",
    ),
    pred_qa_isolation_helps: (
        0.85,
        "The architectural-isolation hypothesis is well-motivated: keeping "
        "belief separate from reasoning is what enables the LP to operate "
        "on belief alone. Confirmed by both the EM gap vs MEM1 Instruct and "
        "by the LP being applicable.",
    ),
    alt_qa_just_better_rl: (
        0.25,
        "The 'incidental training details' alternative for the QA result. "
        "The authors run MEM1 Instruct (apples-to-apples re-implementation) "
        "and the gap remains, weakening this alternative. Additionally, the "
        "alternative cannot explain the LP-specific result. Low prior — but "
        "non-trivial because hyperparameter sensitivity is real.",
    ),
    # --- Failure-mode observations (anchor as observed facts so the induction "
    #     to the law @finding_failure_modes pulls the law upward) ---
    fm_uninformative_repeats: (
        0.92,
        "Direct trace-inspection observation reported in Section 4.3: "
        "Customer Service traces where the customer says 'I'm not sure' lead "
        "to repeated actions under ABBEL. Behavior is causally explainable "
        "by the framework (no past-action info in belief). High prior; small "
        "discount because trace inspection is qualitative.",
    ),
    fm_belief_error_propagation: (
        0.92,
        "Direct trace-inspection observation in Wordle/Mastermind (Section "
        "4.3 and Appendix C.2.1): early belief errors (e.g., 'no repeated "
        "characters in code') persist across steps. High prior; well-grounded "
        "by both the architectural argument and the qualitative trace.",
    ),
    fm_hallucinated_memories: (
        0.88,
        "Trace-inspection observation in Appendix C.2.1: agents sometimes "
        "fabricate past actions/observations in the belief. Slightly lower "
        "than the other two failure modes because hallucination prevalence "
        "is harder to quantify and the appendix shows fewer concrete examples.",
    ),
    # --- Anchor key observations directly so inductions to laws are pulled up ---
    obs_belief_lengths_short: (
        0.93,
        "Direct token-count plot from Fig. 2b across 3 frontier models and 6 "
        "environments. The qualitative summary (significantly shorter beyond "
        "first few steps, with one Gemini exception in two envs) is "
        "well-supported by the figure. Slight discount for the qualitative "
        "framing.",
    ),
    obs_cl_bg_outperforms: (
        0.92,
        "Direct training-curve observation from Fig. 4a: at ~120 training "
        "steps, ABBEL-BG's test success rate is visibly above VANILLA and "
        "BELIEF PROMPTING. Belief-length plot in Fig. 4b confirms beliefs "
        "remain shorter than history past step 2. Reproducible from the "
        "open-sourced code per the Reproducibility Statement.",
    ),
    obs_qa_abbel_outperforms_mem1: (
        0.94,
        "Tabulated EM scores in Table 1 directly show ABBEL > MEM1 Instruct "
        "at 4+ objectives (e.g., 16-obj: 3.57 vs 2.50, ~43% higher). "
        "Reported with SEM and grounded in 16-objective benchmark. "
        "Comparison is apples-to-apples (both Qwen2.5-7B-Instruct base).",
    ),
}
