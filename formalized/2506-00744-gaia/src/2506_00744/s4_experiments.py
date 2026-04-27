"""Section 4: Experiments — language modeling, expressivity, retrieval, and POMDP RL."""

from gaia.lang import (
    claim,
    setting,
    support,
    deduction,
    abduction,
    induction,
    compare,
    contradiction,
    complement,
)

from .motivation import (
    proposal_synchronous_best,
    claim_compatibility_with_efficient_kernels,
)
from .s2_background import (
    claim_softmax_sharpness,
    claim_negative_eigvals,
    claim_deltanet_choice_for_hybrid,
)
from .s3_methods import (
    claim_delayed_lose_expressivity,
    claim_synchronous_keeps_expressivity,
    def_sum_mixing,
    def_dynamic_scalar_mixing,
    def_dynamic_vector_mixing,
    def_delayed_chunk,
    def_delayed_stream,
    def_synchronous,
)

# ---------------------------------------------------------------------------
# Common experimental setup
# ---------------------------------------------------------------------------

def_lm_training_setup = setting(
    "Language models are trained from scratch on 15B tokens of HuggingFace "
    "FineWeb-Edu [@Penedo2024FineWeb], with 24 layers, sequence length 2048 "
    "(340M params) or 2240 (1.3B params), 8/16 attention heads, hidden size "
    "1024/2048, and the fla-hub/transformer-1.3B-100B tokenizer (32k vocab). "
    "Models are implemented with the fla toolkit and trained with the flame "
    "framework. Effective batch size is 64 per GPU, peak LR $1\\!\\times\\!10^{-3}$ "
    "with 1024 warmup steps and minimum LR $0.1$ of the peak, AdamW with "
    "max-norm clipping 1.0.",
    title="Setting: language-modeling training configuration",
)

def_eval_protocol = setting(
    "Evaluation uses the standard lm-evaluation-harness [@EvalHarness2024]. We "
    "report perplexity on WikiText-2 (Wiki.) and LAMBADA (LMB.), plus zero-shot "
    "accuracy on PIQA, HellaSwag (acc_n), WinoGrande (Wino.), ARC-easy and "
    "ARC-challenge. The default KV-window size is $S=64$ tokens and the default "
    "mixer is dynamic vector mixing (Eq. 17).",
    title="Setting: language-modeling evaluation protocol",
)

def_baselines = setting(
    "The two baselines are: (i) Transformer++ — a Llama-style softmax-attention "
    "transformer with the configuration of Touvron et al. used in prior work; "
    "and (ii) DeltaNet with the configuration of Yang et al. [@Yang2024Delta]. "
    "For fair comparison the DeltaNet baseline omits the short-window convolution "
    "used in some recent reports.",
    title="Setting: Transformer++ and DeltaNet baselines",
)

# ---------------------------------------------------------------------------
# Section 4.1 General LM results (Table 2)
# ---------------------------------------------------------------------------

# Stitch observation-table claims into derived-claim chains so they are not orphaned
obs_table2_main = claim(
    "Main language-modeling results (Table 2). Lower is better for ppl; higher "
    "is better for acc and average. Window size $S=64$, dynamic vector mixing.\n\n"
    "**340M parameters**\n\n"
    "| Model               | Wiki ppl | LMB ppl | LMB acc | PIQA | Hella | Wino | ARC-e | ARC-c | Avg |\n"
    "|---------------------|---------|---------|---------|------|-------|------|-------|-------|-----|\n"
    "| Transformer++       | 26.5    | 34.9    | 33.9    | 67.6 | 41.0  | 53.7 | 60.2  | 29.0  | 47.6 |\n"
    "| DeltaNet            | 27.6    | 35.0    | 32.8    | 67.1 | 40.8  | 52.6 | 58.5  | 28.8  | 46.8 |\n"
    "| HQLT Delayed-Stream | 26.4    | 33.1    | 33.6    | 67.9 | 42.1  | 51.8 | 59.4  | 29.5  | 47.4 |\n"
    "| HQLT Delayed-Chunk  | 26.7    | 29.9    | 33.5    | 66.8 | 42.3  | 50.9 | 61.1  | 30.6  | 47.5 |\n"
    "| HQLT Synchronous    | 26.3    | 29.4    | 33.3    | 66.2 | 42.7  | 53.8 | 61.5  | 29.4  | 47.8 |\n\n"
    "**1.3B parameters**\n\n"
    "| Model               | Wiki ppl | LMB ppl | LMB acc | PIQA | Hella | Wino | ARC-e | ARC-c | Avg |\n"
    "|---------------------|---------|---------|---------|------|-------|------|-------|-------|-----|\n"
    "| Transformer++       | 19.8    | 17.9    | 42.6    | 71.0 | 50.3  | 55.8 | 65.2  | 33.2  | 53.0 |\n"
    "| DeltaNet            | 20.6    | 19.9    | 39.3    | 70.1 | 49.5  | 52.5 | 68.5  | 34.2  | 52.3 |\n"
    "| HQLT Delayed-Stream | 20.0    | 16.5    | 43.5    | 70.7 | 51.6  | 56.0 | 69.3  | 36.0  | 54.5 |\n"
    "| HQLT Delayed-Chunk  | 20.2    | 16.3    | 41.3    | 71.8 | 50.9  | 55.0 | 67.9  | 35.2  | 53.7 |\n"
    "| HQLT Synchronous    | 19.8    | 15.9    | 42.8    | 72.0 | 51.5  | 56.1 | 68.1  | 33.1  | 53.9 |\n",
    title="Observation: general LM results (Table 2)",
    metadata={"source_table": "artifacts/2506.00744.pdf, Table 2"},
)

