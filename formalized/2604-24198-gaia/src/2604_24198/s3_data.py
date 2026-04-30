"""Section 4.2: Step-Level Data Construction Pipeline"""

from gaia.lang import claim, setting, support
from .s2_architecture import setup_ternary_reward

# ── Settings: data pipeline ───────────────────────────────────────────────────

setup_diversity_driven = setting(
    "For each validated query x, Qwen3-235B-A22B-Instruct generates K=4 distinct "
    "trajectories. A judge model (DeepSeek-V3.2) verifies whether final answers "
    "are inconsistent. Only trajectory sets where not all answers are identical are "
    "retained — focusing on boundary cases where PRM guidance is most needed.",
    title="Diversity-driven trajectory generation"
)

setup_knowledge_augmented = setting(
    "Step-level annotation uses Qwen3-235B-A22B-Instruct to score steps and "
    "perform error attribution. Similar errors are merged following AutoManual "
    "methodology. Identified errors are curated into few-shots as external "
    "knowledge for expert annotation by DeepSeek-V3.2, using the ternary reward "
    "strategy.",
    title="Knowledge-augmented step-level annotation"
)

# ── Claims: data pipeline results ─────────────────────────────────────────────

claim_diversity_over_purity = claim(
    "Counter-intuitively, aggressive trajectory filtering does not consistently "
    "yield better reward modeling performance. Unfiltered training data achieves "
    "40.89% at N=16 on DABStep, outperforming all filtered variants: Meta-Critic "
    "(40.00%), Outcome-Consistency (39.77%), and Process-Consistency (39.34%). "
    "Strict filtering enhances data purity but discards diverse step-wise "
    "supervision samples, making the PRM overly conservative.",
    title="Data diversity outweighs purity for PRM training",
    metadata={"source_table": "artifacts/2604.24198.pdf, Table 4"}
)

claim_7k_instances = claim(
    "The data generation pipeline produces over 7,000 high-quality step-level "
    "supervision instances from diversity-driven trajectory generation and "
    "knowledge-augmented expert annotation.",
    title="7K supervision instances generated"
)

# claim_diversity_over_purity and claim_7k_instances are leaf claims —
# their priors are assigned in priors.py.
