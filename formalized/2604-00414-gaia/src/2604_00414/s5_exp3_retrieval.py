"""Section 5.3: Modular Signals for Retrieval Control with Diagnosable Feedback (Experiment 3)"""

from gaia.lang import claim, setting, support, abduction, compare, induction

from .motivation import dc_framework_proposed, implicit_control_problem, separation_enables_attribution
from .s3_framework import sufficiency_signal_def

# ─── Settings ─────────────────────────────────────────────────────────────────

retrieval_setup = setting(
    "Retrieval sufficiency experiment: given a question and accumulated BM25 passages, the "
    "system decides whether to 'stop' (current passages are sufficient) or 'expand k' "
    "(retrieve more passages, with $k = 3 \\to 6 \\to 9$). Budget: 2 retrieval rounds. "
    "150 Natural Questions examples [@Kwiatkowski2019] over a 2000-passage BM25 corpus, "
    "split into $N=50$ each by difficulty: easy (gold passage present at round 0), medium "
    "(absent at round 0, retrieved within budget), hard (never retrieved within budget). "
    "Retrieval states (accumulated passages at $k=3,6,9$) are precomputed once and shared "
    "across all methods [@Sun2026].",
    title="Retrieval experiment setup",
)

signal_variants_def = setting(
    "Four retrieval control methods compared, all acting over the same action set and "
    "receiving the same state: (1) Prompt: direct LLM call to select stop/expand_k; "
    "(2) DC-LLM: LLM answerability judge outputting $\\hat{p}_{\\text{llm}} \\in [0,1]$, "
    "where $\\hat{p} = \\text{confidence}$ if answerable else $1 - \\text{confidence}$ "
    "(temperature 0.1); (3) DC-Dense: max cosine similarity between question and passage "
    "embeddings using all-MiniLM-L6-v2, normalized to $[0,1]$; (4) DC-Composite: "
    "$\\hat{p} = \\alpha \\hat{p}_{\\text{dense}} + (1-\\alpha)\\hat{p}_{\\text{llm}}$ with "
    "$\\alpha=0.4$. All DC variants use a fixed threshold controller: stop if "
    "$\\hat{p} \\geq \\tau = 0.8$, else expand. Parameters selected on a held-out validation "
    "set (N=30) [@Sun2026].",
    title="Retrieval signal variant definitions",
)

# ─── Key experimental results ─────────────────────────────────────────────────

medium_bucket_results = claim(
    "On medium-difficulty questions (gold passage absent at round 0 but retrievable within "
    "budget), the four methods achieve: Prompt 14% success (avg 0.08 retrieval rounds), "
    "DC-LLM 88% success (1.34 rounds), DC-Dense 90% success (1.66 rounds), DC-Composite "
    "94% success (1.62 rounds). The Prompt model achieves near-zero retrieval rounds, "
    "indicating it nearly always stops at round 0 [@Sun2026].",
    title="Medium bucket retrieval results: Prompt 14% vs DC-LLM 88% vs DC-Composite 94%",
    background=[retrieval_setup, signal_variants_def],
    metadata={
        "source_table": "artifacts/2604.00414.pdf, Table 5",
        "caption": "Table 5: Retrieval control results. Succ. = success rate; RR = avg retrieval rounds.",
    },
)

easy_bucket_results = claim(
    "On easy questions (gold passage present at round 0), all four methods achieve 100% "
    "success. However, they differ in retrieval efficiency: Prompt uses 0.10 rounds, "
    "DC-LLM uses 0.62 rounds, DC-Dense uses 1.12 rounds, DC-Composite uses 0.84 rounds. "
    "DC-Dense tends to over-expand on easy questions (treating retrieved passages as "
    "insufficient when they are sufficient) [@Sun2026].",
    title="Easy bucket: all methods 100% success but DC-Dense over-expands",
    background=[retrieval_setup, signal_variants_def],
)

hard_bucket_results = claim(
    "On hard questions (gold passage never retrieved within budget), all methods achieve "
    "~14–18% success: Prompt 14% (0.14 rounds), DC-LLM 18% (1.66 rounds), DC-Dense 18% "
    "(1.84 rounds), DC-Composite 18% (1.84 rounds). The DC variants expand more but cannot "
    "improve success because the gold passage is simply not in the 2000-passage corpus "
    "within budget. Hard failures are corpus gaps, not signal failures [@Sun2026].",
    title="Hard bucket: ~18% success for all methods — corpus gap limits performance",
    background=[retrieval_setup, signal_variants_def],
)

prompt_correct_assessment_wrong_action = claim(
    "In 28 of 44 medium-bucket Prompt failures (64%), the model's own free-text reason "
    "string explicitly states that the passages do not contain the answer, yet the model "
    "still outputs 'stop'. This demonstrates the core failure of implicit control: the "
    "internal assessment is correct, but it is not bound to the action selection — the "
    "failure is of mapping recognition to control, not of recognition itself [@Sun2026].",
    title="Prompt failure: correct internal assessment overridden by fused action selection (64%)",
    background=[retrieval_setup],
    metadata={
        "source_table": "artifacts/2604.00414.pdf, Table 13",
        "caption": "Table 13: Prompt failure modes on medium questions. Type 1 (64%): correct assessment, wrong action.",
    },
)