claim_lm_baselines_comparable = claim(
    "On the general language-modeling evaluation suite, Transformer++ and "
    "DeltaNet perform comparably at both 340M and 1.3B scales: 6-task averages "
    "are 47.6 vs 46.8 (340M) and 53.0 vs 52.3 (1.3B). DeltaNet trails by "
    "$\\le 0.8$ absolute on average.",
    title="Transformer++ and DeltaNet baselines are nearly equivalent on standard LM tasks",
    background=[def_eval_protocol],
)
strat_baselines_comparable = support(
    [obs_table2_main],
    claim_lm_baselines_comparable,
    reason=(
        "Direct numerical reading of the 6-task averages in Table 2 "
        "(@obs_table2_main): 47.6 vs 46.8 at 340M and 53.0 vs 52.3 at 1.3B. The "
        "differences are within 1 absolute point, so 'comparable' is a faithful "
        "summary."
    ),
    prior=0.95,
    background=[def_eval_protocol],
)

claim_hqlts_match_or_beat = claim(
    "All three HQLT variants match or slightly improve on the average 6-task "
    "score relative to both baselines. At 340M the best HQLT (Synchronous) "
    "averages 47.8 vs 47.6 (Transformer++) and 46.8 (DeltaNet); at 1.3B the "
    "best HQLT (Delayed-Stream) averages 54.5 vs 53.0 (Transformer++) and 52.3 "
    "(DeltaNet), an improvement of up to ~1% absolute over DeltaNet.",
    title="HQLTs match or improve on baselines in 6-task average",
    background=[def_eval_protocol],
)
strat_hqlts_match_or_beat = support(
    [obs_table2_main],
    claim_hqlts_match_or_beat,
    reason=(
        "Reading the HQLT rows of Table 2 (@obs_table2_main) against the "
        "baselines: at 340M Synchronous (47.8) > Transformer++ (47.6) and "
        "Delayed-Stream/Chunk are within 0.2 points of Transformer++; at 1.3B "
        "Delayed-Stream reaches 54.5, which is 1.5 above Transformer++. None of "
        "the three HQLT variants underperforms the baselines by more than 1 "
        "point."
    ),
    prior=0.95,
    background=[def_eval_protocol],
)

claim_lambada_synchronous_best = claim(
    "On LAMBADA perplexity (LMB ppl), Synchronous HQLT achieves about 15% "
    "relative improvement over both baselines at both scales: 29.4 vs 34.9 "
    "(Transformer++) / 35.0 (DeltaNet) at 340M, and 15.9 vs 17.9 / 19.9 at 1.3B.",
    title="Synchronous HQLT delivers ~15% LMB ppl improvement over baselines",
    background=[def_eval_protocol],
)
strat_lambada_sync_best = support(
    [obs_table2_main],
    claim_lambada_synchronous_best,
    reason=(
        "Reading the LMB ppl column in both blocks of Table 2 "
        "(@obs_table2_main): 340M Synchronous 29.4 vs Transformer++ 34.9 / "
        "DeltaNet 35.0 = ~16% relative improvement; 1.3B Synchronous 15.9 vs "
        "17.9 / 19.9 = ~11-20% relative. The 15% figure is the rounded average."
    ),
    prior=0.95,
    background=[def_eval_protocol],
)

