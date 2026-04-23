"""Prior assignments for independent (leaf) claims in the 2604-08224 package.

Only the four independent claims identified by `gaia check` receive explicit priors.
All other claims are derived and receive beliefs from BP propagation.
"""

from .motivation import (
    externalization_thesis,
    software_engineering_example,
)
from .s3_memory import memory_failure_modes
from .s5_protocols import alt_adhoc_prompting

PRIORS = {
    # ── Four independent (leaf) claims ─────────────────────────────────────
    externalization_thesis: (
        0.88,
        "The central thesis is explicitly argued with multiple examples and grounded "
        "in Norman's cognitive-artifact theory. High confidence given the scope and "
        "quality of argumentation, but as a framework claim it remains partially "
        "unfalsifiable as an empirical prediction.",
    ),
    software_engineering_example: (
        0.92,
        "The software-engineering motivating example is a concrete, verifiable observation "
        "about how mature coding agents (SWE-agent, OpenHands) are actually built — "
        "high confidence as it describes existing deployed systems.",
    ),
    memory_failure_modes: (
        0.88,
        "The four failure modes (stale, over-abstracted, under-abstracted, poisoned) "
        "are well-characterized and empirically observable in production memory systems. "
        "Framing them as 'representational design failures' rather than bugs is a "
        "philosophical claim but well-supported by the analysis.",
    ),
    alt_adhoc_prompting: (
        0.72,
        "The alternative (ad-hoc prompting sufficient at small scale) is plausible and "
        "represents a genuine competing view — it is the status quo for many small-scale "
        "single-agent deployments. The contradiction with adhoc_to_structured at scale "
        "is modeled explicitly.",
    ),
}
