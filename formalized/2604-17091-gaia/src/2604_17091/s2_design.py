"""Section 2: GenericAgent Design Principles and Architecture"""

from gaia.lang import claim, setting, support, deduction

from .motivation import (
    thesis_density,
    thesis_minimal_capability,
    context_context_window,
)

# ── Settings: design definitions ─────────────────────────────────────────────

def_completeness_conciseness = setting(
    "Context design involves a core trade-off between completeness (all decision-relevant "
    "information is present) and conciseness (no low-value content wastes the context "
    "budget). Naturalness — how easily the model interprets the representation — acts "
    "as a secondary constraint rather than a third independent dimension. The finite "
    "effective context window sharpens this into a constrained optimization: maximize "
    "completeness subject to conciseness, with naturalness as a guard rail.",
    title="Completeness-conciseness trade-off in context design",
)

def_hallucination_free_length = setting(
    "The 'hallucination-free context length' is defined as the effective ceiling below "
    "which the LLM can process context without significantly increased confabulation. "
    "For current models, this is roughly an order of magnitude smaller than the "
    "nominal window — approximately 30k tokens for models with 200k–1M token windows.",
    title="Hallucination-free context length definition",
)

def_atomic_tool = setting(
    "An atomic tool is a minimal, general-purpose primitive with a single, non-overlapping "
    "capability. Complex behaviors emerge from sequential composition of atomic tools "
    "rather than from task-specific tool enumeration. GenericAgent (GA) uses exactly "
    "9 atomic tools: file_read, file_write, file_patch, code_run, web_scan, "
    "web_execute_js, ask_user, update_working_checkpoint, and start_long_term_update.",
    title="Definition of atomic tool and GA's tool set",
)

def_memory_layers = setting(
    "GA's hierarchical memory is organized into four layers: "
    "L1 (Insight Index) — always-on, lightweight orientation layer showing only "
    "category existence (bounded by Kolmogorov complexity of the categorical structure); "
    "L2 (Global Facts) — stable accumulated knowledge retrieved on demand; "
    "L3 (Task Skills/SOPs) — reusable workflows and executable code retrieved on demand; "
    "L4 (Session Archive) — task records for long-horizon recall. "
    "A global meta-memory layer defines the memory map, core rules, and update "
    "boundaries. GA injects only the meta-memory and L1 by default.",
    title="GA hierarchical memory layer definitions",
)

def_agent_loop = setting(
    "GA's unified agent loop: at each step, construct execution context from global "
    "memory and current task; the LLM generates outputs or tool calls; tool results "
    "return as structured signals; after task completion, compress execution traces "
    "into structured long-term representations for L2/L3 storage. Two execution modes: "
    "Interact mode (user-initiated tasks) and Reflect mode (autonomous event-triggered "
    "execution via watchdog-style polling).",
    title="GA unified agent loop and execution modes",
)

def_context_budget = setting(
    r"GA's context budget management uses a character-domain heuristic. "
    r"Total character length $C_H = \sum_{m \in H} \mathrm{len}(m)$ is compared against "
    r"character budget $B = \alpha \cdot W_{\mathrm{tokens}}$ where $\alpha \approx 3$ "
    r"chars/token. Compression or eviction triggers when $C_H > B$. Target: < 30k tokens.",
    title="Context budget heuristic definition",
)

# ── Design principle claims ───────────────────────────────────────────────────

claim_tool_minimality = claim(
    "Keeping the tool interface minimal — using 9 atomic tools rather than 53+ "
    "specialized tools — preserves context information density by preventing tool "
    "descriptions from consuming large fractions of the context budget before task "
    "execution begins. Tool minimality is not a functional restriction but the mechanism "
    "by which GA preserves general-purpose capability while reducing interface overhead "
    "and creating favorable conditions for experience consolidation.",
    title="Tool minimality as density-preserving mechanism",
)

