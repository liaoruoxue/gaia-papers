"""Section 3: Experimental Apparatus.

Datasets, models, evaluation metrics, and procedural choices used to test
the Soft-ZCA whitening method.
"""

from gaia.lang import claim, setting

# --- Datasets ---

dataset_codesearchnet = setting(
    "CodeSearchNet [@Husain2019] is a benchmark for studying the code-search "
    "capabilities of machine learning models. It contains code-comment pairs "
    "from six popular programming languages -- Python, Go, Java, JavaScript, "
    "Ruby, and PHP -- with a full corpus of approximately 2 million pairs.",
    title="CodeSearchNet dataset",
)

dataset_statcodesearch = setting(
    "StatCodeSearch [@Diera2023] is a low-resource code search test dataset "
    "comprising 1,070 code-comment pairs from social-science research code "
    "written in the R language. It is used here only as a held-out test set "
    "(no fine-tuning is performed on it).",
    title="StatCodeSearch (R) dataset",
)

# --- Models ---

model_codebert = setting(
    "CodeBERT [@Feng2020] is an encoder-only language model designed for "
    "programming-language understanding. It has 125M parameters, an "
    "embedding dimension of 768, supports 6 programming languages, and is "
    "not contrastively pre-trained.",
    title="CodeBERT model",
)

model_codet5plus = setting(
    "CodeT5+ [@Wang2023] is an encoder-decoder language model trained for "
    "both code understanding and generation. The variant used here has 110M "
    "parameters, an embedding dimension of 256, supports 9 programming "
    "languages, and is contrastively pre-trained.",
    title="CodeT5+ model",
)

model_codellama = setting(
    "Code Llama [@Roziere2023] is the code-specialized variant of Llama 2. "
    "The version used here has 7B parameters, an embedding dimension of "
    "4,096, supports 7 programming languages, and is not contrastively "
    "pre-trained.",
    title="Code Llama (7B) model",
)

model_finetuned_codebert = setting(
    "FT CodeBERT denotes CodeBERT contrastively fine-tuned on the "
    "code-comment pairs of each CodeSearchNet language individually using "
    "InfoNCE loss, learning rate 5e-5, batch size 32, for 5 epochs. No "
    "fine-tuning is performed on R (StatCodeSearch).",
    title="Fine-tuned CodeBERT (FT CodeBERT)",
)

# --- Procedure / metrics ---

procedure_independent_encoding = setting(
    "Code and natural-language inputs are encoded independently, mirroring "
    "real-world search systems. Each input sequence is truncated to 256 "
    "tokens with no padding. Sequence representations are mean-pooled over "
    "the last hidden state for CodeBERT and Code Llama, and use the default "
    "down-projection pooling for CodeT5+.",
    title="Encoding procedure",
)

procedure_separate_whitening = setting(
    "Whitening matrices are computed independently for the code embeddings "
    "and the comment embeddings, using all embeddings in the test set of "
    "the dataset.",
    title="Separate whitening for code and comments",
)

metric_isoscore = setting(
    "IsoScore [@Rudman2022] measures the isotropy of an embedding space, "
    "bounded to $[0, 1]$, where 1 indicates perfect isotropy.",
    title="IsoScore metric definition",
)

metric_mrr = setting(
    "Code-search performance is evaluated via Mean Reciprocal Rank (MRR) "
    "based on cosine distance between comment and code embeddings: for each "
    "comment in the test set, all codes are ranked, and the reciprocal of "
    "the true code's rank is averaged over the test set.",
    title="MRR metric definition",
)

# --- Reported model details (Table 1) ---

table1_model_details = claim(
    "Reported architectural details (Table 1):\n\n"
    "| Model      | Parameters | Embed. Dim. | Supported Lang. | Contrastive Pre-training |\n"
    "|------------|-----------:|------------:|----------------:|:------------------------:|\n"
    "| CodeBERT   | 125M       | 768         | 6               | no                       |\n"
    "| CodeT5+    | 110M       | 256         | 9               | yes                      |\n"
    "| Code Llama | 7B         | 4,096       | 7               | no                       |",
    title="Architectural details of the three studied code LMs",
    metadata={"source_table": "artifacts/2411.17538.pdf, Table 1"},
)

__all__ = [
    "dataset_codesearchnet",
    "dataset_statcodesearch",
    "model_codebert",
    "model_codet5plus",
    "model_codellama",
    "model_finetuned_codebert",
    "procedure_independent_encoding",
    "procedure_separate_whitening",
    "metric_isoscore",
    "metric_mrr",
    "table1_model_details",
]
