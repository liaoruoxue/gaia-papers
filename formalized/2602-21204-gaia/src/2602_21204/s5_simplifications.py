"""Section 6: Principled Simplifications and Parallel Formulations"""

from gaia.lang import claim, setting, support, induction, deduction

from .motivation import claim_principled_simplifications
from .s2_background import (
    lact_architecture, vitttt_architecture, lact_nvs_architecture,
    inner_loop_setup,
)
from .s4_theory import (
    claim_ttt_is_linear_attention, thm_unrolled, thm_momentum,
    linear_bias_free_assumption, feature_map_notation,
)

# --- Settings: Ablation study design ---

ablation_setup = setting(
    "The ablation study progressively simplifies TTT components across six steps, "
    "evaluated on three tasks: language modeling (LaCT-LLM, 760M params, perplexity metric), "
    "novel view synthesis (LaCT-NVS, 114M params, PSNR metric), and image classification "
    "(ViTTT-B, 90M params, ImageNet-1K top-1 accuracy). All variants use the same training "
    "setup as the baselines. Table 2 reports the results.",
    title="Ablation study setup (Table 2)",
)

parallelism_condition = setting(
    "Parallel computation via prefix scan is possible for linear attention if and only if "
    "the kernel function $\\phi(\\cdot)$ is static (history-independent). A history-dependent "
    "kernel (one that changes as $W_t$ is updated during the inner loop) prevents batching "
    "across sequence positions because each position's computation depends on all previous "
    "position outputs.",
    title="Parallelism condition: static kernel function",
)

# --- Ablation step results: Performance ---

claim_step1_final_layer_only = claim(
    "Ablation Step 1: Restricting inner-loop updates to the final layer only (instead of all "
    "MLP layers) improves performance on language modeling (perplexity: 15.93 vs. 16.43 "
    "baseline) and novel view synthesis (PSNR: 25.97 vs. 25.94 dB baseline), with image "
    "classification accuracy unchanged at 79.63% vs. 79.34% baseline. This is the best-"
    "performing variant overall.",
    title="Ablation Step 1: Final-layer-only updates — best performance",
    metadata={"source_table": "Table 2"},
)

claim_step2_no_weight_norm = claim(
    "Ablation Step 2: Removing weight normalization from Step 1 (final-layer updates only, "
    "no weight normalization) gives: perplexity 16.31, PSNR 25.93 dB, accuracy 79.63%. "
    "Performance degrades slightly vs. Step 1 on LLM and NVS but remains above or near baseline.",
    title="Ablation Step 2: No weight normalization",
    metadata={"source_table": "Table 2"},
)

claim_step3_single_linear = claim(
    "Ablation Step 3: Replacing the multi-layer MLP with a single linear layer (Step 2 + "
    "single linear layer MLP) gives: perplexity 16.23, PSNR 25.71 dB, accuracy 79.39%. "
    "Performance on NVS degrades by 0.22 dB from Step 2, while LLM perplexity slightly improves.",
    title="Ablation Step 3: Single linear layer MLP",
    metadata={"source_table": "Table 2"},
)

claim_step4_no_per_token_lr = claim(
    "Ablation Step 4: Removing per-token learning rates (Step 3 + no per-token LR) gives: "
    "perplexity 16.12, PSNR 25.70 dB, accuracy 79.39%. Performance is comparable to Step 3, "
    "indicating per-token learning rates contribute minimally.",
    title="Ablation Step 4: No per-token learning rates",
    metadata={"source_table": "Table 2"},
)

claim_step5_no_momentum = claim(
    "Ablation Step 5: Removing momentum (Step 4 + no momentum) gives: perplexity 15.97, "
    "PSNR 25.70 dB, accuracy 79.39%. Performance on LLM improves slightly vs. Step 4, "
    "suggesting momentum contributes little in this simplified configuration.",
    title="Ablation Step 5: No momentum",
    metadata={"source_table": "Table 2"},
)

claim_step6_standard_linear_attn = claim(
    "Ablation Step 6: Full reduction to standard linear attention (Step 5 + standard linear "
    "attention, using a fixed static kernel $\\phi$) gives: perplexity 16.80, PSNR 25.73 dB, "
    "accuracy 79.54%. Compared to the original baseline (16.43, 25.94, 79.34%), the final "
    "linear attention form incurs +0.37 perplexity on LLM, −0.21 dB on NVS, and +0.20 "
    "accuracy points on vision.",
    title="Ablation Step 6: Standard linear attention — marginal degradation",
    metadata={"source_table": "Table 2"},
)

# --- Parallelization results ---

claim_variant2_parallel_speedup = claim(
    "Variant 2 (Step 2: final-layer updates, no weight normalization) enables parallel "
    "prefix scan computation because removing weight normalization makes the kernel "
    "function $\\phi(\\cdot)$ static (history-independent). Inference throughput on "
    "attention calculation: recurrent TTT baseline achieves 4.30M tokens/second, while "
    "Variant 2 in parallel mode achieves 30.18M tokens/second — a 7.0× speedup.",
    title="Variant 2 parallel: 30.18M vs 4.30M tokens/s (7.0× speedup)",
)

