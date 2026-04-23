"""Section 5: Tool Authorization and Control Boundaries"""

from gaia.lang import claim, setting, support, compare, abduction, contradiction

from .s2_values_principles import (
    principle_deny_first,
    principle_graduated_trust,
    principle_defense_in_depth,
    principle_reversibility_weighted,
    five_values_motivate_architecture,
)
from .s3_architecture import (
    deny_first_safety_posture,
    seven_independent_safety_layers,
    reasoning_separation_claim,
)

# ── Permission system settings ─────────────────────────────────────────────────

seven_permission_modes_setting = setting(
    "Seven permission modes exist across the type definitions (types/permissions.ts): "
    "(1) plan — model must create a plan; execution only after user approval; "
    "(2) default — standard interactive use, most operations require user approval; "
    "(3) acceptEdits — edits in working directory and certain shell commands auto-approved; "
    "(4) auto — ML-based classifier evaluates requests (gated by TRANSCRIPT_CLASSIFIER); "
    "(5) dontAsk — no prompting, but deny rules still enforced; "
    "(6) bypassPermissions — skips most permission prompts, but safety-critical checks remain; "
    "(7) bubble — internal-only mode for subagent permission escalation to parent terminal. "
    "Five external modes (acceptEdits, bypassPermissions, default, dontAsk, plan) are defined "
    "in EXTERNAL_PERMISSION_MODES. The auto mode is conditionally included only when "
    "TRANSCRIPT_CLASSIFIER feature flag is active.",
    title="Seven permission modes",
)

authorization_pipeline_setting = setting(
    "The full authorization pipeline proceeds through four stages (permissions.ts, tools.ts): "
    "(1) Pre-filtering: filterToolsByDenyRules() strips blanket-denied tools from the model's "
    "view at tool pool assembly time, before any tool request reaches runtime evaluation; "
    "(2) PreToolUse hook: can return permissionDecision (deny or ask) or updatedInput; "
    "a hook allow does not bypass subsequent rule-based denies; "
    "(3) Rule evaluation: deny-first rule engine; MCP tools matched by mcp__server__tool name; "
    "(4) Permission handler (useCanUseTool.tsx): branches into coordinator, swarm worker, "
    "speculative classifier, or interactive paths.",
    title="Authorization pipeline stages",
)

auto_mode_classifier_setting = setting(
    "The auto-mode classifier (yoloClassifier.ts) uses a two-stage approach: a fast-filter "
    "and chain-of-thought evaluation. When TRANSCRIPT_CLASSIFIER is enabled, it loads "
    "three prompt resources: a base system prompt, an external permissions template, and "
    "(for Anthropic-internal users) a separate internal template. The function "
    "isUsingExternalPermissions() checks USER_TYPE and a forceExternalPermissions config "
    "flag to select the appropriate template. A speculative classifier (BASH_CLASSIFIER) "
    "races a pre-started classification against a timeout for BashTool requests.",
    title="Auto-mode ML classifier",
)

shell_sandboxing_setting = setting(
    "Shell sandboxing provides an additional protection layer for Bash and PowerShell "
    "commands (shouldUseSandbox.ts). A command can be permission-approved but still "
    "sandboxed, or permission-denied and never reach the sandbox check. The two systems "
    "operate on different axes: authorization versus isolation. When active, the sandbox "
    "provides filesystem and network isolation independent of the application-level permission model.",
    title="Shell sandboxing layer",
)

hook_permission_events_setting = setting(
    "Of the 27 hook events (coreTypes.ts), five participate directly in the permission flow "
    "(types/hooks.ts): "
    "(1) PreToolUse: can return permissionDecision (deny or ask; allow does not bypass checks), "
    "permissionDecisionReason, and updatedInput; "
    "(2) PostToolUse: can inject additionalContext and (for MCP tools) return updatedMCPToolOutput; "
    "(3) PostToolUseFailure: can inject additionalContext for error-specific guidance; "
    "(4) PermissionDenied: can provide retry guidance after auto-mode denials; "
    "(5) PermissionRequest: can return allow or deny; in coordinator paths, can resolve "
    "before the user dialog.",
    title="Five permission-related hook events",
)

# ── Core claims ────────────────────────────────────────────────────────────────

approval_fatigue_observation = claim(
    "Anthropic's auto-mode analysis (Hughes, 2026) found that users approve approximately "
    "93% of permission prompts, indicating that approval fatigue renders interactive "
    "confirmation behaviorally unreliable as a sole safety mechanism. Because users "
    "habitually approve without careful review, the system must maintain safety independently "
    "of human vigilance.",
    title="93% approval rate shows approval fatigue",
)

deny_first_motivated_by_approval_fatigue = claim(
    "The architectural commitment to deny-first evaluation, blanket-deny pre-filtering, "
    "and sandboxing as independent layers that operate regardless of user attentiveness "
    "is motivated by the 93% approval rate demonstrating that interactive approval is "
    "behaviorally unreliable as a sole safety mechanism.",
    title="Deny-first motivated by approval fatigue",
)

strat_deny_first_motivation = support(
    [approval_fatigue_observation],
    deny_first_motivated_by_approval_fatigue,
    reason=(
        "The empirical observation that users approve 93% of prompts (@approval_fatigue_observation) "
        "means interactive approval is not a reliable safety mechanism — users stop reviewing "
        "once habituated. The deny-first principle (@principle_deny_first) and layered safety "
        "architecture follow as the architectural response: safety must be maintained "
        "independently of human vigilance. This is stated explicitly in the source analysis "
        "(Tier A/B evidence from Hughes, 2026 and permissions.ts)."
    ),
    prior=0.9,
)

