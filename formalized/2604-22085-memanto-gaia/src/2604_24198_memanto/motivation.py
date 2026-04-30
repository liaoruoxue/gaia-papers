"""Introduction and Motivation: The Memory Tax Problem"""

from gaia.lang import claim, setting, question

# --- Settings ---

setting_llm_stateless = setting(
    "Current LLMs are stateless, single-turn inference systems that lack persistent state across sessions.",
    title="LLM statelessness",
)

setting_agent_memory_demand = setting(
    "Autonomous agents require persistent memory for multi-step reasoning, tool utilization, and long-horizon task execution.",
    title="Agent memory requirement",
)

setting_hybrid_architectures = setting(
    "Current production memory systems (Mem0, Zep, Letta, A-MEM) use hybrid architectures combining dense vector representations with structured knowledge graphs.",
    title="Hybrid memory architectures",
)

setting_production_requirements = setting(
    "Production-grade agentic memory must satisfy: high accuracy, low latency, cost efficiency, and reduced operational complexity.",
    title="Production memory requirements",
)

# --- Claims ---

claim_memory_tax_exists = claim(
    "The 'Memory Tax' exists: hybrid graph+vector memory architectures impose cumulative increases in compute cost, latency, and system complexity during ingestion and retrieval, primarily due to LLM-mediated entity extraction, explicit graph schema maintenance, and multi-query retrieval pipelines.",
    title="Memory tax exists",
)

claim_llm_ingestion_overhead = claim(
    "Hybrid memory systems require ≥2 LLM calls per memory write for entity extraction and graph construction, resulting in approximately 2-3 seconds of ingestion latency per write.",
    title="LLM ingestion overhead",
)

claim_multiquery_retrieval_latency = claim(
    "Hybrid memory systems that use multi-query and recursive retrieval strategies incur multi-second round-trip retrieval latencies, compared to sub-100ms for single-query vector search.",
    title="Multi-query retrieval latency",
)

claim_infrastructure_complexity = claim(
    "Hybrid architectures require provisioning and maintaining separate vector and graph database instances, increasing operational complexity and fixed idle costs, unlike vector-only systems that can scale to zero.",
    title="Infrastructure complexity of hybrid systems",
)

# --- Questions ---

question_main = question(
    "Can a vector-only architecture with optimized information-theoretic retrieval and structured memory typing achieve or surpass the performance of complex hybrid graph+vector systems while eliminating the Memory Tax?",
    title="Main research question",
)

question_recall_vs_precision = question(
    "For agentic memory retrieval, is higher recall (broader, noisier context) more effective than higher precision (aggressive filtering), given modern LLMs' in-context reasoning capability?",
    title="Recall vs precision question",
)