claim_hierarchical_memory = claim(
    "GA's on-demand hierarchical memory preserves context information density by keeping "
    "only the L1 index (category-level orientation, bounded in size) permanently "
    "in context while routing deeper factual and procedural knowledge (L2/L3) through "
    "tool calls only when needed. This prevents prior interactions, intermediate states, "
    "and execution traces from progressively consuming the context budget and burying "
    "decision-critical information.",
    title="Hierarchical on-demand memory for density preservation",
)

claim_self_evolution = claim(
    "GA's self-evolution mechanism converts verified past trajectories into reusable "
    "standard operating procedures (SOPs) and executable code stored in L3. This "
    "allows later tasks to begin from compact, task-relevant context rather than "
    "rebuilding understanding from scratch. The evolution pathway is: initial "
    "exploration → textual SOP → codified executable SOP, with autonomous exploration "
    "triggered via Reflect Mode using idle-time polling.",
    title="Self-evolution via trajectory-to-SOP-to-code conversion",
)

claim_context_compression = claim(
    "GA's context truncation and compression layer maintains information density during "
    "long-horizon execution through four staged mechanisms: "
    "(Stage 1) per-tool truncation thresholds (e.g., code_run: 10,000 chars; "
    "file_read: ~1,280 chars/line, 20,000 total; web_scan HTML: 35,000 chars); "
    "(Stage 2) assistant message compression — replacing earlier messages with "
    "one-line summaries, exempting the 4 most recent; "
    "(Stage 3) FIFO message eviction when $C_H > B$, reducing to 60% of budget; "
    "(Stage 4) working-memory anchor prompt injected after every tool invocation, "
    "containing the 20 most recent one-line turn summaries, current turn number, "
    "and a persistent key_info block maintained by the agent.",
    title="Four-stage context truncation and compression mechanism",
)

claim_failure_escalation = claim(
    "GA uses a three-step failure escalation mechanism to prevent stagnation loops: "
    "(1) analyze the error and make a localized adjustment; "
    "(2) if failure persists, abandon the current approach entirely and switch strategy "
    "or search for missing information; "
    "(3) if all automated attempts fail, pause and request human intervention. "
    "This staged design prevents the agent from blindly repeating mistakes.",
    title="Three-step failure escalation mechanism",
)

claim_web_scan_optimization = claim(
    "GA's web_scan tool implements a layout-analysis algorithm that clones the live DOM, "
    "computes per-element visibility, classifies regions as main or non-essential through "
    "overlay and partition analysis, and removes covered or hidden elements before "
    "serialization. This reduces token cost by an order of magnitude compared to raw "
    "DOM output while preserving decision-relevant web content.",
    title="web_scan DOM layout analysis for token reduction",
)

claim_l1_bounded = claim(
    "GA's L1 index layer remains bounded even as L2 and L3 expand. Each L1 entry "
    "records only the existence of a knowledge category, not its content. New entries "
    "are introduced only when genuinely new categories arise, so the overall L1 "
    "description length approaches the Kolmogorov complexity of the categorical "
    "structure of the knowledge set. The LLM acts as the decoder to retrieve full "
    "content from deeper layers via tool calls.",
    title="L1 index bounded by Kolmogorov complexity of knowledge categories",
)

claim_triggered_commit = claim(
    "GA uses a triggered commit mechanism rather than immediate memory writing. "
    "When information is identified as potentially valuable, it enters a validation "
    "stage where usefulness and reusability are checked before being written into "
    "L2 or L3 via small, incremental updates. Only verified information is committed, "
    "preventing memory from growing in an uncontrolled manner.",
    title="Triggered commit mechanism for memory quality control",
)

# ── Strategies: how design principles instantiate the core thesis ─────────────

strat_tool_minimality = support(
    [thesis_minimal_capability],
    claim_tool_minimality,
    reason=(
        "From @thesis_minimal_capability, tool interfacing is the first stage where "
        "information density is degraded. Keeping only 9 atomic tools means tool "
        "descriptions occupy a small, fixed fraction of the context budget. "
        "Complex behaviors emerge from compositional sequences of primitives, "
        "so minimal tool count does not constrain functional reach [@GenericAgent2026]."
    ),
    prior=0.87,
)

