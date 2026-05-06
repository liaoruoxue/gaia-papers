# LKM Smoke — 2603.23802 MCP Tools Cross-Platform Evidence

**Date**: 2026-05-06
**Query**: "large-scale empirical analysis of MCP tools agent ecosystem; software development tools dominate; AI co-authorship of agent tools"

## Match Result

- top_k=15, scores [0.015, 0.031] — highest of the three test papers
- 14 papers in `data.papers`, mostly MCP-related papers from 2025

## Candidate Priors (date-filtered, all before 2026-03)

| Date | Paper | DOI | Relevance |
|------|-------|-----|-----------|
| 2025-06 | MCPWorld: Unified Benchmarking for API/GUI Computer Use Agents | 2506.07672 | ⚠️ Benchmark, not large-N study |
| 2025-07 | Making REST APIs Agent-Ready: OpenAPI to MCP | 2507.16044 | ❌ Tool generation, not corpus analysis |
| 2025-09 | Code2MCP: Multi-Agent Framework | 2509.05941 | ❌ Tool generation |
| 2025-09 | Democratizing AI scientists using ToolUniverse | 2509.23426 | ❌ Different scope |
| 2025-10 | PentestMCP: Toolkit for Pentesting | 2510.03610 | ❌ Niche application |
| 2025-10 | TheMCPCompany: General-purpose Agents | 2510.19286 | ⭐ Closest — tool-discovery via MCP |
| 2025-10 | OSWorld-MCP: Benchmarking MCP Tool Invocation | 2510.24563 | ⚠️ Benchmark |
| 2026-02 | MalTool: Malicious Tool Attacks on LLM Agents | 2602.12194 | ⚠️ Security angle |

## Critical observation

**No prior performs large-N empirical analysis (177k tools / 19k servers) of the MCP ecosystem itself.** All priors are either:
- Tool-generation methods (Code2MCP, OpenAPI→MCP)
- Specific benchmarks (MCPWorld, OSWorld-MCP)
- Domain applications (PentestMCP, ToolUniverse)
- Security analyses (MalTool)

→ The paper's "first large-N empirical baseline" claim is **likely true** in this corpus.

## TheMCPCompany Evidence (gcn_5a35a04db2ea40bd)

```
Conclusion: "MCPAgent baseline ... gateway MCP server with find_tools/call_tool"
Chain 0: 1 factor / 3 premises
  P0: tool spec d = UTF-8 JSON serialization with name/desc/inputSchema
  P1: retrieval system embed both tool spec and agent query, rank by cosine
  P2: gateway architecture prevents direct tool invocation
```

Slightly richer chain than paper 2. 3 premises but still no factor diamonds (P1+P2+P3+P4 → C structure).

## Self-positioning Verify

If 2603.23802 publishes claim "first large-N empirical baseline", PDF should ideally cite or contrast against:
- MCPWorld (different scope: benchmark, not corpus)
- TheMCPCompany (different scope: tool discovery, not ecosystem analysis)

**TODO**: PDF grep verification not yet performed.

## Verdict

Novelty claim **strengthened** by LKM check — no direct competitor in the LKM-indexed corpus does what this paper does. L2 belief on `large_n_tool_evidence` (0.92) reasonable.

## What this tells us about the pipeline

- **Date-filter is mandatory** to identify true priors vs concurrent work
- LKM's strength is *finding adjacent work* even when no direct prior exists — useful for "Related Work" diff
- Even at score=0.031 (highest in our 3 tests), the chains are ≤1 factor — suggests **factor-diamond depth requires papers with formalized provenance** (likely older, well-indexed papers like Toker NAACL 2025)
