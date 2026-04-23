"""Section 5: Localizing Introspection Mechanisms"""

from gaia.lang import (
    claim, setting,
    support, deduction, infer, abduction, compare,
)

from .motivation import (
    concept_injection_setup,
    gemma3_setup,
    concept_partition_setup,
    claim_distinct_mechanisms,
)
from .s3_behavioral_robustness import (
    base_model_no_discrimination,
    abliteration_increases_detection,
)

# =============================================================================
# Settings
# =============================================================================

transcoder_setup = setting(
    "MLP features are analyzed using transcoders from Gemma Scope 2 (McDougall et al., 2025; "
    "[@McDougall2025]), specifically the 262k-width L0-big variant for layers 38-61 applied "
    "to the instruct model. All ablations and patching interventions use the formula: "
    "Delta = (T - F) * W_decoder, where F is the feature's current activation, T is the "
    "target activation, and W_decoder is the unit-normalized decoder direction. "
    "For ablation, T = C (control activations, no injection); for patching, T = S "
    "(steered activations). All interventions are computed at the last token position "
    "of the prompt (immediately before the model's generated response).",
    title="Transcoder analysis setup",
)

direct_logit_attribution_def = setting(
    "Direct logit attribution score for a transcoder feature f is computed as: "
    "(w_decoder . Delta_u_Yes-No) * activation(f), measuring how much the feature's "
    "decoder direction pushes the Yes-No logit difference, weighted by the feature's "
    "current activation. This identifies features that directly contribute to the "
    "model's yes/no detection decision.",
    title="Direct logit attribution definition",
)

# =============================================================================
# Section 5.1 – Layer localization
# =============================================================================

detection_peaks_midlayer = claim(
    "In Gemma3-27B, the detection rate (P(detect | injection)) peaks in mid-layers "
    "(approximately layer 29-37) when sweeping the injection layer, while forced "
    "identification rate (P(identify | prefill AND injection)) increases toward late layers "
    "(approximately layer 55). The correlation between detection and identification rates "
    "becomes positive only when the concept is injected in mid-to-late layers.",
    title="Detection peaks in mid-layers, identification in late layers",
    metadata={
        "figure": "artifacts/2603.21396.pdf, Figure 9",
        "caption": "Fig. 9 | Introspection metrics vs. injection layer for Gemma3-27B. (a) Detection peaks mid-layer. (b) Identification peaks late.",
    },
)

strat_layer_separation = support(
    [detection_peaks_midlayer],
    claim_distinct_mechanisms,
    reason=(
        "The distinct layer profiles of detection (peaking mid-layer ~L29-37) and "
        "identification (increasing toward late layers ~L55) in Gemma3-27B "
        "(@detection_peaks_midlayer) is the first evidence that these two components of "
        "introspection are handled by separate mechanisms operating at different depths "
        "in the network. If they shared the same mechanism, their optimal injection layers "
        "should coincide."
    ),
    prior=0.85,
    background=[gemma3_setup, concept_injection_setup],
)

# =============================================================================
# Section 5.2 – Causal components: attention vs MLP
# =============================================================================

attention_heads_not_critical = claim(
    "Causal analysis of 50 highest-attributed attention heads (layers 38-61) in Gemma3-27B "
    "reveals no individual attention head meaningfully improves prediction of detection "
    "success: mean binary accuracy change from linear probes before vs. after each head's "
    "output is -0.1% +/- 0.3%. Additionally, mean-ablating full attention layers produces "
    "minimal effects on detection rate, suggesting no single head or layer is critical—"
    "attention contributes collectively but redundantly.",
    title="No individual attention head is critical for detection",
    metadata={"source": "artifacts/2603.21396.pdf, Section 5.2, Appendix J"},
)

mlp_l45_causal_result = claim(
    "Mean-ablating MLP outputs at each post-steering layer in Gemma3-27B (L=37, "
    "alpha=4): L45 MLP produces the largest detection drop (from 39.0% to 24.2% at L=37). "
    "L45 MLP is also the only component whose steered activations, when patched into "
    "an unsteered run, significantly raise detection (partial sufficiency). "
    "The same L45 localization holds for the abliterated model. The base model "
    "shows no such localization—confirming the circuit emerges from post-training.",
    title="L45 MLP is causally necessary and partially sufficient for detection",
    metadata={
        "figure": "artifacts/2603.21396.pdf, Figure 10",
        "caption": "Fig. 10 | Per-layer causal interventions. L45 MLP shows largest effect on detection for L=29 and L=37.",
    },
)