# Ablations within Synchronous HQLT (Table 2 bottom)

obs_la_ablation = claim(
    "Replacing DeltaNet by vanilla linear attention inside Synchronous HQLT "
    "(340M) drops the 6-task average from 47.8 to 42.2 and inflates LMB ppl "
    "from 29.4 to 114.2 (Table 2 bottom block).",
    title="Observation: vanilla LA in place of DeltaNet collapses HQLT (340M)",
    metadata={"source_table": "artifacts/2506.00744.pdf, Table 2 ablations"},
)

claim_fw_choice_matters = claim(
    "The choice of FW-memory operator matters: Synchronous HQLT requires a "
    "DeltaNet-class FWP rather than a vanilla LA. Substituting vanilla LA loses "
    "5.6 points of average accuracy and quadruples LAMBADA perplexity, "
    "indicating that the hybrid's quality is bounded by the strength of its FW "
    "branch.",
    title="Hybrid quality requires a strong FWP (DeltaNet) — vanilla LA insufficient",
    background=[def_synchronous],
)

obs_window_ablation_lm = claim(
    "Increasing KV-window size for Synchronous HQLT on the standard LM suite "
    "(340M) shows minimal effect: average over 6 tasks moves from 47.8 ($S{=}64$) "
    "to 48.0 / 47.7 / 47.6 at $S{=}128, 256, 512$, while LMB ppl improves only "
    "modestly (29.4 -> 27.8 / 27.7 / 28.0).",
    title="Observation: window size has minimal effect on general LM performance",
    metadata={"source_table": "artifacts/2506.00744.pdf, Table 2 ablations"},
)

claim_window_minor_for_lm = claim(
    "On general language modeling, KV-window size is a minor hyperparameter for "
    "Synchronous HQLT: even a small window of 64 captures most of the achievable "
    "performance, supporting the hypothesis that long-range structure is being "
    "absorbed by the FW-memory branch.",
    title="Window size has small impact on general LM (suggesting FW-memory absorbs long-range info)",
)
strat_window_minor_for_lm = support(
    [obs_window_ablation_lm],
    claim_window_minor_for_lm,
    reason=(
        "From the window-ablation rows in Table 2 (@obs_window_ablation_lm), the "
        "average over 6 tasks varies only between 47.6 and 48.0 across "
        "$S \\in \\{64, 128, 256, 512\\}$, which is well within typical "
        "inter-seed variance for these benchmarks. LMB ppl improves only "
        "modestly (29.4 -> 27.7-28.0). The conclusion that window size is a "
        "minor LM hyperparameter follows directly."
    ),
    prior=0.9,
    background=[def_eval_protocol],
)

obs_mixer_ablation_lm = claim(
    "Mixer ablation on Synchronous HQLT 340M: sum mixing yields 6-task avg "
    "47.2 / LMB ppl 34.8, while dynamic vector mixing yields 47.8 / 29.4. "
    "Dynamic vector mixing wins clearly on LMB ppl but is essentially tied on "
    "the average.",
    title="Observation: dynamic vector mixing slightly improves over sum mixing",
)

claim_vector_mixer_default = claim(
    "Dynamic vector mixing is the right default mixer for HQLT: it strictly "
    "improves LAMBADA perplexity over sum mixing (29.4 vs 34.8 at 340M), is "
    "essentially tied on the average over 6 tasks (47.8 vs 47.2), and adds "
    "only ~25M parameters relative to a 340M model.",
    title="Design choice: dynamic vector mixing is the recommended default",
)
strat_vector_mixer_default = support(
    [obs_mixer_ablation_lm],
    claim_vector_mixer_default,
    reason=(
        "Reading the mixer-ablation rows (@obs_mixer_ablation_lm), dynamic "
        "vector mixing dominates sum mixing on the LMB-ppl axis with no penalty "
        "on the average-accuracy axis. Hence vector mixing is the better default "
        "in the empirical regime studied."
    ),
    prior=0.9,
    background=[def_dynamic_vector_mixing, def_sum_mixing],
)

# ---------------------------------------------------------------------------
# Section 4.2 Expressivity (Table 3) — the central abductive experiment
# ---------------------------------------------------------------------------

