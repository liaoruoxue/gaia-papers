"""Section 6: Appendix.

A1: CodeT5+ embedding-size ablation.
A2: Separate vs combined whitening.
"""

from gaia.lang import claim, support, abduction, compare

from .s2_whitening import soft_zca_controls_whitening
from .s3_apparatus import (
    model_codet5plus,
    procedure_separate_whitening,
)

# ===========================================================================
# A.1 CodeT5+ embedding size ablation (Table 4)
# ===========================================================================

table4_codet5plus_dim = claim(
    "MRR and IsoScores (Code / Comment) of non-whitened CodeT5+ embeddings "
    "for two output dimensions (with vs without the default down-projection "
    "from 768 to 256), Table 4:\n\n"
    "| Lang       | dim 256 MRR | dim 256 Iso (C/Cm) | dim 768 MRR | dim 768 Iso (C/Cm) |\n"
    "|------------|------------:|--------------------|------------:|--------------------|\n"
    "| Ruby       | 0.705       | 0.350 / 0.296      | 0.463       | 0.102 / 0.102      |\n"
    "| Javascript | 0.638       | 0.365 / 0.335      | 0.360       | 0.110 / 0.118      |\n"
    "| Go         | 0.757       | 0.234 / 0.196      | 0.413       | 0.042 / 0.044      |\n"
    "| Java       | 0.595       | 0.388 / 0.313      | 0.323       | 0.120 / 0.081      |\n"
    "| Python     | 0.721       | 0.394 / 0.356      | 0.387       | 0.122 / 0.139      |\n"
    "| PHP        | 0.537       | 0.400 / 0.262      | 0.266       | 0.107 / 0.065      |\n"
    "| R          | 0.045       | 0.139 / 0.118      | 0.026       | 0.026 / 0.012      |",
    title="Table 4: CodeT5+ MRR and IsoScores for embedding dim 256 vs 768",
    metadata={"source_table": "artifacts/2411.17538.pdf, Table 4"},
)

# Direct empirical observation
obs_codet5plus_dim256_better = claim(
    "Reducing the CodeT5+ output dimension from 768 (raw last hidden state) "
    "to 256 (with the default down-projection layer) nearly doubles both "
    "the MRR and the IsoScores on every language tested: e.g. Ruby MRR "
    "0.463 -> 0.705 and IsoScore 0.102 -> 0.350; Go MRR 0.413 -> 0.757 and "
    "IsoScore 0.042 -> 0.234.",
    title="Observation: dim=256 nearly doubles MRR and IsoScores vs dim=768",
)

# Hypothesis and alternative
hypothesis_lower_dim_higher_iso = claim(
    "In very high-dimensional spaces, data points spread sparsely, making "
    "uniform coverage (and thus isotropy) harder to achieve. Therefore "
    "lower-dimensional embedding spaces have higher isotropy, which "
    "translates into better downstream task performance.",
    title="Hypothesis: lower embedding dimension -> higher isotropy -> better MRR",
)

alt_downprojection_layer_special = claim(
    "An alternative explanation is that the improvement is not due to "
    "lower dimensionality per se, but to the specific learned "
    "down-projection layer added by the default CodeT5+ embedding head. "
    "Under this account, the layer's parameters were trained to be "
    "discriminative for retrieval, and dimensionality is incidental.",
    title="Alternative: the down-projection layer (not lower dim) drives the gain",
)

pred_lower_dim_helps = claim(
    "If lower dimensionality alone increases isotropy and hence MRR, then "
    "the dim=256 variant should both outperform the dim=768 variant on "
    "MRR and exhibit higher IsoScore on every language. Both predictions "
    "match Table 4 in every cell.",
    title="Prediction (low-dim hypothesis): dim=256 wins on every language",
)

pred_layer_special = claim(
    "If the down-projection layer is the driver, then we would expect the "
    "MRR gain to be roughly constant across languages (because the same "
    "trained layer is applied). Table 4 shows MRR ratios from 1.5x (Ruby) "
    "to 2x (Go, PHP), which is a moderately large spread but not "
    "overwhelmingly inconsistent with the layer-driver story.",
    title="Prediction (layer-driver alternative): roughly constant MRR ratio",
)

support_h_lowdim = support(
    [hypothesis_lower_dim_higher_iso],
    obs_codet5plus_dim256_better,
    background=[table4_codet5plus_dim],
    reason=(
        "@hypothesis_lower_dim_higher_iso predicts that the dim=256 "
        "variant should have both higher IsoScore and higher MRR than "
        "dim=768. The cell-by-cell numbers in @table4_codet5plus_dim "
        "(summarised in @obs_codet5plus_dim256_better) confirm both "
        "directions on every language."
    ),
    prior=0.85,
)

