"""Phase 3R-03 behavior and structural-delta reference logic.

These helpers compare structured evidence/state. They do not infer actor intent
from prose and do not create a single aggregate risk score.
"""

from __future__ import annotations

from typing import Mapping

RESOURCE_ORDER = {"none": 0, "low": 1, "medium": 2, "high": 3, "unknown": -1}
PERSISTENCE_GATE = {"repeated", "sustained", "structural"}
REVERSIBILITY_GATE = {"moderate", "hard", "committed"}
H_ORDER = {"H0": 0, "H1": 1, "H2": 2, "H3": 3}
C_ORDER = {"C0": 0, "C1": 1, "C2": 2, "C3": 3}
B_ORDER = {"B0": 0, "B1": 1, "B2": 2, "B3": 3}
VELOCITY_ORDER = {"slow": 0, "medium": 1, "fast": 2, "acute": 3}


def assess_costly_signal(
    behavior: Mapping,
    *,
    assessment_id: str = "csa-derived",
    assessed_at: str = "1970-01-01T00:00:00Z",
) -> dict:
    """Assess observable costly-signal strength without treating speech as action."""
    reasons: list[str] = []

    if not behavior.get("observable_action", False) or behavior.get("behavior_kind") == "speech":
        return {
            "schema_version": "0.1.0",
            "assessment_id": assessment_id,
            "behavior_id": behavior["behavior_id"],
            "eligible": False,
            "strength": "NOT_APPLICABLE",
            "resource_commitment_present": False,
            "persistence_gate": False,
            "reversibility_gate": False,
            "reasons": ["speech/non-observable action cannot establish a costly signal"],
            "assessed_at": assessed_at,
            "sensitivity": behavior.get("sensitivity", "public"),
        }

    levels = list(behavior["resource_commitment"].values())
    known = [RESOURCE_ORDER[v] for v in levels if v != "unknown"]
    if not known:
        strength = "UNKNOWN"
        resource_present = False
        reasons.append("resource commitment is unknown")
    else:
        max_resource = max(known)
        resource_present = max_resource > 0
        persistence_gate = behavior["persistence"] in PERSISTENCE_GATE
        reversibility_gate = behavior["reversibility"] in REVERSIBILITY_GATE

        if max_resource >= 3 and (persistence_gate or behavior["reversibility"] in {"hard", "committed"}):
            strength = "STRONG"
        elif resource_present and (persistence_gate or reversibility_gate):
            strength = "MODERATE"
        else:
            strength = "WEAK"

        reasons.append(f"max resource commitment level={max_resource}")
        if persistence_gate:
            reasons.append("behavior persists beyond one-off action")
        if reversibility_gate:
            reasons.append("behavior has meaningful reversal cost")

    persistence_gate = behavior["persistence"] in PERSISTENCE_GATE
    reversibility_gate = behavior["reversibility"] in REVERSIBILITY_GATE

    return {
        "schema_version": "0.1.0",
        "assessment_id": assessment_id,
        "behavior_id": behavior["behavior_id"],
        "eligible": True,
        "strength": strength,
        "resource_commitment_present": resource_present,
        "persistence_gate": persistence_gate,
        "reversibility_gate": reversibility_gate,
        "reasons": reasons,
        "assessed_at": assessed_at,
        "sensitivity": behavior.get("sensitivity", "public"),
    }


def classify_rhetoric_action_gap(rhetoric_direction: str, behavior_direction: str) -> str:
    if "unknown" in {rhetoric_direction, behavior_direction}:
        return "unknown"
    if "mixed" in {rhetoric_direction, behavior_direction}:
        return "mixed"
    if rhetoric_direction == behavior_direction:
        return "aligned"

    order = {"easing": -1, "neutral": 0, "intensifying": 1}
    if order[rhetoric_direction] > order[behavior_direction]:
        return "rhetoric_more_intensifying"
    return "behavior_more_intensifying"


def classify_h_state_delta(from_state: str, to_state: str) -> str:
    if from_state == to_state:
        return "unchanged"
    if to_state == "Hx":
        return "falsified"
    if from_state == "Hx":
        return "recovered"
    if from_state not in H_ORDER or to_state not in H_ORDER:
        return "uncertain"
    return "strengthened" if H_ORDER[to_state] > H_ORDER[from_state] else "weakened"


def classify_coupling_delta(from_band: str, to_band: str) -> str:
    if from_band == to_band:
        return "unchanged"
    return "denser" if C_ORDER[to_band] > C_ORDER[from_band] else "sparser"


def classify_buffer_delta(from_band: str, to_band: str) -> str:
    if from_band == to_band:
        return "unchanged"
    if "BU" in {from_band, to_band}:
        return "unknown"
    return "depleted" if B_ORDER[to_band] > B_ORDER[from_band] else "restored"


def classify_scenario_delta(previous: Mapping, current: Mapping) -> dict:
    p_low_delta = float(current["probability"]["low"]) - float(previous["probability"]["low"])
    p_high_delta = float(current["probability"]["high"]) - float(previous["probability"]["high"])
    lead_min_delta = float(current["lead_time"]["min_days"]) - float(previous["lead_time"]["min_days"])
    lead_max_delta = float(current["lead_time"]["max_days"]) - float(previous["lead_time"]["max_days"])

    worsening = []
    improving = []

    if p_low_delta > 0 or p_high_delta > 0:
        worsening.append("probability increased")
    if p_low_delta < 0 or p_high_delta < 0:
        improving.append("probability decreased")

    v_from = previous["velocity"]
    v_to = current["velocity"]
    if VELOCITY_ORDER[v_to] > VELOCITY_ORDER[v_from]:
        worsening.append("velocity accelerated")
    elif VELOCITY_ORDER[v_to] < VELOCITY_ORDER[v_from]:
        improving.append("velocity slowed")

    if lead_min_delta < 0 or lead_max_delta < 0:
        worsening.append("lead time compressed")
    if lead_min_delta > 0 or lead_max_delta > 0:
        improving.append("lead time expanded")

    if worsening and improving:
        direction = "mixed"
    elif worsening:
        direction = "worse"
    elif improving:
        direction = "improved"
    else:
        direction = "unchanged"

    return {
        "scenario_id": current["scenario_id"],
        "probability_low_delta": round(p_low_delta, 6),
        "probability_high_delta": round(p_high_delta, 6),
        "velocity_from": v_from,
        "velocity_to": v_to,
        "lead_time_min_days_delta": round(lead_min_delta, 6),
        "lead_time_max_days_delta": round(lead_max_delta, 6),
        "direction": direction,
        "reasons": worsening + improving,
    }