def_expressivity_setup = setting(
    "Following Grazzi et al. [@Grazzi2025], expressivity is evaluated on two "
    "regular-language tasks: parity and modular arithmetic without brackets. "
    "Models are 2 layers (parity) or 3 layers (modular arithmetic). Training "
    "sequences have length 3-40 and test sequences 40-256 (testing length "
    "generalization). KV-window for HQLTs is $S=8$, except $S=16$ for "
    "Delayed-Chunk. Accuracy is normalised so that chance level is 0%.",
    title="Setting: parity and modular arithmetic protocol",
)

obs_table3_expressivity = claim(
    "Expressivity results on parity and modular arithmetic without brackets "
    "(Table 3). Normalised accuracy [%], chance = 0%.\n\n"
    "| Model                       | Parity | Mod Arith |\n"
    "|-----------------------------|--------|-----------|\n"
    "| Transformer [@Grazzi2025]   | 2.2    | 3.1       |\n"
    "| Mamba [@Grazzi2025]         | 100.0  | 24.1      |\n"
    "| DeltaNet [@Grazzi2025]      | 100.0  | 97.1      |\n"
    "| HQLT Delayed-Stream         | 3.3    | 27.8      |\n"
    "| HQLT Delayed-Chunk          | 2.8    | 1.4       |\n"
    "| HQLT Synchronous            | 100.0  | 97.0      |\n"
    "| HQLT Synchronous w. Linear Attn. | 2.5  | 44.5    |\n",
    title="Observation: expressivity results (Table 3)",
    metadata={"source_table": "artifacts/2506.00744.pdf, Table 3"},
)

obs_synchronous_solves_parity = claim(
    "On parity, Synchronous HQLT achieves 100.0% normalised accuracy — matching "
    "standalone DeltaNet and Mamba — while both delayed variants stay near "
    "chance (3.3% Delayed-Stream, 2.8% Delayed-Chunk).",
    title="Observation: Synchronous solves parity (100%); delayed variants fail (~3%)",
)

obs_synchronous_solves_modarith = claim(
    "On modular arithmetic, Synchronous HQLT achieves 97.0% — within 0.1 point "
    "of standalone DeltaNet (97.1%) — while Delayed-Stream is at 27.8% and "
    "Delayed-Chunk at 1.4%.",
    title="Observation: Synchronous matches DeltaNet on modular arithmetic; delayed variants fail",
)

obs_synchronous_la_fails = claim(
    "Replacing DeltaNet with vanilla LA inside the Synchronous HQLT also fails "
    "the expressivity tasks: 2.5% on parity, 44.5% on modular arithmetic.",
    title="Observation: Synchronous + vanilla LA fails expressivity tasks",
)

# Competing-cause hypotheses for delayed-variant failure on expressivity tasks
alt_random_failure = claim(
    "The failure of Delayed-Streaming and Delayed-Chunk on parity and modular "
    "arithmetic is incidental — caused by training instability, optimisation, "
    "or insufficient capacity, rather than by the delay itself.",
    title="Alternative: delayed variants' failure is due to training/capacity, not delay",
)

# Both causal hypotheses are mutually exclusive: either the delay is the cause,
# or the noise/optimisation is the cause (in the strong sense the alt asserts).
contra_delay_vs_noise = contradiction(
    claim_delayed_lose_expressivity,
    alt_random_failure,
    reason=(
        "@claim_delayed_lose_expressivity asserts the FW-memory delay is the "
        "structural reason the delayed variants cannot solve state-tracking. "
        "@alt_random_failure asserts the failure is *not* due to the delay but "
        "to noise/capacity. These cannot both be the cause."
    ),
    prior=0.9,
)

# Direct support for the delay-causes-failure hypothesis from Table 3
strat_table3_supports_delay_cause = support(
    [obs_table3_expressivity, obs_synchronous_solves_parity, obs_synchronous_solves_modarith],
    claim_delayed_lose_expressivity,
    reason=(
        "Table 3 (@obs_table3_expressivity) shows a sharp design correlation: "
        "both delayed variants (Delayed-Stream 3.3%, Delayed-Chunk 2.8%) fail "
        "parity at the same level as the softmax-only baseline, while Synchronous "
        "reaches 100% (@obs_synchronous_solves_parity) and matches DeltaNet on "
        "modular arithmetic (@obs_synchronous_solves_modarith). The pattern "
        "tracks 'has FW-memory access on current input', not training noise."
    ),
    prior=0.9,
    background=[def_expressivity_setup],
)

# Induction: parity result + mod arith result jointly support
# claim_synchronous_keeps_expressivity (the law)

