"""Section 4: Results.

Reports MRR and IsoScores for non-whitened and whitened embeddings, and
synthesises the empirical findings on isotropy and code-search performance.
"""

from gaia.lang import claim, support, induction, abduction, compare, contradiction

from .motivation import (
    contribution_softzca_method,
    contribution_experimental_validation,
    contribution_isotropy_analysis,
    contrastive_finetuning_limited,
    code_search_anisotropy_problem,
    anisotropy_harms_semantics,
    research_gap,
)
from .s2_whitening import (
    soft_zca_controls_whitening,
    zca_amplifies_noise_at_small_eigenvalues,
)
from .s3_apparatus import (
    dataset_codesearchnet,
    dataset_statcodesearch,
    model_codebert,
    model_codet5plus,
    model_codellama,
    model_finetuned_codebert,
    metric_isoscore,
    metric_mrr,
    procedure_separate_whitening,
    table1_model_details,
)

# ---------------------------------------------------------------------------
# Table 2: Baseline (non-whitened) MRR and IsoScores
# ---------------------------------------------------------------------------

table2_nonwhitened = claim(
    "Reported MRR and IsoScores (Code / Comment) on the non-whitened "
    "embeddings (Table 2):\n\n"
    "| Lang       | CodeBERT MRR | CodeBERT Iso (C/Cm) | FT CodeBERT MRR | FT CodeBERT Iso | CodeT5+ MRR | CodeT5+ Iso | Code Llama MRR | Code Llama Iso |\n"
    "|------------|-------------:|---------------------|----------------:|------------------|------------:|-------------|---------------:|----------------|\n"
    "| Ruby       | 0.006        | 0.007 / 0.014       | 0.547           | 0.052 / 0.062    | 0.705       | 0.350 / 0.296 | 0.047        | 0.008 / 0.003 |\n"
    "| Javascript | 0.002        | 0.005 / 0.013       | 0.427           | 0.065 / 0.072    | 0.638       | 0.365 / 0.335 | 0.026        | 0.010 / 0.002 |\n"
    "| Go         | 0.002        | 0.006 / 0.010       | 0.619           | 0.050 / 0.036    | 0.757       | 0.234 / 0.196 | 0.031        | 0.006 / 0.003 |\n"
    "| Java       | 0.000        | 0.007 / 0.007       | 0.395           | 0.059 / 0.067    | 0.595       | 0.388 / 0.313 | 0.015        | 0.009 / 0.002 |\n"
    "| Python     | 0.001        | 0.006 / 0.021       | 0.500           | 0.067 / 0.071    | 0.721       | 0.394 / 0.356 | 0.017        | 0.007 / 0.005 |\n"
    "| PHP        | 0.000        | 0.006 / 0.007       | 0.248           | 0.072 / 0.048    | 0.537       | 0.400 / 0.262 | 0.009        | 0.009 / 0.001 |\n"
    "| R          | 0.011        | 0.005 / 0.004       | (no FT data)    | -                | 0.045       | 0.139 / 0.118 | 0.024        | 0.002 / 0.002 |",
    title="Baseline non-whitened MRR and IsoScores (Table 2)",
    metadata={"source_table": "artifacts/2411.17538.pdf, Table 2"},
)

# ---------------------------------------------------------------------------
# Table 3: MRR improvement after Soft-ZCA whitening at the best epsilon
# ---------------------------------------------------------------------------

