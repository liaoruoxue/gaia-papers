"""Section 1: Introduction and Motivation.

Establishes the problem of anisotropic embedding spaces in code language
models and motivates Soft-ZCA whitening as a post-processing remedy.
"""

from gaia.lang import claim, setting

# --- Background settings (definitions and established conventions) ---

isotropy_definition = setting(
    "Isotropy in language models (LMs) refers to the uniform distribution of "
    "vector representations in the embedding space. An embedding space with "
    "high isotropy spreads vectors evenly across the space; low isotropy "
    "(anisotropy) means vectors are unevenly concentrated.",
    title="Definition of isotropy",
)

semantic_code_search_definition = setting(
    "Semantic code search is the task of retrieving relevant code snippets "
    "given a natural language query. Performance is measured by ranking the "
    "true code snippet for a given comment among the candidate set.",
    title="Definition of semantic code search task",
)

contrastive_finetuning_definition = setting(
    "Contrastive fine-tuning is a training approach that pulls semantically "
    "similar code/comment representations closer in embedding space and "
    "pushes dissimilar ones apart, typically using a loss such as InfoNCE.",
    title="Definition of contrastive fine-tuning",
)

# --- Background claims established in the introduction ---

isotropy_benefits = claim(
    "Higher isotropy in an embedding space enhances efficient use of the "
    "embedding capacity and increases robustness to perturbations [@Cai2021]. "
    "By spreading vectors more uniformly, semantic distinctions between "
    "different inputs are preserved more reliably.",
    title="Isotropy improves embedding space utilization and robustness",
)

anisotropy_harms_semantics = claim(
    "Anisotropic embedding spaces hinder model performance on semantic tasks "
    "because the small angular distances between vectors make it difficult "
    "to distinguish different meanings [@Attieh2023]. The effect is "
    "especially severe in tasks demanding precise representational alignment, "
    "such as cross-lingual transfer [@Ji2023].",
    title="Anisotropy degrades performance on semantic inference tasks",
)

code_search_anisotropy_problem = claim(
    "In semantic code search, high anisotropy in the encoder's embedding "
    "space causes semantically different code snippets to be encoded into "
    "vectors that are too close to one another, leading to suboptimal "
    "retrieval performance [@Husain2019]. The dominance of programming "
    "language keywords and symbols intensifies the problem because these "
    "syntactic tokens can dominate the sequence representation and obscure "
    "semantic content [@Eghbali2022].",
    title="Anisotropy specifically harms semantic code search retrieval",
)

contrastive_finetuning_limited = claim(
    "Although contrastive fine-tuning improves semantic code search by "
    "rearranging the embedding space, it only marginally mitigates "
    "anisotropy: the underlying low angular distance between encoded "
    "representations is not fully addressed by the contrastive objective "
    "[@Rajaee2021].",
    title="Contrastive fine-tuning does not fully fix anisotropy",
)

zca_whitening_known_isotropy = claim(
    "Zero-phase Component Analysis (ZCA) whitening has been shown to be a "
    "particularly fitting post-processing method for decorrelating hidden "
    "features and increasing the isotropy of embeddings [@Su2021; @Bell1996].",
    title="Standard ZCA whitening is known to increase embedding isotropy",
)

# --- Research questions / gap ---

research_gap = claim(
    "Lightweight post-processing techniques that boost embedding isotropy "
    "(such as ZCA whitening) have been studied for natural-language "
    "embeddings but remain unexplored for the semantic code search setting, "
    "where queries are natural language and candidates are code [@Husain2019].",
    title="Research gap: post-processing for code search isotropy is unexplored",
)

# --- Stated contributions of the paper ---

contribution_isotropy_analysis = claim(
    "The paper analyzes the isotropy of the embedding spaces in three "
    "popular code language models (CodeBERT, CodeT5+, Code Llama) with "
    "respect to their semantic code search performance, treating code and "
    "comment representations independently.",
    title="Contribution 1: isotropy analysis of three code LMs",
)

contribution_softzca_method = claim(
    "The paper introduces an eigenvalue regularizer $\\epsilon$ added to the "
    "ZCA whitening matrix, which they call Soft-ZCA, providing direct "
    "control over the degree of whitening (and hence the resulting isotropy "
    "level) applied to the embeddings.",
    title="Contribution 2: Soft-ZCA whitening with eigenvalue regularizer",
)

contribution_experimental_validation = claim(
    "The paper experimentally demonstrates on six popular programming "
    "languages plus one low-resource language (R) that post-processing "
    "embeddings with Soft-ZCA whitening improves Mean Reciprocal Rank (MRR) "
    "for both pre-trained and contrastively fine-tuned code language models.",
    title="Contribution 3: experimental validation on 6+1 programming languages",
)

__all__ = [
    "isotropy_definition",
    "semantic_code_search_definition",
    "contrastive_finetuning_definition",
    "isotropy_benefits",
    "anisotropy_harms_semantics",
    "code_search_anisotropy_problem",
    "contrastive_finetuning_limited",
    "zca_whitening_known_isotropy",
    "research_gap",
    "contribution_isotropy_analysis",
    "contribution_softzca_method",
    "contribution_experimental_validation",
]
