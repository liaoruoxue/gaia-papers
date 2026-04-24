"""Section 3: Case Studies — Emergent Discovery Across Domains"""

from gaia.lang import (
    claim, setting,
    support, deduction, abduction, induction, compare,
)

from .motivation import (
    emergent_coordination_claim,
    provenance_traceability_claim,
    framework_overview,
    q_autonomous_coordination,
)
from .s2_system_design import (
    agent_diversity_claim,
    multiparent_synthesis_claim,
    plannerless_coordination_design_claim,
    mutation_layer_claim,
    pressure_scoring_definition,
    skill_registry_definition,
    memory_stores_definition,
    six_node_loop,
)

# ─────────────────────────────────────────────────────────────────────────────
# 3.1 Quantitative Characterization
# ─────────────────────────────────────────────────────────────────────────────

case_study_setup = setting(
    "Four autonomous investigations were conducted using the ScienceClaw + Infinite framework: "
    "(1) Protein Design — peptide binder design for the somatostatin receptor SSTR2, "
    "(2) Materials Discovery — lightweight impact-resistant ceramic screening, "
    "(3) Cross-Domain Resonance — bridging biology, materials, and music via resonant structures, "
    "(4) Formal Analogy — mapping urban morphology to grain-boundary evolution. "
    "Each investigation ran with 8-13 agents and no human task assignment.",
    title="Four case study setup",
)

quantitative_summary = claim(
    "Across four autonomous investigations, the ScienceClaw + Infinite framework produced "
    "the following quantitative results:\n\n"
    "| Study | Agents | Tools | Artifacts | Syntheses | Avg DAG Depth |\n"
    "|-------|--------|-------|-----------|-----------|---------------|\n"
    "| Protein Design (SSTR2) | 10 | 23 | 177 | 57 | 2.15 |\n"
    "| Materials Discovery | 8 | 10 | 73 | 22 | 2.25 |\n"
    "| Cross-Domain Resonance | 13 | 12 | 159 | 19 | 2.00 |\n"
    "| Formal Analogy | 9 | 23 | 52 | 25 | 2.00 |\n\n"
    "Synthesis fractions range from 12% (resonance: 19/159) to 48% (materials: 22/73 ≈ 30%, "
    "protein: 57/177 ≈ 32%), and from 32% to 48% in design-driven studies [@Wang2025].",
    title="Quantitative case study summary table",
    metadata={"source_table": "artifacts/2603-14312.pdf, Table 1"},
)

synthesis_density_claim = claim(
    "Design-driven studies (protein design and materials discovery) achieve synthesis "
    "fractions of 30-32%, while open-ended reasoning studies (resonance, formal analogy) "
    "achieve lower synthesis fractions of approximately 12-48%, with DAG depths of 2.0-2.25 "
    "indicating multi-stage aggregation across all four investigations [@Wang2025].",
    title="Synthesis density by study type",
)

strat_synthesis_density = support(
    [quantitative_summary],
    synthesis_density_claim,
    reason=(
        "The quantitative summary table (@quantitative_summary) provides raw artifact and "
        "synthesis counts per study. Computing synthesis fractions: protein design 57/177=32%, "
        "materials 22/73=30%, resonance 19/159=12%, formal analogy 25/52=48%. Average DAG "
        "depths (2.00-2.25) confirm multi-stage aggregation. The pattern that design-driven "
        "studies cluster at 30-32% while open-ended studies vary more widely follows "
        "directly from these numbers."
    ),
    prior=0.95,
)

# ─────────────────────────────────────────────────────────────────────────────
# 3.2 Protein Design (SSTR2 Binder)
# ─────────────────────────────────────────────────────────────────────────────

sstr2_setup = setting(
    "The protein design case study targeted single-point mutations of a somatostatin-derived "
    "peptide to improve binding-related sequence fitness for the somatostatin receptor SSTR2. "
    "Ten agents were assigned distinct roles: structural analysis, evolutionary analysis, "
    "sequence design, ranking, and visualization. The ArtifactReactor linked outputs "
    "asynchronously across agents.",
    title="SSTR2 protein design setup",
)