table3_whitened_delta = claim(
    "Reported MRR improvement vs non-whitened embeddings ($\\Delta$MRR) and "
    "IsoScores (Code / Comment) after applying Soft-ZCA at the best epsilon "
    "for each (model, language) cell (Table 3):\n\n"
    "| Lang       | CodeBERT $\\Delta$MRR | CodeBERT Iso     | FT CodeBERT $\\Delta$MRR | FT CodeBERT Iso  | CodeT5+ $\\Delta$MRR | CodeT5+ Iso      | Code Llama $\\Delta$MRR | Code Llama Iso   |\n"
    "|------------|---------------------:|------------------|------------------------:|------------------|--------------------:|------------------|----------------------:|------------------|\n"
    "| Ruby       | +0.230               | 0.365 / 0.511    | +0.075                  | 0.998 / 0.998    | +0.007              | 0.377 / 0.340    | +0.476                | 0.224 / 0.298    |\n"
    "| Javascript | +0.142               | 0.348 / 0.551    | +0.049                  | 0.992 / 0.994    | +0.003              | 0.394 / 0.367    | +0.369                | 0.299 / 0.428    |\n"
    "| Go         | +0.250               | 0.673 / 0.863    | +0.042                  | 0.998 / 0.998    |  0.000              | 0.317 / 0.291    | +0.465                | 0.257 / 0.433    |\n"
    "| Java       | +0.148               | 0.736 / 0.889    | +0.064                  | 0.991 / 0.992    | +0.002              | 0.522 / 0.495    | +0.329                | 0.453 / 0.388    |\n"
    "| Python     | +0.156               | 0.381 / 0.555    | +0.062                  | 0.998 / 0.998    |  0.000              | 0.420 / 0.386    | +0.399                | 0.326 / 0.496    |\n"
    "| PHP        | +0.102               | 0.726 / 0.899    | +0.055                  | 0.998 / 0.998    | +0.002              | 0.423 / 0.327    | +0.227                | 0.275 / 0.450    |\n"
    "| R          | +0.077               | 0.462 / 0.352    | (no FT data)            | -                | +0.035              | 0.706 / 0.641    | +0.337                | 0.247 / 0.248    |",
    title="MRR improvement and IsoScores after Soft-ZCA at best epsilon (Table 3)",
    metadata={"source_table": "artifacts/2411.17538.pdf, Table 3"},
)

# ---------------------------------------------------------------------------
# Per-(model, dataset) baseline observations
# ---------------------------------------------------------------------------

obs_codebert_low_mrr_low_iso = claim(
    "Without whitening, base CodeBERT exhibits very low semantic code search "
    "performance on CodeSearchNet (MRR ranging from 0.000 on Java/PHP to "
    "0.011 on R) together with very low IsoScores (typically $\\leq 0.02$ "
    "on both code and comment embeddings).",
    title="Observation: base CodeBERT shows low MRR and low IsoScore",
)

obs_ft_codebert_higher_mrr_low_iso = claim(
    "Fine-tuned CodeBERT (FT CodeBERT) exhibits substantially higher MRR "
    "than base CodeBERT (e.g. 0.547 vs 0.006 on Ruby; 0.619 vs 0.002 on "
    "Go), but its IsoScores remain low (in the range 0.036-0.072), with an "
    "average IsoScore increase of only 0.073 over base CodeBERT.",
    title="Observation: contrastive fine-tuning boosts MRR but barely increases isotropy",
)

obs_codet5plus_high_mrr_high_iso = claim(
    "Without whitening, CodeT5+ achieves the highest MRR (0.537-0.757 across "
    "the six CodeSearchNet languages, vs 0.248-0.619 for FT CodeBERT) and "
    "the highest IsoScores (0.196-0.400 on code and comments) of all four "
    "configurations -- surpassing even contrastively fine-tuned CodeBERT.",
    title="Observation: CodeT5+ is best on MRR and isotropy among baselines",
)

obs_codellama_low_mrr = claim(
    "Without whitening, Code Llama (7B) yields the lowest MRR among the "
    "non-CodeBERT baselines (MRR 0.009-0.047 across all languages), with "
    "very low IsoScores (mostly < 0.011).",
    title="Observation: Code Llama baseline MRR and IsoScore are low",
)

# ---------------------------------------------------------------------------
# Effect of standard ZCA (epsilon = 0)
# ---------------------------------------------------------------------------

obs_standard_zca_helps_base_models = claim(
    "Applying standard ZCA whitening ($\\epsilon = 0$) greatly improves the "
    "MRR of the base (pre-trained only) CodeBERT and Code Llama models on "
    "the CodeSearchNet languages.",
    title="Observation: standard ZCA improves base CodeBERT and Code Llama",
)