graduated_trust_spectrum_claim = claim(
    "The seven permission modes span a graduated autonomy spectrum from plan (user approves "
    "all plans before execution) through default and acceptEdits to bypassPermissions (minimal "
    "prompting). This gradient reflects a recurring design tension: as autonomy increases, "
    "the system must shift from interactive approval to automated safety checks. "
    "Longitudinal usage data (McCain et al., 2026) shows that auto-approve rates increase "
    "from approximately 20% at fewer than 50 sessions to over 40% by 750 sessions, "
    "suggesting the gradient is navigated by gradual habituation rather than deliberate mode selection. "
    "Sandboxing reduced permission prompt frequency by an estimated 84% (Dworken and Weller-Davies, 2025).",
    title="Graduated trust spectrum across seven modes",
    background=[seven_permission_modes_setting, principle_graduated_trust],
)

strat_graduated_trust = support(
    [deny_first_motivated_by_approval_fatigue, five_values_motivate_architecture],
    graduated_trust_spectrum_claim,
    reason=(
        "Given approval fatigue (@deny_first_motivated_by_approval_fatigue) and the five "
        "values (@five_values_motivate_architecture) — especially contextual adaptability "
        "and human decision authority — the graduated trust spectrum provides a structured "
        "way to shift from per-action approval to automated safety as the human-agent "
        "relationship matures. The modes are confirmed from types/permissions.ts (Tier B). "
        "The longitudinal data from McCain et al. (2026) is Tier A evidence that in practice "
        "the gradient is navigated by habituation, not deliberate selection — an important "
        "empirical finding about user behavior."
    ),
    prior=0.87,
)

defense_in_depth_shared_failure_modes = claim(
    "The defense-in-depth architecture rests on an independence assumption: if one layer "
    "fails, others catch the violation. However, several safety layers share common "
    "performance and economic constraints. Security researchers (Adversa.ai, 2026) have "
    "documented that commands with more than 50 subcommands fall back to a single generic "
    "approval prompt instead of running per-subcommand deny-rule checks, because per-subcommand "
    "parsing caused UI freezes. This demonstrates that defense-in-depth can degrade when "
    "its layers share failure modes — a structural tension between safety and performance.",
    title="Defense-in-depth fails when layers share failure modes",
)

strat_shared_failure = support(
    [seven_independent_safety_layers],
    defense_in_depth_shared_failure_modes,
    reason=(
        "The seven-layer safety architecture (@seven_independent_safety_layers) relies on "
        "independence of layers. The Adversa.ai (2026) findings provide direct empirical "
        "evidence that this independence assumption can be violated: performance pressure "
        "(UI freezes from parsing overhead) caused the deny-rule layer to degrade, "
        "allowing commands that would otherwise be denied per-subcommand to receive only "
        "generic approval. The auto-mode classifier also has direct token cost, creating "
        "economic constraints that can degrade that layer simultaneously. "
        "This is Tier C evidence (security research), but independently verified (two CVEs)."
    ),
    prior=0.88,
)

pre_trust_ordering_vulnerability = claim(
    "Independent security research reveals a temporal ordering property not captured in "
    "the permission pipeline diagram: code executing during project initialization "
    "(hooks, MCP server connections, and settings file resolution) runs before the "
    "interactive trust dialog is presented to the user. Two independently verified "
    "vulnerabilities share this root cause: CVE-2025-59536 (CVSS 8.7) and CVE-2026-21852 "
    "(CVSS 5.3), discovered by Check Point Research (Donenfeld and Vanunu, 2026). "
    "All four related CVEs were patched within weeks of disclosure.",
    title="Pre-trust initialization ordering vulnerability",
)

strat_pre_trust = support(
    [defense_in_depth_shared_failure_modes],
    pre_trust_ordering_vulnerability,
    reason=(
        "The shared failure mode finding (@defense_in_depth_shared_failure_modes) identifies "
        "that defense-in-depth can degrade. The pre-trust ordering vulnerability is a specific "
        "instance: the extensibility architecture (Section 6) operates before the safety "
        "architecture (Section 5) is fully engaged during initialization. The temporal "
        "dimension — not just the spatial ordering in Figure 4 — creates a privileged "
        "phase. CVE-2025-59536 and CVE-2026-21852 independently confirm this pattern "
        "(Tier C evidence, Donenfeld and Vanunu, 2026), and two separate CVEs "
        "(CVE-2025-54794, CVE-2025-54795) exploit path validation and command parsing "
        "flaws elsewhere in the pipeline."
    ),
    prior=0.85,
)

# ── Contradiction: deny-first vs alternative safety architectures ──────────────

alt_container_isolation = claim(
    "Container-based isolation (as used by SWE-Agent and OpenHands) sandboxes the agent's "
    "entire execution environment rather than evaluating individual tool invocations. "
    "This provides environment-level containment of arbitrary execution, relying on OS-level "
    "boundaries rather than application-level policy enforcement.",
    title="Alternative: Container-based isolation approach",
)

alt_git_rollback = claim(
    "Version-control-based safety (as used by Aider) uses Git rollback as the primary safety "
    "mechanism, making all changes reversible through version control rather than preventing "
    "them through policy enforcement.",
    title="Alternative: Git rollback safety approach",
)

not_both_approaches = contradiction(
    deny_first_motivated_by_approval_fatigue,
    alt_container_isolation,
    reason=(
        "Claude Code's deny-first per-action policy enforcement and container-based isolation "
        "represent incompatible primary safety architectures. A system cannot simultaneously "
        "use per-action deny-first evaluation as its primary boundary AND container isolation "
        "as its primary boundary — one places the trust boundary inside the agent (per-action), "
        "the other at the container perimeter. Claude Code explicitly contrasts its layered "
        "policy approach against container isolation in Section 5.1."
    ),
    prior=0.85,
)