sstr2_structural_finding = claim(
    "Structural analysis of the somatostatin-derived peptide identified the lysine-threonine-"
    "cysteine (K-T-C) triad as the dominant interaction hotspot for SSTR2 receptor binding, "
    "based on contact-map analysis of the peptide-receptor complex [@Wang2025].",
    title="K-T-C triad as binding hotspot",
)

sstr2_esm_finding = claim(
    "ESM-2 protein language model scanning revealed that positions within the conserved "
    "CWKTCT motif of the somatostatin-derived peptide are less tolerant to single-point "
    "mutations than flanking positions, as quantified by per-position log-likelihood "
    "differences under mutation [@Wang2025].",
    title="ESM-2 mutation tolerance in CWKTCT motif",
)

sstr2_convergence = claim(
    "Structural analysis, evolutionary conservation analysis, and ESM-2 language model "
    "scanning converged on overlapping constraint sets for the SSTR2 binder: all three "
    "approaches identified the core CWKTCT motif positions as least tolerant to mutation, "
    "providing independent corroboration of the binding hotspot [@Wang2025].",
    title="Multi-method convergence on SSTR2 binding constraints",
)

strat_sstr2_s1 = support(
    [sstr2_convergence],
    sstr2_structural_finding,
    reason=(
        "If multi-method convergence (@sstr2_convergence) holds — meaning all three approaches "
        "agree on CWKTCT motif constraints — then the structural contact-map analysis "
        "predicts the K-T-C triad as dominant (@sstr2_structural_finding). Confirmation of "
        "the structural finding flows back to support the convergence law."
    ),
    prior=0.85,
)

strat_sstr2_s2 = support(
    [sstr2_convergence],
    sstr2_esm_finding,
    reason=(
        "If multi-method convergence (@sstr2_convergence) holds, then ESM-2 sequence-based "
        "analysis should independently identify CWKTCT positions as mutation-intolerant "
        "(@sstr2_esm_finding). Confirmation from a different modality (sequence statistics "
        "vs structural coordinates) flows back to support the convergence law."
    ),
    prior=0.85,
)

strat_sstr2_convergence = induction(
    strat_sstr2_s1,
    strat_sstr2_s2,
    law=sstr2_convergence,
    reason=(
        "Structural and language-model evidence are independent in modality: one uses "
        "3D coordinate data, the other uses sequence statistics from evolutionary databases. "
        "Their agreement strengthens confidence in the convergence law beyond "
        "what either observation alone would support."
    ),
)

sstr2_weight_finding = claim(
    "The optimized SSTR2 binder candidate (sequence MGLKNFFLKTFTSC) has a molecular weight "
    "of approximately 1639 Da, which exceeds the therapeutic weight limit for oral "
    "bioavailability (typically ~500-1000 Da) and is substantially larger than the "
    "clinical reference octreotide (~1019 Da) [@Wang2025].",
    title="SSTR2 optimized candidate molecular weight",
)

sstr2_design_recommendation = claim(
    "Based on the molecular weight excess of the optimized SSTR2 candidate (approximately "
    "1639 Da versus the ~1019 Da reference octreotide), cyclization and truncation strategies "
    "are predicted to be more promising routes for therapeutic optimization than linear "
    "elongation of the peptide sequence [@Wang2025].",
    title="SSTR2 design recommendation: cyclize and truncate",
)

strat_sstr2_recommendation = support(
    [sstr2_weight_finding, sstr2_convergence],
    sstr2_design_recommendation,
    reason=(
        "The molecular weight finding (@sstr2_weight_finding) establishes that the optimized "
        "linear candidate at ~1639 Da already exceeds therapeutic limits. The convergence "
        "result (@sstr2_convergence) shows the CWKTCT motif is mutation-intolerant, "
        "constraining sequence space for elongation. Together: elongation would increase "
        "weight further (worsening bioavailability) while constrained positions limit "
        "sequence diversity. Cyclization reduces effective molecular weight and can "
        "preserve binding contacts; truncation shortens the sequence while targeting "
        "the identified hotspot triad."
    ),
    prior=0.78,
)

