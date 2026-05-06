"""Section 6.1: Experimental setup -- task, baselines, metrics,
implementation, and the alignment-verification check (Appendix B)
that justifies applying Theorem 5.1 to this domain.

Source: Rodriguez 2026 [@Rodriguez2026PressureField], Section 6.1 +
Appendix A + Appendix B.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# 6.1.1 Task: meeting-room scheduling
# ---------------------------------------------------------------------------

setup_task_meeting_scheduling = setting(
    "**Task: meeting-room scheduling.** Assign $N$ meetings to $R$ "
    "rooms over $D$ days to minimize gaps (unscheduled time), "
    "overlaps (attendee double-bookings), and to maximize "
    "utilization balance. Each schedule spans 5 days with 30-minute "
    "time slots (8am-4pm). Regions are 2-hour time blocks (4 blocks "
    "per day x 5 days = **20 regions per schedule**). A problem is "
    "*solved* when all meetings are scheduled with zero attendee "
    "overlaps within 50 ticks.",
    title="Setup: meeting-room scheduling (5 days, 30-min slots, 20 regions = 2-hour blocks; solved = all meetings + zero overlaps within 50 ticks)",
)

setup_difficulty_table = setting(
    "**Table 2: Problem difficulty configurations.**\n\n"
    "| Difficulty | Rooms | Meetings | Pre-scheduled |\n"
    "|---|---|---|---|\n"
    "| Easy | 3 | 20 | 70% |\n"
    "| Medium | 5 | 40 | 50% |\n"
    "| Hard | 5 | 60 | 30% |\n\n"
    "Pre-scheduled percentage indicates meetings already placed; "
    "remaining meetings must be scheduled by agents.",
    title="Setup: Table 2 difficulty tiers (easy / medium / hard with rooms x meetings x %pre-scheduled)",
    metadata={
        "figure": "artifacts/2601.08129.pdf, Table 2 (page 23)",
    },
)

setup_meeting_pressure_function = setting(
    "**Pressure function for meeting scheduling.** The total "
    "pressure is "
    "$P = \\text{gaps} \\cdot 1.0 + \\text{overlaps} \\cdot 2.0 + "
    "\\text{util\\_var} \\cdot 0.5 + \\text{unsched} \\cdot 1.5$, "
    "where: *gaps* measures empty slots as a fraction; *overlaps* "
    "counts attendee double-bookings; *util_var* measures room-"
    "utilization variance; *unsched* is the fraction of unscheduled "
    "meetings. The first three components are evaluated per-region; "
    "the fourth (unsched) is added to total pressure only.",
    title="Setup: pressure function P = 1.0*gaps + 2.0*overlaps + 0.5*util_var + 1.5*unsched",
)

# ---------------------------------------------------------------------------
# Alignment verification (Appendix B) -- the per-region pressure is separable
# ---------------------------------------------------------------------------

claim_alignment_separability = claim(
    "**Per-region pressure is separable in this domain "
    "(Appendix B.1).** The per-region components depend only on the "
    "region's own content: (i) *gap_ratio* -- fraction of empty "
    "slots in the time block, strictly local; (ii) *overlap_count* "
    "-- attendee double-bookings counted within this block only "
    "(not across blocks); (iii) *utilization_variance* -- variance "
    "in room utilization within this time block, strictly local. "
    "The *unscheduled count* is added to **total** pressure only, "
    "not to per-region pressure -- a deliberate design choice that "
    "ensures separability.",
    title="Result: per-region pressure is separable (Appendix B.1) -- the unsched component is added to total pressure only",
)

claim_alignment_attendee_constraint_local = claim(
    "**Why attendee constraints do not create cross-region "
    "coupling.** While the same attendee may have meetings in "
    "multiple time blocks, the overlap sensor counts overlaps "
    "**within each block independently**. Moving a meeting from "
    "region $i$ to region $j$ may create or resolve overlaps in "
    "region $j$, but this is a *local* effect on $j$'s pressure -- "
    "not a coupling effect where modifying region $i$ affects "
    "region $j$ through some indirect mechanism.",
    title="Result: attendee constraints are local (overlap sensor counts within-block overlaps only)",
)

claim_alignment_empirical_zero_eps = claim(
    "**Empirical alignment validation: $\\epsilon = 0$ on this "
    "domain (Appendix B.3).** Analysis of 270 pressure-field trials "
    "yielded 9,873 total tick-to-tick transitions. Of these, 1,160 "
    "(11.7%) showed pressure improvement, 0 (0.0%) showed pressure "
    "degradation, and 8,713 (88.3%) showed no change. **The "
    "complete absence of pressure degradation is consistent with "
    "separable pressure** (each accepted patch reduces local "
    "pressure, which directly reduces global pressure with no "
    "adverse effect on other regions). Mean improvement magnitude "
    "is 2.67 pressure units; minimum observed reduction is 1.0 "
    "(confirming $\\delta_{\\min} \\ge 1 > 0$). With $\\epsilon = 0$, "
    "the convergence theorem's premise $\\delta_{\\min} > "
    "(n-1)\\epsilon$ reduces to $\\delta_{\\min} > 0$, which is "
    "satisfied.",
    title="Result: 9,873 transitions / 270 trials show 0 pressure-degradation events, consistent with eps = 0 separable pressure (Appendix B.3)",
)

# ---------------------------------------------------------------------------
# 6.1.2 Baselines (5 strategies)
# ---------------------------------------------------------------------------

setup_pressure_field_strategy = setting(
    "**Pressure-field strategy (ours).** Full system with decay "
    "(fitness half-life 5 s), inhibition (2 s cooldown), greedy "
    "region selection (highest-pressure region per tick), and "
    "parallel validation. Includes band escalation "
    "(Exploitation -> Balanced -> Exploration) and model escalation "
    "(qwen2.5:0.5b -> 1.5b -> 3b).",
    title="Setup: pressure-field strategy (decay + inhibition + parallel validation + band/model escalation)",
)

setup_conversation_strategy = setting(
    "**Conversation strategy (AutoGen-style baseline) [@AutoGen].** "
    "Multi-agent dialogue with three roles: a *Coordinator* selects "
    "which region to address; a *Proposer* suggests schedule "
    "changes; a *Validator* critiques proposals. Each tick: "
    "Coordinator identifies a high-pressure region (1 LLM call), "
    "then Proposer and Validator exchange up to 5 dialogue turns "
    "(2 calls per turn); if Validator approves, the patch is "
    "applied. This yields **4-12 LLM calls per tick for a single "
    "region**, compared to pressure-field's $K$ parallel calls "
    "across $K$ regions.",
    title="Setup: conversation strategy (AutoGen-style 3-role dialogue: Coordinator / Proposer / Validator; 4-12 LLM calls per tick)",
)

setup_hierarchical_strategy = setting(
    "**Hierarchical strategy.** A single agent selects the highest-"
    "pressure time block each tick, proposes one schedule change, "
    "and validates before applying (only accepts pressure-reducing "
    "patches). Uses identical prompts to pressure-field; the "
    "differences are: (i) greedy region selection always targets "
    "the hardest region; (ii) sequential execution processes one "
    "region per tick. Represents centralized, quality-gated control.",
    title="Setup: hierarchical strategy (single agent, highest-pressure region, one patch per tick, validated)",
)

setup_sequential_random_strategies = setting(
    "**Sequential and Random strategies (no-coordination "
    "baselines).** *Sequential* iterates through time blocks in "
    "fixed (round-robin) order, proposing schedule changes one "
    "region at a time without parallelism, pressure guidance, or "
    "patch validation. *Random* selects regions uniformly at "
    "random, also without validation. Both apply any syntactically "
    "valid patch regardless of quality impact.",
    title="Setup: sequential / random strategies (no parallelism, no pressure guidance, no validation; baselines for 'is coordination doing anything?')",
)

setup_fairness_guarantees = setting(
    "**Baseline fairness guarantees (Appendix A.4).** All "
    "strategies use identical model chains "
    "(qwen2.5:0.5b -> 1.5b -> 3b) with the same escalation "
    "triggers; identical schedule state, room capacities, meeting "
    "requirements, and constraint information; identical 50-tick "
    "limits per problem; identical response parsing and schedule-"
    "extraction logic. The conversation baseline gets up to 5 "
    "dialogue turns per region, *more* opportunity for refinement "
    "than pressure-field's single-shot proposals. The only "
    "intentional differences are the coordination mechanisms "
    "themselves (region selection, proposal generation, validation).",
    title="Setup: baseline fairness (same model chain / same problems / same tick budget; only coordination mechanism varies)",
)

setup_seeding_protocol = setting(
    "**Deterministic problem seeding (Appendix A.5).** Each trial "
    "generates its problem from $\\text{seed} = \\text{trial} "
    "\\times 1000 + \\text{agent\\_count}$. Trial 5 with 2 agents "
    "yields seed 5002, producing identical meeting configurations "
    "whether evaluated with pressure-field, conversation, or "
    "hierarchical coordination. Each strategy faces the *same* "
    "scheduling challenge within a trial.",
    title="Setup: deterministic seeding (seed = trial*1000 + agent_count) -- all strategies face identical problems",
)

# ---------------------------------------------------------------------------
# 6.1.3 Metrics
# ---------------------------------------------------------------------------

setup_metrics = setting(
    "**Metrics.** (i) **Solve rate**: percentage of schedules "
    "reaching all meetings placed with zero overlaps within 50 "
    "ticks. (ii) **Ticks to solve**: convergence speed for solved "
    "cases. (iii) **Final pressure**: remaining gaps + overlaps + "
    "unscheduled for unsolved cases. (iv) **Token efficiency**: "
    "total prompt and completion tokens per trial and per "
    "successful solve.",
    title="Setup: metrics (solve rate / ticks-to-solve / final pressure / tokens per trial and per solve)",
)

# ---------------------------------------------------------------------------
# 6.1.4 Implementation: hardware, software, model-choice rationale
# ---------------------------------------------------------------------------

setup_implementation = setting(
    "**Implementation (Appendix A.1-A.3).** Hardware: NVIDIA RTX "
    "4070 8 GB Graphics Processing Unit (GPU), AMD Ryzen 9 7940HS, "
    "64 GB RAM. Software: Rust 1.75+ (edition 2024) implementation "
    "with Ollama (local LLM inference server). Models: "
    "qwen2.5:0.5b, 1.5b, 3b. Trials: **30 per configuration**, 270 "
    "per strategy across $\\{$easy, medium, hard$\\} \\times \\{1, "
    "2, 4\\}$ agents.",
    title="Setup: implementation (RTX 4070 / AMD Ryzen 9 / 64 GB RAM / Rust + Ollama / qwen2.5 0.5b-1.5b-3b / 30 trials per config)",
)

setup_band_escalation = setting(
    "**Band escalation mechanism.** When pressure velocity (rate "
    "of improvement) drops to zero for 7 consecutive ticks, "
    "sampling parameters escalate Exploitation $(T \\in [0.15, "
    "0.35], p \\in [0.80, 0.90])$ -> Balanced $(T \\in [0.35, "
    "0.55], p \\in [0.85, 0.95])$ -> Exploration $(T \\in [0.55, "
    "0.85], p \\in [0.90, 0.98])$, randomly sampling $T$ and top-"
    "$p$ within range for diversity.",
    title="Setup: band escalation (Exploitation -> Balanced -> Exploration when velocity stalls for 7 ticks)",
)

setup_model_escalation = setting(
    "**Model escalation mechanism.** After exhausting all bands "
    "with zero progress (21 ticks total), the system escalates "
    "through the model chain qwen2.5:0.5b -> 1.5b -> 3b, resetting "
    "to the Exploitation band on each upgrade. Each model upgrade "
    "gives the more capable model an opportunity to exploit "
    "solutions invisible to its predecessor before resorting to "
    "exploration.",
    title="Setup: model escalation (0.5b -> 1.5b -> 3b after 21 ticks at high pressure; resets band on upgrade)",
)

claim_model_choice_rationale = claim(
    "**Model-choice rationale: small models strengthen the "
    "thesis.** The experiments deliberately use small (0.5b-3b "
    "parameter) models rather than frontier models. The reasoning: "
    "if the coordination mechanism extracts effective performance "
    "from weak models, the mechanism itself is valuable -- "
    "*independent* of model capability. Using identical model "
    "chains across all strategies isolates coordination effects "
    "from model effects. The paper hypothesizes that frontier "
    "models (e.g., GPT-4, Claude) would raise absolute solve rates "
    "across all strategies while preserving relative rankings.",
    title="Setup: small-model choice (0.5b-3b) deliberately strengthens the thesis (coordination mechanism orthogonal to model capability)",
)

# ---------------------------------------------------------------------------
# 6.1.4 negative pheromones (mechanism)
# ---------------------------------------------------------------------------

setup_negative_pheromones = setting(
    "**Negative pheromones mechanism.** In addition to *positive* "
    "pheromones (successful patches stored as few-shot examples), "
    "the system implements *negative pheromones*: tracking "
    "rejected patches that worsened pressure. Rejection history is "
    "injected into subsequent prompts via *positive* language "
    "('TIP: Schedule meetings in Room A (improves by X)') rather "
    "than 'AVOID' framing that small (1.5b parameter) models "
    "struggle to follow. Negative pheromones decay at the same rate "
    "as positive examples (weight $\\times 0.95$ per tick, evicted "
    "below 0.1); up to 3 recent rejections per region appear in "
    "prompts as 'Hints for better scheduling'.",
    title="Setup: negative pheromones (rejected-patch hints, positive-language reframing, decay-matched 0.95/tick)",
)

__all__ = [
    "setup_task_meeting_scheduling",
    "setup_difficulty_table",
    "setup_meeting_pressure_function",
    "claim_alignment_separability",
    "claim_alignment_attendee_constraint_local",
    "claim_alignment_empirical_zero_eps",
    "setup_pressure_field_strategy",
    "setup_conversation_strategy",
    "setup_hierarchical_strategy",
    "setup_sequential_random_strategies",
    "setup_fairness_guarantees",
    "setup_seeding_protocol",
    "setup_metrics",
    "setup_implementation",
    "setup_band_escalation",
    "setup_model_escalation",
    "claim_model_choice_rationale",
    "setup_negative_pheromones",
]
