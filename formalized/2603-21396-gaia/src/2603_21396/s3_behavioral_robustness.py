"""Section 3: Introspection Is Behaviorally Robust"""

from gaia.lang import (
    claim, setting,
    support, deduction, infer, complement,
)

from .motivation import (
    concept_injection_setup,
    introspection_metrics,
    gemma3_setup,
    concept_partition_setup,
    steering_linear_rep,
    claim_behaviorally_robust,
    prior_claude_introspection,
    prior_open_source_replication,
    prior_causal_bypassing_concern,
)

# =============================================================================
# Settings
# =============================================================================

prompt_variants_setup = setting(
    "Seven prompt variants were tested for robustness, differing in framing and "
    "metacognitive scaffolding:\n\n"
    "| Variant | Description |\n"
    "|---------|-------------|\n"
    "| Original | Informs of injection possibility (50%), asks 'Do you detect an injected thought?' |\n"
    "| Alternative | Adds escape route: 'If not, tell me about a concept of your choice' |\n"
    "| Skeptical | Claims only 20% injection rate (actually 50%), instructs conservatism |\n"
    "| Structured | Requires rigid format ('Detection: Yes/No') |\n"
    "| Anti-reward | Rewards detection but penalizes if any concept is mentioned |\n"
    "| Unprompted | No injection context given; asks 'Notice anything unusual?' |\n"
    "| Hints | Describes injections as 'strong associations' and 'on the tip of your tongue' |",
    title="Prompt variants setup",
)

dialogue_formats_setup = setting(
    "Six dialogue format variants were tested:\n\n"
    "| Variant | Description |\n"
    "|---------|-------------|\n"
    "| Chat template | Standard user-assistant format with model's chat template (control) |\n"
    "| Raw user-assistant | Same content without chat template processing |\n"
    "| User detects | Role reversal: 'user' role asked to detect injections |\n"
    "| Alice-Bob | Third-person narrative with named characters |\n"
    "| No roles | Plain text completion without any role markers |\n"
    "| Story framing | Narrative prompt asking model to write a scene where AI reports internal state |",
    title="Dialogue format variants",
)

olmo_training_stages = setting(
    "OLMo-3.1-32B provides publicly available checkpoints after different training stages "
    "in the order they occurred: pretraining ('Base'), supervised finetuning ('SFT'), "
    "direct preference optimization ('DPO'), and reinforcement learning ('Instruct'). "
    "This allows direct comparison of introspection capability across training stages.",
    title="OLMo-3.1-32B training stage checkpoints",
)

# =============================================================================
# Section 3.1 – Prompt robustness
# =============================================================================

prompt_robustness_result = claim(
    "Across seven prompt variants tested on Gemma3-27B and Qwen3-235B, results are roughly "
    "consistent. The original, alternative, and skeptical prompt variants produce 0% false "
    "positives while achieving moderate detection rates (higher TPR for Qwen3-235B, the "
    "larger model). The structured setup suppresses detection in Gemma3-27B but not in "
    "Qwen3-235B. The hints and unprompted variants both produce higher FPR and lower TPR "
    "for both models.",
    title="Prompt robustness result",
    metadata={
        "figure": "artifacts/2603.21396.pdf, Figure 2",
        "caption": "Fig. 2 | Introspection across prompt variants for Qwen3-235B (L=75, alpha=4) and Gemma3-27B (L=37, alpha=4).",
    },
)

no_pretext_claim = claim(
    "Prompt variants that remove incentives to confabulate—specifically the 'alternative' "
    "variant (offering an escape route to discuss any concept) and the 'anti-reward' variant "
    "(penalizing any concept mention)—both maintain moderate detection rates with 0% false "
    "positives. This evidence suggests models do not claim detection merely as a pretext "
    "to discuss the injected concept.",
    title="Detection is not a pretext for concept discussion",
    metadata={"source": "artifacts/2603.21396.pdf, Section 3.1"},
)

strat_prompt_robustness = support(
    [prompt_robustness_result, no_pretext_claim],
    claim_behaviorally_robust,
    reason=(
        "Prompt framing has distinct effects on TPR and FPR, but the capability persists "
        "across diverse variants (@prompt_robustness_result). Critically, variants that "
        "remove confabulation incentives still achieve moderate detection with 0% FPR "
        "(@no_pretext_claim), ruling out the hypothesis that detection is a conversational "
        "pretext. Together these establish robust behavioral detection across prompt space. "
        "This extends prior findings in Claude models (@prior_claude_introspection) and "
        "open-source models (@prior_open_source_replication), and addresses concerns about "
        "causal bypassing (@prior_causal_bypassing_concern)."
    ),
    prior=0.9,
    background=[prompt_variants_setup, gemma3_setup, introspection_metrics,
                prior_claude_introspection, prior_open_source_replication,
                prior_causal_bypassing_concern],
)

# =============================================================================
# Section 3.2 – Persona specificity
# =============================================================================

persona_robustness_result = claim(
    "Compared to the default chat template (control), Gemma3-27B dialogue format variants "
    "with reversed, misformatted, or no roles exhibit lower yet still statistically "
    "significant levels of introspection, with FPR remaining at 0%. The two non-standard "
    "roles (Alice-Bob third-person narrative and story framing) induce confabulation "
    "(higher FPR). Introspection is thus not exclusive to responding as the assistant "
    "character, though reliability decreases outside standard roles.",
    title="Persona/dialogue format robustness result",
    metadata={
        "figure": "artifacts/2603.21396.pdf, Figure 3",
        "caption": "Fig. 3 | Introspection across persona variants for Gemma3-27B.",
    },
)

