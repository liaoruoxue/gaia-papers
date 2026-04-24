"""Section 4: Experimental Validation on Towers of Hanoi"""

from gaia.lang import claim, setting, support, deduction, abduction, induction

from .motivation import (
    setting_hanoi_benchmark,
    setting_mdap_framework,
    llm_degrade_hanoi,
    single_agent_infeasible,
)
from .s3_framework import (
    setting_mad_definition,
    setting_voting_formula,
    setting_voting_algorithm,
    setting_red_flag_types,
    mad_reduces_context,
    mad_enables_error_correction,
    voting_pfull_high_mad,
    cost_scales_log_linearly,
    red_flag_reduces_correlation,
)

# --- Section 4.1: Experimental Setup ---

setting_experiment_setup = setting(
    "Experimental setup: MAKER is applied to the 20-disk Towers of Hanoi problem, "
    "which requires 2^20 - 1 = 1,048,575 steps (~1 million steps). Each agent receives "
    "the current disk configuration (state) and the previous move, and must output the "
    "next move and the resulting state. The overall strategy (a standard iterative "
    "algorithm for even numbers of disks) is provided in each agent's prompt. "
    "Agents are given gpt-4.1-mini at temperature 0.1 as the primary model for the "
    "full million-step run. The prompt format requires: "
    "move = [disk_id, from_peg, to_peg] and next_state = [[...], [...], [...]].",
    title="MAKER experimental setup: 20-disk Towers of Hanoi",
)

# --- Section 4.2: Per-step Error Rate Estimation ---

error_rate_mini_low = claim(
    "The empirical per-step error rate (1-p) of gpt-4.1-mini at temperature tau=0.1 "
    "on the 20-disk Towers of Hanoi task is approximately 0.00223 (0.223%), estimated "
    "from 10,000 random single-step samples. The mean number of output tokens per step "
    "is 538 tokens. This gives a k_min = 3 votes required and estimated total cost of "
    "$3.5K for the full million-step task at target reliability t=0.95.",
    title="gpt-4.1-mini (tau=0.1) per-step error rate and cost estimate",
    metadata={"figure": "artifacts/2511.09030.pdf, Figure 6b"},
)

error_rate_nano = claim(
    "The empirical per-step error rate (1-p) of gpt-4.1-nano on the 20-disk Towers of "
    "Hanoi task is approximately 0.3571 (35.71%). The estimated total cost at t=0.95 is "
    "$41.9K, with k_min=29 votes required — making it the most expensive proprietary model "
    "despite having the cheapest per-token cost ($0.484/MTok).",
    title="gpt-4.1-nano high error rate makes it costliest despite cheap tokens",
    metadata={"figure": "artifacts/2511.09030.pdf, Figure 6b"},
)

error_rate_oss_20b = claim(
    "The empirical per-step error rate (1-p) of the open-source gpt-oss-20B model "
    "on the 20-disk Towers of Hanoi task is approximately 0.0358 (3.58%), with "
    "k_min=6 votes and estimated total cost of $1.7K at t=0.95, making it "
    "the most cost-effective open-source choice.",
    title="gpt-oss-20B: best open-source choice at $1.7K estimated cost",
    metadata={"figure": "artifacts/2511.09030.pdf, Figure 6b"},
)

error_rate_stable = claim(
    "The per-step error rates of LLMs on the Towers of Hanoi task do not notably "
    "decrease as the number of disks (i.e., as the log of the solution length) increases "
    "from 10 to 20 disks. This stability suggests the per-step error rate p is "
    "approximately independent of task length, an encouraging sign for scalability.",
    title="Per-step error rates stable with increasing task length",
    metadata={"figure": "artifacts/2511.09030.pdf, Figure 6a"},
)

model_cost_tradeoff = claim(
    "The cost-error-rate tradeoff across models shows that cheapest-per-token is not "
    "cheapest overall: gpt-4.1-nano ($0.484/MTok) has error rate 35.71% and costs "
    "$41.9K for the full task; gpt-4.1-mini ($1.6/MTok) has error rate 0.40% and costs "
    "$4.9K (temperature 1.0) or $3.5K (temperature 0.1); gpt-oss-20B ($0.2/MTok) has "
    "error rate 3.58% and costs $1.7K. Among proprietary models, gpt-4.1-mini at low "
    "temperature is optimal; gpt-oss-20B is the open-source leader.",
    title="Model cost-error tradeoff: gpt-4.1-mini optimal proprietary, gpt-oss-20B optimal OSS",
    metadata={"figure": "artifacts/2511.09030.pdf, Figure 6b"},
)