obs_standard_zca_hurts_ft_and_codet5 = claim(
    "Applying standard ZCA whitening ($\\epsilon = 0$) decreases the MRR of "
    "fine-tuned CodeBERT and CodeT5+ on most CodeSearchNet datasets.",
    title="Observation: standard ZCA hurts FT CodeBERT and CodeT5+",
)

# ---------------------------------------------------------------------------
# Effect of Soft-ZCA (epsilon > 0)
# ---------------------------------------------------------------------------

obs_optimal_epsilon_base = claim(
    "For the base (pre-trained only) models (CodeBERT, CodeT5+, Code Llama), "
    "moderate whitening with $\\epsilon \\in \\{0.1, 0.01\\}$ yields the best "
    "MRR; the optimal IsoScore for these models lies between 0.2 and 0.8.",
    title="Observation: best epsilon for base models is in {0.1, 0.01}",
    metadata={"source_figure": "artifacts/2411.17538.pdf, Fig. 1"},
)

obs_optimal_epsilon_ft = claim(
    "Fine-tuned CodeBERT requires stronger whitening for optimal MRR: the "
    "best $\\epsilon = 0.0001$, producing IsoScores consistently above 0.99 "
    "across all six CodeSearchNet languages.",
    title="Observation: fine-tuned CodeBERT prefers near-perfect isotropy",
    metadata={"source_figure": "artifacts/2411.17538.pdf, Fig. 1"},
)

obs_softzca_positive_delta_mrr = claim(
    "Across nearly all (model, language) combinations in Table 3, $\\Delta$MRR "
    "is positive after applying Soft-ZCA at the best epsilon -- including on "
    "the held-out R dataset that was not used for fine-tuning. The only "
    "exceptions are CodeT5+ on Go and Python, where $\\Delta$MRR = 0.000.",
    title="Observation: Soft-ZCA improves MRR almost universally (Table 3)",
    metadata={"source_table": "artifacts/2411.17538.pdf, Table 3"},
)

obs_codellama_largest_gain = claim(
    "Code Llama shows the largest MRR gains from Soft-ZCA: $\\Delta$MRR up "
    "to +0.476 (Ruby), with IsoScores between 0.224 and 0.496 after "
    "whitening.",
    title="Observation: Code Llama has the largest MRR gains from Soft-ZCA",
)

obs_ft_codebert_modest_gain = claim(
    "Fine-tuned CodeBERT exhibits more modest MRR gains from Soft-ZCA, "
    "ranging from $\\Delta$MRR = +0.042 (Go) to +0.075 (Ruby), even though "
    "IsoScores reach $> 0.99$ after whitening.",
    title="Observation: FT CodeBERT only gains modest MRR despite near-perfect isotropy",
)

obs_low_resource_r_helped = claim(
    "On the held-out low-resource R dataset (StatCodeSearch), Soft-ZCA "
    "yields positive $\\Delta$MRR for all three model families: +0.077 "
    "(CodeBERT), +0.035 (CodeT5+), and +0.337 (Code Llama).",
    title="Observation: Soft-ZCA generalises to the held-out low-resource R dataset",
)

# ---------------------------------------------------------------------------
# Higher-order findings (synthesis claims) -- exported conclusions
# ---------------------------------------------------------------------------

finding_code_lms_anisotropic = claim(
    "Similarly to standard natural-language LMs, all three studied code "
    "language models exhibit highly anisotropic embedding spaces: their "
    "raw IsoScores are typically far below 1 (e.g. 0.005-0.014 for "
    "CodeBERT, 0.234-0.400 for CodeT5+, 0.002-0.010 for Code Llama on "
    "CodeSearchNet, see @table2_nonwhitened).",
    title="Finding: code language models are highly anisotropic",
)

finding_finetuning_weak_on_isotropy = claim(
    "Contrastive fine-tuning does not strongly increase isotropy: on "
    "CodeBERT, fine-tuning improves the average IsoScore by only 0.073 "
    "while delivering large MRR gains, confirming that the MRR "
    "improvement from fine-tuning is largely orthogonal to the isotropy "
    "of the embedding space.",
    title="Finding: contrastive fine-tuning has only minor effect on isotropy",
)

