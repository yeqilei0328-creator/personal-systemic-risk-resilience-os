"""Phase 3R-04 precision output/alert gate.

Scheduled briefs and interrupt alerts are intentionally separate modes.
The gate consumes already-structured state; it does not classify news prose.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from typing import Mapping

SIGNAL_NAMES = (
    "geopolitical_conflicts",
    "energy_shipping",
    "east_asia_security",
    "extreme_weather_disasters",
    "price_real_economy_transmission",
)


def _parse_dt(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        raise ValueError("datetime must be timezone-aware")
    return dt.astimezone(timezone.utc)


def _iso_z(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def output_state_signature(candidate: Mapping) -> str:
    """Hash only gate-relevant state; timestamps/notes do not create novelty."""
    signals = {
        name: {
            "direction": candidate["observation_signals"][name]["direction"],
            "real_world_evidence": candidate["observation_signals"][name]["real_world_evidence"],
        }
        for name in SIGNAL_NAMES
    }
    payload = {
        "subject_ref": candidate["subject_ref"],
        "event_ids": sorted(candidate.get("event_ids", [])),
        "delivery_mode": candidate["delivery_mode"],
        "intelligence_priority": candidate["intelligence_priority"],
        "material_change": candidate["material_change"],
        "structural_delta_material": candidate["structural_delta_material"],
        "observation_signals": signals,
        "validated_cross_system_transmission": candidate["validated_cross_system_transmission"],
        "major_system_event": candidate["major_system_event"],
        "new_strong_edge": candidate["new_strong_edge"],
        "hypothesis_falsified": candidate["hypothesis_falsified"],
        "lead_time_compressed": candidate["lead_time_compressed"],
        "global_stage_change": candidate["global_stage_change"],
        "global_stage_direction": candidate["global_stage_direction"],
        "personal_action_change": candidate["personal_action_change"],
        "common_cause_refs": sorted(candidate.get("common_cause_refs", [])),
    }
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def decide_output_gate(
    candidate: Mapping,
    context: Mapping,
    *,
    decision_id: str = "ogd-derived",
) -> dict:
    """Return EMIT/SUPPRESS without sending any notification."""
    reasons: list[str] = []
    triggers: list[str] = []
    suppressions: list[str] = []
    signature = output_state_signature(candidate)
    mode = candidate["delivery_mode"]
    now = _parse_dt(context["now"])

    worsening_count = sum(
        candidate["observation_signals"][name]["direction"] == "worsen"
        and candidate["observation_signals"][name]["real_world_evidence"] is True
        for name in SIGNAL_NAMES
    )

    def decision(notify: bool, next_eligible_at: str | None = None) -> dict:
        return {
            "schema_version": "0.1.0",
            "decision_id": decision_id,
            "candidate_id": candidate["candidate_id"],
            "delivery_mode": mode,
            "notify": notify,
            "outcome": "EMIT" if notify else "SUPPRESS",
            "trigger_codes": triggers,
            "suppression_codes": suppressions,
            "state_signature": signature,
            "worsening_signal_count": worsening_count,
            "next_eligible_at": next_eligible_at,
            "reasons": reasons,
            "decided_at": context["now"],
            "sensitivity": candidate.get("sensitivity", "public"),
        }

    if candidate["intelligence_priority"] == "P3":
        suppressions.append("P3_SILENT")
        reasons.append("P3 is stored/background and does not interrupt the user")
        return decision(False)

    if not candidate["material_change"]:
        suppressions.append("NO_SUBSTANTIVE_CHANGE")
        reasons.append("no material change since the prior state")
        return decision(False)

    previous_signature = context.get("previous_notified_state_signature")
    if previous_signature and previous_signature == signature:
        suppressions.append("DUPLICATE_STATE")
        reasons.append("gate-relevant state is identical to the previously notified state")
        return decision(False)

    if mode == "scheduled_brief":
        triggers.append("SCHEDULED_MATERIAL_ITEM")
        reasons.append("P0-P2 scheduled-brief item has material new information")
        return decision(True)

    if candidate["intelligence_priority"] == "P0":
        triggers.append("P0_MATERIAL")
    if (
        worsening_count >= 3
        and candidate["structural_delta_material"]
        and candidate["validated_cross_system_transmission"]
    ):
        triggers.append("TRIGGER_A_RESONANCE")
    if candidate["major_system_event"]:
        triggers.append("TRIGGER_B_MAJOR_EVENT")
    if candidate["new_strong_edge"] and candidate["structural_delta_material"]:
        triggers.append("TRIGGER_C_NEW_STRONG_EDGE")
    if candidate["hypothesis_falsified"]:
        triggers.append("HYPOTHESIS_FALSIFIED")
    if candidate["lead_time_compressed"]:
        triggers.append("LEAD_TIME_COMPRESSION")
    if candidate["global_stage_change"]:
        triggers.append("GLOBAL_STAGE_CHANGE")
    if candidate["personal_action_change"]:
        triggers.append("PERSONAL_ACTION_CHANGE")

    if not triggers:
        suppressions.append("NO_TRIGGER")
        reasons.append("material update did not cross any interrupt-alert trigger")
        return decision(False)

    # Cooldown/hysteresis apply only to a low-level resonance-only re-alert.
    low_level_resonance_only = set(triggers) == {"TRIGGER_A_RESONANCE"}

    if low_level_resonance_only:
        h = context["hysteresis"]
        if h["applicable"] and h["persistence_count"] < h["required_count"]:
            suppressions.append("HYSTERESIS")
            reasons.append(
                f"threshold persistence {h['persistence_count']}/{h['required_count']} is insufficient"
            )
            return decision(False)

        last = context.get("last_notified_at")
        cooldown_hours = float(context["cooldown_hours"])
        if last and cooldown_hours > 0:
            eligible = _parse_dt(last) + timedelta(hours=cooldown_hours)
            if now < eligible:
                suppressions.append("COOLDOWN")
                reasons.append("repeated resonance remains inside cooldown window")
                return decision(False, _iso_z(eligible))

    reasons.append("material update crossed an interrupt-alert gate")
    return decision(True)
