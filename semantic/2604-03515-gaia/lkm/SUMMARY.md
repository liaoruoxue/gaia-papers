# LKM Smoke — 2604.03515 Inside the Scaffold

**Date**: 2026-05-06
**Query**: "taxonomy of coding agents from source code analysis; loop primitives compose; agents are spectra not discrete categories; scaffold differentiates by primitives"

## Match Result

- top_k=15, scores all in [0.014, 0.017] — uniformly low
- 14 papers in `data.papers`, but most only weakly related
- **No directly-overlapping prior found** that frames coding-agent taxonomy from source code

## Top Candidates (subjectively most relevant)

| Date | Paper | Relevance |
|------|-------|-----------|
| ? | Why Agentic-PRs Get Rejected: A Comparative Study of Coding Agents | ⭐ Comparative study but on PR rejection, not source taxonomy |
| ? | Agentsway – Software Development Methodology for AI Agents-based Teams | ⚠️ Methodology angle, not taxonomy |
| ? | CaP-X: A Framework for Benchmarking Coding Agents for Robot Manipulation | ❌ Different domain (robot) |

## Self-positioning Verify

Skipped — no prior strong enough to warrant grep against the paper.

## Verdict

LKM corpus weak coverage for "coding agent source-code taxonomy" topic. **No prior found that challenges scaffold_taxonomy_fills_gap claim**. The L2 belief (0.92) stands.

## What this tells us about the pipeline

- LKM 不是万能的检索源；某些细分主题召回偏稀
- 即便如此，"找不到 prior" 本身是一个有用信号（确认空白）
- score 普遍在 0.01-0.02 区间提示当前 LKM embedding 对这类查询区分度不足，需要观察是否后续 embedding 升级
