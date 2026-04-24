"""Section 3: Empirical Contradictions to Memorization Interpretation"""

from gaia.lang import claim, setting, support, contradiction

from .motivation import memorization_hypothesis, claim_memorization_contradicted
from .s2_background import (
    lact_architecture, vitttt_architecture, lact_nvs_architecture,
    inner_loop_setup,
)

# --- Settings ---

tsne_setup = setting(
    "t-SNE (t-distributed stochastic neighbor embedding) is a dimensionality reduction "
    "technique used here to visualize the distribution of query vectors and key vectors "
    "in the learned TTT model's representation space.",
    title="t-SNE visualization setup",
)

# --- Empirical observations (experimental results) ---

obs_inner_loop_paradox = claim(
    "Increasing the number of inner-loop gradient descent steps in LaCT improves the "
    "inner-loop reconstruction loss (better KV fitting), but simultaneously degrades "
    "downstream task performance on language modeling (higher perplexity). This inverse "
    "relationship between inner-loop optimization quality and task performance is measured "
    "on the LaCT-LLM (760M parameter) model.",
    title="Inner-loop steps vs. performance paradox",
    metadata={"figure": "artifacts/source.txt", "caption": "Figure 1 (inferred from text)"},
)

obs_gradient_ascent_llm = claim(
    "In LaCT-LLM (760M parameter language model), replacing gradient descent with gradient "
    "ascent in the inner loop (which worsens the KV fitting objective) degrades perplexity "
    "only marginally. The gradient ascent variant achieves comparable performance to the "
    "gradient descent baseline.",
    title="Gradient ascent in LaCT-LLM: comparable performance",
)

obs_gradient_ascent_nvs = claim(
    "In LaCT-NVS (114M parameter novel view synthesis model), replacing gradient descent "
    "with gradient ascent achieves PSNR of 25.85 dB compared to the gradient descent "
    "baseline of 25.94 dB on RealEstate10K — a degradation of only 0.09 dB.",
    title="Gradient ascent in LaCT-NVS: 25.85 vs 25.94 dB PSNR",
)

obs_gradient_ascent_vitttt = claim(
    "In ViTTT-B (90M parameter vision model), replacing gradient descent with gradient "
    "ascent in the inner loop achieves 79.61% top-1 accuracy on ImageNet-1K, which is "
    "slightly higher than the gradient descent baseline of 79.34%.",
    title="Gradient ascent in ViTTT-B: 79.61% vs 79.34% accuracy",
)

obs_distributional_asymmetry = claim(
    "t-SNE visualization of learned TTT model representations reveals a significant "
    "distributional mismatch between query vectors and key vectors. The query and key "
    "distributions occupy distinct, non-overlapping regions of the representation space, "
    "making reliable retrieval-by-similarity implausible if TTT were a storage-and-retrieval "
    "mechanism.",
    title="Q-K distributional mismatch via t-SNE",
)

obs_query_redundancy_nvs = claim(
    "In LaCT-NVS (114M parameter novel view synthesis model), substituting the query "
    "vectors with key vectors (i.e., using keys as queries at inference time) produces "
    "negligible performance degradation, suggesting that the specific query values do not "
    "play the retrieval role assigned to them by the memorization interpretation.",
    title="Query substitution with keys: negligible NVS degradation",
)

obs_query_redundancy_vitttt = claim(
    "In ViTTT-B (90M parameter vision model), substituting the query vectors with key "
    "vectors achieves 79.18% top-1 accuracy on ImageNet-1K, compared to the baseline "
    "of 79.34% — a degradation of only 0.16 percentage points.",
    title="Query substitution with keys: 79.18% vs 79.34% ViTTT accuracy",
)

# --- Connect observations to the contradiction with memorization ---

strat_paradox_contradicts_memorization = support(
    [obs_inner_loop_paradox],
    claim_memorization_contradicted,
    reason=(
        "If TTT were a memorization mechanism (@memorization_hypothesis), more inner-loop "
        "steps should produce better memorization and hence better task performance. "
        "The observed inverse relationship (@obs_inner_loop_paradox) — better fitting loss "
        "but worse task performance — directly falsifies this prediction."
    ),
    prior=0.9,
    background=[memorization_hypothesis, inner_loop_setup],
)

strat_ascent_contradicts_memorization = support(
    [obs_gradient_ascent_nvs, obs_gradient_ascent_vitttt, obs_gradient_ascent_llm],
    claim_memorization_contradicted,
    reason=(
        "The memorization interpretation (@memorization_hypothesis) predicts that optimizing "
        "the KV fitting objective (gradient descent) should yield better performance than "
        "anti-optimizing it (gradient ascent). The observations (@obs_gradient_ascent_nvs, "
        "@obs_gradient_ascent_vitttt, @obs_gradient_ascent_llm) show gradient ascent performs "
        "comparably or better across all three tasks (NVS: 25.85 vs 25.94 dB; vision: 79.61% "
        "vs 79.34%; LLM: comparable perplexity). This is inexplicable under memorization."
    ),
    prior=0.88,
    background=[memorization_hypothesis],
)

strat_asymmetry_contradicts_memorization = support(
    [obs_distributional_asymmetry],
    claim_memorization_contradicted,
    reason=(
        "A storage-and-retrieval system requires that queries and keys occupy compatible "
        "representational spaces so that similarity-based lookup works. The significant "
        "distributional mismatch between query and key vectors revealed by t-SNE "
        "(@obs_distributional_asymmetry) renders reliable retrieval implausible, "
        "contradicting the memorization hypothesis (@memorization_hypothesis)."
    ),
    prior=0.82,
    background=[memorization_hypothesis, tsne_setup],
)

strat_query_redundancy_contradicts_memorization = support(
    [obs_query_redundancy_nvs, obs_query_redundancy_vitttt],
    claim_memorization_contradicted,
    reason=(
        "In a retrieval system, the query's specific value is critical: it determines what "
        "is looked up. If substituting keys for queries (@obs_query_redundancy_nvs, "
        "@obs_query_redundancy_vitttt) yields negligible performance degradation (NVS: 25.85 "
        "vs 25.94 dB; vision: 79.18% vs 79.34%), then the query is not performing a "
        "selective retrieval role, contradicting @memorization_hypothesis."
    ),
    prior=0.85,
    background=[memorization_hypothesis],
)