s_parity_supports_law = support(
    [claim_synchronous_keeps_expressivity],
    obs_synchronous_solves_parity,
    reason=(
        "If the law that Synchronous HQLT preserves DeltaNet's state-tracking "
        "expressivity (@claim_synchronous_keeps_expressivity) holds, then on parity "
        "(a state-tracking task DeltaNet solves) Synchronous HQLT should also reach "
        "DeltaNet-level accuracy (~100%). The observed 100.0% is exactly this "
        "prediction."
    ),
    prior=0.95,
)
s_modarith_supports_law = support(
    [claim_synchronous_keeps_expressivity],
    obs_synchronous_solves_modarith,
    reason=(
        "Modular arithmetic without brackets is a different state-tracking task; "
        "the same law (@claim_synchronous_keeps_expressivity) predicts Synchronous "
        "HQLT should match DeltaNet's accuracy here too. Observed 97.0% vs "
        "DeltaNet's 97.1%."
    ),
    prior=0.95,
)
ind_synchronous_keeps_expressivity = induction(
    s_parity_supports_law,
    s_modarith_supports_law,
    law=claim_synchronous_keeps_expressivity,
    reason=(
        "Two independent state-tracking tasks (parity and modular arithmetic) both "
        "show Synchronous HQLT matching standalone DeltaNet. Each provides "
        "evidence for the general law that Synchronous HQLT preserves DeltaNet's "
        "expressivity; together they rule out task-specific artefacts."
    ),
)

# Inference: HQLT Synchronous w. Linear Attn fails -> FW operator choice matters

strat_fw_operator_matters = support(
    [obs_synchronous_la_fails, obs_la_ablation],
    claim_fw_choice_matters,
    reason=(
        "Two complementary ablations both swap DeltaNet for vanilla LA inside "
        "Synchronous HQLT. On general LM (@obs_la_ablation) the average drops 5.6 "
        "points and LMB ppl quadruples; on parity/modular arithmetic "
        "(@obs_synchronous_la_fails) accuracies fall to near chance (2.5% / 44.5%). "
        "Together these establish that hybrid quality is bounded by the FW operator's "
        "individual quality — so DeltaNet (rather than LA) is the right choice."
    ),
    prior=0.92,
    background=[def_synchronous],
)

# ---------------------------------------------------------------------------
# Section 4.3 Retrieval (Table 4)
# ---------------------------------------------------------------------------

def_retrieval_setup = setting(
    "Recall-intensive evaluation follows Yang et al. [@Yang2024Delta] and uses "
    "FDA, SWDE and SQuAD. The original FDA evaluation script is used (rather "
    "than lm-evaluation-harness) per [@Yang2025GatedDelta] recommendations. "
    "Default KV-window is $S=64$.",
    title="Setting: retrieval evaluation protocol (FDA, SWDE, SQuAD)",
)

obs_table4_retrieval = claim(
    "Retrieval results (Table 4). All HQLTs are Synchronous variants. \n\n"
    "**340M params**\n\n"
    "| Model                          | Window | SWDE | SQuAD | FDA  | Avg  |\n"
    "|--------------------------------|--------|------|-------|------|------|\n"
    "| Transformer++                  | 2048   | 44.9 | 36.9  | 52.3 | 44.7 |\n"
    "| Transformer++                  | 1024   | 30.4 | 25.5  | 31.2 | 29.0 |\n"
    "| DeltaNet                       | -      | 18.5 | 25.2  | 8.6  | 17.4 |\n"
    "| HQLT sum mixer                 | 64     | 13.3 | 26.2  | 12.6 | 17.4 |\n"
    "| HQLT dynamic scalar mixer      | 64     | 21.1 | 27.7  | 11.4 | 20.1 |\n"
    "| HQLT dynamic vector mixer      | 64     | 20.0 | 28.4  | 10.9 | 19.8 |\n"
    "| HQLT (vector mixer)            | 128    | 16.9 | 30.5  | 17.9 | 21.8 |\n"
    "| HQLT (vector mixer)            | 256    | 18.6 | 35.6  | 15.1 | 23.1 |\n"
    "| HQLT (vector mixer)            | 512    | 22.9 | 35.7  | 17.3 | 25.3 |\n"
    "| HQLT (vector mixer)            | 1024   | 34.0 | 37.1  | 50.1 | 40.4 |\n\n"
    "**1.3B params**\n\n"
    "| Model            | Window | SWDE | SQuAD | FDA  | Avg  |\n"
    "|------------------|--------|------|-------|------|------|\n"
    "| Transformer++    | 2048   | 53.7 | 41.5  | 64.7 | 53.3 |\n"
    "| DeltaNet         | -      | 32.9 | 29.9  | 23.6 | 28.8 |\n"
    "| HQLT Synchronous | 64     | 31.9 | 31.2  | 30.2 | 31.1 |\n",
    title="Observation: retrieval results (Table 4)",
    metadata={"source_table": "artifacts/2506.00744.pdf, Table 4"},
)