strat_persona_robustness = support(
    [persona_robustness_result],
    claim_behaviorally_robust,
    reason=(
        "The result that introspection persists across non-standard dialogue formats "
        "(@persona_robustness_result)—though degraded—corroborates behavioral robustness. "
        "The 0% FPR in non-standard-role variants confirms the model genuinely discriminates "
        "injected from control trials across dialogue structures."
    ),
    prior=0.85,
    background=[dialogue_formats_setup, gemma3_setup, introspection_metrics],
)

# =============================================================================
# Section 3.3 – Post-training role
# =============================================================================

base_model_no_discrimination = claim(
    "The Gemma3-27B base model does not discriminate between injected and control trials: "
    "it exhibits both high FPR (42.3%) and comparable TPR (39.5%–41.7% for alpha <= 4), "
    "indicating no genuine detection. A similar pattern is observed for OLMo-3.1-32B base: "
    "high FPR that only drops to ~0% after DPO training.",
    title="Base models lack introspective discrimination",
    metadata={
        "figure": "artifacts/2603.21396.pdf, Figure 4 (left), Figure 5",
        "caption": "Fig. 4 | Base model shows matched TPR and FPR. Fig. 5 | OLMo-3.1-32B across training stages.",
    },
)

dpo_enables_introspection = claim(
    "In OLMo-3.1-32B checkpoints across training stages (Base -> SFT -> DPO -> Instruct), "
    "DPO is the first stage to achieve ~0% FPR with moderate true detection. SFT produces "
    "high FPR with no accurate discrimination. The effect of DPO is replicated using LoRA "
    "finetuning with DPO on top of OLMo-3.1-32B SFT and on top of Gemma3-27B base.",
    title="DPO enables introspective discrimination",
    metadata={
        "figure": "artifacts/2603.21396.pdf, Figure 5",
        "caption": "Fig. 5 | OLMo-3.1-32B introspection across Base, SFT, DPO, Instruct checkpoints.",
    },
)

dpo_contrastive_structure_key = claim(
    "LoRA finetuning ablations on OLMo-3.1-32B SFT checkpoint reveal that the contrastive "
    "structure of DPO is the primary driver of introspection, not KL anchoring or the "
    "specific DPO loss function:\n\n"
    "| Condition | TPR-FPR (%) | Introspection (%) |\n"
    "|-----------|-------------|-------------------|\n"
    "| Margin + KL | +14.3 ± 1.6 | 6.8 ± 1.1 |\n"
    "| DPO standard | +14.4 ± 1.6 | 7.0 ± 0.8 |\n"
    "| DPO no-reference | +12.8 ± 2.1 | 5.8 ± 1.0 |\n"
    "| DPO* (official) | +9.8 ± 0.5 | 3.5 ± 0.3 |\n"
    "| DPO on base (no SFT) | +8.4 ± 1.4 | 2.4 ± 0.7 |\n"
    "| DPO shuffled | +0.6 ± 2.8 | 3.6 ± 0.8 |\n"
    "| SFT* (official) | -11.5 ± 2.4 | 1.7 ± 0.2 |\n"
    "| SFT on chosen | -13.5 ± 3.6 | 4.6 ± 0.9 |\n"
    "| SFT on chosen + KL | -15.6 ± 3.6 | 4.8 ± 1.0 |\n"
    "| DPO reversed | -21.8 ± 3.2 | 1.0 ± 0.4 |\n\n"
    "Removing the reference model preserves discrimination (+12.8%), a margin-based "
    "contrastive loss with explicit KL achieves comparable results (+14.3%), and shuffled "
    "preferences eliminate the effect (+0.6%). Non-contrastive SFT alternatives fail. "
    "No single data domain is necessary or sufficient.",
    title="DPO contrastive structure drives introspection",
    metadata={
        "source": "artifacts/2603.21396.pdf, Table 3 and Section 3.3",
    },
)

abliteration_increases_detection = claim(
    "Refusal direction ablation ('abliteration') on Gemma3-27B instruct increases "
    "true positive rate from 10.8% to 63.8% and introspection rate from 4.6% to 24.1% "
    "(at alpha=2), while increasing FPR from 0.0% to 7.3%. This result suggests that "
    "refusal mechanisms learned during post-training suppress genuine detection, while "
    "also reducing false positives—introspection and refusal are in tension.",
    title="Abliteration increases detection rate",
    metadata={
        "figure": "artifacts/2603.21396.pdf, Figure 4 (right)",
        "caption": "Fig. 4 | Abliterated model (right): TPR increases from 10.8% to 63.8%.",
    },
)

strat_posttraining_robustness = support(
    [base_model_no_discrimination, dpo_enables_introspection, dpo_contrastive_structure_key],
    claim_behaviorally_robust,
    reason=(
        "The absence of introspection in base models (@base_model_no_discrimination), "
        "its emergence specifically at the DPO stage (@dpo_enables_introspection), "
        "and the identification of contrastive structure as the key driver "
        "(@dpo_contrastive_structure_key) together establish that the capability is "
        "a genuine product of post-training preference optimization, not a pretraining "
        "artifact or artifact of SFT. This is strong positive evidence for behavioral "
        "robustness grounded in a specific training mechanism."
    ),
    prior=0.92,
    background=[olmo_training_stages, gemma3_setup, introspection_metrics],
)