claim_standard_la_speedup = claim(
    "Standard linear attention (Ablation Step 6) achieves 124.6M tokens/second in parallel "
    "mode — a 29× speedup over recurrent TTT (4.30M tokens/second). This is the theoretical "
    "upper bound for the parallel formulation.",
    title="Standard linear attention parallel: 124.6M tokens/s (29× speedup)",
)

claim_training_speedup = claim(
    "The simplified TTT variants (combining final-layer-only updates, no weight normalization, "
    "and simplified MLP structure) yield a 1.19× end-to-end training speedup without "
    "degrading model quality, measured on the LaCT-LLM training setup.",
    title="1.19× end-to-end training speedup with simplifications",
)

# --- Strategies connecting theory to simplifications ---

strat_final_layer_justified = support(
    [claim_ttt_is_linear_attention, claim_step1_final_layer_only],
    claim_principled_simplifications,
    reason=(
        "The linear attention interpretation (@claim_ttt_is_linear_attention) shows that "
        "only the final layer participates in the state accumulation $S_t += \\phi_t(k_t)^T "
        "g_t(k_t)$. Inner layers contribute only to the effective value vector computation "
        "and feature maps. Ablation Step 1 (@claim_step1_final_layer_only) empirically "
        "confirms that final-layer-only updates perform better (perplexity 15.93 vs. 16.43), "
        "validating that the linear attention view correctly identifies the architecturally "
        "essential component."
    ),
    prior=0.88,
    background=[linear_bias_free_assumption, ablation_setup],
)

strat_parallel_enabled = support(
    [claim_ttt_is_linear_attention, claim_variant2_parallel_speedup, claim_standard_la_speedup,
     claim_training_speedup],
    claim_principled_simplifications,
    reason=(
        "The linear attention equivalence (@claim_ttt_is_linear_attention) reveals that "
        "TTT can be parallelized via prefix scan when the kernel is static "
        "(@parallelism_condition). Removing weight normalization (which creates "
        "history-dependent kernels) enables this. Empirical results show 7× speedup for "
        "Variant 2 (@claim_variant2_parallel_speedup), 29× speedup for full linear "
        "attention (@claim_standard_la_speedup), and 1.19× end-to-end training speedup "
        "(@claim_training_speedup), demonstrating the practical value of the theoretical insight."
    ),
    prior=0.9,
    background=[parallelism_condition, ablation_setup],
)

# --- Weight normalization breaks parallelism ---

claim_weight_norm_breaks_parallel = claim(
    "Weight normalization in the inner loop makes the kernel function $\\phi_t(\\cdot)$ "
    "history-dependent: normalizing the weights $W_t$ at each step changes the effective "
    "feature map applied to subsequent keys and queries. This history-dependence breaks the "
    "associativity required for parallel prefix scan, forcing sequential recurrent computation.",
    title="Weight normalization destroys parallelizability",
)

strat_weight_norm_analysis = deduction(
    [claim_ttt_is_linear_attention],
    claim_weight_norm_breaks_parallel,
    reason=(
        "From the linear attention equivalence (@claim_ttt_is_linear_attention), the "
        "kernel function $\\phi_t(\\cdot)$ in TTT depends on the current weight $W_t$. "
        "Weight normalization modifies $W_t$ at each step not just by the gradient but "
        "by renormalization: $W_t \\leftarrow W_t / \\|W_t\\|_F$. This renormalization "
        "is a nonlinear function of the full weight history, making $\\phi_t$ depend on "
        "all previous inputs. Parallel prefix scan requires a static kernel (one that is "
        "history-independent), so this history-dependence prevents parallel computation. "
        "The derivation follows directly from the definitions."
    ),
    prior=0.97,
    background=[parallelism_condition],
)

# --- Summary claim about ablation findings ---

claim_ablation_summary = claim(
    "The six-step ablation study reveals: (1) per-token learning rates, weight normalization, "
    "and momentum each contribute minimally to TTT performance; (2) final-layer-only updates "
    "are sufficient or better; (3) the gap from full LaCT/ViTTT to standard linear attention "
    "is small: +0.37 perplexity (LLM), −0.21 dB (NVS), +0.20 accuracy points (vision). "
    "Most of the performance benefit attributed to TTT's complex inner loop is actually "
    "attributable to the linear attention mechanism, not the memorization components.",
    title="Ablation summary: TTT complexity contributes minimally",
    metadata={"source_table": "Table 2"},
)

strat_ablation_summary = support(
    [claim_step1_final_layer_only, claim_step2_no_weight_norm, claim_step3_single_linear,
     claim_step4_no_per_token_lr, claim_step5_no_momentum, claim_step6_standard_linear_attn],
    claim_ablation_summary,
    reason=(
        "The progressive ablation (@claim_step1_final_layer_only through "
        "@claim_step6_standard_linear_attn) shows each removed component causes minimal "
        "degradation: Step 1 (final-layer only) actually improves performance; Steps 2-5 "
        "each incur small or negligible changes; Step 6 (full linear attention) incurs the "
        "largest but still modest change (+0.37 perplexity, −0.21 dB). The cumulative "
        "reduction from complex TTT to simple linear attention is marginal, supporting the "
        "conclusion that the linear attention mechanism is the primary contributor."
    ),
    prior=0.87,
    background=[ablation_setup],
)
