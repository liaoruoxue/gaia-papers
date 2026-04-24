"""Section 5 — Experimental Setup and Datasets"""

from gaia.lang import claim, setting

# --- Dataset settings ---

internal_dataset_setting = setting(
    "Internal dataset: 140 CUA trajectories sampled from WebTailBench using Fara-7B "
    "(Awadallah et al., 2025a). In-house expert annotators labeled each trajectory for "
    "both process success and outcome success following the design principles in Section 3. "
    "Used for all ablation studies and auto-research experiments.",
    title="Internal dataset: 140 expert-annotated WebTailBench trajectories",
)

browserbase_dataset_setting = setting(
    "Browserbase dataset: 106 CUA trajectories sampled from Fara-7B on Online-Mind2Web "
    "(OM2W), labeled by external annotators from Browserbase with $2\\times$ annotator "
    "overlap per trajectory. Annotators first calibrated on 10 practice trajectories. "
    "Annotation used a two-stage protocol: UV-blind stage (independent judgment without UV) "
    "and UV-informed stage (judgment after seeing UV's verdict and scores). "
    "Outcome labels: majority vote of binary judgments. "
    "Process labels: median of continuous rubric scores, binarized at $\\geq 0.8$ threshold.",
    title="Browserbase dataset: 106 trajectories with two-stage annotation",
)

auto_research_setup = setting(
    "Auto-research study setup: The Universal Verifier (~3,000 lines of code, ~2,000 lines "
    "of prompts) was used as the target for automated reproduction. Two settings: "
    "(1) From-blank: all ~2,000 prompt lines replaced with // TODO placeholders, only code "
    "scaffold remains; agent given high-level design principles but no prior prompts. "
    "A compliance agent audits each iteration to prevent memorizing test examples. "
    "Optimization rule: maximize Cohen's $\\kappa$ without increasing false positive rate (FPR). "
    "(2) Continuing expert work: agent starts from human expert's best prompts, same objective. "
    "System used Claude Code v2.1.87 with Claude Opus 4.6 (1M context).",
    title="Auto-research study: two settings for automated verifier design",
)

# --- Claims about datasets and evaluation approach ---

cuaverifierbench_novel = claim(
    "CUAVerifierBench is the first benchmark designed specifically to measure verifier "
    "quality for both process and outcome rewards for computer use agents, enabling the "
    "community to compare verifier alignment with human judgment in a standardized way. "
    "No existing benchmarks provide both process and outcome labels for CUA trajectories.",
    title="CUAVerifierBench: first benchmark measuring both process and outcome verifier quality",
)

uv_as_annotator = claim(
    "The Universal Verifier is treated as an annotator like any other human: "
    "inter-annotator agreement metrics (Cohen's $\\kappa$, precision, recall, FPR, FNR) "
    "are computed between the UV's labels and human labels on CUAVerifierBench trajectories.",
    title="Universal Verifier is evaluated as an annotator against human labels",
)

iterative_development_requires_benchmark = claim(
    "Building a high-quality verifier is not a one-shot problem but an iterative development "
    "process, and this process is only possible when grounded in a reliable evaluation "
    "procedure. CUAVerifierBench serves this role: each candidate verifier design is scored "
    "against human judgments using Cohen's $\\kappa$, providing a clear and immediate signal "
    "for what works and what does not.",
    title="Iterative verifier development requires a reliable evaluation benchmark",
)
