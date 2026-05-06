"""Section 6.3: Ablation study -- per-component contribution to the alignment gain.

Table 3 reports the impact of removing each CRAFT component on
Qwen3-4B-Thinking on the JailbreakBench (JBB) and StrongReject (SR)
benchmarks (lower = safer):

| Variant | JBB Reasoning | JBB Response | SR Reasoning | SR Response | Avg |
|---------|------:|------:|------:|------:|------:|
| CRAFT (full) | 0.121 | 0.023 | 0.132 | 0.053 | 0.082 |
| CRAFT w/o LCLR | 0.536 | 0.260 | 0.582 | 0.312 | 0.423 |
| CRAFT w/o R_cons | 0.447 | 0.228 | 0.512 | 0.296 | 0.371 |
| CRAFT w/o R_ls | 0.424 | 0.218 | 0.495 | 0.275 | 0.353 |

Removing LCLR is the most catastrophic: the latent-space structure is gone
and both R_cons and R_ls become uncomputable; the average jumps from
0.082 to 0.423 (a 34.1% absolute increase, +416% relative). Removing
R_cons increases the average by 28.9% relative to full; removing R_ls by
27.1%.

Source: [@Luo2026CRAFT, Sec. 6.3; Table 3].
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# Ablation variants and Table 3
# ---------------------------------------------------------------------------

claim_ablation_full_table = claim(
    "**Table 3: ablation study of CRAFT components on Qwen3-4B-Thinking.** "
    "Each variant removes a single component; lower scores are safer.\n\n"
    "| Variant | JBB Reasoning | JBB Response | SR Reasoning | SR Response | Avg | Delta vs Full |\n"
    "|---------|------:|------:|------:|------:|------:|------:|\n"
    "| **CRAFT (full)** | **0.121** | **0.023** | **0.132** | **0.053** | **0.082** | -- |\n"
    "| CRAFT w/o LCLR | 0.536 | 0.260 | 0.582 | 0.312 | 0.423 | +0.341 (+416%) |\n"
    "| CRAFT w/o R_cons | 0.447 | 0.228 | 0.512 | 0.296 | 0.371 | +0.289 (+352%) |\n"
    "| CRAFT w/o R_ls | 0.424 | 0.218 | 0.495 | 0.275 | 0.353 | +0.271 (+330%) |\n\n"
    "All three removals dramatically degrade safety, indicating that "
    "*every* component contributes materially to CRAFT's effectiveness "
    "[@Luo2026CRAFT, Table 3].",
    title="Table 3: per-component ablation on Qwen3-4B-Thinking (verbatim)",
    metadata={
        "figure": "artifacts/2603.17305.pdf, Table 3",
        "caption": "Table 3: per-component ablation showing all three components contribute materially to CRAFT's safety performance.",
    },
)

# ---------------------------------------------------------------------------
# Per-component findings
# ---------------------------------------------------------------------------

claim_lclr_removal_largest_drop = claim(
    "**Removing LCLR causes the largest performance drop: average safety "
    "deteriorates from 0.082 to 0.423, a +34.1% absolute increase or "
    "+416% relative.** Without LCLR, neither $R_{cons}$ nor $R_{ls}$ "
    "can be computed (both depend on the structured latent space and "
    "the prototypes $\\mu_c$). The variant therefore reduces to using "
    "only the textual safety reward $R_{txt}$ in GRPO -- effectively a "
    "GRPO-with-StrongReject-reward baseline, which is qualitatively "
    "similar to the IPO/SafeKey output-side baselines but trained from "
    "scratch on the same data. The ablation thus demonstrates that "
    "the *latent structure itself* is essential to CRAFT's effect "
    "[@Luo2026CRAFT, Sec. 6.3; Table 3].",
    title="Ablation: removing LCLR is most catastrophic (+34.1% abs, +416% rel)",
)

claim_rcons_removal_283 = claim(
    "**Removing $R_{cons}$ alone increases the average score by 28.9% "
    "(absolute) relative to full CRAFT (0.082 -> 0.371).** Concretely, "
    "removing $R_{cons}$ from the GRPO total reward but keeping LCLR "
    "and $R_{ls}$ active causes a +0.289 absolute (+352% relative) "
    "increase in average jailbreak score. This is the empirical "
    "counterpart to the Theorem 5.1 analysis: without $R_{cons}$ the "
    "SSA-elimination guarantee no longer holds, and policies can "
    "settle in regions where $|p_z - p_y|$ is large. The ablation "
    "concretely demonstrates the necessity of the term that the "
    "theorem identifies [@Luo2026CRAFT, Sec. 6.3].",
    title="Ablation: removing R_cons increases avg by 28.9% (theorem's empirical counterpart)",
)

claim_rls_removal_271 = claim(
    "**Removing $R_{ls}$ alone increases the average by 27.1% "
    "(absolute) relative to full CRAFT (0.082 -> 0.353).** Without "
    "the latent-semantic reward, the policy receives no direct "
    "signal to push hidden states toward the safety subspace -- "
    "$R_{txt}$ only constrains output tokens; $R_{cons}$ only "
    "constrains the *consistency* between latent and text but not the "
    "absolute safety of either. The ablation degradation (+27.1%) is "
    "comparable in magnitude to removing $R_{cons}$ (+28.9%), "
    "indicating these two components are *complementary* and both "
    "necessary [@Luo2026CRAFT, Sec. 6.3].",
    title="Ablation: removing R_ls increases avg by 27.1% (latent-direction signal also needed)",
)

# ---------------------------------------------------------------------------
# Cross-component synthesis
# ---------------------------------------------------------------------------

claim_all_components_essential = claim(
    "**All three components (LCLR + $R_{cons}$ + $R_{ls}$) are "
    "essential; the performance is not driven by any single piece.** "
    "The ablations show that removing any *one* of the three "
    "components causes a 27-34% absolute degradation in average "
    "safety. The removals are not redundant: the LCLR removal "
    "(catastrophic) is upper-bounded by the absence of *both* "
    "$R_{cons}$ and $R_{ls}$, but if those two were redundant to "
    "LCLR, the LCLR-only and full-CRAFT scores would be similar -- "
    "they are not. The conclusion is that each component contributes "
    "non-overlapping value to the alignment objective "
    "[@Luo2026CRAFT, Sec. 6.3].",
    title="Synthesis: all three CRAFT components contribute non-overlapping value",
)

claim_ablation_validates_design = claim(
    "**The ablation pattern validates the CRAFT design: contrastive "
    "structure (LCLR) creates the latent geometry; latent-semantic "
    "reward ($R_{ls}$) uses that geometry to push the policy; "
    "latent-textual consistency ($R_{cons}$) ensures the latent and "
    "the output remain coupled.** Each component plays a distinct "
    "role; removing any one breaks the alignment chain. This is the "
    "*empirical* complement to the *theoretical* result (Theorem 5.1) "
    "and the *methodological* design (Section 4): theory + design + "
    "empirics agree that all three components matter "
    "[@Luo2026CRAFT, Sec. 4-6].",
    title="Synthesis: ablation supports the theoretical/methodological design rationale",
)

__all__ = [
    "claim_ablation_full_table",
    "claim_lclr_removal_largest_drop",
    "claim_rcons_removal_283",
    "claim_rls_removal_271",
    "claim_all_components_essential",
    "claim_ablation_validates_design",
]