modularity_signal_isolation = claim(
    "The three DC variants (DC-LLM, DC-Dense, DC-Composite) share an identical fixed-"
    "threshold controller and differ only in how the sufficiency signal $\\hat{p}$ is "
    "constructed. DC-Dense behaves like a relevance signal and tends to over-expand; "
    "DC-LLM behaves like an answerability signal and is more selective; DC-Composite "
    "achieves the best medium-bucket performance at 94%. Because the controller is fixed, "
    "performance differences isolate the effect of signal construction, not action policy "
    "[@Sun2026].",
    title="DC variants isolate signal quality from control logic via shared controller",
    background=[signal_variants_def],
)

failure_attribution_retrieval = claim(
    "Failure attribution for DC-Composite: medium-bucket failures (3 total) are entirely "
    "cases where both DC-Dense and DC-LLM confidently support 'stop' incorrectly (both "
    "signals high). Hard-bucket failures (41 total) are 98% corpus gaps (gold passage "
    "never retrieved within budget) and 2% both-signals-high errors. This suggests different "
    "remedies: medium failures require a signal of a different type (e.g., passage "
    "highlighting, answer-type matching, token-level overlap); hard failures require a "
    "stronger retriever or corpus-exhaustion signal [@Sun2026].",
    title="DC-Composite failure attribution: medium=both-signals-wrong; hard=corpus-gap",
    background=[signal_variants_def],
    metadata={
        "source_table": "artifacts/2604.00414.pdf, Table 12",
        "caption": "Table 12: Failure attribution for DC-Composite on the test set.",
    },
)

threshold_robustness = claim(
    "A robustness sweep over DC-Composite parameters $\\alpha \\in \\{0.2, \\ldots, 0.6\\}$ "
    "and $\\tau \\in \\{0.5, \\ldots, 0.9\\}$ on the held-out test set shows: easy-bucket "
    "success is 100% throughout. Medium-bucket success ranges from 78% ($\\tau=0.5$) to 92% "
    "($\\tau=0.9$). The selected operating point ($\\alpha=0.4$, $\\tau=0.8$, medium 88%) "
    "is conservative — higher $\\tau$ or $\\alpha$ further improves medium-bucket success "
    "at the cost of more retrieval rounds on easy questions. Parameters were selected on a "
    "separate validation set, confirming results are not cherry-picked [@Sun2026].",
    title="DC-Composite threshold sweep: medium success 78-92%, conservative setting chosen",
    background=[signal_variants_def],
    metadata={
        "source_table": "artifacts/2604.00414.pdf, Table 11",
        "caption": "Table 11: Offline threshold sweep for DC-Composite.",
    },
)

# ─── Prediction claims for abduction ─────────────────────────────────────────

dc_predicts_medium_expand = claim(
    "The decision-centric approach predicts high medium-bucket success because the explicit "
    "sufficiency signal $\\hat{p}$ is computed independently of the action, allowing the "
    "controller to correctly identify $\\hat{p} < \\tau$ (insufficient) and select 'expand' "
    "even when the model internally assesses insufficiency but would fuse that assessment "
    "with a 'stop' action in a prompt-based system [@Sun2026].",
    title="DC predicts medium-bucket success via externalized sufficiency signal",
    background=[sufficiency_signal_def],
)

prompt_predicts_medium_failure = claim(
    "Prompt-based control predicts medium-bucket failure because the sufficiency assessment "
    "and action selection are fused in a single call: the model's internal recognition that "
    "passages are insufficient cannot reliably propagate to a 'expand' action, producing the "
    "observed 64% rate of correct-assessment-wrong-action failures [@Sun2026].",
    title="Prompt predicts medium failure via assessment-action fusion",
    background=[implicit_control_problem],
)

# ─── Abduction: DC-LLM vs Prompt on medium bucket ────────────────────────────

s_dc_medium = support(
    [dc_predicts_medium_expand],
    medium_bucket_results,
    reason=(
        "DC-LLM's prediction of high medium success (@dc_predicts_medium_expand) is borne out "
        "by the 88% success rate (vs Prompt's 14%). The 74 percentage-point improvement with "
        "identical LLM, passages, and action set — only differing in whether sufficiency is "
        "externalized — directly supports the DC prediction [@Sun2026]."
    ),
    prior=0.92,
)

s_prompt_medium = support(
    [prompt_predicts_medium_failure],
    medium_bucket_results,
    reason=(
        "The prompt failure prediction (@prompt_predicts_medium_failure) is consistent with "
        "Prompt's 14% medium success and the 64% correct-assessment-wrong-action rate. "
        "However, this prediction cannot explain DC-LLM's 88% success with the same LLM, "
        "since the only structural difference is signal externalization [@Sun2026]."
    ),
    prior=0.3,
)