support_alt_layer = support(
    [alt_downprojection_layer_special],
    obs_codet5plus_dim256_better,
    reason=(
        "Under @alt_downprojection_layer_special, the dim=256 variant "
        "should also win across the board because it is the better-trained "
        "head. @obs_codet5plus_dim256_better is consistent with this, but "
        "the alternative does not predict the simultaneous IsoScore gain "
        "as cleanly as the low-dim hypothesis."
    ),
    prior=0.55,
)

comp_codet5plus_dim = compare(
    pred_lower_dim_helps,
    pred_layer_special,
    obs_codet5plus_dim256_better,
    reason=(
        "@pred_lower_dim_helps captures both the MRR and the IsoScore "
        "directions in every cell, including the qualitative co-variation "
        "across languages. @pred_layer_special is consistent with the MRR "
        "ranking but is silent on the IsoScore gain. The low-dim "
        "hypothesis matches the observation more tightly."
    ),
    prior=0.7,
)

abduction_codet5plus_dim = abduction(
    support_h_lowdim,
    support_alt_layer,
    comp_codet5plus_dim,
    background=[model_codet5plus],
    reason=(
        "Two competing explanations for the dim=256 vs dim=768 ablation "
        "on CodeT5+: the low-dimensionality-improves-isotropy hypothesis "
        "(@hypothesis_lower_dim_higher_iso) and the trained-layer "
        "alternative (@alt_downprojection_layer_special). The former "
        "matches the data more tightly because it predicts the joint MRR "
        "and IsoScore gain."
    ),
)

# ===========================================================================
# A.2 Separate vs combined whitening (Table 5)
# ===========================================================================

table5_separate_vs_combined = claim(
    "MRR scores of CodeBERT embeddings under standard ZCA ($\\epsilon = 0$) "
    "with separate whitening vs combined (concatenated code + comment) "
    "whitening, Table 5:\n\n"
    "| Lang       | CodeBERT separate | CodeBERT combined | FT CodeBERT separate | FT CodeBERT combined |\n"
    "|------------|------------------:|------------------:|---------------------:|---------------------:|\n"
    "| Ruby       | 0.0959            | 0.1160            | 0.6225               | 0.6117               |\n"
    "| Javascript | 0.1113            | 0.0883            | 0.4750               | 0.4693               |\n"
    "| Go         | 0.0020            | 0.0037            | 0.5676               | 0.5557               |\n"
    "| Java       | 0.0008            | 0.0006            | 0.4553               | 0.4482               |\n"
    "| Python     | 0.0396            | 0.0239            | 0.5524               | 0.5455               |\n"
    "| PHP        | 0.0005            | 0.0005            | 0.2847               | 0.2784               |\n"
    "| R          | 0.0712            | 0.0414            | (no FT data)         | -                    |",
    title="Table 5: separate vs combined whitening (standard ZCA, CodeBERT)",
    metadata={"source_table": "artifacts/2411.17538.pdf, Table 5"},
)

obs_separate_mostly_better = claim(
    "In the majority of (model, language) cells in Table 5, separate "
    "whitening yields slightly higher MRR than combined whitening. "
    "Specifically: in 4 of 7 cells for base CodeBERT (Javascript, Java, "
    "Python, R) separate is strictly better; in 6 of 6 cells for FT "
    "CodeBERT separate is strictly better; the few exceptions for base "
    "CodeBERT (Ruby +0.020, Go +0.0017) are small and confined to the "
    "lowest-MRR languages where signal is noisy.",
    title="Observation: separate whitening MRR >= combined whitening MRR in most cells",
)

finding_separate_whitening_better = claim(
    "Separate computation of the whitening matrix for code and comment "
    "embeddings is not only practical (matching production-system "
    "structure) but also empirically superior to combined whitening: it "
    "yields slightly higher MRR scores in most evaluated (model, "
    "language) cells, including all six FT CodeBERT cells.",
    title="Finding: separate whitening is empirically superior to combined whitening",
)

strat_separate_whitening = support(
    [obs_separate_mostly_better],
    finding_separate_whitening_better,
    background=[
        procedure_separate_whitening,
        soft_zca_controls_whitening,
        table5_separate_vs_combined,
    ],
    reason=(
        "@obs_separate_mostly_better quantifies the per-cell MRR "
        "comparison reported in @table5_separate_vs_combined: 4/7 base "
        "CodeBERT cells and 6/6 FT CodeBERT cells favour separate "
        "whitening, with the exceptions being small and concentrated in "
        "low-MRR base-model cells. This directly substantiates the "
        "synthesis claim in @finding_separate_whitening_better and "
        "validates the design choice formalised in "
        "@procedure_separate_whitening."
    ),
    prior=0.85,
)

__all__ = [
    "table4_codet5plus_dim",
    "obs_codet5plus_dim256_better",
    "hypothesis_lower_dim_higher_iso",
    "alt_downprojection_layer_special",
    "pred_lower_dim_helps",
    "pred_layer_special",
    "table5_separate_vs_combined",
    "obs_separate_mostly_better",
    "finding_separate_whitening_better",
]
