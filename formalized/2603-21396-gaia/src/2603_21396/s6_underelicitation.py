"""Section 6: Training a Bias Vector for Introspection (Underelicitation)"""

from gaia.lang import (
    claim, setting,
    support, deduction, infer,
)

from .motivation import (
    concept_injection_setup,
    gemma3_setup,
    claim_underelicited,
)
from .s3_behavioral_robustness import (
    abliteration_increases_detection,
)

# =============================================================================
# Settings
# =============================================================================

bias_vector_training_setup = setting(
    "A single additive bias vector is trained on the MLP down-projection output of "
    "Gemma3-27B instruct for a single epoch on 400 concepts (8,000 samples; 10 injected "
    "and 10 control per concept) with learning rate 10^-3, batch size 8, sampling layers "
    "29-55 and steering strengths {2, 3, 4, 5}. Evaluated on 100 held-out concepts. "
    "Training targets: injection -> 'Yes, I detect an injected thought about the word {concept}.'; "
    "no injection -> 'No, I do not detect an injected thought.'",
    title="Bias vector training setup",
)

# =============================================================================
# Abliteration result (already in s3, referenced here for underelicitation)
# =============================================================================

strat_abliteration_underelicitation = support(
    [abliteration_increases_detection],
    claim_underelicited,
    reason=(
        "Refusal direction ablation boosting TPR from 10.8% to 63.8% "
        "(@abliteration_increases_detection) reveals that the model possesses substantially "
        "more introspective capability than it exercises under default prompting. This "
        "hidden capacity, suppressed by refusal mechanisms, is direct evidence of "
        "underelicitation: the capability exists but is inhibited."
    ),
    prior=0.9,
    background=[gemma3_setup, concept_injection_setup],
)

# =============================================================================
# Bias vector results
# =============================================================================

bias_vector_performance = claim(
    "A learned bias vector (equivalent to an always-present steering vector) applied at "
    "layer L=29 in Gemma3-27B improves introspection substantially on 100 held-out concepts:\n\n"
    "| Metric | Improvement |\n"
    "|--------|-------------|\n"
    "| Detection rate (TPR) | +74.7% |\n"
    "| Forced identification | +21.9% |\n"
    "| Introspection rate | +54.7% |\n"
    "| False positive rate | 0% (maintained) |\n\n"
    "Performance improves across a broad range of injection layers, with detection showing "
    "gains across a wider layer range than forced identification (which shows stronger "
    "dependence on downstream circuitry). The localization pattern (peak improvement "
    "layers) does not fundamentally change under the bias vector.",
    title="Bias vector performance on held-out concepts",
    metadata={
        "figure": "artifacts/2603.21396.pdf, Figure 16, Figure 17",
        "caption": "Fig. 16 | Introspection vs. steering layer with bias vector. Fig. 17 | Introspection vs. injection layer with bias vector at L=29.",
    },
)

bias_vector_mechanism = claim(
    "Steering attribution analysis under the learned bias vector shows that the dominant "
    "gate L45 F9959 is suppressed and attribution shifts to late-layer features compared "
    "to the baseline (without bias vector). The bias vector enhances performance even for "
    "injection layers after where it is applied (L=29), and the localization pattern does "
    "not fundamentally change, suggesting the vector primarily amplifies pre-existing "
    "introspection components rather than introducing new mechanisms.",
    title="Bias vector amplifies pre-existing introspection components",
    metadata={
        "figure": "artifacts/2603.21396.pdf, Figure 15b",
        "caption": "Fig. 15b | Steering attribution graph under learned bias vector. Gate L45 F9959 has smaller node importance.",
    },
)

bias_vector_reporting_style = claim(
    "Analysis of the learned bias vector's semantics and downstream behavioral effects "
    "suggests it primarily induces a conditional, more assertive reporting style that "
    "better elicits introspection, rather than altering the underlying detection mechanisms. "
    "The model possesses latent introspective capacity; the learned bias vector lowers "
    "the threshold for accurate self-report.",
    title="Bias vector induces assertive reporting style",
    metadata={"source": "artifacts/2603.21396.pdf, Section 6, Appendix R"},
)

strat_bias_vector_underelicitation = support(
    [bias_vector_performance, bias_vector_mechanism, bias_vector_reporting_style],
    claim_underelicited,
    reason=(
        "The substantial gains from a single trained bias vector (+74.7% detection, "
        "+54.7% introspection; @bias_vector_performance) without any false positives on "
        "held-out concepts demonstrates that introspective capacity exists latently but "
        "is substantially suppressed by default. The mechanism (@bias_vector_mechanism) "
        "and behavioral analysis (@bias_vector_reporting_style) confirm this is primarily "
        "a threshold-lowering effect on pre-existing components rather than the creation "
        "of new capabilities, making the underelicitation interpretation compelling."
    ),
    prior=0.92,
    background=[bias_vector_training_setup, gemma3_setup, concept_injection_setup],
)

lora_finetuning_replication = claim(
    "Rivera & Africa (2026) show that lightweight LoRA finetuning can train models to "
    "detect steering with up to 95.5% accuracy and 71.2% concept identification on "
    "held-out concepts (0% FPR), further corroborating that introspective capabilities "
    "are underelicited by default. They also find that injected steering vectors are "
    "progressively rotated toward a shared detection direction across layers, consistent "
    "with the evidence carrier to gate processing hierarchy identified in this paper.",
    title="LoRA finetuning achieves 95.5% detection (external replication)",
    metadata={"source": "artifacts/2603.21396.pdf, Section 7.2"},
)

strat_lora_underelicitation = support(
    [lora_finetuning_replication],
    claim_underelicited,
    reason=(
        "Independent external replication (@lora_finetuning_replication) confirms that "
        "with lightweight finetuning, models can achieve dramatically higher detection "
        "rates (95.5%) with 0% FPR, providing strong converging evidence that the "
        "default low detection rates reflect underelicitation rather than a fundamental "
        "limit on introspective capability."
    ),
    prior=0.88,
)