strat_hierarchical_memory = support(
    [thesis_density],
    claim_hierarchical_memory,
    reason=(
        "Given @thesis_density, the second density-degradation point is what enters "
        "the model's context per step. The L1/L2/L3/L4 hierarchy (@def_memory_layers) "
        "allows only the meta-memory and L1 (always-on, size-bounded) to stay in "
        "context, routing deeper retrieval through explicit tool calls. This ensures "
        "irrelevant procedural and factual knowledge never occupies the active context "
        "unless the current reasoning step explicitly needs it [@GenericAgent2026]."
    ),
    prior=0.85,
    background=[def_memory_layers],
)

strat_self_evolution = support(
    [thesis_density, thesis_minimal_capability],
    claim_self_evolution,
    reason=(
        "From @thesis_minimal_capability, memory formation is the third density "
        "requirement. @thesis_density implies that starting each task from scratch "
        "wastes context budget on re-understanding. GA's self-evolution converts "
        "verified execution traces into SOPs and code, so later tasks begin from "
        "compact, high-density representations rather than verbose re-exploration. "
        "The codification from SOP to executable code further compresses per-task "
        "token cost [@GenericAgent2026]."
    ),
    prior=0.83,
)

strat_compression = support(
    [thesis_density],
    claim_context_compression,
    reason=(
        "Given @thesis_density and the hallucination-free context length constraint "
        "(@def_hallucination_free_length: ~30k tokens for current models), GA targets "
        "a compact budget using the character-domain heuristic (@def_context_budget). "
        "The four-stage compression pipeline (per-tool truncation, assistant compression, "
        "FIFO eviction, anchor injection) actively maintains information density as "
        "conversation grows. Each stage targets a different density-degradation "
        "mechanism [@GenericAgent2026]."
    ),
    prior=0.82,
    background=[def_hallucination_free_length, def_context_budget],
)

strat_failure_escalation = support(
    [claim_self_evolution],
    claim_failure_escalation,
    reason=(
        "@claim_self_evolution requires that the agent can detect and recover from "
        "failures to maintain its evolutionary trajectory. The three-step escalation "
        "(localized fix → strategy switch → human intervention) prevents the agent "
        "from getting trapped in loops that would degrade rather than improve "
        "long-term performance [@GenericAgent2026]."
    ),
    prior=0.82,
)

strat_triggered_commit = support(
    [claim_hierarchical_memory],
    claim_triggered_commit,
    reason=(
        "@claim_hierarchical_memory requires memory quality control: unvalidated "
        "information must not silently pollute L2/L3. The triggered commit mechanism "
        "enforces a validation stage before committing, maintaining the quality "
        "invariant that L2/L3 contain only verified, reusable knowledge "
        "[@GenericAgent2026]."
    ),
    prior=0.85,
)

strat_web_scan_optimization = support(
    [claim_context_compression],
    claim_web_scan_optimization,
    reason=(
        "@claim_context_compression requires token efficiency at the tool output "
        "level. The web_scan DOM layout analysis (cloning DOM, computing visibility, "
        "overlay/partition analysis, pruning hidden elements) instantiates this at "
        "the web-observation layer — reducing raw HTML by an order of magnitude "
        "while preserving decision-relevant content [@GenericAgent2026]."
    ),
    prior=0.88,
)

strat_l1_bounded = support(
    [claim_hierarchical_memory],
    claim_l1_bounded,
    reason=(
        "From @claim_hierarchical_memory, GA's L1 layer records only the existence of "
        "knowledge categories (@def_memory_layers). Since category count grows "
        "sublinearly with knowledge volume (new categories arise only for genuinely "
        "new knowledge types), L1 is bounded by the Kolmogorov complexity of the "
        "categorical structure. The LLM decodes category existence into full content "
        "retrieval via tool calls — decoupling index size from knowledge volume "
        "[@GenericAgent2026]."
    ),
    prior=0.90,
    background=[def_memory_layers],
)