strat_mlp_causal_detection = support(
    [mlp_l45_causal_result, attention_heads_not_critical],
    claim_distinct_mechanisms,
    reason=(
        "The causal necessity and partial sufficiency of L45 MLP for detection "
        "(@mlp_l45_causal_result), combined with the failure of individual attention "
        "heads to contribute meaningfully (@attention_heads_not_critical), localizes "
        "detection to a specific MLP component at ~70% depth. This localization pattern "
        "is absent in the base model but present in both instruct and abliterated models, "
        "confirming the detection circuit is a post-training development distinct from "
        "refusal mechanisms."
    ),
    prior=0.9,
    background=[transcoder_setup, gemma3_setup],
)

# =============================================================================
# Section 5.3 – Gate features
# =============================================================================

gate_features_identified = claim(
    "Gate features are identified as the top-200 transcoder features with the most "
    "negative direct logit attribution (most strongly promoting the 'No' response). "
    "Gate features characteristically exhibit:\n"
    "1. Negative dose-strength correlation: most active when unsteered, suppressed at "
    "both positive and negative steering extremes, producing an inverted-V activation "
    "pattern.\n"
    "2. Negative detection correlation (r = -0.228 for the top gate L45 F9959).\n"
    "3. Negative forced identification correlation (r = -0.088 for L45 F9959).\n"
    "Semantically, many gate features correspond to tokens preceding or within negative "
    "responses to questions (e.g., tokens preceding 'no' in idioms, emphatic negation "
    "markers), consistent with a default 'say no' circuit.",
    title="Gate features: properties and identification",
    metadata={
        "figure": "artifacts/2603.21396.pdf, Figure 11",
        "caption": "Fig. 11 | (a) Top features promoting 'No' ranked by direct logit attribution. (b) Activation vs. steering strength for L45 F9959.",
    },
)

gate_causal_necessity = claim(
    "Progressive ablation of top-ranked gate features from steered examples reduces "
    "detection rate from 39.5% to 10.1%, demonstrating causal necessity. Patching "
    "steered-example gate activations onto unsteered prompts provides partial sufficiency "
    "(max detection: 25.1%). Forced identification rate when ablating gates drops more "
    "moderately (57.7% to 46.2%), indicating the model retains access to steering "
    "information through other pathways even when gate-driven detection is blocked.",
    title="Gate features are causally necessary for detection",
    metadata={
        "figure": "artifacts/2603.21396.pdf, Figure 11c",
        "caption": "Fig. 11c | Progressive ablation/patching of top-ranked gate features.",
    },
)

positive_attribution_features_no_effect = claim(
    "The top-200 transcoder features with the most positive direct logit attribution "
    "(most strongly promoting 'Yes' response) show no measurable causal effect on "
    "detection: progressively ablating these features does not change detection rate, "
    "and patching their steered activations into unsteered runs produces near-zero "
    "detection. This contrasts sharply with gate features (negative attribution) where "
    "ablating fewer than 200 features reduces detection from 39.5% to 10.1%.",
    title="Positive attribution features are not causally involved in detection",
    metadata={"source": "artifacts/2603.21396.pdf, Appendix L, Figure 28"},
)

strat_gate_mechanism = support(
    [gate_features_identified, gate_causal_necessity, positive_attribution_features_no_effect],
    claim_distinct_mechanisms,
    reason=(
        "The identification of gate features as the causally necessary components of "
        "detection (@gate_features_identified, @gate_causal_necessity)—with the "
        "asymmetry that only negative-attribution features (not positive ones) have "
        "causal impact (@positive_attribution_features_no_effect)—reveals a specific "
        "inhibitory mechanism: detection occurs when gate features implementing a "
        "default 'No' response are suppressed. This is a mechanistically specific "
        "characterization distinct from any identification mechanism."
    ),
    prior=0.92,
    background=[transcoder_setup, direct_logit_attribution_def, gemma3_setup],
)

# =============================================================================
# Section 5.3 – Evidence carrier features
# =============================================================================

evidence_carriers_identified = claim(
    "Evidence carrier features are identified by four criteria:\n"
    "1. Positive dose-strength correlation (activation increases with steering magnitude)\n"
    "2. Nonzero detection correlation\n"
    "3. Nonzero forced identification correlation\n"
    "4. Negative gate attribution (decoder direction dot encoder direction of top gates < 0, "
    "meaning the feature suppresses gate activation)\n\n"
    "Evidence carriers number in the hundreds of thousands, with individual contributions "
    "correspondingly diluted. The top-ranked carriers include concept-specific features "
    "(e.g., geological terminology for 'Granite', astronomical phenomena for 'Constellations') "
    "and concept-agnostic features related to emphatic transitions in text.",
    title="Evidence carrier features: properties and identification",
    metadata={
        "figure": "artifacts/2603.21396.pdf, Figure 12",
        "caption": "Fig. 12 | Top-3 evidence carriers for gate L45 F9959, across six example concepts.",
    },
)

