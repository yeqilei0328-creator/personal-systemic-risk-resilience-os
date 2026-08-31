"""Phase 3R-02 event / claim state primitives.

The module persists V0.3 event-cluster and atomic-claim state. It does not
perform semantic news extraction or decide P0 automatically.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Mapping, Sequence

SAFE_COMPONENT = re.compile(r"^[A-Za-z0-9._-]+$")
MATERIAL_LIFECYCLES = {"confirmed", "contained", "reversed", "closed"}


def _safe_component(value: str, label: str) -> str:
    if not SAFE_COMPONENT.fullmatch(value) or value in {".", ".."}:
        raise ValueError(f"unsafe {label}: {value!r}")
    return value


def _write_json(path: Path, obj: Mapping) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.write_text(payload, encoding="utf-8")


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_text(value: str) -> str:
    return " ".join(value.casefold().split())


def _normalize_list(values: Sequence[str]) -> list[str]:
    return sorted({_normalize_text(v) for v in values if _normalize_text(v)})


def event_fingerprint(basis: Mapping) -> str:
    """Stable fingerprint from V0.3 Actor+Action+Object+Location+Time+Consequence."""
    normalized = {
        "actors": _normalize_list(basis.get("actors", [])),
        "actions": _normalize_list(basis.get("actions", [])),
        "objects": _normalize_list(basis.get("objects", [])),
        "locations": _normalize_list(basis.get("locations", [])),
        "time_window_key": _normalize_text(str(basis.get("time_window_key", ""))),
        "consequences": _normalize_list(basis.get("consequences", [])),
    }
    if not normalized["actors"] or not normalized["actions"] or not normalized["time_window_key"]:
        raise ValueError("fingerprint requires actors, actions, and time_window_key")
    payload = json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class EventClaimStateStore:
    """Minimal deterministic file-backed event/claim state store."""

    def __init__(self, root: str | Path):
        self.root = Path(root)

    def put_event(self, record: Mapping) -> Path:
        event_id = _safe_component(str(record["event_id"]), "event_id")
        path = self.root / "events" / f"{event_id}.json"
        _write_json(path, record)
        return path

    def get_event(self, event_id: str) -> dict:
        event_id = _safe_component(event_id, "event_id")
        return _load_json(self.root / "events" / f"{event_id}.json")

    def put_claim(self, record: Mapping) -> Path:
        claim_id = _safe_component(str(record["claim_id"]), "claim_id")
        path = self.root / "claims" / f"{claim_id}.json"
        _write_json(path, record)
        return path

    def get_claim(self, claim_id: str) -> dict:
        claim_id = _safe_component(claim_id, "claim_id")
        return _load_json(self.root / "claims" / f"{claim_id}.json")

    def put_value_observation(self, record: Mapping) -> Path:
        value_id = _safe_component(str(record["value_observation_id"]), "value_observation_id")
        claim_id = _safe_component(str(record["claim_id"]), "claim_id")
        path = self.root / "claim-values" / claim_id / f"{value_id}.json"
        _write_json(path, record)
        return path

    def get_value_observation(self, claim_id: str, value_observation_id: str) -> dict:
        claim_id = _safe_component(claim_id, "claim_id")
        value_id = _safe_component(value_observation_id, "value_observation_id")
        return _load_json(self.root / "claim-values" / claim_id / f"{value_id}.json")

    def put_material_change(self, record: Mapping) -> Path:
        assessment_id = _safe_component(str(record["assessment_id"]), "assessment_id")
        event_id = _safe_component(str(record["event_id"]), "event_id")
        path = self.root / "material-change" / event_id / f"{assessment_id}.json"
        _write_json(path, record)
        return path

    def get_material_change(self, event_id: str, assessment_id: str) -> dict:
        event_id = _safe_component(event_id, "event_id")
        assessment_id = _safe_component(assessment_id, "assessment_id")
        return _load_json(
            self.root / "material-change" / event_id / f"{assessment_id}.json"
        )


def numeric_material_change(
    policy: Mapping | None,
    previous_value: float,
    current_value: float,
) -> tuple[bool, str]:
    """Apply claim-specific materiality without inventing a global numeric threshold."""
    if policy is None:
        return False, "no dynamic-value policy"

    rule = policy["materiality_rule"]
    absolute_delta = abs(float(current_value) - float(previous_value))

    if rule == "none":
        return False, "materiality rule is none"
    if rule == "any_change":
        return absolute_delta > 0, "any-change rule"

    absolute_threshold = policy.get("absolute_delta")
    relative_threshold = policy.get("relative_delta")
    absolute_hit = (
        absolute_threshold is not None and absolute_delta >= float(absolute_threshold)
    )

    relative_hit = False
    relative_defined = float(previous_value) != 0
    if relative_threshold is not None and relative_defined:
        relative_delta = absolute_delta / abs(float(previous_value))
        relative_hit = relative_delta >= float(relative_threshold)

    if rule == "absolute":
        return absolute_hit, "absolute-delta rule"
    if rule == "relative":
        if not relative_defined:
            return False, "relative delta undefined from zero baseline"
        return relative_hit, "relative-delta rule"
    if rule == "either":
        if absolute_threshold is None and relative_threshold is None:
            raise ValueError("either rule requires at least one threshold")
        return absolute_hit or relative_hit, "either absolute/relative rule"

    raise ValueError(f"unsupported materiality rule: {rule}")


def detect_material_change(
    previous: Mapping | None,
    current: Mapping,
    *,
    changed_claim_ids: Sequence[str] = (),
    numeric_change_refs: Sequence[str] = (),
    claim_grade_changed: bool = False,
    assessment_id: str = "mca-derived",
    current_state_ref: str = "current",
    previous_state_ref: str | None = None,
    assessed_at: str = "1970-01-01T00:00:00Z",
) -> dict:
    """Detect structural update, excluding display-title/source-list noise."""
    change_types: list[str] = []
    reasons: list[str] = []

    if previous is None:
        change_types.append("new_event")
        reasons.append("new event entered the candidate/event state")
        material = True
        priority_from = None
    else:
        if previous["event_id"] != current["event_id"]:
            raise ValueError("cannot compare different event_id values")
        if previous["fingerprint"] != current["fingerprint"]:
            raise ValueError("event fingerprint drift requires re-clustering, not in-place comparison")

        priority_from = previous["intelligence_priority"]
        if priority_from != current["intelligence_priority"]:
            change_types.append("priority_change")
            reasons.append(
                f"priority changed {priority_from}->{current['intelligence_priority']}"
            )

        previous_markers = set(previous.get("material_markers", []))
        current_markers = set(current.get("material_markers", []))
        added = sorted(current_markers - previous_markers)
        removed = sorted(previous_markers - current_markers)
        if added:
            change_types.append("material_marker_added")
            reasons.append("material markers added: " + ", ".join(added))
        if removed:
            change_types.append("material_marker_removed")
            reasons.append("material markers removed: " + ", ".join(removed))

        if (
            previous.get("lifecycle") != current.get("lifecycle")
            and (
                previous.get("lifecycle") in MATERIAL_LIFECYCLES
                or current.get("lifecycle") in MATERIAL_LIFECYCLES
            )
        ):
            change_types.append("lifecycle_change")
            reasons.append(
                f"lifecycle changed {previous.get('lifecycle')}->{current.get('lifecycle')}"
            )

        if claim_grade_changed:
            change_types.append("claim_grade_change")
            reasons.append("one or more material claim grades changed")

        if numeric_change_refs:
            change_types.append("numeric_material_change")
            reasons.append("one or more dynamic claims crossed their own materiality rule")

        material = bool(change_types)
        if not material:
            change_types.append("non_material_update")
            reasons.append("only non-material metadata/title/source-list update detected")

    return {
        "schema_version": "0.1.0",
        "assessment_id": assessment_id,
        "event_id": current["event_id"],
        "previous_state_ref": previous_state_ref,
        "current_state_ref": current_state_ref,
        "material": material,
        "change_types": change_types,
        "changed_claim_ids": sorted(set(changed_claim_ids)),
        "numeric_change_refs": sorted(set(numeric_change_refs)),
        "priority_from": priority_from,
        "priority_to": current["intelligence_priority"],
        "reasons": reasons,
        "assessed_at": assessed_at,
        "sensitivity": current.get("sensitivity", "public"),
    }