strat_cost_tradeoff = support(
    [error_rate_mini_low, error_rate_nano, error_rate_oss_20b],
    model_cost_tradeoff,
    reason=(
        "@error_rate_mini_low gives gpt-4.1-mini's 0.223% error rate and $3.5K cost. "
        "@error_rate_nano gives gpt-4.1-nano's 35.71% error rate and $41.9K cost. "
        "@error_rate_oss_20b gives gpt-oss-20B's 3.58% error rate and $1.7K cost. "
        "Comparing these three data points shows that per-token cost alone is a poor "
        "predictor of total task cost — error rate determines k_min, which dominates."
    ),
    prior=0.92,
)

cost_estimate_mini = claim(
    "Given gpt-4.1-mini's per-step error rate of 0.00223 and 538 mean output tokens, "
    "Eq. 18 (E[cost] = Theta(c*s*ln(s))) yields an estimated total cost of $3.5K "
    "for the full 20-disk (1,048,575-step) task at target reliability t=0.95, "
    "with k_min=3 votes per step.",
    title="Cost estimate for gpt-4.1-mini from scaling law",
)

strat_cost_from_error_rate = deduction(
    [error_rate_mini_low],
    cost_estimate_mini,
    reason=(
        "Plugging the empirical values from @error_rate_mini_low (p=0.99777, mean tokens=538, "
        "per-token cost) into the scaling law formula E[cost] = Theta(c*s*ln(s)) "
        "yields the $3.5K cost estimate with k_min=3. This is a deterministic arithmetic "
        "calculation given the empirical inputs."
    ),
    prior=0.99,
    background=[setting_voting_formula, setting_experiment_setup],
)

errors_decorrelated = claim(
    "In two independent runs of gpt-4.1-mini (tau=0.1) on 10,000 random single-step "
    "samples, zero steps had errors in both runs. This empirical result demonstrates "
    "that errors are effectively decorrelated across independent samples of the same step, "
    "validating the i.i.d. assumption required for the voting error correction to work.",
    title="Zero shared errors across two independent runs confirms error decorrelation",
)

# --- Section 4.4: Full Million-Step Run ---

maker_zero_errors = claim(
    "MAKER, using gpt-4.1-mini (tau=0.1) with k_min=3 first-to-ahead-by-k voting and "
    "red-flagging, successfully solved the 20-disk Towers of Hanoi task "
    "(1,048,575 sequential steps) with zero errors. This is the first demonstration of "
    "an LLM-based system solving a task with over one million steps without any error.",
    title="MAKER achieves zero-error solution to 1,048,575-step Towers of Hanoi",
    metadata={"figure": "artifacts/2511.09030.pdf, Figure 7"},
)

# Build abduction: MAKER success via MAD+voting hypothesis vs single-agent alternative
pred_maker = claim(
    "MAKER (MAD + first-to-ahead-by-k voting + red-flagging) predicts zero errors on "
    "the 1,048,575-step 20-disk Towers of Hanoi task given p=0.99777 and k_min=3, "
    "since the theoretical p_full at these parameters is extremely close to 1.",
    title="MAKER theoretical prediction: near-certain zero-error completion",
)

pred_single_agent = claim(
    "A single LLM agent (no decomposition, m = s = 1,048,575) predicts certain failure: "
    "the probability of zero errors is (1-0.00223)^1048575 which is astronomically small, "
    "effectively zero. No practically feasible model achieves zero errors without decomposition.",
    title="Single-agent prediction: certain failure on 1M-step task",
)

s_maker = support(
    [pred_maker],
    maker_zero_errors,
    reason=(
        "@pred_maker states that the theoretical prediction of MAKER is near-certain "
        "zero-error completion given the empirical per-step error rate and k_min=3. "
        "The observation @maker_zero_errors confirms this prediction exactly."
    ),
    prior=0.93,
)

s_single_agent = support(
    [pred_single_agent],
    maker_zero_errors,
    reason=(
        "@pred_single_agent predicts that without decomposition, zero errors on 1M steps "
        "is essentially impossible — the single-agent alternative cannot explain the "
        "observed zero-error outcome."
    ),
    prior=0.05,
)

from gaia.lang import compare

comp_strat = compare(
    pred_maker, pred_single_agent, maker_zero_errors,
    reason=(
        "MAKER predicts near-unity success probability for the observation; the "
        "single-agent alternative predicts near-zero probability. The match is decisive."
    ),
    prior=0.95,
)