# ─────────────────────────────────────────────────────────────────────────────
# 3.3 Materials Discovery (Lightweight Impact-Resistant Ceramics)
# ─────────────────────────────────────────────────────────────────────────────

materials_setup = setting(
    "The materials discovery case study screened for lightweight impact-resistant ceramics "
    "satisfying simultaneous constraints: density < 5 g/cm³ AND bulk modulus > 200 GPa, "
    "with thermodynamic stability (on the convex hull). Eight agents used 10 tools and "
    "produced 73 artifacts with 22 synthesis events.",
    title="Materials discovery constraints and setup",
)

materials_screening_result = claim(
    "Screening for ceramics with density < 5 g/cm³ AND bulk modulus > 200 GPa identified "
    "14 phases satisfying both mechanical constraints, of which 7 were verified to be "
    "thermodynamically stable (on the convex hull of formation energies) [@Wang2025].",
    title="Materials screening: 14 candidates, 7 stable",
)

materials_top_candidates = claim(
    "The top two thermodynamically stable candidates for lightweight impact-resistant ceramics are:\n\n"
    "| Material | Density (g/cm³) | Bulk Modulus (GPa) |\n"
    "|----------|-----------------|--------------------|\n"
    "| B₄C (boron carbide) | 2.54 | 238 |\n"
    "| B₆O (boron suboxide) | 2.62 | 229 |\n\n"
    "Both are boron-rich compounds with anomalously high stiffness relative to their "
    "density [@Wang2025].",
    title="Top materials candidates: B4C and B6O",
    metadata={"source": "artifacts/2603-14312.pdf, Section 3.3"},
)

materials_novel_phases = claim(
    "Two novel boron-rich phases identified in the screening, Mg₂B₂₄C and MgB₉N, "
    "satisfy the mechanical constraints but have lower predicted synthesis success "
    "probabilities: 0.38 for Mg₂B₂₄C and 0.31 for MgB₉N, indicating higher synthesis "
    "difficulty compared to the established B₄C and B₆O candidates [@Wang2025].",
    title="Novel boron-rich phases with synthesis uncertainty",
)

materials_loglog_regression = claim(
    "A log-log regression analysis of density versus bulk modulus across the screened "
    "ceramic phases confirms that B₄C and B₆O are anomalously stiff relative to their "
    "density: they lie significantly above the regression trendline, "
    "indicating exceptional specific stiffness compared to the broader ceramic database [@Wang2025].",
    title="Log-log regression confirms anomalous stiffness",
)

strat_materials_top = support(
    [materials_screening_result, materials_loglog_regression],
    materials_top_candidates,
    reason=(
        "The screening result (@materials_screening_result) provides the candidate pool of "
        "7 thermodynamically stable phases. The log-log regression (@materials_loglog_regression) "
        "confirms that within this pool, B₄C (2.54 g/cm³, 238 GPa) and B₆O (2.62 g/cm³, 229 GPa) "
        "are anomalously stiff relative to their density. Ranking by this specific stiffness "
        "metric (bulk modulus per unit density) selects these two as the top candidates."
    ),
    prior=0.88,
)

strat_novel_phases = support(
    [materials_screening_result],
    materials_novel_phases,
    reason=(
        "The screening of 7 thermodynamically stable phases (@materials_screening_result) "
        "that satisfy density < 5 g/cm³ and bulk modulus > 200 GPa includes two previously "
        "unreported boron-rich phases: Mg₂B₂₄C and MgB₉N. These are identified as novel "
        "because they do not appear in standard ceramic databases, and their lower synthesis "
        "success probabilities (0.38 and 0.31) reflect higher uncertainty compared to "
        "established B₄C and B₆O candidates."
    ),
    prior=0.80,
)

