"""Introduction and Motivation: The disconnect between agent memory and skill communities."""

from gaia.lang import claim, setting, question, support

# --- Background and scope ---

setup_scope = setting(
    "This paper studies knowledge extracted at the **scaffold level** -- runtime systems "
    "outside model weights. Training-time methods such as Reinforcement Learning from Human "
    "Feedback (RLHF, [@Ouyang2022rlhf]) and Constitutional AI ([@Bai2022cai]) are "
    "complementary but out of scope. Inclusion criteria for surveyed systems: (a) learn "
    "from interaction traces (excluding pre-specified rules), (b) produce persistent "
    "knowledge artifacts, and (c) have been published since 2023.",
    title="Scope: scaffold-level knowledge",
)

setup_communities = setting(
    "Two research communities address experience accumulation in Large Language Model (LLM) "
    "agents at the scaffold level: "
    "(a) the **agent memory community**, which builds systems for extracting and retrieving "
    "experiential knowledge (representative systems include MemGPT [@Packer2023memgpt], "
    "Mem0 [@Chhikara2025mem0], MemoryOS [@Kang2025memos]); "
    "(b) the **agent skill community**, which builds frameworks for discovering and reusing "
    "procedural capabilities from execution traces (representative systems include Voyager "
    "[@Wang2023voyager], SkillWeaver [@Zheng2025skillweaver], EvoSkill [@Alzubi2026evoskill]). "
    "Both communities address the same fundamental problem -- extracting reusable knowledge "
    "from interaction experience.",
    title="Two research communities on experience accumulation",
)

setup_cls_theory = setting(
    "Cognitive science offers analogues to multi-level knowledge representation. "
    "Complementary Learning Systems (CLS) theory [@McClelland1995cls] describes how the "
    "hippocampus rapidly encodes episodic memories that are gradually consolidated into "
    "neocortical knowledge -- a biological compression spectrum. ACT-R's "
    "declarative-procedural distinction [@Anderson1983actr] maps onto a memory/skill "
    "boundary, and Fitts and Posner's [@Fitts1967] skill acquisition theory shows that "
    "knowledge flows bidirectionally -- explicit rules compile into automatic procedures "
    "through practice.",
    title="Cognitive-science analogues",
)

# --- Research question ---

rq_unification = question(
    "Can the apparent split between agent memory systems and agent skill discovery "
    "systems be unified into a single conceptual framework that exposes shared "
    "sub-problems and missing capabilities, and what design implications follow?",
    title="Unification research question",
)

# --- Citation analysis observations (empirical motivation) ---

obs_total_references = claim(
    "A citation analysis spanning 22 primary papers (covering both agent memory and "
    "agent skill systems) catalogues a total of 1,136 references across these papers' "
    "bibliographies.",
    title="Citation analysis corpus size",
    metadata={"source_section": "artifacts/2604.15877.pdf, Abstract and Section 1"},
)

obs_memory_to_skill_citation = claim(
    "Memory papers cite skill work at a rate of approximately 0.7%: only 4 out of 566 "
    "outgoing references in the surveyed memory papers point to agent-skill work.",
    title="Memory-to-skill cross-citation rate",
)

obs_skill_to_memory_citation = claim(
    "Skill papers cite memory work at a rate of approximately 1.2%: only 7 out of 570 "
    "outgoing references in the surveyed skill papers point to agent-memory work.",
    title="Skill-to-memory cross-citation rate",
)

obs_skill_surveys_no_memory = claim(
    "Two recent surveys of agent skills ([@Jiang2026sok], [@Xu2026skillsurvey]) do not "
    "cite a single agent memory system in their bibliographies.",
    title="Skill surveys ignore memory work",
)

obs_memory_survey_only_voyager = claim(
    "Among the recent agent memory surveys, only one ([@Yang2026graph]) cites any agent "
    "skill work, and that citation is restricted to a single system (Voyager).",
    title="Memory surveys cite at most one skill system",
)

# --- Aggregate empirical conclusion ---

community_disconnect = claim(
    "The agent memory and agent skill research communities are largely disconnected: "
    "the cross-community citation rate is below 1% (0.7% memory-to-skill, 1.2% "
    "skill-to-memory). This separation is structural -- it is reflected not only in "
    "primary-paper citation patterns but also in the surveys, where skill surveys cite "
    "no memory work and memory surveys cite at most a single skill system.",
    title="Cross-community citation rate is below 1%",
)

strat_community_disconnect = support(
    [
        obs_total_references,
        obs_memory_to_skill_citation,
        obs_skill_to_memory_citation,
        obs_skill_surveys_no_memory,
        obs_memory_survey_only_voyager,
    ],
    community_disconnect,
    reason=(
        "The four citation-rate observations consistently demonstrate cross-community "
        "isolation. Memory papers cite skill work at 0.7% (@obs_memory_to_skill_citation) "
        "and skill papers cite memory work at 1.2% (@obs_skill_to_memory_citation), both "
        "drawn from the 1,136-reference corpus (@obs_total_references). The survey-level "
        "evidence (@obs_skill_surveys_no_memory, @obs_memory_survey_only_voyager) "
        "corroborates this at the literature-review layer. Aggregated, the evidence "
        "supports the qualitative summary of 'cross-community citation rate below 1%'."
    ),
    prior=0.95,
    background=[setup_communities],
)

# --- Core observation: the unifying view ---

shared_problem = claim(
    "Memory extraction and skill discovery are instantiations of the same operation: "
    "compressing interaction experience into reusable knowledge at different "
    "granularities. A memory system extracts structured event records (~10x compression); "
    "a skill system extracts reusable behavioral patterns (~100x compression); a rule "
    "system extracts abstract decision principles (~1,000x+ compression). These are not "
    "three separate problems but three points on a single experience compression spectrum, "
    "where higher compression directly translates to reduced context consumption, faster "
    "retrieval, and lower compute overhead per decision.",
    title="Memory, skills, rules as a single compression operation",
)

# --- Practitioner evidence ---

practitioner_compression = claim(
    "Practitioners already perform full-spectrum compression manually: hundreds of "
    "thousands of developers maintain CLAUDE.md and .cursorrules files that distill "
    "deployment experience into reusable rules (Level 0 raw experience compressed to "
    "Level 3 declarative rules). However, no automated system performs this compression; "
    "each existing system operates at a single, predetermined compression level.",
    title="Manual full-spectrum compression by practitioners",
)
