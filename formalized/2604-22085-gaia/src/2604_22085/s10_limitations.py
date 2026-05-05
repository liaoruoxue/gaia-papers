"""Section V.E + Conclusion: Limitations and Future Work, Conclusion.

Section V.E of [@Abtahi2026Memanto] surfaces five limitations:
* Benchmark scope (conversational only; non-conversational agentic
  workflows untested);
* Benchmark saturation and label quality (5% LongMemEval, 6-7% LoCoMo
  questions exhibit labelling inconsistencies);
* Inference-model dependence (Stage 5's +4.8 pp gain comes from Gemini 3);
* Scale evaluation (Moorcheh has been validated at 10M+ docs / 2000+ QPS
  on MAIR but not yet at thousands of concurrent agents);
* Multi-agent memory sharing (Memanto namespace currently isolates).

The Conclusion restates the headline.
"""

from gaia.lang import claim

# ---------------------------------------------------------------------------
# V.E Limitations
# ---------------------------------------------------------------------------

claim_lim_benchmark_scope = claim(
    "**Limitation 1 -- benchmark scope: conversational only.** Both "
    "LongMemEval and LoCoMo target *conversational* settings. Non-"
    "conversational agentic workflows (research agents, code "
    "generation, multi-agent coordination) remain untested. Merrill et "
    "al. [@Merrill2026] identify the need for benchmark testing of "
    "high-level memory organisation beyond factual recall "
    "[@Abtahi2026Memanto, Sec. V.E].",
    title="Limitation 1: benchmarks are conversational only; non-conversational workflows untested",
)

claim_lim_label_noise = claim(
    "**Limitation 2 -- benchmark saturation and label noise.** Manual "
    "inspection of individual questions suggests that approximately 5% "
    "of LongMemEval questions and 6-7% of LoCoMo questions contain "
    "labelling inconsistencies (ambiguous reference answers and "
    "questions whose ground truth cannot be unambiguously determined "
    "from the provided dialogue context). This label noise establishes "
    "a practical performance ceiling that is independent of memory "
    "architecture quality. Compounding this concern, competing systems "
    "are rapidly approaching the accuracy levels reported here, so both "
    "benchmarks may soon be insufficient to distinguish strong memory "
    "architectures. The development of more targeted evaluation "
    "protocols -- particularly stress-tests for conflict resolution, "
    "multi-agent coordination, and non-conversational workflows -- is "
    "an important direction for the field [@Abtahi2026Memanto, "
    "Sec. V.E].",
    title="Limitation 2: ~5% LME / 6-7% LoCoMo questions have label noise; benchmarks approaching saturation",
)

claim_lim_inference_model_dependence = claim(
    "**Limitation 3 -- inference-model dependence.** Final results use "
    "Gemini 3 (Stage 5), contributing +4.8 pp on LongMemEval relative "
    "to Stage 4 (Claude Sonnet 4 inference). As foundation models "
    "improve, retrieval quality will likely become an even larger "
    "differentiator relative to inference capability "
    "[@Abtahi2026Memanto, Sec. V.E].",
    title="Limitation 3: Stage 5's +4.8 pp comes from inference-model upgrade (Gemini 3)",
)

claim_lim_scale = claim(
    "**Limitation 4 -- scale evaluation incomplete.** Moorcheh's engine "
    "has been validated at 10M+ documents and 2,000+ QPS on MAIR "
    "[@MoorchehITS], but large-scale memory benchmarks testing Memanto "
    "with thousands of concurrent agents remain future work "
    "[@Abtahi2026Memanto, Sec. V.E].",
    title="Limitation 4: scale validation only at 10M+ docs / 2000 QPS; concurrent-agents stress test pending",
)

claim_lim_multi_agent_sharing = claim(
    "**Limitation 5 -- multi-agent memory sharing.** Memanto's namespace "
    "architecture currently isolates agent memories by design. Shared "
    "memory across agent teams with appropriate access control and "
    "consistency protocols is under active development "
    "[@Abtahi2026Memanto, Sec. V.E].",
    title="Limitation 5: per-agent namespaces preclude shared multi-agent memory (active dev)",
)

# ---------------------------------------------------------------------------
# Conclusion
# ---------------------------------------------------------------------------

claim_conclusion_restated = claim(
    "**Conclusion (restated).** Memanto is a universal memory layer for "
    "agentic AI achieving state-of-the-art results on LongMemEval "
    "(89.8%) and LoCoMo (87.1%) using a vector-only architecture with "
    "zero-cost ingestion, a 13-category typed semantic schema, and "
    "built-in conflict resolution. The five-stage ablation demonstrates "
    "that *retrieval recall, rather than architectural complexity, is "
    "the dominant performance driver*, and that modern LLMs perform the "
    "reasoning and filtering that graph-based systems attempt to pre-"
    "compute at ingestion time. By eliminating the Memory Tax (the "
    "compounding cost of LLM-mediated ingestion, multi-query retrieval "
    "pipelines, and graph infrastructure management), Memanto enables "
    "production-grade agentic memory at a fraction of the cost and "
    "complexity of hybrid alternatives. Memanto's design embodies a "
    "principled trade: structural expressiveness of knowledge graphs is "
    "exchanged for operational simplicity, determinism, and zero-"
    "latency ingestion, on top of a single highly optimised semantic "
    "search backend [@Abtahi2026Memanto, Conclusion].",
    title="Conclusion: SOTA via vector-only + typed schema + IT-search; trade graph expressiveness for simplicity / determinism / zero-latency",
)

__all__ = [
    "claim_lim_benchmark_scope",
    "claim_lim_label_noise",
    "claim_lim_inference_model_dependence",
    "claim_lim_scale",
    "claim_lim_multi_agent_sharing",
    "claim_conclusion_restated",
]