# Abduction: why does the log-log regression show boron-rich anomaly?
hypothesis_boron_rich = claim(
    "Boron-rich compounds achieve anomalously high bulk modulus per unit density because "
    "boron's short, strong covalent bonds with carbon, oxygen, or nitrogen create "
    "exceptionally stiff networks at low atomic mass [@Wang2025].",
    title="Boron-rich stiffness hypothesis (covalent network)",
)
alt_boron_rich = claim(
    "The anomalous stiffness of boron-rich ceramics is an artifact of the computational "
    "screening methodology (e.g., DFT overbinding), not a genuine materials property.",
    title="Alternative: DFT artifact hypothesis for boron stiffness",
)

# Both hypotheses predict the log-log regression anomaly (the observation)
strat_h_boron = support(
    [hypothesis_boron_rich],
    materials_loglog_regression,
    reason=(
        "If boron's covalent networks drive anomalous stiffness (@hypothesis_boron_rich), "
        "the log-log regression observation (@materials_loglog_regression) — that B₄C and "
        "B₆O lie significantly above the regression trendline — is expected: genuine high "
        "specific stiffness would appear as anomalous above-trend scatter in density vs "
        "bulk modulus space."
    ),
    prior=0.82,
)
strat_alt_boron = support(
    [alt_boron_rich],
    materials_loglog_regression,
    reason=(
        "If DFT overbinding inflates moduli for boron-rich phases (@alt_boron_rich), "
        "these phases would appear above the regression trendline in the log-log plot "
        "(@materials_loglog_regression) even if their true bulk moduli are not anomalous. "
        "DFT overbinding is a known systematic error for short-bond covalent systems."
    ),
    prior=0.25,
)
pred_covalent = claim(
    "The covalent-network hypothesis predicts that boron-rich ceramics will show "
    "anomalously high specific stiffness (bulk modulus per unit density) consistently "
    "above the log-log regression trendline across the screened ceramic database [@Wang2025].",
    title="Covalent network prediction: above-trend log-log anomaly",
)
pred_artifact = claim(
    "The DFT-artifact hypothesis predicts that the anomalous stiffness should be "
    "concentrated specifically in phases with very short B-X bonds (where DFT overbinding "
    "is largest), disappearing if validated with experimental bulk modulus measurements.",
    title="DFT artifact prediction: bond-length-dependent anomaly",
)
comp_boron = compare(
    pred_covalent, pred_artifact, materials_loglog_regression,
    reason=(
        "The log-log regression (@materials_loglog_regression) shows systematic above-trend "
        "anomaly for the boron-rich subgroup, which is equally consistent with the covalent "
        "network hypothesis (@pred_covalent) and partially consistent with the DFT artifact "
        "hypothesis (@pred_artifact). However, no experimental validation is presented in the "
        "paper, limiting discrimination between the two explanations."
    ),
    prior=0.7,
)
abduction_boron = abduction(
    strat_h_boron, strat_alt_boron, comp_boron,
    reason=(
        "Both the covalent-network hypothesis (@hypothesis_boron_rich) and the DFT-artifact "
        "hypothesis (@alt_boron_rich) attempt to explain the same observation: the log-log "
        "regression anomaly for boron-rich ceramics (@materials_loglog_regression). "
        "Abduction selects the covalent-network explanation as better supported, though "
        "experimental validation is absent from the paper."
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# 3.4 Cross-Domain Resonance
# ─────────────────────────────────────────────────────────────────────────────

resonance_setup = setting(
    "The cross-domain resonance investigation used 13 agents to map resonant structures "
    "across biology, engineered materials, and music. 39 resonators were characterized "
    "in a six-dimensional feature space: 10 biological, 14 engineered, 7 musical "
    "instruments, and 8 Bach chorale segments. PCA was applied to the feature matrix.",
    title="Cross-domain resonance setup",
)

pca_result = claim(
    "Principal component analysis (PCA) of 39 resonators in a six-dimensional feature space "
    "produced two dominant principal components:\n\n"
    "- PC1 (61.2% variance explained): encodes membrane character — degree to which the "
    "resonator exhibits thin-membrane versus bulk-structural vibration modes.\n"
    "- PC2 (27.4% variance explained): captures structural periodicity — degree of "
    "repeating geometric patterns in the resonator architecture.\n\n"
    "Together, PC1 and PC2 account for 88.6% of total variance in the feature space "
    "[@Wang2025].",
    title="PCA result: two principal components explain 88.6% variance",
    metadata={"source": "artifacts/2603-14312.pdf, Section 3.4"},
)

design_gap_claim = claim(
    "In the PCA embedding of 39 resonators, a design gap is identified at coordinates "
    "approximately (-0.521, +0.425) in (PC1, PC2) space. This gap is located approximately "
    "12 times closer to the centroid of biological resonators than to the centroid of "
    "current engineered materials, indicating a region of biology-inspired design space "
    "not yet explored by human-engineered resonators [@Wang2025].",
    title="Bio-inspired design gap at (-0.521, +0.425)",
    metadata={"source": "artifacts/2603-14312.pdf, Section 3.4, Figure"},
)

bio_candidate_claim = claim(
    "The design gap in the resonator PCA space inspired the proposal of a bio-inspired "
    "engineered structure: the Hierarchical Ribbed Membrane Lattice, designed to occupy "
    "the gap coordinates by combining membrane-like geometry (high PC1) with periodic "
    "ribbing (high PC2) analogous to cricket wing architecture [@Wang2025].",
    title="Hierarchical Ribbed Membrane Lattice candidate",
)

fem_validation_claim = claim(
    "Finite element method (FEM) simulation of the Hierarchical Ribbed Membrane Lattice "
    "variant v1_cricket_fine validated the design: the fundamental resonance frequency "
    "was 2116 Hz, within the target band of 2-8 kHz (matching natural cricket wing "
    "acoustic emission). The simulation yielded nine resonance modes within the target "
    "band, giving a modal density of 1.5 modes/kHz, consistent with natural cricket "
    "wings [@Wang2025].",
    title="FEM validation: 2116 Hz fundamental, 1.5 modes/kHz",
    metadata={"source": "artifacts/2603-14312.pdf, Section 3.4"},
)

strat_design_gap = support(
    [pca_result, design_gap_claim],
    bio_candidate_claim,
    reason=(
        "The PCA result (@pca_result) establishes the coordinate system and the biological "
        "resonator cluster location. The design gap (@design_gap_claim) identifies the "
        "unexplored region at (-0.521, +0.425), 12× closer to biological than engineered "
        "centroids. The Hierarchical Ribbed Membrane Lattice is proposed specifically to "
        "occupy this gap: membrane character targets high-PC1, ribbing periodicity targets "
        "high-PC2, motivated by cricket wing morphology at those coordinates."
    ),
    prior=0.80,
)

strat_fem = support(
    [bio_candidate_claim],
    fem_validation_claim,
    reason=(
        "The bio-inspired candidate (@bio_candidate_claim) defines the Hierarchical Ribbed "
        "Membrane Lattice geometry. FEM simulation of this geometry predicts resonance "
        "frequencies. The validation criterion is whether the fundamental frequency falls "
        "in the 2-8 kHz cricket wing acoustic range. The result (2116 Hz fundamental, "
        "1.5 modes/kHz) meets this criterion, providing computational confirmation that "
        "the PCA-guided design achieves the target acoustic properties."
    ),
    prior=0.82,
)

resonance_cross_domain_claim = claim(
    "The PCA embedding demonstrates genuine cross-domain structure in resonance properties: "
    "biological resonators cluster away from engineered resonators in a statistically "
    "meaningful region of the feature space, and musical instruments occupy an intermediate "
    "position, supporting the hypothesis that resonance principles generalize across "
    "biology, engineering, and music in a continuous rather than categorically disjoint "
    "feature space [@Wang2025].",
    title="Cross-domain resonance structure in PCA",
)

strat_cross_domain = support(
    [pca_result, design_gap_claim],
    resonance_cross_domain_claim,
    reason=(
        "The PCA result (@pca_result) shows biological resonators load differently on PC1 "
        "and PC2 than engineered ones. The design gap (@design_gap_claim) is 12× closer "
        "to biological than engineered centroids, confirming that the two populations "
        "are spatially separated in the feature space rather than randomly intermixed. "
        "The continuous geometry of PCA (no hard boundary between clusters) supports "
        "the hypothesis that cross-domain resonance principles form a shared feature manifold."
    ),
    prior=0.75,
)

# ─────────────────────────────────────────────────────────────────────────────
# 3.5 Formal Analogy (Urban Morphology ↔ Grain Boundary Evolution)
# ─────────────────────────────────────────────────────────────────────────────

analogy_setup = setting(
    "The formal analogy case study used 9 agents and 23 tools to construct a cross-domain "
    "mapping between urban morphology and grain boundary evolution. A PRISMA-style systematic "
    "review produced a 66-concept ontology. Reduced correspondence networks and a power-law "
    "growth model were used as quantitative validators.",
    title="Urban-grain boundary analogy setup",
)

analogy_ontology = claim(
    "A PRISMA-style systematic review of literature on urban morphology and grain boundary "
    "evolution produced a 66-concept ontology with nine cross-domain conceptual edges "
    "in the reduced correspondence map, mapping urban concepts (street network, district, "
    "growth front) to grain boundary analogs (boundary network, grain, migration front) "
    "[@Wang2025].",
    title="66-concept ontology with 9 cross-domain edges",
)

analogy_power_law = claim(
    "A power-law growth model fitted to a normalized 60-point dataset spanning both urban "
    "and grain boundary growth data yields: exponent α = 1.25 ± 0.08, coefficient of "
    "determination R² = 0.71. This indicates a moderate shared growth scaling, with "
    "significant residual variance unexplained by the shared model [@Wang2025].",
    title="Power-law fit: α=1.25±0.08, R²=0.71",
)

analogy_degree_sequence = claim(
    "The reduced network graphs for urban morphology and grain boundary evolution share "
    "an identical degree sequence: [3, 3, 3, 2, 2, 1, 1], indicating that the coarse "
    "topological connectivity structure of the two domains is formally equivalent at "
    "the level of node-degree distribution [@Wang2025].",
    title="Identical degree sequence [3,3,3,2,2,1,1]",
)

analogy_bayesian = claim(
    "Bayesian comparison of the power-law growth exponents from urban and grain boundary "
    "datasets yields a posterior probability of 0.82 that the two exponents differ by "
    "less than 0.5, providing moderate statistical support for shared growth dynamics "
    "while not ruling out domain-specific differences [@Wang2025].",
    title="Bayesian comparison: 0.82 probability exponents differ by <0.5",
)

lsystem_claim = claim(
    "A six-rule L-system grammar was constructed to represent growth, infill, junction "
    "formation, and consolidation processes across both urban morphology and grain boundary "
    "evolution domains. The grammar is executable and generates patterns consistent with "
    "observed morphologies in both domains [@Wang2025].",
    title="Six-rule L-system grammar for cross-domain growth",
)

analogy_strength_claim = claim(
    "The urban morphology–grain boundary evolution analogy is characterized as a "
    '"constrained formal analogy supported by coarse topological similarity and symbolic '
    'generative compatibility" rather than a mathematical isomorphism: the shared degree '
    "sequence and L-system grammar support structural correspondence, but the R² = 0.71 "
    "power-law fit and Bayesian probability 0.82 leave substantial uncertainty about "
    "whether the analogy reflects deep mechanistic equivalence [@Wang2025].",
    title="Analogy strength assessment: formal but not isomorphic",
)

strat_analogy_strength = support(
    [analogy_ontology, analogy_power_law, analogy_degree_sequence, analogy_bayesian, lsystem_claim],
    analogy_strength_claim,
    reason=(
        "Five lines of evidence bound the analogy strength from above and below. "
        "The 66-concept ontology with 9 cross-domain edges (@analogy_ontology) provides "
        "conceptual grounding for the mapping. The degree sequence identity "
        "(@analogy_degree_sequence) establishes coarse topological equivalence. "
        "The L-system grammar (@lsystem_claim) provides symbolic generative compatibility. "
        "The power-law fit (@analogy_power_law) with R²=0.71 shows shared scaling but "
        "with substantial unexplained variance. The Bayesian comparison (@analogy_bayesian) "
        "gives 0.82 probability that exponents are within 0.5 — consistent with broad "
        "similarity but not tight mechanistic equivalence. Together these support "
        "'constrained formal analogy' as the appropriate characterization."
    ),
    prior=0.82,
)

# ─────────────────────────────────────────────────────────────────────────────
# 3.6 Cross-study emergent coordination evidence
# ─────────────────────────────────────────────────────────────────────────────

cross_study_coordination_claim = claim(
    "Across all four autonomous investigations, agents exhibited emergent convergence: "
    "independently operating agents, with no explicit task assignment, produced synthesis "
    "events (artifact merges across agents) at rates of 12-48% of total artifacts, "
    "demonstrating that plannerless ArtifactReactor coordination achieves genuine "
    "multi-agent integration at scale [@Wang2025].",
    title="Cross-study emergent coordination evidence",
)

design_driven_synthesis_obs = claim(
    "In design-driven studies (protein design: 57/177 = 32% synthesis fraction; materials "
    "discovery: 22/73 = 30% synthesis fraction), agents produced cross-agent synthesis events "
    "at rates of 30-32% without explicit task assignment, consistent with plannerless "
    "ArtifactReactor coordination [@Wang2025].",
    title="Design-driven studies synthesis observation",
)

open_ended_synthesis_obs = claim(
    "In open-ended reasoning studies (cross-domain resonance: 19/159 = 12% synthesis fraction; "
    "formal analogy: 25/52 = 48% synthesis fraction), agents produced cross-agent synthesis "
    "events at highly variable rates without explicit task assignment, demonstrating plannerless "
    "coordination even in unconstrained investigation modes [@Wang2025].",
    title="Open-ended studies synthesis observation",
)

strat_coord_s1 = support(
    [cross_study_coordination_claim],
    design_driven_synthesis_obs,
    reason=(
        "If plannerless coordination achieves genuine multi-agent integration at scale "
        "(@cross_study_coordination_claim), then design-driven studies — where agents have "
        "a defined design target — should show measurable synthesis fractions. "
        "The law predicts @design_driven_synthesis_obs (30-32% synthesis), "
        "which was confirmed by the protein and materials studies."
    ),
    prior=0.85,
)

strat_coord_s2 = support(
    [cross_study_coordination_claim],
    open_ended_synthesis_obs,
    reason=(
        "If plannerless coordination achieves genuine multi-agent integration at scale "
        "(@cross_study_coordination_claim), then open-ended studies — where no defined "
        "design target exists — should also show synthesis events through need broadcasting. "
        "The law predicts @open_ended_synthesis_obs, confirmed by resonance (12%) and "
        "formal analogy (48%) studies. The high variance is expected in unconstrained settings."
    ),
    prior=0.80,
)

strat_cross_study_coord = induction(
    strat_coord_s1,
    strat_coord_s2,
    law=cross_study_coordination_claim,
    reason=(
        "The four studies span two distinct investigation types (design-driven and open-ended) "
        "and four different scientific domains. The design-driven and open-ended pairs are "
        "largely independent in methodology and topic, providing two independent lines of "
        "evidence that plannerless coordination generalizes across investigation modes."
    ),
)
