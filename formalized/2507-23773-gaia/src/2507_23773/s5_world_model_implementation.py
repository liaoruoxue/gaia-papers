"""Section 4 (Implementation for Web Browsing) and Section 4 baselines:
the concrete LLM-based instantiation of SIMURA's encoder/policy/world
model/critic/actor for web browsing, plus the autoregressive-planning
baseline that holds all other modules fixed.

Source: Deng et al. 2025 [@Deng2025SIMURA], Section 4 narrative + Fig. 5
+ Appendix A/B prompts.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Web-browsing observation/action setup
# ---------------------------------------------------------------------------

setup_web_browser_environment = setting(
    "**Web-browsing environment.** Web browsing is selected as the "
    "first concrete environment for SIMURA because of its practical "
    "value (gathering information, booking travels, submitting "
    "applications) and technical challenge (immense complexity, "
    "long-horizon nature, partial observability, multimodality "
    "[@WebArena; @WebVoyager]). Most existing web-using products "
    "[@ChatGPTSearch; @Perplexity] use specialized tools "
    "(search engines, data APIs) and capture only a subset of "
    "browser capabilities (reading) -- not full functionality "
    "(content not exposed to search engines or predefined "
    "flight/hotel APIs).",
    title="Setup: web-browsing environment -- complex, long-horizon, partially observable, multimodal",
)

setup_observation_format = setting(
    "**Observation format: HTML accessibility tree.** At each step "
    "$t$, the agent receives the observation $o_t$ as the **HTML-"
    "based accessibility tree** visible in the browser viewport. "
    "An example accessibility-tree observation (Google Flights) is "
    "given in Appendix A. The accessibility tree exposes URL, "
    "scroll position, viewport dimensions, the structural element "
    "hierarchy, interactive components (links, buttons, form "
    "fields), and accessibility metadata (role, focus, aria "
    "labels).",
    title="Setup: observation o_t = HTML accessibility tree of the visible viewport (Appendix A)",
    metadata={
        "figure": "artifacts/2507.23773.pdf, Appendix A",
        "caption": "Appendix A: example accessibility-tree observation for Google Flights.",
    },
)

setup_action_space = setting(
    "**Concrete action space.** The agent's concrete action space $A$ "
    "consists of 13 atomic browser actions (16 in the action-"
    "clustering prompt for WebArena), including `noop`, "
    "`send_msg_to_user`, `scroll`, `fill`, `select_option`, `click`, "
    "`dblclick`, `hover`, `press`, `focus`, `clear`, "
    "`drag_and_drop`, `upload_file` (and `go_back`, `go_forward`, "
    "`goto` for clustering). Only one action can be issued per "
    "step. Element identifiers (bid) are referenced as quoted "
    "strings.",
    title="Setup: concrete action space A = 13 atomic browser actions (Appendix B)",
)

# ---------------------------------------------------------------------------
# LLM-substrate instantiation of each module
# ---------------------------------------------------------------------------

setup_llm_encoder_actor = setting(
    "**Encoder and actor implementation.** The encoder $h$ summarizes "
    "the accessibility tree as a natural-language description of all "
    "elements (dialogs, progress indicators, errors, interactive "
    "elements with values, task-relevant facts), wrapped in "
    "`<state>...</state>` tags (Appendix B). The actor $\\alpha$ "
    "takes the memory, the *observation text* $o_t$, the current "
    "state, and the chosen intent and produces a single action API "
    "call wrapped in `<action>...</action>` tags. The observation "
    "text is included in the actor prompt to ensure action grounding "
    "to live page elements.",
    title="Setup: encoder h and actor alpha implemented as LLM prompts (Appendix B prompts)",
)

setup_llm_policy = setting(
    "**Policy implementation.** The policy $\\tilde\\pi$ takes the "
    "memory and current state and returns one *intent* per call -- a "
    "natural-language description of the next action, wrapped in "
    "`<intent>...</intent>` tags (with internal `<think>...</think>` "
    "reasoning). Prompt instructions emphasize creativity, novelty, "
    "no element-ID grounding (since IDs may change), and avoidance "
    "of multi-step combinations. Sampling is repeated $M = 20$ times "
    "to obtain candidate actions; an *action-clustering* LLM call "
    "(Appendix B) groups semantically equivalent intents into "
    "distinct clusters.",
    title="Setup: policy pi-tilde implemented as LLM intent generator with M=20 samples + action clustering",
)

setup_llm_world_model = setting(
    "**World-model implementation.** The world model $f$ takes "
    "memory, current state, memory update, and action intent, and "
    "produces the predicted next state wrapped in `<next_state>...</"
    "next_state>` tags. The prompt explicitly instructs the LLM to "
    "*infer* the result of the action even when execution may not "
    "be successful, noting any new dialogs/progress indicators/error "
    "messages, and to be as comprehensive and detailed as possible. "
    "This is the key module that makes simulation-based planning "
    "concrete in SIMURA.",
    title="Setup: world model f implemented as LLM next-state predictor (Appendix B prompt)",
)

setup_llm_critic = setting(
    "**Critic implementation.** The critic $v$ evaluates the terminal "
    "belief state $\\hat s_{T'}$ by prompting the LLM to output a "
    "*categorical* judgment ('success' or 'failure'), an "
    "'on_the_right_track' yes/no flag, and a `<think>...</think>` "
    "rationale. Categorical judgments are converted to numerical "
    "scores (e.g., 'success' = 1) and the call is repeated $N = 20$ "
    "times to produce fine-grained terminal-state values. Following "
    "[@TreeSearchKoh2024; @WebDreamer], the planning horizon is set "
    "to $T = t + 1$.",
    title="Setup: critic v implemented as categorical LLM evaluator repeated N=20 times; horizon T=t+1",
)

setup_memory_update = setting(
    "**Memory and selective belief construction.** SIMURA maintains a "
    "*selective memory* $\\{m(\\tilde s_k, a'^*_k)\\}_{k=1}^{t-1}$ "
    "of past belief summaries and chosen simulated actions. The "
    "estimated world state used for planning is "
    "$\\hat s_t = [m(\\tilde s_1, a'^*_1), \\ldots, m(\\tilde "
    "s_{t-1}, a'^*_{t-1}), \\tilde s_t]$. After the planner selects "
    "$a'^*_t$, the memory is updated with $m(\\tilde s_t, a'^*_t)$ "
    "via a dedicated *Memory Update* LLM prompt that summarizes "
    "webpage changes, infers progress, and revises beliefs when the "
    "current state contradicts prior history.",
    title="Setup: SIMURA's selective memory + memory-update prompt (Appendix B)",
)

# ---------------------------------------------------------------------------
# Autoregressive-planning baseline (within-architecture comparator)
# ---------------------------------------------------------------------------

setup_autoregressive_planning_baseline = setting(
    "**Within-architecture autoregressive-planning baseline.** Holding "
    "the encoder, actor, memory, and prompts fixed at SIMURA's "
    "implementation, the *autoregressive-planning* variant simplifies "
    "the planner to commit to the **first sample** from the policy: "
    "$a'^*_t = \\arg\\max_{a'_t} p_{\\tilde\\pi}(a'_t \\mid \\hat "
    "s_t)$. No world-model rollouts and no critic evaluation occur. "
    "This is the matched baseline used to isolate the contribution "
    "of world-model-based planning from the other architectural "
    "components (structured natural-language pipeline, selective "
    "memory).",
    title="Setup: autoregressive-planning baseline = SIMURA pipeline minus world model + critic",
)

setup_browsingagent_baseline = setting(
    "**OpenHands BrowsingAgent baseline.** The OpenHands BrowsingAgent "
    "[@OpenHands] is a *representative open-web autoregressive agent*: "
    "it generates a chain-of-thought before each action and selects "
    "an atomic browser action without explicit world-model "
    "simulation. It is the cross-architecture baseline used to "
    "compare SIMURA's full pipeline (structured pipeline + world-"
    "model planning) against typical open-source web-browsing "
    "agents.",
    title="Setup: OpenHands BrowsingAgent baseline -- cross-architecture autoregressive comparator",
)

# ---------------------------------------------------------------------------
# Implementation summary claim
# ---------------------------------------------------------------------------

claim_prototype_summary = claim(
    "**Prototype summary.** The web-browsing prototype "
    "(REASONERAGENT-WEB [@ReasonerAgent]) fully instantiates SIMURA "
    "with LLM modules (Encoder, Policy, World Model, Critic, "
    "Memory-Update, Actor, Action-Clustering -- 7 prompted LLM "
    "calls; Appendix B) communicating via natural-language belief "
    "states and natural-language simulated actions. It runs over "
    "BrowserGym [@BrowserGym] (open-source browser sandbox) with "
    "30-action budget per task and standard failure modes (response, "
    "max-steps, repeat-action $\\geq 3$, action-error $> 3$). The "
    "implementation demonstrates that SIMURA's modular abstract "
    "design (@setup_simura_modules) can be realized with off-the-"
    "shelf LLMs.",
    title="Prototype: full LLM-based instantiation of SIMURA -- 7 prompted LLM modules over BrowserGym",
)

claim_natural_language_actions_in_prototype = claim(
    "**Natural-language simulated actions, concrete grounded actions.** "
    "In the prototype, simulated actions $a'_t$ are natural-language "
    "phrases (e.g., \"Select the 'Cheapest' tab\"), while the "
    "concrete action $a_t$ is the corresponding browser API call "
    "(e.g., `click('128')`). The actor $\\alpha$ grounds the "
    "natural-language intent to a specific element ID by inspecting "
    "$o_t$, ensuring that planning over abstract intents translates "
    "into a valid live-DOM action.",
    title="Prototype: simulated action a' = NL phrase; concrete action a = browser API call grounded by actor",
    metadata={
        "figure": "artifacts/2507.23773.pdf, Fig. 5",
        "caption": "Fig. 5: LLM-based implementation of SIMURA for web tasks.",
    },
)

__all__ = [
    "setup_web_browser_environment",
    "setup_observation_format",
    "setup_action_space",
    "setup_llm_encoder_actor",
    "setup_llm_policy",
    "setup_llm_world_model",
    "setup_llm_critic",
    "setup_memory_update",
    "setup_autoregressive_planning_baseline",
    "setup_browsingagent_baseline",
    "claim_prototype_summary",
    "claim_natural_language_actions_in_prototype",
]