abduction_maker = abduction(
    s_maker, s_single_agent, comp_strat,
    reason="Both frameworks attempt to explain the zero-error million-step result",
)

# --- Section 4.4: Convergence Analysis ---

exponential_convergence = claim(
    "The number of undecided steps decreases exponentially with each voting round. "
    "In the 20-disk experiment: after round 1, 1,048,575 steps are undecided; "
    "after round 2, ~81,959; after round 3, ~18,461; after round 4, ~3,807; "
    "continuing to decrease until 0 undecided steps (zero errors). The vast majority "
    "of LLM calls and therefore cost is spent in the first k_min=3 rounds; "
    "subsequent rounds cost effectively nothing.",
    title="Exponential convergence of voting to zero-error solution",
    metadata={"figure": "artifacts/2511.09030.pdf, Figure 8a"},
)

strat_exp_convergence = support(
    [voting_pfull_high_mad],
    exponential_convergence,
    reason=(
        "@voting_pfull_high_mad establishes theoretically that the voting mechanism "
        "converges with exponentially decaying probability of remaining undecided steps. "
        "The empirical observation in @exponential_convergence matches this theoretical "
        "prediction: after the first k=3 rounds there is a sharp exponential decrease "
        "in undecided steps, and the pathological case (one step requiring 18 rounds) "
        "was handled by the decorrelation mechanism."
    ),
    prior=0.90,
)

# --- Section 4.5: Red-Flagging Impact ---

red_flag_reduces_collisions = claim(
    "Red-flagging (discarding responses with max-token-cutoff violations) substantially "
    "reduces the number of collision steps — steps where both the first two votes are "
    "incorrect. With a high max-token cutoff (repairing parser), collision counts exceed "
    "the i.i.d. expectation of 1-2 by a large margin. Switching to the red-flagging "
    "parser (stricter token cutoff) reduces collision counts to near the i.i.d. baseline, "
    "confirming that red-flagging successfully decorrelates errors.",
    title="Red-flagging empirically reduces correlated-error collisions",
    metadata={"figure": "artifacts/2511.09030.pdf, Figure 9b"},
)

strat_red_flag_empirical = support(
    [red_flag_reduces_correlation],
    red_flag_reduces_collisions,
    reason=(
        "The theoretical mechanism in @red_flag_reduces_correlation predicts that "
        "discarding pathological (long/malformatted) responses removes correlated errors. "
        "The empirical result in Figure 9b confirms the prediction: collision counts "
        "(steps where both the first two votes are incorrect) drop to the i.i.d. "
        "baseline (~1-2 collisions) when red-flagging is applied, compared to much higher "
        "counts with the repairing parser. This validates the decorrelation mechanism."
    ),
    prior=0.88,
    background=[setting_red_flag_types],
)

obs_mini_stable = claim(
    "gpt-4.1-mini's per-step error rate at 10 disks is approximately 0.0045, "
    "consistent with its error rate at 20 disks (0.00223), showing no significant "
    "increase in error rate as task size grows.",
    title="gpt-4.1-mini error rate consistent across disk counts (10 vs 20 disks)",
)

obs_o3_stable = claim(
    "o3-mini's per-step error rate at 10 disks is approximately 0.0018 and remains "
    "consistent at 14-20 disks, showing no significant trend with task length.",
    title="o3-mini error rate consistent across disk counts",
)

s_ind_mini = support(
    [error_rate_stable],
    obs_mini_stable,
    reason=(
        "The law @error_rate_stable predicts that per-step error rates are approximately "
        "constant regardless of disk count. gpt-4.1-mini's rates at 10 and 20 disks "
        "(0.0045 and 0.00223) are consistent with this prediction."
    ),
    prior=0.9,
)

s_ind_o3 = support(
    [error_rate_stable],
    obs_o3_stable,
    reason=(
        "The law @error_rate_stable predicts stable error rates across disk counts. "
        "o3-mini's rate of ~0.0018 is consistent from 10 to 20 disks."
    ),
    prior=0.9,
)

error_rate_stable_ind = induction(
    s_ind_mini,
    s_ind_o3,
    law=error_rate_stable,
    reason=(
        "Two independent models (gpt-4.1-mini and o3-mini) both show stable per-step "
        "error rates across the range of 10 to 20 disks. This convergent evidence from "
        "independent model types supports the general law @error_rate_stable."
    ),
)
