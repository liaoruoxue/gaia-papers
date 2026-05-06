"""Priors for independent (leaf) claims in the SIMURA formalization
(Deng et al. 2025 [@Deng2025SIMURA]).

Calibration philosophy
----------------------
* **Numerical readouts from per-task tables** (Tables 1-3 cells:
  FlightQA, FanOutQA, WebArena) -- 0.93. These are direct
  transcriptions of values reported in the paper, but a small
  discount accounts for transcription/computation risk and the
  possibility of run-to-run noise (the paper does not report
  per-run standard deviations for the web-browsing experiments).
* **Method-description / setup claims** (FlightQA construction,
  evaluation protocol, WebArena setup, SIMURA module spec,
  natural-language state definition) -- 0.9-0.95. These are
  procedurally verifiable specifications whose only failure mode
  is misreading.
* **Diagnostic / literature-summary claims** (existing-agents
  characterization, generalist-agent lines, world-model history,
  benchmark-limits diagnosis) -- 0.82-0.88. Author-stated
  characterizations of competing methods drawn from cited works.
* **Conceptual claims** (LLM-pretraining ~ world-modeling) --
  0.78. A non-controversial but non-tautological framing claim
  ([@RAP; @HuShu2023]).
* **Empirical observations / motivating examples** (ChatGPT-4o
  flight hallucination, ground-truth unavailability) -- 0.85-0.95.
  Single-instance demonstrations.
* **Limitations** (runtime, tooling, modality) -- 0.92. The paper's
  own self-reports of operational shortcomings; high prior because
  the authors directly observe them.
* **Foundational mathematical lemma** (value-function recursion,
  Eq. 2) -- 0.97. Standard Bellman decomposition; treated here as
  a near-axiomatic claim because the recursion is a textbook
  consequence of the value-function definition [@SuttonBarto].
* **Abduction-component prediction claims** (H = world-model
  simulation explains the 5-fact fingerprint; Alt = trivial
  confounds explain it) -- pi(H) ~ 0.7, pi(Alt) ~ 0.2. The
  alternative's pi(Alt) is the probability that the trivial
  alternative *alone* explains the joint fingerprint, NOT whether
  trivial confounds have correct local explanations. Trivial
  confounds predict opposite signs for fact (iv) (loop avoidance)
  and (v) (constraint-count consistency), so pi(Alt) is held low.
"""

from .s2_related_work import (
    claim_llm_agents_two_lines,
    claim_world_model_history,
    claim_existing_wm_continuous_embedding_limit,
    claim_existing_web_agents_react_limited,
    claim_existing_benchmarks_limit,
    claim_generalist_two_lines,
)
from .s3_optimal_agent_formulation import (
    setup_value_recursion,
    claim_ground_truth_unavailable,
    claim_atomic_action_rollout_limits,
    setup_natural_language_state_def,
)
from .s4_simura_architecture import (
    setup_simura_modules,
    claim_llm_pretraining_is_world_modeling,
)
from .s7_per_task_results import (
    setup_flightqa_dataset,
    setup_flightqa_evaluation,
    claim_flightqa_table1,
    claim_chatgpt_4o_hallucination_example,
    claim_fanoutqa_table2,
    setup_webarena_eval,
    claim_webarena_table3,
)
from .s9_discussion_limitations import (
    claim_limit_runtime,
    claim_limit_tooling,
    claim_limit_modality,
)
from .s10_wiring import (
    claim_h_world_model_explains,
    claim_alt_lm_capability_explains,
)