comp_medium = compare(
    dc_predicts_medium_expand,
    prompt_predicts_medium_failure,
    medium_bucket_results,
    reason=(
        "DC-LLM's prediction (@dc_predicts_medium_expand) matches the 88% DC-LLM medium "
        "success exactly. The prompt prediction (@prompt_predicts_medium_failure) explains "
        "only Prompt's 14%. The 74pp gap with identical LLM, corpus, and action set provides "
        "strong evidence that signal externalization — not model capability — drives the "
        "difference [@Sun2026]."
    ),
    prior=0.92,
)

abduction_retrieval = abduction(
    s_dc_medium,
    s_prompt_medium,
    comp_medium,
    reason=(
        "Both DC-LLM and Prompt use the same LLM and act over the same action set. The "
        "abduction tests whether the externalization of the sufficiency signal (DC-LLM) or "
        "its absence (Prompt) better explains the medium-bucket performance gap "
        "[@Sun2026]."
    ),
)

# ─── Induction: modularity benefit across tasks ───────────────────────────────

dc_reduces_wasted_calendar = claim(
    "In the calendar scheduling task, the DC approach reduces wasted executions to 0 in "
    "most scenarios compared to Prompt-Clarify's average 1.35–2.90 wasted executions at "
    "$k=1$ to $k=4$, by enforcing explicit sufficiency-based gating before execution "
    "[@Sun2026].",
    title="DC reduces wasted actions in calendar scheduling",
)

dc_improves_graph_success = claim(
    "In the graph disambiguation task, the DC approach achieves 100% success across all "
    "five scenarios including the correlated-update scenario S5 where prompt-based approaches "
    "reach only 35%, by maintaining explicit belief state that captures passive candidate "
    "elimination [@Sun2026].",
    title="DC improves success in graph disambiguation via explicit belief state",
)

dc_improves_retrieval_medium = claim(
    "In the retrieval control task, DC-LLM achieves 88% medium-bucket success versus "
    "Prompt's 14% by externalizing the sufficiency assessment as a scalar signal that "
    "is bound to the action selection policy rather than fused inside generation [@Sun2026].",
    title="DC improves retrieval success by externalizing sufficiency signal",
)

# Law: explicit decision layer improves control across tasks
explicit_control_law = claim(
    "Making the decision layer explicit — separating decision-relevant signals from the "
    "policy that maps them to actions — improves LLM system control reliability, "
    "interpretability, and ease of improvement across diverse task types and signal "
    "modalities [@Sun2026].",
    title="Explicit decision layer improves control across diverse task types",
)

s_ind_calendar = support(
    [explicit_control_law],
    dc_reduces_wasted_calendar,
    reason=(
        "The explicit decision layer law (@explicit_control_law) predicts that externalizing "
        "the sufficiency signal and policy will reduce wasted actions in calendar scheduling. "
        "The DC calendar policy achieves this by gating execution on $\\hat{p}_{\\text{suff}} "
        "= 1.0$ and enforcing no-blind-retry, confirming the law's prediction for this task "
        "[@Sun2026]."
    ),
    prior=0.9,
)

s_ind_graph = support(
    [explicit_control_law],
    dc_improves_graph_success,
    reason=(
        "The explicit decision layer law (@explicit_control_law) predicts that maintaining "
        "explicit belief state enables richer sequential control. Graph disambiguation's "
        "100% DC success (vs 35% Prompt in S5) confirms the prediction for multi-signal "
        "settings with correlated belief updates [@Sun2026]."
    ),
    prior=0.9,
)

s_ind_retrieval = support(
    [explicit_control_law],
    dc_improves_retrieval_medium,
    reason=(
        "The explicit decision layer law (@explicit_control_law) predicts improvement from "
        "externalizing sufficiency. The 74pp gap in medium bucket (DC-LLM 88% vs Prompt 14%) "
        "with identical LLM confirms the law's prediction for retrieval control under noisy "
        "signals [@Sun2026]."
    ),
    prior=0.9,
)

ind_calendar_graph = induction(
    s_ind_calendar,
    s_ind_graph,
    law=explicit_control_law,
    reason=(
        "Calendar scheduling and graph disambiguation are independently designed tasks with "
        "different action spaces, signal types, and decision structures. They constitute "
        "independent observations supporting the explicit control law."
    ),
)

ind_all_three = induction(
    ind_calendar_graph,
    s_ind_retrieval,
    law=explicit_control_law,
    reason=(
        "Retrieval control is a third independently designed task with a different domain "
        "(information retrieval vs structured task completion), different signal type (BM25 "
        "passages + embeddings), and noisy evidence. Together with the calendar and graph "
        "tasks, the three experiments provide independent converging support for the explicit "
        "control law [@Sun2026]."
    ),
)
