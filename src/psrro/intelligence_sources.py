"""Phase 3R-01 source/evidence persistence primitives.

The point of this module is not to decide which source is "good". It persists
identity, lineage and access state so later claim/judgment logic can be audited.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping, Sequence

DERIVATIVE_RELATIONS = {
    "repost",
    "syndication",
    "shared_press_release",
    "shared_anonymous_origin",
}
ACCESS_LIMITED = {
    "partial",
    "paywall",
    "robots_blocked",
    "unavailable",
    "metadata_only",
    "unknown",
}


def _write_json(path: Path, obj: Mapping) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.write_text(payload, encoding="utf-8")


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class SourceStateStore:
    """Minimal file-backed store for durable source intelligence state."""

    def __init__(self, root: str | Path):
        self.root = Path(root)

    def upsert_source(self, record: Mapping) -> Path:
        path = self.root / "sources" / f"{record['source_id']}.json"
        _write_json(path, record)
        return path

    def get_source(self, source_id: str) -> dict:
        return _load_json(self.root / "sources" / f"{source_id}.json")

    def upsert_reputation(self, record: Mapping) -> Path:
        safe_domain = record["domain"].replace("/", "_")
        safe_claim = record["claim_type"].replace("/", "_")
        path = (
            self.root
            / "reputation"
            / record["source_id"]
            / f"{safe_domain}__{safe_claim}.json"
        )
        _write_json(path, record)
        return path

    def get_reputation(self, source_id: str, domain: str, claim_type: str) -> dict:
        return _load_json(
            self.root
            / "reputation"
            / source_id
            / f"{domain.replace('/', '_')}__{claim_type.replace('/', '_')}.json"
        )

    def put_observation(self, record: Mapping) -> Path:
        path = self.root / "observations" / f"{record['observation_id']}.json"
        _write_json(path, record)
        return path

    def get_observation(self, observation_id: str) -> dict:
        return _load_json(self.root / "observations" / f"{observation_id}.json")


def assess_source_concentration(
    observations: Sequence[Mapping],
    *,
    assessment_id: str = "sca-derived",
    claim_ref: str | None = None,
    as_of: str = "1970-01-01T00:00:00Z",
    sensitivity: str = "public",
) -> dict:
    """Assess independence without converting search-result count into evidence count."""

    if claim_ref is None:
        claim_refs = {obs.get("claim_ref") for obs in observations if obs.get("claim_ref")}
        if len(claim_refs) == 1:
            claim_ref = next(iter(claim_refs))
        elif not claim_refs:
            claim_ref = "claim-unknown"
        else:
            raise ValueError("observations must refer to one claim_ref")

    unique_sources = {obs["source_id"] for obs in observations}
    known_groups = {
        obs.get("lineage", {}).get("independence_group_id")
        for obs in observations
        if obs.get("lineage", {}).get("independence_group_id")
    }
    unknown_lineage = sum(
        not bool(obs.get("lineage", {}).get("independence_group_id"))
        or obs.get("lineage", {}).get("relation") == "unknown"
        for obs in observations
    )
    derivative_count = sum(
        obs.get("lineage", {}).get("relation") in DERIVATIVE_RELATIONS
        for obs in observations
    )
    access_limited_count = sum(
        obs.get("access_status") in ACCESS_LIMITED for obs in observations
    )

    reasons: list[str] = []

    if not observations or not known_groups:
        state = "UNKNOWN"
        single_source_bias = False
        reasons.append("independence lineage is insufficient to establish source diversity")
    elif len(known_groups) == 1 and unknown_lineage == 0:
        state = "SINGLE_ORIGIN"
        single_source_bias = True
        reasons.append("all observations trace to one known independence group")
    elif len(known_groups) == 1:
        state = "CONCENTRATED"
        single_source_bias = False
        reasons.append("one known origin plus unresolved lineage")
    else:
        state = "DIVERSE"
        single_source_bias = False
        reasons.append("at least two known independent evidence groups")

    if derivative_count:
        reasons.append(f"{derivative_count} derivative observations do not add independent evidence")
    if access_limited_count:
        reasons.append(f"{access_limited_count} observations have limited/unknown access")

    return {
        "schema_version": "0.1.0",
        "assessment_id": assessment_id,
        "claim_ref": claim_ref,
        "observation_ids": [obs["observation_id"] for obs in observations],
        "unique_source_count": len(unique_sources),
        "known_independence_group_count": len(known_groups),
        "unknown_lineage_count": unknown_lineage,
        "derivative_observation_count": derivative_count,
        "access_limited_count": access_limited_count,
        "state": state,
        "single_source_bias": single_source_bias,
        "reasons": reasons,
        "as_of": as_of,
        "sensitivity": sensitivity,
    }


def access_disclosure_required(observation: Mapping) -> bool:
    """True when the observation must disclose an access limitation."""
    return observation.get("access_status") in ACCESS_LIMITED


def can_claim_full_text_verified(observation: Mapping) -> bool:
    """Fail closed: only full_access + explicit verification supports this claim."""
    return (
        observation.get("access_status") == "full_access"
        and observation.get("provenance", {}).get("full_text_verified") is True
    )