claim_window_drives_retrieval = claim(
    "On retrieval-intensive tasks, KV-window size is the dominant performance "
    "lever for HQLT: increasing $S$ from 64 to 1024 raises the 3-task average "
    "from 19.8 to 40.4 at 340M parameters, while task-level effects are "
    "non-monotonic (e.g., SWDE: 20.0 -> 16.9 at S=128 then up to 22.9 at S=512).",
    title="Window size strongly improves retrieval; per-task curves are non-monotonic",
    background=[def_retrieval_setup],
)

claim_hqlt_beats_matched_window = claim(
    "Holding window size equal at $S=1024$, HQLT Synchronous (340M) reaches "
    "average 40.4 across SWDE/SQuAD/FDA versus 29.0 for the Transformer++ "
    "trained with the same 1024-token context — a 11.4 point absolute "
    "improvement attributable to the FW-memory branch covering the part of "
    "context outside the KV-window.",
    title="At matched window size, HQLT beats Transformer++ by ~11 pts on retrieval",
    background=[def_retrieval_setup],
)

claim_hqlt_beats_deltanet_at_scale = claim(
    "At 1.3B parameters with a tiny $S{=}64$ window, HQLT Synchronous still "
    "outperforms standalone DeltaNet on retrieval: SWDE 31.9 vs 32.9 (slight "
    "loss), SQuAD 31.2 vs 29.9 (+1.3), FDA 30.2 vs 23.6 (+6.6), 3-task average "
    "31.1 vs 28.8 (+2.3).",
    title="At 1.3B with S=64, HQLT improves average retrieval over DeltaNet by 2.3 pts",
)
strat_hqlt_beats_deltanet_at_scale = support(
    [obs_table4_retrieval],
    claim_hqlt_beats_deltanet_at_scale,
    reason=(
        "Direct numerical reading of the 1.3B block of Table 4 "
        "(@obs_table4_retrieval): HQLT Synchronous (S=64) reaches 31.1 average "
        "vs DeltaNet's 28.8, with the largest per-task gain on FDA "
        "(+6.6 absolute)."
    ),
    prior=0.95,
    background=[def_retrieval_setup],
)

claim_retrieval_unsatisfactory = claim(
    "Even with the largest tested window of 1024, HQLT (40.4 avg) does not "
    "match the full-window 2048-token Transformer++ (44.7 avg) at 340M — and "
    "the 1.3B HQLT with $S{=}64$ remains far below the 1.3B Transformer++ "
    "with 2048 (31.1 vs 53.3). The paper itself flags retrieval as still "
    "unsatisfactory.",
    title="HQLT retrieval is still below full-context Transformer++",
    background=[def_retrieval_setup],
)
strat_retrieval_unsatisfactory = support(
    [obs_table4_retrieval],
    claim_retrieval_unsatisfactory,
    reason=(
        "Reading the largest-window HQLT row (S=1024, avg 40.4) against the "
        "full-context Transformer++ rows in Table 4 (@obs_table4_retrieval): "
        "the 4.3-point shortfall at 340M and the 22.2-point shortfall at 1.3B "
        "(31.1 vs 53.3) directly quantify the residual gap that the paper's "
        "own Limitations section flags."
    ),
    prior=0.95,
    background=[def_retrieval_setup],
)

# Reasoning for retrieval claims

strat_window_drives_retrieval = support(
    [obs_table4_retrieval],
    claim_window_drives_retrieval,
    reason=(
        "Reading down the 340M block of Table 4 (@obs_table4_retrieval), the "
        "average improves monotonically with window size at coarse granularity "
        "(19.8 -> 21.8 -> 23.1 -> 25.3 -> 40.4 at S = 64, 128, 256, 512, 1024) "
        "while individual tasks show local non-monotonicities (SWDE drops 20.0 -> "
        "16.9 at S=128 before recovering)."
    ),
    prior=0.95,
    background=[def_retrieval_setup],
)

