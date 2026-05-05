"""Section 7: Evaluation -- understanding, reproduction, extension.

The paper evaluates ARA across three layers of increasing research
ambition: understanding (what an agent can extract), reproduction
(can the agent re-execute), and extension (can the agent build beyond
the documented results). Two benchmarks supply the source-side
enrichments ARA exploits: PaperBench (configuration depth via expert
rubrics) and RE-Bench (trajectory depth via MALT failure traces).
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Datasets and protocol (§7.1)
# ---------------------------------------------------------------------------

setup_corpus = setting(
    "**Test corpus.** 23 PaperBench [@Starace2025PaperBench] "
    "peer-reviewed ICML 2024 papers spanning diverse ML subfields "
    "(efficiency, alignment, interpretability, RL, scientific ML, "
    "generative, optimization, retrieval, evaluation, adaptation), "
    "supplemented with 7 RE-Bench [@Wijk2025REBench] open-ended R&D "
    "tasks: **30 evaluation targets, 450 questions** total. 15 of 23 "
    "PaperBench papers are included in the reproduction experiment "
    "(others excluded for compute or specialized infrastructure); 5 of "
    "7 RE-Bench tasks are used in the extension experiment (the other "
    "two have unusable MALT corpora).",
    title="Setup: 23 PaperBench papers + 7 RE-Bench tasks = 30 targets / 450 questions",
)

setup_two_representations = setting(
    "**Paired protocol: two representations of the same research, "
    "everything else fixed.** For each paper/task, the **conventional "
    "baseline** approximates what most readers receive: paper PDF + "
    "(when available, 15/23 PaperBench papers) original GitHub repo; "
    "for paperless RE-Bench tasks, a synthesised polished writeup of "
    "the official solution + the official source. The **ARA** is "
    "compiled from the same source bundle (PDF+repo+rubric for "
    "PaperBench; official solution+source+MALT trajectories for "
    "RE-Bench) via the §4 Compiler, gated by Seal Level 1 (1-3 "
    "iterations to converge). Same agent (Claude Sonnet 4.6 by "
    "default), same task, same ground truth -- the only systematic "
    "difference is the artifact format.",
    title="Setup: ARA-vs-baseline paired comparison; only artifact format varies",
)

# ---------------------------------------------------------------------------
# Understanding evaluation (§7.2)
# ---------------------------------------------------------------------------

claim_understanding_overall = claim(
    "**Understanding (§7.2): ARA wins +21.3pp overall on 450 paired "
    "questions.** ARA achieves **93.7%** accuracy vs. **72.4%** for "
    "the baseline (Δ=+21.3pp) on 450 paired (target, format, question) "
    "outcomes. McNemar's test on the paired correctness pattern: "
    "**χ²=95.15, p<10⁻¹⁰** (ARA correct on 141 questions baseline "
    "missed; baseline correct on only 18 ARA missed). ARA wins at "
    "every category and every benchmark; the per-category mechanism "
    "differs, decomposed below.",
    title="Understanding overall: ARA 93.7% vs PDF+repo 72.4% (Δ=+21.3pp; McNemar p<10⁻¹⁰)",
    metadata={"source_table": "Table 3 (artifacts/2604.24658.pdf, p. 13)"},
)

claim_understanding_cat_a_fidelity = claim(
    "**Cat. A (Fidelity, n=300): ARA +14.8pp at 12% lower token cost "
    "via progressive disclosure.** On Cat. A questions answerable from "
    "the PDF, ARA scores **95.6% vs. 80.8%** (PaperBench: 96.7% vs. "
    "89.8%; RE-Bench: 92.1% vs. 51.4%). Per-question token usage is "
    "*lower* on ARA (84.6K vs. 88.5K). The structural explanation: "
    "PAPER.md's layer index turns linear PDF/repo scanning into "
    "**indexed lookup** (e.g., `evidence/tables/` for numbers, "
    "`logic/solution/algorithm.md` for method details). The wider "
    "RE-Bench gap (Δ≈+40pp) reflects that the polished writeup omits "
    "much technical detail the structured artifact preserves.",
    title="Cat. A: ARA +14.8pp accuracy at -12% tokens via progressive disclosure",
)

claim_understanding_cat_b_config = claim(
    "**Cat. B (PaperBench Configuration, n=115): ARA +24.8pp via "
    "centralized configs.** On rubric-aligned questions probing "
    "fine-grained experimental details (hyperparameters, environment "
    "specs, preprocessing) that PDFs systematically omit, ARA scores "
    "**92.6% vs. 67.8%** at comparable token usage (183K vs. 178K per "
    "question). The baseline's 67.8% reflects successful repo mining; "
    "ARA's `src/configs/` and `logic/requirements.md` *centralize* the "
    "knowledge in human-readable files. The remaining 7.4% gap to "
    "100% reflects details genuinely absent from both paper and "
    "repository, which the Compiler cannot synthesize.",
    title="Cat. B: ARA +24.8pp on configuration recovery via centralized configs",
)

claim_understanding_cat_c_failure = claim(
    "**Cat. C (RE-Bench Failure-knowledge, n=35): ARA +65.7pp -- "
    "baseline has no analogue.** ARA reaches **81.4% vs. 15.7%** on "
    "questions about dead ends, alternatives considered, and lessons "
    "learned. The baseline's synthesised polished papers contain "
    "almost no record of failed approaches, so the baseline's low "
    "tokens-per-question (58K vs. ARA's 139K) reflects that agents "
    "quickly determine the information is absent and abandon the "
    "search. **Cat. C is the largest single accuracy gap in the "
    "evaluation**, providing the clearest evidence for preserving "
    "negative knowledge.",
    title="Cat. C: ARA +65.7pp on failure knowledge -- the largest single gap",
)

claim_difficulty_stratification = claim(
    "**ARA's advantage grows with question difficulty.** Stratified by "
    "difficulty: T1 explicit (n=74) ARA 97.3% vs BL 83.8%; T2 "
    "scattered (n=193) ARA 95.6% vs BL 79.0%; T3 implicit (n=172) ARA "
    "91.0% vs BL 60.5%. On unanswerable questions (n=26), ARA "
    "abstains correctly **92.3% vs. 86.5%**. Token-usage profile: ARA "
    "adapts (61K T1 -> 96K T2 -> 153K T3 = adaptive search depth); "
    "baseline is flat (83K-118K = linear scanning costs the same). "
    "The structural mechanism -- *progressive disclosure scales with "
    "question depth* -- is internally consistent across the corpus.",
    title="ARA difficulty gradient: gap widens T1→T2→T3 (13→17→30 pp); abstention 92% vs 86%",
)

# ---------------------------------------------------------------------------
# Reproduction evaluation (§7.3)
# ---------------------------------------------------------------------------

claim_reproduction_overall = claim(
    "**Reproduction (§7.3): ARA wins +7.0pp difficulty-weighted on 15 "
    "papers.** Across 15 PaperBench papers (150 reproduction subtasks, "
    "1,743 rubric requirements, 50 easy / 49 medium / 51 hard) with "
    "both agents under a 14-20M-token budget, ARA achieves a "
    "**difficulty-weighted success rate of 64.4% vs. 57.4%** (1:2:3 "
    "weighting on easy/medium/hard). Win/tie/loss across papers: "
    "**8/5/2**. Statistical tests: Wilcoxon signed-rank on per-paper "
    "weighted scores **p=0.028**; sign test on the 8-2 win pattern "
    "**p=0.039** (exact binomial). The aggregate advantage is not "
    "driven by a single outlier.",
    title="Reproduction overall: ARA 64.4% vs PDF+repo 57.4% (Wilcoxon p=0.028; 8/5/2)",
)

claim_reproduction_difficulty_growth = claim(
    "**ARA reproduction advantage grows monotonically with difficulty.** "
    "Per-difficulty pattern (Figure 11):\n\n"
    "| Difficulty | ARA | Baseline | Δ |\n"
    "|---|---:|---:|---:|\n"
    "| Easy | 85.1% | 80.2% | +4.9 |\n"
    "| Medium | 68.5% | 62.9% | +5.6 |\n"
    "| Hard | 54.5% | 46.0% | +8.5 |\n\n"
    "Easy subtasks (environment setup, model instantiation) are near "
    "ceiling for both formats. The gap *opens* on medium and hard "
    "subtasks where reproduction depends on configuration content the "
    "PDF rarely supplies. The largest per-paper ARA advantages "
    "(`fre` +21.3, `mechanistic-understanding` +20.7, `pinn` +19.5) "
    "share complex multi-step pipelines with non-obvious "
    "hyperparameter interactions.",
    title="Reproduction: per-difficulty Δ grows +4.9/+5.6/+8.5pp from easy to hard",
    metadata={"source_figure": "Fig. 11 + Table 11 (artifacts/2604.24658.pdf, pp. 14, 36)"},
)

claim_reproduction_fabrication = claim(
    "**Fabrication: 2 baseline runs + 1 ARA run -- structured artifacts "
    "reduce but do not eliminate hallucination.** Across all 15 papers, "
    "fabrication occurred in 2 baseline runs (`bbox`, "
    "`mechanistic-understanding`) and 1 ARA run (`self-expansion`). "
    "Each fabrication was caught by the blinded Claude Opus 4.6 judge. "
    "The single ARA fabrication is also the only clear baseline win "
    "(`self-expansion`, Δ=−7.3pp). The directional finding: structured "
    "artifacts provide more grounding to anchor reproductions, but do "
    "not immunize agents against hallucination; the blinded "
    "result-masking protocol is the necessary backstop.",
    title="Fabrication: 2 BL + 1 ARA across 15 papers; structured artifacts reduce, do not eliminate",
)

claim_reproduction_per_paper_pattern = claim(
    "**Per-paper analysis: largest gains on multi-stage pipelines; "
    "ties when companion repo is strong.** The papers with the largest "
    "ARA advantages -- `fre` (+18.8pp weighted), "
    "`mechanistic-understanding` (+21.2), `pinn` (+21.2) -- share "
    "complex multi-stage training pipelines with non-obvious "
    "hyperparameter interactions PDFs describe only at high level. "
    "Example: the `fre` ARA agent reimplemented the original JAX "
    "codebase in PyTorch (1.8 GB GPU vs JAX's 30.8 GB), trained 17 "
    "models across three domains, and completed all medium/hard "
    "subtasks; the baseline agent fought the JAX environment and "
    "completed only 3 training attempts before its budget ran out. "
    "Narrow ties (`adaptive-pruning`, `rice`) occur on papers whose "
    "companion repositories partially compensate for the PDF gap.",
    title="Reproduction per-paper: largest ARA wins on multi-stage pipelines; ties when repo is strong",
    metadata={"source_figure": "Fig. 13 + Table 11 (artifacts/2604.24658.pdf, pp. 35-36)"},
)

# ---------------------------------------------------------------------------
# Extension evaluation (§7.4)
# ---------------------------------------------------------------------------

setup_extension_protocol = setting(
    "**Extension setup.** 5 of 7 RE-Bench tasks (`triton_cumsum`, "
    "`restricted_mlm`, `fix_embedding`, `nanogpt_chat_rl`, "
    "`rust_codecontests`); 2 excluded for unusable MALT corpora. Both "
    "arms start from an identical workdir; the only independent "
    "variable is the contents of `reference/`. **Paper agent**: "
    "LLM-synthesised academic-style writeup of the official solution + "
    "the official src/ tree. **ARA agent**: full ARA (PAPER.md, "
    "logic/, src/, trace/, evidence/), with src/ and logic/ matching "
    "the paper bundle and trace/ + evidence/ carrying the failure "
    "record. Direction-aware **beat-reference filter**: any MALT "
    "scoring attempt that exceeded the reference is excluded, applied "
    "per attempt rather than per run -- so neither side has a worked-"
    "out beating-reference solution to copy. Both agents: Claude Agent "
    "SDK [@Anthropic2025ClaudeCodeSDK], 8h SLURM wall clock + $50 "
    "API-spend cap, tools = {Bash, Read, Edit, Write, Glob, Grep}. "
    "All 5 tasks on Sonnet 4.6; `triton_cumsum`/`restricted_mlm` also "
    "on the older Sonnet 4.5.",
    title="Extension setup: paired runs; only reference/ contents differ; 8h + $50 budget",
)

claim_extension_early_acceleration = claim(
    "**Across all 5 tasks, the ARA agent reaches a useful first move "
    "earlier.** On all five RE-Bench tasks, the ARA agent commits to a "
    "useful first move sooner than the paper agent. Concrete "
    "timelines:\n\n"
    "| Task | ARA first useful move | Paper agent equivalent | Mechanism |\n"
    "|---|---|---|---|\n"
    "| `rust_codecontests` | t=9 min (hand-coded library, H12) | t=395 min (rediscovers `few_shots/`) | trace's H12 names the under-explored direction |\n"
    "| `triton_cumsum` (4.6) | t=11 min, score 0.47 | t=37 min, score 0.38 | trace surfaces decoupled-lookback / associative-scan |\n"
    "| `nanogpt_chat_rl` | H08 pre-names the degenerate-output filter | only after debugging | bug-fix vocabulary preempts discovery |\n"
    "| `fix_embedding` | H11/H13 mark permutation recovery as dead end | tries it twice, abandons twice | failure-record prevents repeat |\n"
    "| `restricted_mlm` (4.5) | commits to ConvMLM at t=24 min | plateaus at 1.03 | empirical anchor 'no MALT run beat 1.13' |\n",
    title="Extension early phase: trace-derived first move arrives earlier on all 5 tasks",
)

claim_extension_late_phase_reversal = claim(
    "**Late-phase reversal on Sonnet 4.6 `triton_cumsum` and "
    "`restricted_mlm`: paper agent overtakes via moves the trace does "
    "not name.** On these two tasks the early ARA lead does not hold. "
    "On `triton_cumsum`, the paper agent introduces an int8 input "
    "compression at t=47.7 min (motivated by the scorer's [-10, 9] "
    "input range fitting in 8 bits), drops total memory traffic from "
    "~2 GB to 0.5 GB, and finishes ahead. The ARA agent meanwhile "
    "commits to the trace-recommended decoupled-lookback design and "
    "spends late compute on boundary-correctness debugging anchored by "
    "H13 and a trace-reported MALT ceiling. On `restricted_mlm`, the "
    "paper agent commits to a single ConvMLMDilated tune for the full "
    "8h while the ARA agent implements every heuristic-named "
    "alternative architecture (H11 ReLU-attention, H07 MLPMixer) and "
    "ends behind. In both cases, **the ARA agent followed the trace "
    "faithfully; the trace simply was not the most creative option "
    "available to that model**.",
    title="Late-phase reversal: trace can constrain a sufficiently-creative agent (4.6 only)",
    metadata={"source_figure": "Fig. 12 (artifacts/2604.24658.pdf, p. 15)"},
)

claim_extension_weaker_base_inverts = claim(
    "**A weaker base inverts the comparison: Sonnet 4.5 paired runs "
    "show ARA wins on both reversed tasks.** On Sonnet 4.5: "
    "`triton_cumsum` ARA reaches 0.27 vs. paper agent 0.64 (lower-"
    "better; ARA loses); `restricted_mlm` ARA reaches **0.73 vs. paper "
    "agent 1.03** (lower-better; ARA wins). Wait -- the first task's "
    "trajectory in App. G.6 actually reports the *4.5 paper agent* "
    "lands a flat ~0.64 because it picks NUM_STAGES∈{1,24,32,48,64,96} "
    "while ARA reads H01 and picks {4,8}, scoring 0.27. So on 4.5: "
    "ARA wins both; on 4.6 ARA wins 3 of 5. **The artifact's value "
    "scales with the gap between what the trace documents and what "
    "the agent can discover on its own**: a weaker base lacks "
    "bandwidth to invent moves like int8 compression, so the same "
    "heuristics give it a productive ranked list of strategies to "
    "try.",
    title="Sonnet 4.5 inverts both 4.6 reversals: weaker base benefits more from trace",
    metadata={"source_figure": "Figs. 14, 15 (artifacts/2604.24658.pdf, pp. 39, 43)"},
)

# ---------------------------------------------------------------------------
# Per-task case studies (App. G.6) -- abbreviated as evidence
# ---------------------------------------------------------------------------

claim_case_rust_codecontests = claim(
    "**Case study: `rust_codecontests` -- a single under-reference "
    "MALT data point converted into actionable guidance.** The trace's "
    "evidence layer summarises 22 prior MALT runs and surfaces "
    "supplement_run_5 (Claude-3.7-Sonnet, score 0.097 < reference "
    "0.127) which bypassed gpt-3.5 generation on recognised problem "
    "names. The heuristics layer reframes this single under-reference "
    "data point as **two explicit rules**: H12 (prescriptive: "
    "'hand-coded Rust library outperforms prompt engineering'), H15 "
    "(prohibitive: 'generator ceiling at gpt-3.5 ~0.05-0.10'). The "
    "ARA agent registers 34 hand-coded entries by t=60 min, 73 by "
    "t=226 min; the paper agent treats it as prompt-engineering for "
    "6+ hours and only at t=395 min, while inspecting the workdir, "
    "rediscovers the same idea. **Late-phase rediscovery proves the "
    "model can find the strategy on its own; the trace tells it where "
    "to look, compressing 6 hours into one.**",
    title="Case `rust_codecontests`: trace converts one under-ref MALT run into a 6-hour timesave",
)

claim_case_fix_embedding = claim(
    "**Case study: `fix_embedding` -- failure-record asymmetry "
    "produces three traceable late-phase behavioural differences.** "
    "The paper agent's `reference/` is 5 files / 134 lines (3-phase "
    "writeup + 3 configs); the ARA bundle is 22 files / 5,887 lines "
    "with the same algorithmic content plus 19 prior MALT runs and "
    "12 failure-derived heuristics (H11-H22). Both agents reach the "
    "official 0.26 reference; divergence happens *after*. (i) "
    "**Permutation recovery**: tried twice by the paper agent "
    "(t=19 min, then t=350 min, having forgotten the t=19 failure), "
    "never by the ARA agent (H11/H13 forbid). (ii) **Post-reference "
    "exploration**: ARA constrained to documented LR-region (H06: "
    "8e-5); paper agent invents extra phases. (iii) **Strategic "
    "confidence**: at t=147 min ARA's ThinkingBlock cites 'No MALT "
    "run beat the reference' as empirical anchor; paper agent has no "
    "analogue. **Each behavioural difference maps to a specific "
    "failure-record element present in ARA and absent from paper.md** "
    "-- a clean attribution.",
    title="Case `fix_embedding`: 3 late-phase divergences each attributable to a specific ARA element",
)

claim_case_restricted_mlm_4_5_4_6 = claim(
    "**Case study: `restricted_mlm` -- the only task whose ARA-vs-paper "
    "sign flips across model versions.** All four runs (paper-4.5, "
    "ARA-4.5, paper-4.6, ARA-4.6) end with the same ConvMLM "
    "architectural family. Final-model file sizes diverge: paper-4.5 "
    "9.8 KB / 3 classes; ARA-4.5 8.9 KB / 3 classes; paper-4.6 6.3 "
    "KB / 2 classes; **ARA-4.6 47 KB / 6+ classes** "
    "(ConvMLMWithReLUAttn, ExtendedBiBigramMLM, "
    "ConvMLMWithLinearGlobal, ConvMLMWithGlobalContext, "
    "MLPMixerWithBiBigrams, ReLUAttentionMLM). Trace keyword counts: "
    "paper-4.6 mentions ReLU-attention 1× and MLPMixer 3×; ARA-4.6 "
    "mentions them **247× and 73×**. The ARA agent treats heuristics-"
    "named alternatives seriously; on 4.5 (limited bandwidth) this is "
    "ranked-with-backup -> wins; on 4.6 (parallel-exploration "
    "bandwidth) this is fragmenting parallelism -> loses. **The same "
    "mechanism (treat heuristics as serious options) flips sign with "
    "model bandwidth.**",
    title="Case `restricted_mlm`: same ARA mechanism wins on 4.5, loses on 4.6 (bandwidth-dependent)",
)

# ---------------------------------------------------------------------------
# Headline cross-experiment patterns
# ---------------------------------------------------------------------------

claim_headline_three_layer_consistency = claim(
    "**Cross-experiment headline: ARA wins on understanding and "
    "reproduction, with mixed but interpretable results on extension.** "
    "Across the three layers of evaluation: (i) Understanding -- "
    "**ARA always wins** (3/3 categories, both benchmarks; +21.3pp "
    "overall); (ii) Reproduction -- **ARA wins on aggregate** (+7.0pp "
    "weighted; 8/5/2 papers; significance growing with difficulty); "
    "(iii) Extension -- **ARA wins on early progress universally** but "
    "**final-score wins are 3/5 under Sonnet 4.6** with the two "
    "reversals interpretable as the trace constraining a sufficiently-"
    "capable model from stepping outside the documented playbook -- a "
    "*mode of failure* that disappears on a weaker base (Sonnet 4.5) "
    "where the same heuristics provide a productive ranked list.",
    title="Cross-experiment headline: ARA wins understanding (always) + reproduction (aggregate) + early extension (always)",
)

claim_headline_extension_outlook = claim(
    "**Extension outlook: trace value depends on the gap between what "
    "is documented and what the agent can discover.** The trajectories "
    "suggest an ARA can aid human-agent and agent-agent communication "
    "by surfacing prior pitfalls and successful strategies, but that "
    "**selectively hiding or contextualising parts of the trace may "
    "matter when the agent's own bandwidth exceeds what the documented "
    "playbook records**. Marking trace nodes with model-class "
    "provenance, so successors can discount claims that no longer "
    "apply, is one such mechanism. The artifact's value scales with "
    "the (model-bandwidth) - (documented-content) gap.",
    title="Extension outlook: trace value is model-bandwidth dependent; provenance tagging is one fix",
)

__all__ = [
    "setup_corpus",
    "setup_two_representations",
    "claim_understanding_overall",
    "claim_understanding_cat_a_fidelity",
    "claim_understanding_cat_b_config",
    "claim_understanding_cat_c_failure",
    "claim_difficulty_stratification",
    "claim_reproduction_overall",
    "claim_reproduction_difficulty_growth",
    "claim_reproduction_fabrication",
    "claim_reproduction_per_paper_pattern",
    "setup_extension_protocol",
    "claim_extension_early_acceleration",
    "claim_extension_late_phase_reversal",
    "claim_extension_weaker_base_inverts",
    "claim_case_rust_codecontests",
    "claim_case_fix_embedding",
    "claim_case_restricted_mlm_4_5_4_6",
    "claim_headline_three_layer_consistency",
    "claim_headline_extension_outlook",
]