finding_iso_mrr_relationship_nonlinear = claim(
    "Models with higher IsoScores generally perform better on code search, "
    "but the relationship between MRR and IsoScore is not linear. Concretely: "
    "FT CodeBERT reaches IsoScore > 0.99 with only modest MRR gains "
    "(+0.04--+0.08), while base Code Llama reaches IsoScore in the range "
    "0.22--0.50 with very large MRR gains (up to +0.476).",
    title="Finding: MRR vs IsoScore relationship is positive but non-linear",
)

finding_code_vs_comment_iso_similar = claim(
    "Code and comment embeddings have only marginally different IsoScores "
    "across all studied models (differences typically $< 0.1$ in Table 2). "
    "In practice they can be treated as similarly isotropic.",
    title="Finding: code and comment embeddings have similar isotropy",
)

finding_softzca_improves_code_search = claim(
    "Applying Soft-ZCA whitening with an appropriately chosen eigenvalue "
    "regularizer $\\epsilon$ improves both the isotropy and the code-search "
    "MRR of all four model configurations across all seven evaluated "
    "programming languages (with the only exceptions being CodeT5+ on Go "
    "and Python where $\\Delta$MRR = 0). The improvement is robust across "
    "model architectures (encoder-only, encoder-decoder, decoder-only) and "
    "extends to a held-out low-resource language not seen during training.",
    title="Finding: Soft-ZCA reliably improves isotropy and MRR for code search",
)

finding_optimal_isotropy_depends_on_finetuning = claim(
    "The optimal level of isotropy depends on whether the model has been "
    "contrastively fine-tuned: pre-trained-only models perform best with "
    "IsoScores between 0.2 and 0.8 (achieved at moderate $\\epsilon \\in "
    "\\{0.1, 0.01\\}$), whereas fine-tuned CodeBERT performs best with "
    "near-perfect isotropy (IsoScore $> 0.99$, achieved at $\\epsilon = "
    "0.0001$).",
    title="Finding: optimal isotropy level differs for base vs fine-tuned models",
)

# ---------------------------------------------------------------------------
# Strategies (Pass 2: connect)
# ---------------------------------------------------------------------------

# 1) Code LMs are anisotropic -- supported by the three baseline observations
strat_code_lms_anisotropic = support(
    [
        obs_codebert_low_mrr_low_iso,
        obs_codet5plus_high_mrr_high_iso,
        obs_codellama_low_mrr,
    ],
    finding_code_lms_anisotropic,
    background=[
        metric_isoscore,
        table2_nonwhitened,
        anisotropy_harms_semantics,
        contribution_isotropy_analysis,
    ],
    reason=(
        "Across all three model families, the IsoScores reported in "
        "@table2_nonwhitened are far below 1: base CodeBERT and Code Llama "
        "show IsoScores below 0.02 in essentially all cells "
        "(@obs_codebert_low_mrr_low_iso, @obs_codellama_low_mrr), and even "
        "the relatively isotropic CodeT5+ peaks around 0.40 "
        "(@obs_codet5plus_high_mrr_high_iso) -- well below the 1.0 ceiling "
        "set by @metric_isoscore. This realises the analysis programme of "
        "@contribution_isotropy_analysis and is the precondition under "
        "which @anisotropy_harms_semantics applies to code search. The "
        "three independent model families agreeing on the qualitative "
        "conclusion 'embedding space is highly anisotropic' supports the "
        "general claim."
    ),
    prior=0.95,
)

# 2) Fine-tuning weakly affects isotropy
strat_finetuning_weak_on_iso = support(
    [obs_ft_codebert_higher_mrr_low_iso],
    finding_finetuning_weak_on_isotropy,
    background=[metric_isoscore, table2_nonwhitened, contrastive_finetuning_limited],
    reason=(
        "@obs_ft_codebert_higher_mrr_low_iso reports that contrastive "
        "fine-tuning of CodeBERT raises MRR by orders of magnitude "
        "(e.g. 0.006 -> 0.547 on Ruby) yet only raises the average "
        "IsoScore by 0.073, leaving IsoScore in the 0.036-0.072 range. "
        "This is the direct experimental specialisation of the prior "
        "expectation in @contrastive_finetuning_limited and supports the "
        "conclusion that fine-tuning's MRR gain is largely orthogonal to "
        "isotropy."
    ),
    prior=0.92,
)