PRIORS: dict = {
    # =======================================================================
    # Foundational mathematical lemma (value-function Bellman recursion)
    # =======================================================================
    setup_value_recursion: (
        0.97,
        "Bellman-style value-function recursion (Eq. 2) is the "
        "textbook decomposition of an expected discounted return "
        "into instantaneous reward plus discounted future value. "
        "It follows from the definition of the value function "
        "[@SuttonBarto, Sec. 3] under standard conditions on the "
        "discount sequence. The high prior reflects that this is "
        "a near-axiomatic mathematical fact, not an empirical "
        "claim. The 0.03 discount allows for the possibility of "
        "edge-case discount-sequence pathologies not covered in "
        "the paper's compact statement.",
    ),

    # =======================================================================
    # Independent diagnostic / literature-summary claims
    # =======================================================================
    claim_existing_web_agents_react_limited: (
        0.85,
        "Characterization of existing web-browsing agents as "
        "ReAct-based [@ReAct] autoregressive systems (proprietary: "
        "[@Operator; @AnthropicComputerUse; @ProjectMariner]; "
        "open-source: [@OpenHands; @WebVoyager; @CogAgent; "
        "@WebAgentGur]). The 'difficulty recovering from previous "
        "mistakes' is a standard observation in this literature. "
        "0.85 reflects strong consensus in the open-source agent "
        "research community while leaving room for newer agents "
        "that incorporate explicit deliberation.",
    ),
    claim_llm_agents_two_lines: (
        0.88,
        "Two-line decomposition of LLM-agent practice (data-"
        "collection-then-training: AutoWebGLM [@AutoWebGLM], "
        "AgentQ [@AgentQ], UI-TARS [@UITARS]; prompt-based: AWM "
        "[@AWM], Voyager [@Voyager]) is a literal taxonomy of the "
        "primary research lines as stated in those papers' own "
        "introductions.",
    ),
    claim_existing_wm_continuous_embedding_limit: (
        0.82,
        "Characterization of prior world-model systems as using "
        "continuous holistic embeddings (DreamerV3 [@Dreamer], "
        "WebDreamer [@WebDreamer], MBPO [@MBPO], TDMPC [@TDMPC]). "
        "The 'noise / variability detracts from robust decision-"
        "making' framing is supported by [@Barrett2017] but is a "
        "narrative claim, not a measured deficit. Prior 0.82 to "
        "reflect that this is a contested framing -- continuous-"
        "embedding world models do work in many domains.",
    ),
    claim_existing_benchmarks_limit: (
        0.85,
        "Characterization of existing web-agent benchmarks "
        "(WebArena [@WebArena], WebVoyager [@WebVoyager], MiniWoB++ "
        "[@MiniWoB], Mind2Web [@Mind2Web], WebShop [@WebShop]) as "
        "having simulation-environment / staleness / weak-evaluation "
        "gaps. This characterization is widely shared in the live-"
        "web-agent literature (see [@AssistantBench] for a closely-"
        "argued companion claim). 0.85 reflects consensus while "
        "leaving room for partial counterexamples.",
    ),
    claim_generalist_two_lines: (
        0.85,
        "Two-line decomposition of generalist-agent practice "
        "(multi-agent workflows: [@OWL; @AgentOrchestra; "
        "@MagenticOne]; composable scripts: [@CodeAct; @OpenHands; "
        "@smolagents; @Alita]). Literal taxonomy of stated approaches.",
    ),
    claim_world_model_history: (
        0.92,
        "Historical narrative of model-based planning -- Atari/Go/"
        "Chess/Shogi [@Oh2015AtariVid; @MuZero], control "
        "[@MBPO; @TDMPC], math reasoning [@RAP], Minecraft "
        "[@Dreamer], web browsing [@WebDreamer]. This is a literal "
        "literature reference list, verifiable on cited works.",
    ),

    # =======================================================================
    # Setup / construction claims (FlightQA, WebArena, SIMURA modules,
    # natural-language state definition)
    # =======================================================================
    setup_flightqa_dataset: (
        0.95,
        "FlightQA construction recipe (N=15 sequences, C=3 starting "
        "constraints, K=5 extension iterations -> 90 questions, "
        "constraints 3-8) is procedurally verifiable from the "
        "Appendix C prompts and the released dataset. Direct "
        "specification.",
    ),
    setup_flightqa_evaluation: (
        0.92,
        "FlightQA evaluation protocol (LLM-judged Groundedness + "
        "Relevance, correct = grounded AND relevant, gpt-4o judge, "
        "Appendix C prompt) is procedurally verifiable from the "
        "released evaluation script. The non-trivial design choice "
        "is the LLM-judge robustness; 0.92 reflects high confidence "
        "in the procedure as described, with a small discount for "
        "the documented LLM-judge hallucination-fooling failure "
        "mode in the BrowsingAgent + o1/o3-mini case.",
    ),
    setup_webarena_eval: (
        0.92,
        "WebArena evaluation setup (100-sample random subset, "
        "OpenHands-mediated environment, gpt-4o, 15-step budget, "
        "rewritten agent description) is procedurally specified. "
        "The 0.92 reflects high confidence with a small discount "
        "for the OpenHands-mediated deviation from the standard "
        "WebArena setup (which the paper explicitly flags as a "
        "comparability caveat).",
    ),
    setup_simura_modules: (
        0.93,
        "SIMURA's five-module decomposition (encoder, policy, "
        "world model, critic, actor) is the architectural "
        "specification stated in Section 3.4 + Figure 4. Direct "
        "definition. 0.93 (rather than 0.99) reflects that the "
        "specific decomposition is one of several possible factor"
        "izations of the optimal-agent decision rule -- the "
        "5-module split is sufficient but not necessarily unique.",
    ),
    setup_natural_language_state_def: (
        0.92,
        "Natural-language belief-state factorization (Eqs. 6-7) is "
        "the formal specification of how the encoder h and world "
        "model f produce token-by-token natural-language summaries. "
        "Direct definition; 0.92 reflects that 'each token "
        "conditions on prior tokens and the observation' is "
        "standard autoregressive factorization, but the choice to "
        "factor *belief states* (rather than raw observations) "
        "this way is the paper's specific design.",
    ),

    # =======================================================================
    # Conceptual claim (LLM next-token pretraining ~ world modeling)
    # =======================================================================
    claim_llm_pretraining_is_world_modeling: (
        0.78,
        "The framing 'LLM next-token pretraining $p(x_t \\mid "
        "x_{<t})$ is formally akin to world modeling' is a "
        "conceptual claim with empirical traction (RAP [@RAP], "
        "HuShu2023 [@HuShu2023]) but not a mathematical theorem. "
        "Pretrained LLMs do encode latent world knowledge; whether "
        "this knowledge is sufficient as a world-model substrate "
        "for arbitrary environments is exactly what SIMURA's "
        "empirical results test. 0.78 reflects plausibility "
        "without overclaiming.",
    ),

    # =======================================================================
    # Mathematical premise (ground-truth state/environment unavailable)
    # =======================================================================
    claim_ground_truth_unavailable: (
        0.95,
        "The fact that ground-truth state s and environment "
        "transition mu are typically unavailable to agents in "
        "real-world deployment (Mars landers, humanoid robots, "
        "web browsers, etc.) is a near-tautological observation "
        "about practical agent settings. 0.95 reflects that this "
        "is empirically obvious for the targeted application "
        "domains; counterexamples are confined to closed simulation "
        "environments (Go / Chess [@AlphaGo; @AlphaZero]).",
    ),

    # =======================================================================
    # Argument premises (atomic-action rollout limits)
    # =======================================================================
    claim_atomic_action_rollout_limits: (
        0.82,
        "Argument that concrete-action-space rollouts hinder "
        "transfer + accumulate error vs higher-level abstractions. "
        "The transfer-hindering and error-accumulation pathologies "
        "are documented in [@Dyna] and the broader hierarchical-RL "
        "literature. 0.82 reflects that the argument is widely "
        "accepted but not a measured fact in this paper -- the "
        "paper does not run an explicit ablation against "
        "concrete-action rollouts.",
    ),

    # =======================================================================
    # Per-task table claims (numerical transcriptions from Tables 1-3)
    # =======================================================================
    claim_flightqa_table1: (
        0.93,
        "Table 1 cells (BrowsingAgent / SIMURA-AR / SIMURA-WM / "
        "+ o1 / + o3-mini variants on FlightQA: Correct, Grounded, "
        "Relevant, Response, Browser Crash, Max Steps, Repeat, "
        "Action Err) are direct transcriptions from the paper. "
        "Statistical significance (** p<0.01) is reported in the "
        "table footnote. Sample size n=90.",
    ),
    claim_fanoutqa_table2: (
        0.93,
        "Table 2 cells (BrowsingAgent / SIMURA-AR / SIMURA-WM on "
        "FanOutQA first 100 dev examples: Acc., Acc. Strict, "
        "Response, Browser Crash, Max Steps, Repeat, Action Err, "
        "Parse Err) are direct transcriptions. Statistical "
        "significance (* p=0.011 narrative, p<0.05 footnote) "
        "reported.",
    ),
    claim_webarena_table3: (
        0.93,
        "Table 3 cells (BrowsingAgent 12.0 / SIMURA-AR 19.0 / "
        "SIMURA-WM 23.0 success rate on a 100-sample random "
        "subset of WebArena) are direct transcriptions. The "
        "non-comparability to prior WebArena work (different "
        "OpenHands-mediated env) is flagged explicitly in the "
        "paper.",
    ),

    # =======================================================================
    # Motivating example (ChatGPT-4o flight hallucination)
    # =======================================================================
    claim_chatgpt_4o_hallucination_example: (
        0.9,
        "Concrete hallucination example reported with date "
        "(Dec 17, 2024) and specific values (10:45am hallucinated, "
        "6:10am actual on Kayak.com Pittsburgh-Zurich). "
        "Verifiable in principle from screenshots; 0.9 reflects "
        "high confidence with a small discount for transcription "
        "risk on a single anecdotal example.",
    ),

    # =======================================================================
    # Limitations (paper's own self-reports)
    # =======================================================================
    claim_limit_runtime: (
        0.93,
        "Self-reported runtime overhead from the modular pipeline "
        "(7 LLM calls per step) and 20-sample world-model rollouts. "
        "The authors directly observe their own system's wall-"
        "clock latency; high prior reflects that this is verifiable "
        "by inspection of the released code.",
    ),
    claim_limit_tooling: (
        0.92,
        "Self-reported Captcha / anti-scraping blocking and 24% "
        "browser-crash rate on FanOutQA (Table 2), 1.1% on "
        "FlightQA (Table 1). Numerical browser-crash rates are "
        "verifiable from the tables; the 'Captcha-blocking' "
        "qualitative observation is a standard pathology of open-"
        "web agents.",
    ),
    claim_limit_modality: (
        0.95,
        "Self-reported text-only observation use (HTML accessibility "
        "tree). Verifiable from the released prompts (Appendix B). "
        "Trivially true given the documented architecture.",
    ),

    # =======================================================================
    # Abduction component prediction claims
    # =======================================================================
    claim_h_world_model_explains: (
        0.7,
        "Hypothesis prediction: world-model simulation-and-"
        "evaluation explains the 5-fact fingerprint (i)-(iii) "
        "cross-task gap, (iv) loop avoidance, (v) constraint-"
        "count consistency. The prediction is precise and follows "
        "from the planner architecture: explicit simulation + "
        "evaluation directly implements counterfactual loop "
        "detection and benefits scale with reasoning difficulty. "
        "0.7 reflects that the prediction is well-grounded in the "
        "design but is a claim about which mechanisms produce "
        "which fingerprints, not the underlying architectural "
        "definitions.",
    ),
    claim_alt_lm_capability_explains: (
        0.2,
        "Alternative prediction: trivial confounds (bigger LM / "
        "more compute / better prompt) explain the 5-fact "
        "fingerprint. CRUCIALLY, this is pi(Alt) = 'can the "
        "trivial alternative alone explain the OBSERVED 5-fact "
        "fingerprint?' -- not 'can it explain any single "
        "isolated fact?'. Trivial confounds CANNOT explain: "
        "(iv) the specific repetition reduction (44.4% -> 18.9%) "
        "-- more compute by itself does not implement loop "
        "detection; (v) the consistent gap across constraint "
        "counts (Fig. 9) -- a saturating LM-capability effect "
        "would NOT show consistent advantage at high difficulty; "
        "and (D) the o1/o3-mini collapse to 1.1%/3.3% on FlightQA "
        "(@claim_o1_o3mini_close_to_zero) -- a more capable LM "
        "should help if 'more LM capability' were the true "
        "mechanism. Trivial confounds explain at most fact (i) "
        "in isolation. pi(Alt) = 0.2 reflects that the "
        "alternative's explanatory power for the FULL fingerprint "
        "is poor.",
    ),
}


__all__ = ["PRIORS"]
