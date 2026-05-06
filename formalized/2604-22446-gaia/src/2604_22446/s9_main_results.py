"""Section 3.2-3.3: Main Results -- Table 2 (PRDBench), per-baseline
contrasts, and cross-domain case study outcomes.

Source: Yu et al. 2026 [@Yu2026OMC], Section 3.2-3.3 (pages 13-18).
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Table 2: PRDBench main results
# ---------------------------------------------------------------------------

claim_table_2_prdbench = claim(
    "**Table 2: Performance comparison on PRDBench.**\n\n"
    "| Agent Type | Method | Success Rate (%) | Cost ($) |\n"
    "|---|---|---|---|\n"
    "| Minimal | GPT-5.2 | 62.49 | -- |\n"
    "| Minimal | Claude-4.5 | 69.19 | -- |\n"
    "| Minimal | Gemini-3-Pro | 22.76 | -- |\n"
    "| Minimal | Qwen3-Coder | 43.84 | -- |\n"
    "| Minimal | Kimi-K2 | 20.52 | -- |\n"
    "| Minimal | DeepSeek-V3.2 | 40.11 | -- |\n"
    "| Minimal | GLM-4.7 | 38.39 | -- |\n"
    "| Minimal | Minimax-M2 | 17.60 | -- |\n"
    "| Commercial | CodeX | 62.09 | -- |\n"
    "| Commercial | Claude Code | 56.65 | -- |\n"
    "| Commercial | Gemini CLI | 11.29 | -- |\n"
    "| Commercial | Qwen Code | 39.91 | -- |\n"
    "| **Multi-agent** | **Ours (Claude Code Sonnet 4.6 + Gemini 3.1 Flash Lite Preview)** | **84.67 (+15.48)** | **345.59** |\n\n"
    "OMC achieves 84.67%, a **+15.48 pp** absolute lead over the "
    "next-best baseline (Claude-4.5 at 69.19%). Total cost across "
    "50 tasks: $345.59 (~$6.91/task).",
    title="Table 2: OMC 84.67% vs best baseline Claude-4.5 69.19% (+15.48 pp) at $6.91/task",
    metadata={
        "figure": "artifacts/2604.22446.pdf, Table 2 (page 14)",
        "caption": "Table 2: PRDBench DEV mode, single-attempt zero-shot.",
    },
)

# ---------------------------------------------------------------------------
# Atomic per-baseline contrasts (used by induction over baselines)
# ---------------------------------------------------------------------------

claim_omc_beats_minimal_best = claim(
    "**Per-baseline: OMC vs best Minimal (Claude-4.5).** OMC at "
    "84.67% beats the strongest Minimal baseline Claude-4.5 at "
    "69.19% by **+15.48 pp**. Notably, OMC uses Claude Sonnet 4.6 "
    "as its core LLM, so the gap is not attributable to model "
    "choice alone but to the organisational layer.",
    title="Per-baseline: OMC 84.67% vs Claude-4.5 69.19% Minimal (+15.48 pp)",
)

claim_omc_beats_codex = claim(
    "**Per-baseline: OMC vs CodeX [@Codex] (Commercial).** OMC at "
    "84.67% beats CodeX at 62.09% by **+22.58 pp**. The gap "
    "against the strongest Commercial agent in the panel.",
    title="Per-baseline: OMC 84.67% vs CodeX 62.09% (+22.58 pp)",
)

claim_omc_beats_claude_code = claim(
    "**Per-baseline: OMC vs Claude Code [@ClaudeCode] "
    "(Commercial).** OMC at 84.67% beats Claude Code at 56.65% by "
    "**+28.02 pp**. Same underlying model family (Claude) -- the "
    "+28 pp gap is attributable to OMC's organisational layer "
    "rather than the LLM substrate.",
    title="Per-baseline: OMC 84.67% vs Claude Code 56.65% Commercial (+28.02 pp); same Claude substrate",
)

claim_omc_beats_gemini_minimal = claim(
    "**Per-baseline: OMC vs Gemini-3-Pro Minimal.** OMC at "
    "84.67% beats Gemini-3-Pro at 22.76% by **+61.91 pp** -- a "
    "near-fourfold improvement on the same task panel.",
    title="Per-baseline: OMC 84.67% vs Gemini-3-Pro 22.76% Minimal (+61.91 pp; ~4x improvement)",
)

claim_omc_beats_gemini_cli = claim(
    "**Per-baseline: OMC vs Gemini CLI Commercial.** OMC at "
    "84.67% beats Gemini CLI at 11.29% by **+73.38 pp** -- the "
    "widest gap in the panel, despite Gemini being part of OMC's "
    "internal stack (Gemini 3.1 Flash Lite Preview).",
    title="Per-baseline: OMC 84.67% vs Gemini CLI 11.29% Commercial (+73.38 pp; widest gap)",
)

# ---------------------------------------------------------------------------
# Cross-baseline generalisation: OMC > all 12 baselines
# ---------------------------------------------------------------------------

claim_omc_beats_all_baselines = claim(
    "**Cross-baseline result: OMC beats every baseline in Table "
    "2.** OMC's 84.67% exceeds **all twelve** baselines (8 Minimal "
    "+ 4 Commercial). The minimum gap is +15.48 pp (vs Claude-"
    "4.5); the maximum is +73.38 pp (vs Gemini CLI). Across both "
    "the Minimal and Commercial categories the lead is at least "
    "+15 pp, demonstrating the gain is not specific to any "
    "particular model family or agent stack design.",
    title="Cross-baseline: OMC > all 12 baselines (gap range: +15.48 to +73.38 pp)",
)

# ---------------------------------------------------------------------------
# Three design aspects driving the result
# ---------------------------------------------------------------------------

claim_design_aspect_dynamic_decomposition = claim(
    "**Design aspect D1 contributing to the result: dynamic task "
    "tree.** The task tree adjusts decomposition during execution "
    "based on intermediate results, rather than committing to a "
    "fixed pipeline upfront. This lets OMC respond to mid-execution "
    "discoveries (e.g., the game-development case study creating "
    "a new sprite-slicing skill after evaluator rejection).",
    title="D1: dynamic decomposition adjusts mid-execution based on intermediate results (vs fixed pipeline)",
)

claim_design_aspect_review_gate = claim(
    "**Design aspect D2 contributing to the result: enforced "
    "completed -> accepted review gate.** No subtask result "
    "propagates downstream without supervisor approval. This "
    "reduces hallucinated outputs (the FSM blocks `accepted` "
    "without explicit review) and limits error cascading "
    "(downstream tasks cannot fire on incorrect upstream "
    "results).",
    title="D2: enforced review gate (completed -> accepted requires supervisor) reduces hallucination + cascading",
)

claim_design_aspect_cross_family = claim(
    "**Design aspect D3 contributing to the result: Container-"
    "Talent separation enabling cross-family recruitment.** OMC "
    "recruits agents from different families (LangGraph, Claude "
    "CLI, script-based) within the same project. The right tool "
    "is matched to each subtask -- e.g., on the PRDBench run, "
    "Claude Code-based Software Engineer and Software Architect "
    "coexist with the LangGraph-based founding agent.",
    title="D3: Container-Talent separation enables cross-family recruitment (right tool per subtask)",
)

# ---------------------------------------------------------------------------
# Cross-domain case studies (Section 3.3): per-case results
# ---------------------------------------------------------------------------

claim_case_content_generation_result = claim(
    "**Case 1 result (content generation, Section 3.3.1).** "
    "Single CEO prompt -> dynamically assembled team (Researcher: "
    "GPT-4o + Writer: Claude Sonnet 4) -> verified weekly trend "
    "report on hot AI Agent GitHub repos, emailed automatically. "
    "Pipeline completes in <10 minutes at ~$4.49 total cost. "
    "Manual verification confirmed all repository links and star "
    "counts are real and accurate.",
    title="Case 1: content generation -- $4.49, <10 min; all 15 GitHub links manually verified real",
)

claim_case_game_development_result = claim(
    "**Case 2 result (game development with human iteration, "
    "Section 3.3.2).** Single CEO prompt -> Game Developer (Claude "
    "Sonnet 4) + Art Designer (Gemini 2.5 + NanoBanana). Initial "
    "build forwarded to human evaluator who flagged sprite-sheet "
    "segmentation. Rather than patching ad hoc, COO/EA decide to "
    "extend system capability by creating a *new skill* for the "
    "Art Designer (programmatic sprite-sheet slicing). After "
    "re-execution with the new skill, the corrected build is "
    "delivered. Demonstrates evaluator-rejection -> "
    "re-exploration with skill creation, a closed loop OMC's E2R "
    "+ Talent layer is designed to support.",
    title="Case 2: game development -- evaluator rejection triggers new-skill creation + re-execution; closed feedback loop",
    metadata={
        "figure": "artifacts/2604.22446.pdf, Figure 6 (page 15) and Figure 10 (Appendix F, page 30)",
    },
)

claim_case_audiobook_result = claim(
    "**Case 3 result (audiobook, Section 3.3.3).** Single CEO "
    "prompt -> Novel Writer + AV Producer (Gemini 3.1 Pro). The "
    "two agents run on different LLM backends yet coordinate "
    "through the shared task tree, producing 16 scene "
    "illustrations + 16 voice-overs + background music + 2 final "
    "videos for ~$1.57 (1.56M tokens, ~15.7% of $10 budget). "
    "Demonstrates cross-modal coordination across text + audio + "
    "visual pipelines.",
    title="Case 3: audiobook -- $1.57 / 1.56M tokens; cross-modal (text + audio + visual) on different LLM backends",
    metadata={
        "figure": "artifacts/2604.22446.pdf, Figures 7, 11 (pages 16, 31)",
    },
)

claim_case_research_survey_result = claim(
    "**Case 4 result (research survey, Section 3.3.4).** Single "
    "CEO prompt -> 3 specialists from Talent Market (Research "
    "Scientist + Research Paper Scientist on Claude Sonnet 4.6 + "
    "AI Engineer self-hosted). Project completes in <1 hour at "
    "$16.26 / 15.9M tokens. Deliverables: 17 structured documents, "
    "rendered mind map covering 6 themes with ~70 nodes + 35+ "
    "papers, 3 novel research ideas (HiTeWM, PhysWM, MAWM with "
    "technical formulations + 2-3 yr timelines). Authors manually "
    "verified all cited papers are real; the third idea (MAWM, "
    "meta-learning + conformal prediction for sim-to-real "
    "transfer) is judged to have genuine novelty.",
    title="Case 4: research survey -- $16.26, <1 hr; 17 docs + 70-node mind map + 3 novel ideas (HiTeWM/PhysWM/MAWM)",
    metadata={
        "figure": "artifacts/2604.22446.pdf, Figure 8, Table 3, Figures 12-13 (pages 17, 18, 32, 33)",
    },
)

# ---------------------------------------------------------------------------
# Cross-case generalisation
# ---------------------------------------------------------------------------

claim_cross_case_pattern = claim(
    "**Cross-case pattern: same OMC, four domains, no framework "
    "changes.** All four case studies follow the same pattern: "
    "CEO provides a one-sentence brief; OMC recruits the right "
    "specialists; decomposes the project; executes across "
    "heterogeneous backends; delivers results. None required "
    "changes to the framework itself. Different model families "
    "are exercised (GPT-4o, Claude Sonnet 4, Claude Sonnet 4.6, "
    "Gemini 2.5, Gemini 3.1 Pro, self-hosted) -- the Container-"
    "Talent abstraction handles all of them under the same six "
    "interfaces.",
    title="Cross-case pattern: same OMC across 4 domains + multiple model families with no framework modification",
)

__all__ = [
    "claim_table_2_prdbench",
    "claim_omc_beats_minimal_best",
    "claim_omc_beats_codex",
    "claim_omc_beats_claude_code",
    "claim_omc_beats_gemini_minimal",
    "claim_omc_beats_gemini_cli",
    "claim_omc_beats_all_baselines",
    "claim_design_aspect_dynamic_decomposition",
    "claim_design_aspect_review_gate",
    "claim_design_aspect_cross_family",
    "claim_case_content_generation_result",
    "claim_case_game_development_result",
    "claim_case_audiobook_result",
    "claim_case_research_survey_result",
    "claim_cross_case_pattern",
]