# 3) Code and comment embeddings have similar isotropy
strat_code_vs_comment_similar = support(
    [table2_nonwhitened],
    finding_code_vs_comment_iso_similar,
    background=[metric_isoscore],
    reason=(
        "Inspecting the Code/Comment IsoScore pairs in @table2_nonwhitened "
        "across every (model, language) cell shows differences typically "
        "below 0.1 -- e.g. CodeBERT Python 0.006/0.021, CodeT5+ Java "
        "0.388/0.313, Code Llama Javascript 0.010/0.002. The systematic "
        "near-equality is the direct empirical basis for the synthesis "
        "claim."
    ),
    prior=0.93,
)

# 4) MRR vs IsoScore is positive but non-linear
strat_mrr_iso_nonlinear = support(
    [
        obs_ft_codebert_modest_gain,
        obs_codellama_largest_gain,
    ],
    finding_iso_mrr_relationship_nonlinear,
    background=[table3_whitened_delta, metric_isoscore, metric_mrr],
    reason=(
        "Two contrasting observations from @table3_whitened_delta drive the "
        "non-linearity claim: @obs_ft_codebert_modest_gain shows that "
        "pushing FT CodeBERT to IsoScore > 0.99 only yields +0.04-+0.08 "
        "MRR, while @obs_codellama_largest_gain shows that Code Llama "
        "reaches +0.476 MRR with IsoScores merely between 0.22 and 0.50. "
        "The same isotropy gain therefore produces very different MRR "
        "gains, ruling out a linear MRR(IsoScore) relationship."
    ),
    prior=0.85,
)

# 5) Soft-ZCA reliably improves code search -- this is the headline claim.
#    Modeled as an induction over per-model independent supports of the law.

# Per-model support strategies (induction sub-strategies, generative direction:
# law -> per-model prediction)
sub_softzca_codebert = support(
    [finding_softzca_improves_code_search],
    obs_softzca_positive_delta_mrr,
    background=[model_codebert, dataset_codesearchnet],
    reason=(
        "If @finding_softzca_improves_code_search held universally, then in "
        "particular it predicts that base CodeBERT under Soft-ZCA on "
        "CodeSearchNet should show a positive $\\Delta$MRR. "
        "@obs_softzca_positive_delta_mrr reports +0.102 to +0.250 across "
        "all six languages, matching the prediction."
    ),
    prior=0.9,
)

sub_softzca_codellama = support(
    [finding_softzca_improves_code_search],
    obs_codellama_largest_gain,
    background=[model_codellama, dataset_codesearchnet, table1_model_details],
    reason=(
        "Specialising @finding_softzca_improves_code_search to Code Llama "
        "(architecture details in @table1_model_details) predicts a "
        "positive $\\Delta$MRR for that model. "
        "@obs_codellama_largest_gain reports the largest observed gains "
        "(+0.227 to +0.476), confirming the prediction in the strongest "
        "form."
    ),
    prior=0.9,
)

sub_softzca_ft_codebert = support(
    [finding_softzca_improves_code_search],
    obs_ft_codebert_modest_gain,
    background=[model_finetuned_codebert, dataset_codesearchnet],
    reason=(
        "Specialising @finding_softzca_improves_code_search to fine-tuned "
        "CodeBERT predicts a positive $\\Delta$MRR. "
        "@obs_ft_codebert_modest_gain reports +0.042 to +0.075 across all "
        "six languages -- the prediction holds, with the magnitude smaller "
        "but still positive."
    ),
    prior=0.85,
)

sub_softzca_R = support(
    [finding_softzca_improves_code_search],
    obs_low_resource_r_helped,
    background=[dataset_statcodesearch],
    reason=(
        "If the law holds it should also predict gains on the held-out "
        "low-resource R dataset -- a stricter test, because no model was "
        "fine-tuned for R. @obs_low_resource_r_helped reports +0.077 / "
        "+0.035 / +0.337 across the three model families, all positive."
    ),
    prior=0.88,
)

