"""Section 5 (Related Work): the mixed-policy methods being evaluated.

This module catalogs the five mixed-policy methods that the paper directly
evaluates against the corrected SFT-then-RL pipeline, plus the seven additional
methods the paper discusses qualitatively. Each evaluated method's SFT
configuration is characterized so that the bug attribution in s4/s5/s6 modules
can be tied back to specific papers.

Source: [@Limozin2026SFTthenRL, Sec. 5]; primary refs are the individual method
papers cited in the related-work table.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Methods directly evaluated (the five whose SFT pipelines we audit)
# ---------------------------------------------------------------------------

claim_luffy_method = claim(
    "**LUFFY [@LUFFY] mixes off-policy expert traces into on-policy GRPO.** "
    "It applies regularized importance sampling with a shaped policy "
    "$f(\\pi) = \\pi/(\\pi + \\lambda)$ to control distribution mismatch "
    "and avoid imitation collapse. Its SFT stage uses OpenRLHF [@OpenRLHF] "
    "for fine-tuning, and the OpenR1-Math-46k-8192 dataset is its standard "
    "training set [@LUFFY].",
    title="Method: LUFFY (off-policy mix into GRPO; SFT via OpenRLHF)",
)

claim_relift_method = claim(
    "**ReLIFT [@ReLIFT] alternates between SFT and RL phases.** It "
    "identifies unsolved problems via pass rate, applies SFT on expert "
    "demonstrations to inject missing knowledge, and resumes RL. This "
    "iterative process shrinks the set of hard problems over time. Its "
    "SFT stage uses Llama-Factory [@LlamaFactory] [@ReLIFT].",
    title="Method: ReLIFT (alternates SFT / RL phases; SFT via Llama-Factory)",
)

claim_srft_method = claim(
    "**SRFT [@SRFT] jointly optimizes SFT and RL losses within each "
    "batch.** It uses an adaptive entropy-based weight to balance the two "
    "signals. Its SFT baseline uses a tenfold lower learning rate than "
    "other methods (5x10^-6 vs the LUFFY/ReLIFT 5x10^-5), with batch "
    "size 128 and a linear schedule, producing a weaker SFT starting "
    "point that inflates the apparent mixed-policy gain "
    "[@SRFT; @Limozin2026SFTthenRL, Sec. 4].",
    title="Method: SRFT (joint SFT+RL loss in each batch; weak-LR SFT baseline)",
)

claim_prefix_rft_method = claim(
    "**Prefix-RFT [@PrefixRFT] integrates demonstrations into RFT by "
    "sampling a prefix from expert solutions and generating on-policy "
    "continuations**, forming hybrid trajectories for policy updates. "
    "It adopts its SFT baselines from LUFFY [@LUFFY], inheriting the "
    "OpenRLHF-trained baseline used there [@PrefixRFT].",
    title="Method: Prefix-RFT (expert-prefix + on-policy continuation; baselines inherited from LUFFY)",
)

claim_hpt_method = claim(
    "**HPT [@HPT] unifies SFT and RL under a common policy gradient "
    "objective and uses a binary gate**: SFT when all rollouts fail, "
    "GRPO otherwise. Its own ablations show that pure SFT matches or "
    "beats off-policy RL for the offline signal. HPT does not detail "
    "its SFT setup, stating only that the authors 'endeavored to "
    "follow previous works as closely as possible' [@HPT].",
    title="Method: HPT (binary SFT-or-GRPO gate; SFT setup not detailed)",
)

# ---------------------------------------------------------------------------
# Methods discussed qualitatively (not directly evaluated)
# ---------------------------------------------------------------------------

claim_other_mixed_policy_methods = claim(
    "**Other mixed-policy methods that may warrant SFT auditing.** "
    "UFT [@UFT] and CHORD [@CHORD] combine SFT and RL into a single "
    "loss, with CHORD using dynamic weighting and token-level "
    "uncertainty scaling. SuperRL [@SuperRL] applies RL only when "
    "correct rollouts exist and falls back to SFT otherwise. SASR "
    "[@SASR] adaptively balances SFT and RL using a KL-based switching "
    "signal. RED [@RED] dynamically balances SFT and RL by regulating "
    "their contributions based on entropy changes and sample accuracy. "
    "TemplateRL [@TemplateRL] increases exploration diversity by "
    "augmenting prompts with MCTS-derived templates. MIFO [@MIFO] "
    "interleaves RL and SFT by buffering hard questions for targeted "
    "SFT, freezing RL-critical parameters during SFT phases. These "
    "are *not* directly evaluated in the paper but are flagged as "
    "candidates for SFT auditing using the same methodology "
    "[@Limozin2026SFTthenRL, Sec. 5].",
    title="Other mixed-policy methods (UFT, CHORD, SuperRL, SASR, RED, TemplateRL, MIFO) flagged for auditing",
)

# ---------------------------------------------------------------------------
# Setup: shared training data
# ---------------------------------------------------------------------------

setup_openr1_dataset = setting(
    "**OpenR1-Math-46k-8192 [@OpenR1] is the shared training set.** It "
    "is a length-filtered subset of OpenR1-Math-220k [@OpenR1] whose "
    "prompts are drawn from NuminaMath 1.5 [@NuminaMath] and whose "
    "off-policy reasoning traces are generated by DeepSeek-R1 "
    "[@DeepSeekR1]. Generations longer than 8192 tokens and those "
    "verified incorrect by Math-Verify are filtered out, yielding "
    "approximately 46k prompts paired with high-quality demonstrations. "
    "The full dataset is used for both SFT (prompts + demonstrations) "
    "and RL (prompts + ground-truth answers for reward verification). "
    "This dataset is used by LUFFY, ReLIFT, SRFT, Prefix-RFT, and HPT "
    "as the common training set [@LUFFY; @ReLIFT; @SRFT; @PrefixRFT; "
    "@HPT].",
    title="Setup: OpenR1-Math-46k-8192 is the shared training set across the evaluated methods",
)

# ---------------------------------------------------------------------------
# Setup: base models used
# ---------------------------------------------------------------------------

setup_qwen_base = setting(
    "**Qwen2.5-Math-7B [@Qwen25Math] base model.** Following prior works "
    "[@LUFFY; @ReLIFT; @SRFT; @PrefixRFT; @HPT; @MIFO], the experiments "
    "use Qwen2.5-Math-7B as one base model with an increased max context "
    "length from 4096 to 16,384 tokens and an increased RoPE theta from "
    "10,000 to 40,000. Qwen2.5-Math-7B is pre-trained with emphasis on "
    "mathematical data, so it has substantial baseline math reasoning "
    "capacity from pre-training.",
    title="Setup: Qwen2.5-Math-7B base model with extended context",
)

setup_llama_base = setting(
    "**Llama-3.1-8B [@Llama3] base model.** Llama-3.1-8B is a "
    "general-purpose model with comparatively little mathematical "
    "reasoning content in its pre-training distribution "
    "[@SpuriousRewards], making it a stress test for whether SFT's "
    "knowledge-bootstrapping role is essential. Both Qwen2.5-Math-7B "
    "and Llama-3.1-8B use the same chat template once SFT is "
    "implemented correctly [@Limozin2026SFTthenRL, Appendix E].",
    title="Setup: Llama-3.1-8B base model (general-purpose, little pre-trained math)",
)

__all__ = [
    "claim_luffy_method",
    "claim_relift_method",
    "claim_srft_method",
    "claim_prefix_rft_method",
    "claim_hpt_method",
    "claim_other_mixed_policy_methods",
    "setup_openr1_dataset",
    "setup_qwen_base",
    "setup_llama_base",
]
