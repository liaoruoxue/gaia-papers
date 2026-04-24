"""Introduction and Motivation"""

from gaia.lang import claim, setting, question, support

# --- Settings: established background ---

cot_prompting_def = setting(
    "Chain-of-Thought (CoT) prompting is a technique where large language models (LLMs) "
    "are prompted to produce intermediate reasoning traces before giving a final answer. "
    "It improves accuracy on complex multi-step tasks such as mathematical reasoning.",
    title="Chain-of-Thought prompting definition",
)

budget_forcing_def = setting(
    "Budget Forcing refers to methods that limit or penalize the length of chain-of-thought "
    "reasoning traces in LLMs, trading off inference-time computation against accuracy. "
    "Existing approaches include length penalties, target-length penalties, and early stopping.",
    title="Budget Forcing definition",
)

ib_markov_def = setting(
    "The standard Information Bottleneck (IB) principle [@Tishby2000] assumes a Markov chain "
    "structure Y ↔ X ↔ Z, where Z is a compressed representation that mediates all information "
    "flow from input X to output Y. The IB objective is: ℒ_IB = I(X;Z) − μ I(Y;Z).",
    title="Standard Information Bottleneck definition",
)

transformer_attention_def = setting(
    "Transformer decoder architectures [@Vaswani2017] use causal self-attention, which allows "
    "the answer generation step to attend directly to both the input prompt X and the reasoning "
    "trace Z simultaneously via the key-value cache.",
    title="Transformer causal attention mechanism",
)

# --- Core problem claims ---

cot_cost_problem = claim(
    "Chain-of-Thought (CoT) prompting improves LLM accuracy on complex tasks but significantly "
    "increases token usage and inference cost. Longer reasoning traces translate directly into "
    "higher computational expense at inference time.",
    title="CoT accuracy-cost tradeoff",
    metadata={"source_section": "Introduction"},
)

budget_forcing_heuristic = claim(
    "Existing Budget Forcing methods impose heuristic length penalties on reasoning traces that "
    "treat all tokens uniformly (a 'flat tax' on token count). This approach indiscriminately "
    "suppresses both essential reasoning steps and redundant 'cognitive bloat', making it "
    "brittle with respect to semantic relevance.",
    title="Flat-tax budget forcing is heuristic and brittle",
    metadata={"source_section": "Introduction"},
)

strat_cot_cost = support(
    [budget_forcing_heuristic],
    cot_cost_problem,
    reason=(
        "The existence of @budget_forcing_heuristic (methods attempting to control CoT cost) "
        "presupposes the underlying problem: CoT accuracy gains come at the cost of more tokens. "
        "The flat-tax nature of existing methods implies the problem (CoT cost) is real and "
        "significant enough to motivate a class of solutions."
    ),
    prior=0.9,
)

# --- Research questions ---

q_principled_compression = question(
    "Can efficient LLM reasoning be grounded in information-theoretic principles rather than "
    "heuristic token-length penalties, enabling a principled accuracy-efficiency trade-off?",
    title="Research question: principled compression of reasoning traces",
)