# Chain the inductions
ind_softzca_12 = induction(
    sub_softzca_codebert,
    sub_softzca_codellama,
    law=finding_softzca_improves_code_search,
    reason=(
        "Base CodeBERT and Code Llama are different model architectures "
        "(encoder-only vs decoder-only) trained on different corpora; their "
        "$\\Delta$MRR results provide independent confirmations of the law."
    ),
)

ind_softzca_123 = induction(
    ind_softzca_12,
    sub_softzca_ft_codebert,
    law=finding_softzca_improves_code_search,
    reason=(
        "Adding fine-tuned CodeBERT covers a third regime -- a model whose "
        "embedding geometry has been deliberately reshaped by contrastive "
        "training. Its independent positive $\\Delta$MRR strengthens the "
        "induction."
    ),
)

ind_softzca_1234 = induction(
    ind_softzca_123,
    sub_softzca_R,
    law=finding_softzca_improves_code_search,
    background=[research_gap, contribution_experimental_validation],
    reason=(
        "The R-language StatCodeSearch dataset is held out from all "
        "training/fine-tuning. Confirmation here probes generalisation to "
        "an unseen language and domain (social-science research), making "
        "the induction substantially stronger than within-distribution "
        "agreement alone. This jointly closes the @research_gap and "
        "completes @contribution_experimental_validation."
    ),
)

# 6) Optimal isotropy level depends on whether fine-tuned -- comparison
strat_optimal_iso_depends = support(
    [obs_optimal_epsilon_base, obs_optimal_epsilon_ft],
    finding_optimal_isotropy_depends_on_finetuning,
    background=[soft_zca_controls_whitening, metric_isoscore],
    reason=(
        "@obs_optimal_epsilon_base reports that base models peak at "
        "$\\epsilon \\in \\{0.1, 0.01\\}$ giving IsoScores in $[0.2, 0.8]$, "
        "while @obs_optimal_epsilon_ft reports that FT CodeBERT peaks at "
        "$\\epsilon = 0.0001$ giving IsoScores $> 0.99$. The two regimes "
        "differ in optimal $\\epsilon$ by roughly two-to-three orders of "
        "magnitude and in resulting IsoScore by a factor of $\\sim 5$, "
        "directly substantiating the conditional law."
    ),
    prior=0.9,
)

# 7) Standard ZCA's failure on FT/CodeT5+ vs success on base -- contradiction
#    pair captured as competing claims; resolved by Soft-ZCA's epsilon knob.
strat_standard_zca_split_explained = support(
    [
        obs_standard_zca_helps_base_models,
        obs_standard_zca_hurts_ft_and_codet5,
        zca_amplifies_noise_at_small_eigenvalues,
    ],
    soft_zca_controls_whitening,
    background=[metric_mrr],
    reason=(
        "The empirical split between @obs_standard_zca_helps_base_models "
        "(base models gain) and @obs_standard_zca_hurts_ft_and_codet5 "
        "(FT CodeBERT and CodeT5+ lose) is the experimental analogue of "
        "@zca_amplifies_noise_at_small_eigenvalues: when the embedding "
        "space already has reasonably distributed eigenvalues (FT models, "
        "CodeT5+), zero-$\\epsilon$ whitening amplifies noise and hurts "
        "MRR. This is exactly the failure mode that Soft-ZCA's $\\epsilon$ "
        "knob is designed to repair (@soft_zca_controls_whitening), giving "
        "an experimental warrant for the controllability claim beyond the "
        "purely mathematical derivation in s2."
    ),
    prior=0.85,
)

# ---------------------------------------------------------------------------
# Abduction: Soft-ZCA improves MRR *because* it controls isotropy --
# alternative explanation: it merely down-projects high-dimensional spaces.
# ---------------------------------------------------------------------------