strat_hqlt_beats_matched = support(
    [obs_table4_retrieval, claim_softmax_sharpness],
    claim_hqlt_beats_matched_window,
    reason=(
        "Comparing the two 340M rows with $S{=}1024$ in Table 4 "
        "(@obs_table4_retrieval): HQLT reaches 40.4 avg vs Transformer++ at 29.0. "
        "Both have the same softmax KV-window (so the precise-recall pathway, "
        "@claim_softmax_sharpness, is matched), but HQLT additionally has the "
        "FW-memory branch absorbing context beyond $S$, which is the natural "
        "explanation for the 11.4-point gap."
    ),
    prior=0.85,
    background=[def_retrieval_setup],
)

# ---------------------------------------------------------------------------
# Section 4.4 RL in POMDP (passive visual match)
# ---------------------------------------------------------------------------

def_visual_match_setup = setting(
    "Passive visual match [@Hung2019PassiveVisualMatch; @Ni2023RL]: a 7x11 grid "
    "world. An episode has 3 phases. Phase 1 (15 steps): the agent sees one of "
    "{red, green, blue}. Phase 2 (750 steps): the agent collects apples (each "
    "+1 reward); 10 apples respawn every 20 steps. Phase 3 (max 15 steps): "
    "reaching the pixel of the Phase-1 colour ends the episode with reward "
    "+100; reaching a wrong-colour pixel terminates with no reward. Total "
    "sequence length is 780 steps. Models have hidden size 100 and 2 attention "
    "heads; layer counts are 2 (Transformer) or 3 (DeltaNet, HQLT). Training "
    "uses soft actor-critic for discrete actions [@Ni2023RL].",
    title="Setting: passive visual match POMDP",
    metadata={"figure": "artifacts/2506.00744.pdf, Fig. 2A"},
)

obs_rl_results = claim(
    "Figure 2 (B/C) shows average return and success rate over 20 test episodes "
    "vs training environment steps with 3 seeds. Synchronous HQLT (window $S{=}64$) "
    "largely closes the gap between DeltaNet and the full-context Transformer "
    "(window 780): 'one of [HQLT's] seeds consistently achieved above 70%' "
    "success while DeltaNet underperforms.",
    title="Observation: HQLT closes Transformer-vs-DeltaNet gap on passive visual match",
    metadata={"figure": "artifacts/2506.00744.pdf, Fig. 2B,C"},
)

claim_rl_supports_synchronous = claim(
    "The passive-visual-match result extends Synchronous HQLT's benefit beyond "
    "language: a short KV-window of 64 plus FW-memory recovers most of the "
    "long-range memory benefit of full-context softmax attention (window 780) "
    "for a retrieval-with-distraction RL task.",
    title="Synchronous HQLT generalises beyond language to a POMDP RL task",
    background=[def_visual_match_setup],
)

strat_rl_supports_design = support(
    [obs_rl_results],
    claim_rl_supports_synchronous,
    reason=(
        "The Transformer with full 780-step context outperforms DeltaNet on the "
        "retrieval-focused passive-visual-match task. Synchronous HQLT with a "
        "tiny KV window of only 64 'largely closes this performance gap' "
        "(@obs_rl_results), demonstrating that the hybrid extracts most of the "
        "Transformer's long-range memory benefit at a fraction of the window cost, "
        "and that this advantage carries over from supervised LM to RL."
    ),
    prior=0.85,
    background=[def_visual_match_setup],
)

# ---------------------------------------------------------------------------
# Cross-section synthesis: which design is best?
# ---------------------------------------------------------------------------

# Three competing hypotheses about which HQLT is best.
# (proposal_synchronous_best from motivation is the "Synchronous-best" claim.)
alt_delayed_chunk_best = claim(
    "The Delayed-Chunk variant (akin to Infini-attention) is the best overall "
    "design: chunk-wise processing aligns with hardware-efficient training and "
    "could match Synchronous on most tasks.",
    title="Alternative: Delayed-Chunk HQLT (Infini-attention style) is the best design",
)
alt_delayed_stream_best = claim(
    "The Delayed-Streaming variant is the best overall design: its strict "
    "age-based division of labor (recent -> KV-memory, old -> FW-memory) is "
    "conceptually cleanest and is competitive on standard LM benchmarks.",
    title="Alternative: Delayed-Streaming HQLT is the best design",
)

# These three claims are competing about which is best — model as contradictions

