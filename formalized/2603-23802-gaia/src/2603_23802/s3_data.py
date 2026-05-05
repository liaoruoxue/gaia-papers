"""Section 3: Data -- MCP server harvesting and download tracking.

Section 3 of Stein 2026 [@Stein2026]. Specifies how the 177k-tool panel
was constructed:

* 3.1 -- identification of MCP servers from GitHub, the Smithery
  registry, and two prominent MCP-server lists, with LLM-based
  validation reducing 73,338 candidates to 19,388 verified servers
  exposing 177,436 distinct tools.
* 3.2 -- a sub-set of 8,469 tools on 'official' commercial servers,
  used to confirm that findings carry over to production deployments.
* 3.3 -- monthly NPM and PyPI download counts (11/2024-02/2026)
  matched to 3,854 servers / 42,498 tools as a usage proxy, with
  validation against Smithery use-counts.

This module records the methodology *and* the dataset-scale claims
(numbers of servers, tools, downloads, official-server share) that
later inferential claims in s5 and s7 will rest on.
"""

from gaia.lang import claim, setting

from .motivation import setup_mcp_definition

# ---------------------------------------------------------------------------
# 3.1 Sources and selection
# ---------------------------------------------------------------------------

setup_collection_window = setting(
    "**Data-collection window.** MCP servers were harvested over the "
    "16-month window **November 2024 to February 2026**. Servers created "
    "before October 2025 had their READMEs and tool descriptions captured "
    "on **1 October 2025**; servers created later were captured on **1 "
    "February 2026**. Download statistics were captured on **1 March 2026**. "
    "This means within-server changes after the snapshot date are not "
    "tracked, but cross-server creation-date evolution is.",
    title="Setup: 16-month panel window with two snapshot dates",
)

claim_data_sources = claim(
    "**Three primary data sources.** MCP servers were identified through "
    "(1) **GitHub** repository search for code repositories whose name, "
    "description, README, or tags contain 'mcp server' and that have at "
    "least 1 star (n = 16,956 servers in the final dataset); (2) the "
    "**Smithery MCP registry** (n = 2,437) -- chosen over the official "
    "MCP registry because Smithery has a more permissive API and is an "
    "order of magnitude larger as of 02/2026; (3) **two MCP-server "
    "lists** for prominent / official servers -- the official MCP "
    "repository (n = 841) and the popular `awesome MCP servers` list "
    "(n = 781). All 1,366 entries from source (3) also appear in "
    "source (1) or (2).",
    title="Three sources: GitHub, Smithery, MCP-server lists",
    background=[setup_mcp_definition, setup_collection_window],
)

claim_validation_pipeline = claim(
    "**LLM-validated filtering.** After deduplication and removal of "
    "0-star repositories, **Claude Sonnet 4.5** was used to verify each "
    "candidate was an actual MCP server (not documentation, link list, "
    "or unrelated code). Only servers with clearly defined tools in their "
    "README files or descriptions were retained. This reduced the initial "
    "candidate pool from **73,338** to **19,388** verified servers, "
    "exposing a final dataset of **177,436 distinct agent tools**.",
    title="Validation: 73,338 -> 19,388 verified servers, 177,436 tools",
    background=[setup_mcp_definition],
)

claim_dataset_scale = claim(
    "**Final dataset scale (Section 3 headline).** The constructed panel "
    "comprises:\n\n"
    "| Quantity | Count |\n"
    "|---|---:|\n"
    "| Verified MCP servers | **19,388** |\n"
    "| Distinct agent tools | **177,436** |\n"
    "| Servers in 'official' (commercial-entity) subset | 8,469 tools / "
    "subset of servers |\n"
    "| Servers with NPM/PyPI download data | **3,854** |\n"
    "| Tools on servers with download data | **42,498** |\n"
    "| Total downloads tracked (11/2024-02/2026) | **78M** |\n"
    "| Of which: from official-server subset | **45M** |\n"
    "| Window | 11/2024 - 02/2026 (~16 months) |\n",
    title="Dataset scale summary",
)

# ---------------------------------------------------------------------------
# 3.2 Official servers
# ---------------------------------------------------------------------------

claim_official_subset_definition = claim(
    "**Official-server subset.** A subset of MCP servers published by "
    "**legally registered commercial entities** (PayPal, Stripe, Google, "
    "GitHub, Microsoft, etc., as marked on the MCP-server lists) was "
    "extracted to verify that findings extend to production-grade "
    "deployments. The subset comprises **8,469 of 177k total tools** but "
    "is disproportionately popular -- it accounts for **45 million of 78 "
    "million** total tracked NPM/PyPI downloads (~58%). The owning "
    "entities collectively produce >3 GBP billion in 2024 UK AI-specific "
    "revenue, ~20% of the UK AI sector by AI-revenue, providing "
    "ecological validity.",
    title="Official subset: 8,469 tools, 45M downloads, ~20% of UK AI sector",
)

# ---------------------------------------------------------------------------
# 3.3 Downloads as usage proxy
# ---------------------------------------------------------------------------

claim_downloads_as_usage_proxy = claim(
    "**NPM/PyPI downloads as a usage proxy.** Monthly download counts "
    "from NPM and PyPI for **3,854 servers / 42,498 tools** are used "
    "throughout the paper as a proxy for tool usage. These counts measure "
    "*installation events* (e.g. `claude mcp add playwright`, `uv tool "
    "install arxiv-mcp-server`), not individual tool calls, and they "
    "exclude private mirrors, cached installs, and direct source-code "
    "use. The proxy therefore captures **relative trends and "
    "distribution shifts**, not absolute execution counts. Cross-checks "
    "against Smithery's CLI/OAuth use counts indicate the sample is "
    "*slightly developer-biased* (IT tools account for 90% of "
    "PyPI/NPM-tracked downloads vs 80% of Smithery uses).",
    title="Downloads as usage proxy: relative-trend faithful, developer-biased",
)

claim_downloads_concentration = claim(
    "**Download concentration (Appendix A.7).** Downloads are highly "
    "concentrated. For NPM, the **top 1% of servers (13 servers) account "
    "for 79.3%** of downloads and the top 10% account for 93.1%. For "
    "PyPI, the top 1% (also 13 servers) account for 42.9% and the top "
    "10% for 74.5%. Aggregate trends are therefore sensitive to the "
    "classification of a small number of high-traffic servers.",
    title="Concentration: top 1% of servers carry 43-79% of downloads",
)

# ---------------------------------------------------------------------------
# 3.2 Geographic-split data sub-sample
# ---------------------------------------------------------------------------

claim_geography_subsample = claim(
    "**Geography sub-sample (Section 4.2).** Country-level download splits "
    "based on PyPI IP-address geolocation are available for **528 MCP "
    "servers with action tools**, totalling **N = 11.91 million downloads** "
    "for the period **11/2024-10/2025**. This is a sub-sample of the "
    "**2,467 servers with action tools** that have any download data (out "
    "of 11,174 servers with action tools in total). Geographic splits are "
    "**not available** for NPM, nor for PyPI in 11/2025-02/2026.",
    title="Geography sub-sample: 528 action-tool servers, 11.91M downloads",
)

__all__ = [
    "setup_collection_window",
    "claim_data_sources",
    "claim_validation_pipeline",
    "claim_dataset_scale",
    "claim_official_subset_definition",
    "claim_downloads_as_usage_proxy",
    "claim_downloads_concentration",
    "claim_geography_subsample",
]