# Predictions of the two hypotheses
pred_softzca_isotropy = claim(
    "If Soft-ZCA improves MRR by controlling isotropy then $\\Delta$MRR "
    "should track changes in IsoScore: each model family should show a "
    "positive $\\Delta$MRR whenever Soft-ZCA visibly increases its "
    "IsoScore. Comparing Tables 2 and 3, every model family that increases "
    "IsoScore (CodeBERT 0.005-0.014 -> 0.348-0.889; Code Llama 0.002-0.010 "
    "-> 0.224-0.496; FT CodeBERT 0.036-0.072 -> 0.991-0.998) also yields "
    "$\\Delta$MRR > 0.",
    title="Prediction: Soft-ZCA's MRR gain follows its isotropy gain",
)

pred_softzca_dim_artifact = claim(
    "If Soft-ZCA's MRR gains were a pure artefact of acting on "
    "high-dimensional embeddings (rather than of isotropy), then they "
    "should disappear -- or at least become much smaller -- on the model "
    "with the lowest embedding dimension (CodeT5+, dim=256), and be "
    "largest on the model with the highest dimension (Code Llama, "
    "dim=4,096). The reported pattern is consistent with this only "
    "weakly: Code Llama indeed shows the largest gains, but FT CodeBERT "
    "(dim=768) shows much smaller gains than base CodeBERT (also dim=768) "
    "after similar whitening, which the dimensionality story does not "
    "explain.",
    title="Prediction: dimensionality-only explanation of Soft-ZCA gains",
)

obs_softzca_pattern = claim(
    "The observed pattern of $\\Delta$MRR across all four configurations "
    "and seven languages is: (i) consistently positive (Table 3), (ii) "
    "scales roughly with the magnitude of IsoScore increase produced by "
    "Soft-ZCA, and (iii) Code Llama (highest dim and most anisotropic "
    "baseline) shows the largest gains while FT CodeBERT (already "
    "geometrically reshaped by contrastive training) shows the smallest, "
    "even though both end up with similar post-whitening IsoScores in "
    "their respective optimal regimes.",
    title="Observation: pattern of $\\Delta$MRR across configurations",
    metadata={"source_table": "artifacts/2411.17538.pdf, Tables 2 and 3"},
)

# Hypothesis claim (this is what's being argued for)
hypothesis_isotropy_mediates = claim(
    "Soft-ZCA's MRR improvement is mediated by its control of embedding "
    "isotropy (i.e. by spreading vectors more uniformly so semantically "
    "different inputs become more distinguishable), not by an unrelated "
    "side effect such as dimensionality reduction.",
    title="Hypothesis: isotropy mediates Soft-ZCA's MRR improvement",
)

alt_dimensionality_artifact = claim(
    "An alternative explanation is that Soft-ZCA's MRR improvement is "
    "mainly a side effect of its action on high-dimensional embeddings "
    "(numerical conditioning of the cosine metric on large covariance "
    "matrices), unrelated to the isotropy interpretation.",
    title="Alternative: Soft-ZCA's MRR gains are a dimensionality artefact",
)

# Build the abduction
support_h_isotropy = support(
    [hypothesis_isotropy_mediates],
    obs_softzca_pattern,
    background=[soft_zca_controls_whitening, code_search_anisotropy_problem],
    reason=(
        "Under @hypothesis_isotropy_mediates, the controllable knob "
        "$\\epsilon$ from @soft_zca_controls_whitening should produce MRR "
        "gains that track IsoScore changes, and should be most beneficial "
        "where the baseline anisotropy is worst (@code_search_anisotropy_"
        "problem). @obs_softzca_pattern is exactly that: positive "
        "$\\Delta$MRR co-occurs with isotropy gain in every cell, and the "
        "largest gains occur on the most-anisotropic baseline (Code "
        "Llama)."
    ),
    prior=0.85,
)

support_alt_dim = support(
    [alt_dimensionality_artifact],
    obs_softzca_pattern,
    background=[],
    reason=(
        "Under @alt_dimensionality_artifact one would also expect Code "
        "Llama (4,096-dim) to gain the most, which it does. However the "
        "alternative does not naturally explain why FT CodeBERT (also "
        "768-dim like base CodeBERT) gains far less than base CodeBERT, "
        "nor why CodeT5+ (256-dim) still gains on R."
    ),
    prior=0.35,
)