contra_sync_vs_chunk = contradiction(
    proposal_synchronous_best,
    alt_delayed_chunk_best,
    reason=(
        "Both claim 'this variant is the best overall design.' Only one variant "
        "can be the singular best on the union of reported task suites; the two "
        "labels cannot both be true."
    ),
    prior=0.95,
)
contra_sync_vs_stream = contradiction(
    proposal_synchronous_best,
    alt_delayed_stream_best,
    reason=(
        "Both claim 'this variant is the best overall design.' Only one variant "
        "can be the singular best on the union of reported task suites."
    ),
    prior=0.95,
)
contra_chunk_vs_stream = contradiction(
    alt_delayed_chunk_best,
    alt_delayed_stream_best,
    reason=(
        "Both claim 'this variant is the best overall design.' Mutually exclusive."
    ),
    prior=0.95,
)

# Now the abductive argument that the Synchronous wins

s_h_sync_best = support(
    [
        claim_synchronous_keeps_expressivity,
        claim_lambada_synchronous_best,
        claim_hqlts_match_or_beat,
    ],
    proposal_synchronous_best,
    reason=(
        "Three lines of evidence support the Synchronous-best hypothesis: "
        "(i) Synchronous is the only variant that preserves DeltaNet expressivity "
        "on parity and modular arithmetic (@claim_synchronous_keeps_expressivity); "
        "(ii) it gives ~15% LMB ppl improvement at both 340M/1.3B "
        "(@claim_lambada_synchronous_best); and (iii) all HQLTs match or improve "
        "the baselines on the 6-task LM average (@claim_hqlts_match_or_beat), "
        "removing any LM-side cost. Together these select Synchronous as the "
        "single best design across LM and expressivity axes."
    ),
    prior=0.92,
)

# The expressivity-table evidence is the critical observation distinguishing
# the Synchronous-best hypothesis from the Delayed-best alternatives. We route
# it through plain support strategies and let the contradictions encode the
# 'pick a winner' constraint. (Earlier drafts used `abduction()` here, but the
# `compare` operator's bidirectional equivalences pull both predictions up
# with the observation, defeating the abductive intent.)

strat_table3_supports_synchronous = support(
    [obs_table3_expressivity, claim_synchronous_keeps_expressivity, claim_delayed_lose_expressivity],
    proposal_synchronous_best,
    reason=(
        "The expressivity table (@obs_table3_expressivity) shows Synchronous "
        "matching DeltaNet (~100% parity, ~97% mod arith) while both delayed "
        "variants fail at softmax-baseline level. Combined with the structural "
        "predictions (@claim_synchronous_keeps_expressivity, "
        "@claim_delayed_lose_expressivity), this is the central evidence that "
        "Synchronous is the best overall design: it is the *only* variant that "
        "preserves the FWP expressivity advantage."
    ),
    prior=0.92,
    background=[def_expressivity_setup],
)


__all__ = [
    "def_lm_training_setup",
    "def_eval_protocol",
    "def_baselines",
    "obs_table2_main",
    "claim_lm_baselines_comparable",
    "claim_hqlts_match_or_beat",
    "claim_lambada_synchronous_best",
    "obs_la_ablation",
    "claim_fw_choice_matters",
    "obs_window_ablation_lm",
    "claim_window_minor_for_lm",
    "obs_mixer_ablation_lm",
    "claim_vector_mixer_default",
    "strat_vector_mixer_default",
    "def_expressivity_setup",
    "obs_table3_expressivity",
    "obs_synchronous_solves_parity",
    "obs_synchronous_solves_modarith",
    "obs_synchronous_la_fails",
    "alt_random_failure",
    "contra_delay_vs_noise",
    "strat_table3_supports_delay_cause",
    "s_parity_supports_law",
    "s_modarith_supports_law",
    "ind_synchronous_keeps_expressivity",
    "strat_fw_operator_matters",
    "def_retrieval_setup",
    "obs_table4_retrieval",
    "claim_window_drives_retrieval",
    "claim_hqlt_beats_matched_window",
    "claim_hqlt_beats_deltanet_at_scale",
    "claim_retrieval_unsatisfactory",
    "strat_window_drives_retrieval",
    "strat_hqlt_beats_matched",
    "def_visual_match_setup",
    "obs_rl_results",
    "claim_rl_supports_synchronous",
    "strat_rl_supports_design",
    "alt_delayed_chunk_best",
    "alt_delayed_stream_best",
    "contra_sync_vs_chunk",
    "contra_sync_vs_stream",
    "contra_chunk_vs_stream",
    "s_h_sync_best",
    "strat_table3_supports_synchronous",
]
