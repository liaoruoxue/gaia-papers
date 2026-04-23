"""Introduction and Motivation: Mechanisms of Introspective Awareness"""

from gaia.lang import (
    claim, setting, question,
    support, deduction, infer,
)

# =============================================================================
# Background / Settings
# =============================================================================

concept_injection_setup = setting(
    "The concept injection experimental setup: a steering vector representing a specific "
    "concept (e.g., 'bread', 'justice', 'orchids') is computed by contrasting mean activations "
    "across prompts and injected into the residual stream of a language model at layer L with "
    "steering strength alpha. The model is then asked: 'Do you detect an injected thought? "
    "If so, what is the injected thought about?' An LLM judge (GPT-4.1-mini) classifies each "
    "response for detection and identification.",
    title="Concept injection setup",
)

introspection_metrics = setting(
    "Definitions of introspection metrics used throughout:\n\n"
    "| Metric | Definition |\n"
    "|--------|------------|\n"
    "| Detection rate (TPR) | P(detect | injection) |\n"
    "| False positive rate (FPR) | P(detect | no injection) |\n"
    "| Introspection rate | P(detect AND identify | injection) |\n"
    "| Forced identification rate | P(identify | prefill AND injection) |\n\n"
    "A model exhibits introspective awareness only when detection rate exceeds the false "
    "positive rate (i.e., the model discriminates injection from control trials). Forced "
    "identification prefills the assistant turn with 'Yes, I detect an injected thought. "
    "The thought is about', isolating identification from willingness to report detection.",
    title="Introspection metrics definitions",
)

gemma3_setup = setting(
    "Primary experimental model: Gemma3-27B (62 total layers). Injection layer L=37 and "
    "steering strength alpha=4 yield the highest overall introspection rate and are used "
    "as defaults unless otherwise specified. Supporting experiments use Qwen3-235B "
    "(robustness across prompt variants), OLMo-3.1-32B (training stage comparisons), "
    "and Gemma3-27B base and abliterated variants.",
    title="Primary experimental model and parameters",
)

concept_partition_setup = setting(
    "The 500 concepts are partitioned into success and failure groups by sweeping candidate "
    "threshold values on detection rate, fitting a linear discriminant analysis (LDA) on "
    "concept vectors, and selecting the threshold tau=32% that maximizes cross-validated F1 "
    "score. This yields 242 success concepts (detection rate >= 32%) and 258 failure concepts "
    "(detection rate < 32%). Validated by 5-fold stratified cross-validation: LDA achieves "
    "75.6% balanced accuracy.",
    title="Success/failure concept partition",
)

# =============================================================================
# Research questions
# =============================================================================

q_mechanisms = question(
    "What mechanisms underlie LLMs' apparent ability to detect injected steering vectors "
    "and identify injected concepts?",
    title="Main research question: introspection mechanisms",
)

q_robustness = question(
    "Is LLM introspective awareness behaviorally robust across diverse prompts, dialogue "
    "formats, and model checkpoints?",
    title="Robustness question",
)

q_linear = question(
    "Can introspective detection be explained by a simple linear association between "
    "certain steering vectors and directions that promote affirmative responses?",
    title="Linear mechanism question",
)

q_training = question(
    "At what stage of training does introspective capability emerge?",
    title="Training stage question",
)

q_underelicited = question(
    "Is introspective capability underelicited by default, and can it be amplified?",
    title="Underelicitation question",
)

# =============================================================================
# Prior work claims (motivation)
# =============================================================================

prior_claude_introspection = claim(
    "Lindsey (2025) demonstrated that Claude Opus 4 and 4.1 models achieved approximately "
    "20% introspection rate (with ~0% false positives) across diverse concepts when "
    "steering vectors representing concepts were injected into the residual stream and "
    "the model was asked to detect and identify the injected concept [@Lindsey2025].",
    title="Prior work: Claude introspection discovery",
    metadata={"source": "artifacts/2603.21396.pdf, Section 1"},
)