comp_softzca = compare(
    pred_softzca_isotropy,
    pred_softzca_dim_artifact,
    obs_softzca_pattern,
    reason=(
        "@pred_softzca_isotropy correctly predicts the cell-by-cell "
        "co-variation of $\\Delta$MRR with IsoScore changes (including "
        "the FT-vs-base CodeBERT contrast), whereas "
        "@pred_softzca_dim_artifact only captures the gross 'Code Llama "
        "wins' direction and is silent on the FT-vs-base contrast and on "
        "the small-dim CodeT5+ R-language gain."
    ),
    prior=0.85,
)

abduction_isotropy_mediates = abduction(
    support_h_isotropy,
    support_alt_dim,
    comp_softzca,
    background=[contribution_softzca_method, contribution_experimental_validation],
    reason=(
        "Two competing explanations for the experimental pattern in "
        "@obs_softzca_pattern are weighed: the isotropy-mediation "
        "hypothesis advanced by the paper "
        "(@hypothesis_isotropy_mediates) and the dimensionality-artefact "
        "alternative (@alt_dimensionality_artifact). The detailed "
        "cell-by-cell pattern in @comp_softzca favours the isotropy "
        "explanation."
    ),
)

# ---------------------------------------------------------------------------
# Modeled tension between standard-ZCA helping-base and hurting-FT/CodeT5+
# (these claims can both be true simultaneously, so they are NOT contradictions)
# ---------------------------------------------------------------------------

# Logical contradiction inside Section 4: it cannot simultaneously be the
# case that "standard ZCA whitening helps every model" and that
# "standard ZCA whitening hurts FT CodeBERT and CodeT5+ on most datasets".
# We model the unstated naive expectation against the observed split.
naive_zca_helps_all = claim(
    "Naive expectation: standard ZCA whitening ($\\epsilon = 0$) improves "
    "MRR for every model configuration on every CodeSearchNet language. "
    "(This is the implicit baseline assumption challenged by the paper's "
    "introduction of Soft-ZCA.)",
    title="Naive expectation: standard ZCA helps every model",
)

contradiction_zca_naive_vs_observed = contradiction(
    naive_zca_helps_all,
    obs_standard_zca_hurts_ft_and_codet5,
    reason=(
        "If standard ZCA helped every model on every dataset "
        "(@naive_zca_helps_all) then it would not decrease MRR for "
        "FT CodeBERT and CodeT5+ on most datasets "
        "(@obs_standard_zca_hurts_ft_and_codet5). The two claims cannot "
        "both be true; the experimental observation refutes the naive "
        "expectation, motivating the Soft-ZCA regularizer."
    ),
    prior=0.99,
)

__all__ = [
    # Tables / direct observations
    "table2_nonwhitened",
    "table3_whitened_delta",
    "obs_codebert_low_mrr_low_iso",
    "obs_ft_codebert_higher_mrr_low_iso",
    "obs_codet5plus_high_mrr_high_iso",
    "obs_codellama_low_mrr",
    "obs_standard_zca_helps_base_models",
    "obs_standard_zca_hurts_ft_and_codet5",
    "obs_optimal_epsilon_base",
    "obs_optimal_epsilon_ft",
    "obs_softzca_positive_delta_mrr",
    "obs_codellama_largest_gain",
    "obs_ft_codebert_modest_gain",
    "obs_low_resource_r_helped",
    "obs_softzca_pattern",
    # Headline findings (exported)
    "finding_code_lms_anisotropic",
    "finding_finetuning_weak_on_isotropy",
    "finding_iso_mrr_relationship_nonlinear",
    "finding_code_vs_comment_iso_similar",
    "finding_softzca_improves_code_search",
    "finding_optimal_isotropy_depends_on_finetuning",
    # Abduction-related claims
    "pred_softzca_isotropy",
    "pred_softzca_dim_artifact",
    "hypothesis_isotropy_mediates",
    "alt_dimensionality_artifact",
    "naive_zca_helps_all",
]
