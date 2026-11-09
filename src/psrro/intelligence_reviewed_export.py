"""Operator-reviewed public event packet -> PSRRO native stores, one-shot only.

No scraping, LLM extraction, scheduling, notification, or upstream state mutation.
The caller must have separately reviewed the publicly accessible evidence.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .intelligence_events import EventClaimStateStore, event_fingerprint
from .intelligence_sources import SourceStateStore

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_SCHEMA_NAMES = {
    "event_state": "event-state-record.schema.json",
    "claim": "claim-record.schema.json",
    "material_change": "material-change-assessment.schema.json",
    "observation": "source-observation.schema.json",
}
_REQUIRED = {
    "packet_version", "review_mode", "reviewer_type", "reviewed_at", "review_notes",
    "event_state", "claims", "material_change", "source_observations",
}
_PACKET_VERSION = "psrro-reviewed-public-event.v0.1"
_CONTRACT_SHA = "574b17ade4ee52628ccf5806e0f129e8fd267b0e"
_MAX_BYTES = 262144


def _parse_time(value: Any, field: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f"{field}_invalid")
    try:
        when = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field}_invalid") from exc
    if when.tzinfo is None:
        raise ValueError(f"{field}_no_timezone")
    return when.astimezone(timezone.utc)


def _safe_id(value: Any, label: str, prefix: str) -> str:
    if not isinstance(value, str) or not _SAFE_ID.fullmatch(value) or not value.startswith(prefix):
        raise ValueError(f"{label}_invalid")
    return value


def _unique_json(pairs: list[tuple[str, Any]]) -> dict:
    result: dict[str, Any] = {}
    for k, value in pairs:
        if k in result:
            raise ValueError("duplicate_json_key:" + k)
        result[k] = value
    return result


def read_packet(path: Path) -> dict[str, Any]:
    """Reject symlinks, oversized input, nonobject JSON, and duplicate keys."""
    path = Path(path)
    if path.is_symlink() or not path.is_file() or path.stat().st_size > _MAX_BYTES:
        raise ValueError("packet_path_or_size_invalid")
    try:
        packet = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_json)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("packet_json_invalid") from exc
    if not isinstance(packet, dict):
        raise ValueError("packet_not_object")
    return packet


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def _schema_validate(record: Any, name: str) -> None:
    # jsonschema is already a development dependency of the PSRRO repository.
    # This one-shot CLI never widens runtime dependencies.
    from jsonschema import Draft202012Validator, FormatChecker

    schema = json.loads((_REPO_ROOT / "schemas" / _SCHEMA_NAMES[name]).read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record),
                    key=lambda e: (list(map(str, e.absolute_path)), e.message))
    if errors:
        raise ValueError(f"{name}_schema_invalid:{errors[0].message}")


def validate_reviewed_packet(packet: Mapping[str, Any]) -> dict[str, Any]:
    """Structural + cross-record validation, no automatic fact-claim judgement."""
    if not isinstance(packet, dict) or set(packet) != _REQUIRED:
        raise ValueError("packet_fields_invalid")
    if packet["packet_version"] != _PACKET_VERSION or packet["review_mode"] != "reviewed_public_sources":
        raise ValueError("packet_version_or_review_mode_invalid")
    if packet["reviewer_type"] not in ("ai_assistant", "human_operator"):
        raise ValueError("reviewer_type_invalid")
    reviewed = _parse_time(packet["reviewed_at"], "reviewed_at")
    if not isinstance(packet["review_notes"], list) or not packet["review_notes"] or any(
        not isinstance(note, str) or not note.strip() for note in packet["review_notes"]
    ):
        raise ValueError("review_notes_missing")

    event = packet["event_state"]
    assessment = packet["material_change"]
    claims = packet["claims"]
    observations = packet["source_observations"]
    _schema_validate(event, "event_state")
    _schema_validate(assessment, "material_change")
    if not isinstance(claims, list) or not claims or not isinstance(observations, list) or not observations:
        raise ValueError("claims_or_observations_missing")
    for item in claims:
        _schema_validate(item, "claim")
    for item in observations:
        _schema_validate(item, "observation")

    eid = _safe_id(event["event_id"], "event_id", "evt-")
    _safe_id(assessment["assessment_id"], "assessment_id", "mca-")
    if assessment["event_id"] != eid:
        raise ValueError("assessment_event_mismatch")
    if event_fingerprint(event["fingerprint_basis"]) != event["fingerprint"]:
        raise ValueError("event_fingerprint_mismatch")
    first = _parse_time(event["first_seen"], "first_seen")
    updated = _parse_time(event["last_updated"], "last_updated")
    assessed = _parse_time(assessment["assessed_at"], "assessed_at")
    if not (first <= updated <= assessed <= reviewed):
        raise ValueError("event_review_chronology_invalid")
    if event["intelligence_priority"] != assessment["priority_to"]:
        raise ValueError("assessment_priority_mismatch")
    if "new_event" in assessment["change_types"]:
        if not assessment["material"] or assessment["previous_state_ref"] is not None or assessment["priority_from"] is not None:
            raise ValueError("new_event_assessment_inconsistent")
    if event["sensitivity"] != "public" or assessment["sensitivity"] != "public":
        raise ValueError("private_data_disallowed")

    claim_ids: set[str] = set()
    for claim in claims:
        cid = _safe_id(claim["claim_id"], "claim_id", "clm-")
        if cid in claim_ids:
            raise ValueError("duplicate_claim")
        claim_ids.add(cid)
        if claim["event_id"] != eid or claim["sensitivity"] != "public":
            raise ValueError("claim_event_or_privacy_mismatch")
        if _parse_time(claim["last_updated"], "claim_updated") > assessed:
            raise ValueError("claim_updated_after_assessment")
        if _parse_time(claim["grade_updated_at"], "claim_grade_updated") > reviewed:
            raise ValueError("claim_grade_updated_after_review")

    # Cross-record successor integrity belongs to authoritative PSRRO.
    # Schema syntax alone cannot reject a validly shaped dangling reference.
    # No semantic opinion about whether a historical Claim is factually true.
    claim_by_id = {claim["claim_id"]: claim for claim in claims}
    for claim in claims:
        cid = claim["claim_id"]
        successor = claim["superseded_by_claim_id"]
        if claim["status"] != "superseded":
            if successor is not None:
                raise ValueError("non_superseded_claim_with_successor")
            continue
        if successor == cid:
            raise ValueError("self_supersession_denied")
        if successor not in claim_by_id:
            raise ValueError("supersession_successor_not_in_packet")
    for claim in claims:
        visited: set[str] = set()
        cursor = claim
        while cursor["status"] == "superseded":
            cid = cursor["claim_id"]
            if cid in visited:
                raise ValueError("supersession_cycle_denied")
            visited.add(cid)
            cursor = claim_by_id[cursor["superseded_by_claim_id"]]

    observation_ids: set[str] = set()
    for obs in observations:
        oid = _safe_id(obs["observation_id"], "observation_id", "sob-")
        if oid in observation_ids:
            raise ValueError("duplicate_observation")
        observation_ids.add(oid)
        if obs["claim_ref"] not in claim_ids or obs["sensitivity"] != "public":
            raise ValueError("observation_claim_or_privacy_mismatch")
        if obs["access_status"] not in ("full_access", "partial", "metadata_only"):
            raise ValueError("source_access_not_admitted")
        source_url = obs["provenance"]["source_locator"]
        if not isinstance(source_url, str) or not source_url.startswith("https://") or any(c.isspace() for c in source_url):
            raise ValueError("invalid_source_locator")
        retrieved = _parse_time(obs["retrieved_at"], "retrieved_at")
        published = obs.get("published_at")
        if retrieved > reviewed or (published and _parse_time(published, "published_at") > retrieved):
            raise ValueError("observation_review_chronology_invalid")
        if obs["provenance"]["full_text_verified"] and obs["access_status"] != "full_access":
            raise ValueError("fulltext_access_contradiction")

    if set(event["claim_ids"]) != claim_ids or set(event["source_observation_ids"]) != observation_ids:
        raise ValueError("event_refs_inconsistent")
    for claim in claims:
        ids = claim["source_observation_ids"]
        if not ids or not set(ids).issubset(observation_ids):
            raise ValueError("claim_sources_inconsistent")
        if not any(obs["claim_ref"] == claim["claim_id"] for obs in observations):
            raise ValueError("claim_has_no_supporting_observation")
    if not set(assessment["changed_claim_ids"]).issubset(claim_ids):
        raise ValueError("assessment_claim_refs_inconsistent")
    if not assessment["reasons"] or not isinstance(assessment["material"], bool):
        raise ValueError("assessment_missing_reason")

    return {
        "event_id": eid,
        "assessment_id": assessment["assessment_id"],
        "packet_sha256": hashlib.sha256(_canonical(packet)).hexdigest(),
        "reviewed_at": packet["reviewed_at"],
        "claim_count": len(claims),
        "source_count": len(observations),
    }


def export_reviewed_packet(packet: Mapping[str, Any], output_root: Path) -> dict[str, Any]:
    """Write only into a new temporary-folder output root, never existing live state.

    Uses the authoritative PSRRO native store classes on isolated scratch output.
    """
    proof = validate_reviewed_packet(packet)
    output_root = Path(output_root).expanduser()
    scratch_roots = {Path(tempfile.gettempdir()).resolve(), Path("/tmp").resolve()}
    destination = output_root.resolve()
    if destination == _REPO_ROOT.resolve() or _REPO_ROOT.resolve() in destination.parents:
        raise ValueError("scratch_output_inside_method_repo_denied")
    if not any(root in destination.parents for root in scratch_roots):
        raise ValueError("scratch_output_must_be_under_system_tmp")
    if output_root.exists() or output_root.is_symlink():
        raise ValueError("scratch_output_already_exists")
    if not destination.parent.is_dir() or destination.parent.is_symlink():
        raise ValueError("scratch_parent_invalid")

    with tempfile.TemporaryDirectory(prefix="psrro-review-stage-", dir=destination.parent) as stage_name:
        stage = Path(stage_name)
        events = EventClaimStateStore(stage)
        sources = SourceStateStore(stage)
        written = []
        written.append(events.put_event(packet["event_state"]))
        for claim in packet["claims"]:
            written.append(events.put_claim(claim))
        for obs in packet["source_observations"]:
            written.append(sources.put_observation(obs))
        written.append(events.put_material_change(packet["material_change"]))

        manifest = {
            "export_contract": "psrro-native-reviewed-export.v0.1",
            "review_mode": packet["review_mode"],
            "reviewer_type": packet["reviewer_type"],
            "upstream_contract_commit": _CONTRACT_SHA,
            "evidence_reviewed_at": packet["reviewed_at"],
            "packet_sha256": proof["packet_sha256"],
            "event_id": proof["event_id"],
            "assessment_id": proof["assessment_id"],
            "artifacts": [
                {
                    "path": str(path.relative_to(stage)),
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                }
                for path in sorted(written)
            ],
            "source_urls": sorted(obs["provenance"]["source_locator"] for obs in packet["source_observations"]),
            "limitations": [
                "reviewed_sources_not_automated_news_ingestion",
                "source_locators_declared_evidence_not_independently_attested_by_exporter",
                "first_discovery_not_global_systemic_transmission",
            ],
        }
        manifest_content = _canonical(manifest) + b"\n"
        (stage / "review-manifest.json").write_bytes(manifest_content)
        if destination.exists():
            raise ValueError("scratch_output_collision")
        os.rename(stage, destination)
    return {"status": "NATIVE_REVIEWED_EXPORTED", **proof, "manifest_sha256": hashlib.sha256(manifest_content).hexdigest()}