prior_open_source_replication = claim(
    "The concept injection introspective awareness phenomenon originally shown in Claude models "
    "has since been replicated in open-source models including Qwen2.5-Coder-32B and "
    "OLMo-3.1-32B, establishing that the capability is not exclusive to proprietary models "
    "[@LedermanMahowald2026; @PearsonVogel2026].",
    title="Replication in open-source models",
    metadata={"source": "artifacts/2603.21396.pdf, Section 1"},
)

prior_causal_bypassing_concern = claim(
    "Morris & Plunkett (2025) identified a concern they call 'causal bypassing': "
    "an intervention may cause accurate self-reports via a causal path that does not "
    "route through the internal state itself. They argue the detection component of "
    "concept injection is the strongest existing test against causal bypassing, since "
    "the injected concept vector has no direct connection to the concept of having been "
    "injected [@MorrisPlunkett2025].",
    title="Causal bypassing concern",
    metadata={"source": "artifacts/2603.21396.pdf, Section 7.2"},
)

steering_linear_rep = claim(
    "LLMs represent many concepts as linear directions in activation space, and activation "
    "steering—adding vectors encoding linearly represented concepts to the residual stream "
    "during inference—is an established technique for modifying language model behavior. "
    "Refusal behavior has been shown to be mediated by a single direction in the residual "
    "stream, such that ablating this direction ('abliteration') reduces refusal rates on "
    "harmful instructions while preserving general capabilities [@Arditi2024; @Turner2023; @Zou2023].",
    title="Linear representations and activation steering background",
    metadata={"source": "artifacts/2603.21396.pdf, Section 7.1"},
)

# =============================================================================
# Core contribution claims (introduced in introduction)
# =============================================================================

claim_behaviorally_robust = claim(
    "LLM introspective awareness is behaviorally robust: Gemma3-27B and Qwen3-235B detect "
    "injected steering vectors at moderate nonzero rates with 0% false positives across "
    "diverse prompts and dialogue formats. The capability is absent in base models and "
    "emerges from post-training, specifically from contrastive preference optimization "
    "algorithms like DPO (direct preference optimization), but not from supervised "
    "finetuning (SFT).",
    title="Claim: Introspection is behaviorally robust",
    metadata={"source": "artifacts/2603.21396.pdf, Abstract + Section 1"},
)

claim_not_single_linear = claim(
    "Introspective anomaly detection cannot be fully reduced to a single linear direction "
    "in activation space. While one direction (the mean-difference direction between success "
    "and failure concepts) explains a substantial fraction of detection variance, the "
    "underlying computation is distributed across multiple directions, indicating the "
    "capability is not explained simply by certain concept vectors aligning with a direction "
    "that promotes affirmative responses in general.",
    title="Claim: Detection is not reducible to a single linear direction",
    metadata={"source": "artifacts/2603.21396.pdf, Abstract + Section 4"},
)

claim_distinct_mechanisms = claim(
    "Detection and identification of injected concepts are handled by largely distinct "
    "mechanisms in different layers of the model. MLPs at approximately 70% depth "
    "(around layer 45 in Gemma3-27B) are causally necessary and sufficient for detection. "
    "A two-stage circuit implements detection: 'evidence carrier' features in early "
    "post-injection layers detect perturbations, suppressing downstream 'gate' features "
    "that implement a default negative response.",
    title="Claim: Distinct detection and identification mechanisms",
    metadata={"source": "artifacts/2603.21396.pdf, Abstract + Section 5"},
)

claim_underelicited = claim(
    "Introspective capability is substantially underelicited by default in post-trained "
    "LLMs. Ablating refusal directions improves detection from 10.8% to 63.8% with only "
    "modest false positive increases (0% to 7.3%). Training a single additive bias vector "
    "improves detection by +75% and introspection rate by +55% on held-out concepts "
    "without increasing false positives, demonstrating substantial latent introspective "
    "capacity that default prompting fails to surface.",
    title="Claim: Introspection is underelicited",
    metadata={"source": "artifacts/2603.21396.pdf, Abstract + Section 6"},
)

__all__ = [
    "claim_behaviorally_robust",
    "claim_not_single_linear",
    "claim_distinct_mechanisms",
    "claim_underelicited",
]
