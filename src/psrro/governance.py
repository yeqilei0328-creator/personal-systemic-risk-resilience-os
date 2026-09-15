from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from typing import Any

FAIL_CLOSED_STATES = {
    "UNKNOWN",
    "MISSING",
    "DRIFTED",
    "STALE",
    "UNVERIFIED",
    "UNAUTHORIZED",
    "CONFLICTING_EVIDENCE",
}

RED_FLAGS = {
    "production_write",
    "private_raw_evidence_write",
    "credential_or_account",
    "payment_or_procurement",
    "device_access_or_control",
    "physical_dispatch",
    "destructive_action",
}

AMBER_FLAGS = {
    "governance_change",
    "workflow_change",
    "critical_schema_change",
    "permission_router_change",
    "dependency_widening",
    "architecture_widening",
    "security_boundary_change",
    "method_pin_change",
}

TECH_BLOCKER = {
    "failed_disciplined_fix",
    "repeated_failure_class",
    "third_party_runtime_framework_sdk_or_platform",
    "low_or_unknown_root_cause_confidence",
    "critical_path_delay",
}

TECH_DECISION = {
    "proposed_architecture_widening",
    "proposed_dependency_widening",
    "proposed_scope_widening",
    "proposed_security_widening",
}

COMMERCIAL_DISCOVERY = {
    "market_assumption_change",
    "commercial_debt_change",
}

COMMERCIAL_VALIDATION = {
    "commercial_evidence_change",
    "customer_zero_evidence_change",
    "external_m2_or_higher_evidence_change",
    "commercial_thesis_contradiction",
}

DUAL = {
    "major_product_decision",
    "major_architecture_decision",
    "next_major_technical_iteration",
    "critical_path_rebaseline",
    "new_capability_family",
    "new_industry_pack",
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def evidence_fingerprint(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _enabled(mapping: Mapping[str, Any], names: set[str]) -> list[str]:
    return sorted(name for name in names if bool(mapping.get(name)))


def fail_closed(recovered_states: list[str] | tuple[str, ...] | set[str]) -> dict[str, Any]:
    matched = sorted(set(recovered_states) & FAIL_CLOSED_STATES)
    return {
        "fail_closed": bool(matched),
        "matched_states": matched,
    }


def route_authority(facts: Mapping[str, Any]) -> dict[str, Any]:
    red = _enabled(facts, RED_FLAGS)
    amber = _enabled(facts, AMBER_FLAGS)

    if red:
        return {
            "authority": "RED",
            "matched_flags": red,
            "fresh_owner_authorization_required": True,
            "authorization_granted_equals_consumed": False,
            "automatic_retry_after_consumption": 0,
        }

    if amber:
        return {
            "authority": "AMBER",
            "matched_flags": amber,
            "explicit_review_required": True,
        }

    return {
        "authority": "GREEN",
        "matched_flags": [],
        "continuous_execution_allowed": True,
    }


def _triggered(verdict: str, matched: list[str]) -> dict[str, Any]:
    return {
        "verdict": verdict,
        "matched_triggers": matched,
        "authority_widened": False,
        "next_action_handoff": {
            "gpt_handoff_required": True,
            "local_execution_disposition": "STOP_LOCAL_SPECULATION_ALLOW_READONLY_EVIDENCE",
            "resume_condition": "RADAR_RESULT_RECONCILED_BY_GPT_CONTROL_PLANE",
        },
    }


def route_radar(triggers: Mapping[str, Any]) -> dict[str, Any]:
    dual = _enabled(triggers, DUAL)
    if dual:
        return _triggered("DUAL_RADAR_MAJOR_DECISION", dual)

    blocker = _enabled(triggers, TECH_BLOCKER)
    if blocker:
        return _triggered("TECH_RADAR_BLOCKER", blocker)

    tech_decision = _enabled(triggers, TECH_DECISION)
    if tech_decision:
        return _triggered("TECH_RADAR_DECISION", tech_decision)

    commercial_validation = _enabled(triggers, COMMERCIAL_VALIDATION)
    if commercial_validation:
        return _triggered("COMMERCIAL_RADAR_VALIDATION", commercial_validation)

    commercial_discovery = _enabled(triggers, COMMERCIAL_DISCOVERY)
    if commercial_discovery:
        return _triggered("COMMERCIAL_RADAR_DISCOVERY", commercial_discovery)

    return {
        "verdict": "NO_RADAR",
        "matched_triggers": [],
        "authority_widened": False,
        "next_action_handoff": None,
    }