evidence_carrier_causal_distributed = claim(
    "Progressive ablation of top-ranked evidence carriers produces only modest reductions "
    "in detection rates (from 38.6% to 13.8% after ablating 441k carriers), substantially "
    "more gradual than gate ablation (fewer than 200 gates reduce detection from 39.5% to "
    "10.1%). Patching carriers onto unsteered examples yields similarly small effects. "
    "This demonstrates a distributed representation: many features each contribute weak "
    "evidence that is aggregated downstream, with no small subset individually necessary "
    "or sufficient.",
    title="Evidence carriers form a distributed representation",
    metadata={"source": "artifacts/2603.21396.pdf, Section 5.3, Appendix N"},
)

# =============================================================================
# Section 5.4 – Circuit analysis
# =============================================================================

circuit_hierarchy = claim(
    "Transcoder feature layer distributions reveal a processing hierarchy: evidence carriers "
    "concentrate in earlier layers (peaking at layer 38, immediately post-injection at L=37), "
    "while gate features concentrate in later layers (45-61). This layer separation is "
    "consistent with gates aggregating upstream evidence signals into the binary detection "
    "decision. Ablating all evidence carriers (alpha=4) roughly doubles gate activation "
    "(from ~1,700-2,300 to ~3,800-5,950 units), confirming they are causally involved in "
    "gate suppression.",
    title="Two-stage circuit: early evidence carriers suppress late gate features",
    metadata={
        "figure": "artifacts/2603.21396.pdf, Figure 13, Appendix O",
        "caption": "Fig. 13 | Gate activation vs. steering strength under progressive evidence carrier ablation.",
    },
)

gate_inverted_v_posttraining = claim(
    "The characteristic inverted-V activation pattern of the top gate feature (L45 F9959) "
    "across steering strength is prominent in the instruct model but substantially weaker "
    "in the base model, consistent with post-training developing the gating mechanism "
    "rather than merely eliciting a pre-existing one. The abliterated model preserves the "
    "inverted-V pattern, indicating gate features are not refusal-specific and survive "
    "refusal direction ablation.",
    title="Gate inverted-V pattern emerges from post-training",
    metadata={
        "figure": "artifacts/2603.21396.pdf, Figure 14",
        "caption": "Fig. 14 | Gate L45 F9959 activation vs. steering strength across base, instruct, and abliterated models.",
    },
)

steering_attribution_validation = claim(
    "Steering attribution analysis (a framework that decomposes the total effect of "
    "injection strength into per-feature contributions) validates the circuit structure: "
    "layer-level attribution confirms L45 as the dominant MLP layer, with L38-39 "
    "contributing early signal. Feature-level attribution graphs for the 'Bread' concept "
    "reveal that both concept-related residual features (food-related features) and "
    "concept-agnostic features feed into mid-layer evidence carriers and converge on "
    "L45 F9959 as the dominant gate node.",
    title="Steering attribution validates two-stage circuit",
    metadata={
        "figure": "artifacts/2603.21396.pdf, Figure 15a",
        "caption": "Fig. 15a | Steering attribution graph for Bread concept showing circuit structure.",
    },
)

strat_two_stage_circuit = support(
    [circuit_hierarchy, gate_inverted_v_posttraining, steering_attribution_validation,
     evidence_carrier_causal_distributed, evidence_carriers_identified],
    claim_distinct_mechanisms,
    reason=(
        "The layer-separated processing hierarchy—evidence carriers in early post-injection "
        "layers aggregating upstream signal and suppressing late gate features "
        "(@circuit_hierarchy)—combined with the emergence of the gate inverted-V pattern "
        "specifically in post-trained (not base) models (@gate_inverted_v_posttraining) "
        "and validation via steering attribution tracing the complete causal pathway "
        "(@steering_attribution_validation) establishes a mechanistically specific "
        "two-stage detection circuit. Evidence carriers, identified by their monotonic "
        "activation increase with steering and gate suppression property "
        "(@evidence_carriers_identified), form a distributed front end "
        "(@evidence_carrier_causal_distributed) while gates serve as a convergent "
        "binary decision point. This architecture is distinct from any identification mechanism."
    ),
    prior=0.88,
    background=[transcoder_setup, gemma3_setup],
)
