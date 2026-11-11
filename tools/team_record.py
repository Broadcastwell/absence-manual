"""The team record (brief 18.5) and the author a page's structured data must name (brief 13.4, STEP 3.3 B117).

Names and roles only; no photo, biography, calendar or availability. overrides/brand.html carries the same
twelve as bw_team, and tests/test_docs_gate_20261111.py fails when the two differ.

A library answer shows "Page owner: <name>, <role>" (library_owner) and a research page shows "Lead: <name>"
(lead). On a brand page that byline person is the Article author, a Person with the team-record role;
every other page's author is the one Organization, by reference.
"""

TEAM = {
    "Sairam Sivakumar": "Founder",
    "Priya Nair": "Management Consultant, delivery lead and reviewer",
    "Vikram Patel": "AI Architect and Specialist",
    "Ananya Rao": "AI Engineer",
    "Arjun Mehta": "Management Consultant",
    "Ethan Brooks": "Management Consultant",
    "Rohan Iyer": "AI Engineer",
    "Daniel Kim": "AI Engineer",
    "Marcus Reed": "AI Architect and Specialist",
    "Noah Bennett": "AI Architect and Specialist",
    "Lauren Chen": "AI Architect and Specialist",
    "Maya Thompson": "AI Architect and Specialist",
}
ORGANIZATION_ID = "https://broadcastwell.com/#organization"
ORGANIZATION_REF = {"@type": "Organization", "@id": ORGANIZATION_ID, "name": "Broadcastwell"}


def byline_name(meta):
    """The person the page's visible byline names, or None."""
    meta = meta or {}
    if meta.get("page_class") == "research" and meta.get("lead"):
        return str(meta["lead"]).strip()
    if (meta.get("library_cluster") or meta.get("library_hub")) and meta.get("library_owner"):
        return str(meta["library_owner"]).split(",")[0].strip()
    return None


def expected_author(meta):
    """The exact author node a brand page's Article (and a research Dataset's creator) must carry."""
    name = byline_name(meta)
    if name in TEAM:
        return {"@type": "Person", "name": name, "jobTitle": TEAM[name], "worksFor": ORGANIZATION_REF}
    return ORGANIZATION_REF
