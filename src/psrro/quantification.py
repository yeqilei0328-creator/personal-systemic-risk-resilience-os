"""Transparent v0.1 quantification for Personal Systemic Risk & Resilience OS.

This module intentionally avoids a single doomsday score. It produces structural
vectors and gate-based recommendations that can be inspected and challenged.
"""

from __future__ import annotations

from typing import Iterable, Mapping, Sequence

FIRST_ORDER_VARIABLES = ("A", "B", "C", "D")
MAX_DIRECTED_CROSS_VARIABLE_PAIRS = 12

HQ_PROVENANCE_MIN = 0.70
HQ_INDEPENDENCE_MIN = 0.60
HQ_CONFIDENCE_MIN = 0.60


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def _max_simple_path_length(pairs: set[tuple[str, str]]) -> int:
    adjacency = {node: set() for node in FIRST_ORDER_VARIABLES}
    for source, target in pairs:
        adjacency[source].add(target)

    best = 0

    def dfs(node: str, visited: set[str], length: int) -> None:
        nonlocal best
        best = max(best, length)
        for nxt in adjacency[node]:
            if nxt not in visited:
                dfs(nxt, visited | {nxt}, length + 1)

    for node in FIRST_ORDER_VARIABLES:
        dfs(node, {node}, 0)
    return best


def coupling_snapshot(
    edges: Sequence[Mapping],
    *,
    snapshot_id: str = "cpl-derived",
    as_of: str = "1970-01-01T00:00:00Z",
) -> dict:
    supported = [e for e in edges if e.get("state") in {"H1", "H2", "H3"}]
    validated = [e for e in edges if e.get("state") in {"H2", "H3"}]
    strong = [e for e in edges if e.get("state") == "H3"]

    cross_validated = [
        e for e in validated
        if e["source_node"]["first_order_variable"] != e["target_node"]["first_order_variable"]
    ]
    raw_pairs = {
        (e["source_node"]["first_order_variable"], e["target_node"]["first_order_variable"])
        for e in cross_validated
    }

    independent = [
        e for e in cross_validated
        if not e.get("common_cause", {}).get("present", False)
    ]
    independent_pairs = {
        (e["source_node"]["first_order_variable"], e["target_node"]["first_order_variable"])
        for e in independent
    }
    active_variables = {v for pair in independent_pairs for v in pair}
    persistent = [
        e for e in independent
        if e.get("persistence") in {"persistent", "structural"}
    ]
    common_cause_flagged = [
        e for e in validated if e.get("common_cause", {}).get("present", False)
    ]

    pair_density = len(raw_pairs) / MAX_DIRECTED_CROSS_VARIABLE_PAIRS
    independent_pair_density = len(independent_pairs) / MAX_DIRECTED_CROSS_VARIABLE_PAIRS
    common_cause_share = (
        len(common_cause_flagged) / len(validated) if validated else 0.0
    )
    max_path = _max_simple_path_length(independent_pairs)

    independent_pair_count = len(independent_pairs)
    active_count = len(active_variables)
    strong_count = len(strong)
    persistent_count = len(persistent)

    if (
        independent_pair_count >= 6
        and active_count == 4
        and persistent_count >= 4
        and strong_count >= 2
        and max_path >= 3
    ):
        band = "C3"
    elif (
        independent_pair_count >= 4
        and active_count >= 3
        and persistent_count >= 2
    ):
        band = "C2"
    elif independent_pair_count >= 2 and active_count >= 2:
        band = "C1"
    else:
        band = "C0"

    return {
        "schema_version": "0.1.0",
        "snapshot_id": snapshot_id,
        "as_of": as_of,
        "supported_edge_count": len(supported),
        "validated_edge_count": len(validated),
        "strong_edge_count": strong_count,
        "validated_cross_variable_edge_count": len(cross_validated),
        "unique_validated_directed_pairs": len(raw_pairs),
        "independent_validated_directed_pairs": independent_pair_count,
        "pair_density": round(pair_density, 6),
        "independent_pair_density": round(independent_pair_density, 6),
        "active_variable_count": active_count,
        "coactivation_breadth": round(active_count / 4, 6),
        "persistent_validated_edge_count": persistent_count,
        "common_cause_flagged_validated_edges": len(common_cause_flagged),
        "common_cause_share": round(common_cause_share, 6),
        "max_independent_path_length": max_path,
        "band": band,
        "sensitivity": "public",
    }


def buffer_remaining_fraction(buffer: Mapping) -> float:
    baseline = float(buffer["baseline_capacity"])
    current = float(buffer["current_capacity"])
    floor = float(buffer["minimum_viable_capacity"])
    if baseline <= floor:
        raise ValueError("baseline_capacity must be > minimum_viable_capacity")
    return _clamp((current - floor) / (baseline - floor))


def buffer_floor_days(buffer: Mapping) -> float | None:
    current = float(buffer["current_capacity"])
    floor = float(buffer["minimum_viable_capacity"])
    net_burn = float(buffer["depletion_rate_per_day"]) - float(buffer["replenishment_rate_per_day"])
    if net_burn <= 0:
        return None
    margin = max(0.0, current - floor)
    return margin / net_burn


def buffer_snapshot(
    buffers: Sequence[Mapping],
    *,
    snapshot_id: str = "bfs-derived",
    as_of: str = "1970-01-01T00:00:00Z",
) -> dict:
    critical = [b for b in buffers if int(b["criticality"]) >= 4]
    coverage_gap = len(critical) == 0

    remaining = {b["buffer_id"]: buffer_remaining_fraction(b) for b in critical}
    below_75 = sum(v < 0.75 for v in remaining.values())
    below_50 = sum(v < 0.50 for v in remaining.values())
    below_25 = sum(v < 0.25 for v in remaining.values())
    depleting = sum(
        float(b["depletion_rate_per_day"]) > float(b["replenishment_rate_per_day"])
        for b in critical
    )

    min_remaining = min(remaining.values()) if remaining else 1.0
    floor_days = [buffer_floor_days(b) for b in critical]
    floor_days = [d for d in floor_days if d is not None]
    earliest_floor = min(floor_days) if floor_days else None

    if min_remaining <= 0.10 or below_25 >= 2:
        band = "B3"
    elif min_remaining < 0.50 or below_50 >= 2:
        band = "B2"
    elif min_remaining < 0.75 or below_75 >= 2 or depleting >= 1:
        band = "B1"
    else:
        band = "B0"

    return {
        "schema_version": "0.1.0",
        "snapshot_id": snapshot_id,
        "as_of": as_of,
        "buffer_ids": [b["buffer_id"] for b in buffers],
        "critical_buffer_count": len(critical),
        "critical_below_75_count": below_75,
        "critical_below_50_count": below_50,
        "critical_below_25_count": below_25,
        "critical_depleting_count": depleting,
        "min_critical_remaining_fraction": round(min_remaining, 6),
        "earliest_floor_days": None if earliest_floor is None else round(earliest_floor, 6),
        "coverage_gap": coverage_gap,
        "band": band,
        "sensitivity": "public",
    }


def _is_high_quality(evidence: Mapping) -> bool:
    quality = evidence.get("quality", {})
    return (
        float(quality.get("provenance_score", 0)) >= HQ_PROVENANCE_MIN
        and float(quality.get("independence_score", 0)) >= HQ_INDEPENDENCE_MIN
        and float(quality.get("confidence", 0)) >= HQ_CONFIDENCE_MIN
    )


def recommend_edge_state(
    edge: Mapping,
    evidence_records: Sequence[Mapping],
    assessment: Mapping,
) -> dict:
    reasons: list[str] = []

    if assessment.get("falsification_triggered"):
        return {
            "recommended_state": "Hx",
            "reasons": ["falsification condition triggered"],
        }

    evidence_ids = set(edge.get("evidence_ids", []))
    relevant = [e for e in evidence_records if e.get("evidence_id") in evidence_ids]
    supports = [e for e in relevant if e.get("stance") == "supports"]
    refutes = [e for e in relevant if e.get("stance") == "refutes"]

    high_quality_support_sources = {
        e.get("source", {}).get("name")
        for e in supports
        if _is_high_quality(e) and e.get("source", {}).get("name")
    }
    high_quality_refutes = [e for e in refutes if _is_high_quality(e)]

    mechanism_ok = bool(edge.get("mechanism")) and bool(assessment.get("mechanism_documented"))
    temporal_ok = bool(assessment.get("temporal_ordering_confirmed"))
    metric_ok = bool(assessment.get("metric_observed")) and any(
        metric.get("latest_value") is not None for metric in edge.get("metrics", [])
    )
    unresolved_common_cause = (
        edge.get("common_cause", {}).get("present", False)
        and not assessment.get("common_cause_resolved", False)
    )
    unresolved_counterevidence = (
        bool(high_quality_refutes)
        and not assessment.get("counterevidence_resolved", False)
    )

    if not supports or not mechanism_ok:
        if not supports:
            reasons.append("no supporting evidence")
        if not mechanism_ok:
            reasons.append("mechanism not documented")
        return {"recommended_state": "H0", "reasons": reasons}

    h2_gates = [
        (len(high_quality_support_sources) >= 2, "fewer than two independent high-quality support sources"),
        (temporal_ok, "temporal ordering not confirmed"),
        (metric_ok, "quantitative metric not observed"),
        (not unresolved_common_cause, "unresolved common cause"),
        (not unresolved_counterevidence, "unresolved high-quality counterevidence"),
    ]
    failed = [message for ok, message in h2_gates if not ok]
    if failed:
        return {"recommended_state": "H1", "reasons": failed}

    persistence_observations = int(assessment.get("persistence_observations", 0))
    h3 = (
        len(high_quality_support_sources) >= 3
        and persistence_observations >= 3
        and edge.get("persistence") in {"persistent", "structural"}
    )
    if h3:
        reasons.append("validated across at least three independent high-quality sources")
        reasons.append("persistence observed across at least three assessment windows")
        return {"recommended_state": "H3", "reasons": reasons}

    reasons.append("H2 validation gates satisfied")
    return {"recommended_state": "H2", "reasons": reasons}


def recommend_r_level(
    scenario: Mapping,
    exposure: Mapping,
    *,
    governance_integrity: str = "G0",
    preparation_latency_days: float = 0.0,
    local_disruption: bool = False,
    life_safety_failure: bool = False,
) -> dict:
    reasons: list[str] = []
    impact = int(scenario["impact"])
    p_high = float(scenario["probability"]["high"])
    lead_min = float(scenario["lead_time"]["min_days"])
    velocity = scenario["velocity"]
    gross_exposure = max(int(v) for v in exposure["dimensions"].values())
    sensitivity = int(exposure["sensitivity_score"])
    adaptive = int(exposure["adaptive_capacity_score"])
    material_exposure = gross_exposure >= 3 or sensitivity >= 3
    low_adaptive = adaptive <= 2
    readiness_gap = float(preparation_latency_days) > lead_min
    g_level = int(governance_integrity[1])

    if life_safety_failure:
        return {
            "recommended_r_level": "R5",
            "readiness_gap": readiness_gap,
            "reasons": ["current life-safety capability failure"],
        }

    if (
        (local_disruption and (impact >= 4 or gross_exposure >= 4))
        or (g_level >= 3 and gross_exposure >= 4)
    ):
        reasons.append("direct/local disruption or severe governance degradation")
        return {"recommended_r_level": "R4", "readiness_gap": readiness_gap, "reasons": reasons}

    if (
        impact >= 4
        and material_exposure
        and (p_high >= 0.50 or velocity in {"fast", "acute"})
        and (lead_min <= 30 or readiness_gap)
        and (low_adaptive or gross_exposure >= 4)
    ) or (
        g_level >= 2 and gross_exposure >= 4 and p_high >= 0.25
    ):
        reasons.append("high-impact material exposure with compressed action window")
        return {"recommended_r_level": "R3", "readiness_gap": readiness_gap, "reasons": reasons}

    if (
        impact >= 3 and material_exposure and p_high >= 0.25
    ) or (
        impact >= 5 and gross_exposure >= 2 and readiness_gap
    ) or (
        impact >= 3 and gross_exposure >= 2 and readiness_gap and lead_min <= 180
    ):
        reasons.append("preparation is justified before the window narrows further")
        return {"recommended_r_level": "R2", "readiness_gap": readiness_gap, "reasons": reasons}

    if (
        impact >= 2 and gross_exposure >= 2 and p_high >= 0.10
    ) or (
        impact >= 4 and gross_exposure >= 1
    ):
        reasons.append("material enough to watch, not enough for higher-cost action")
        return {"recommended_r_level": "R1", "readiness_gap": readiness_gap, "reasons": reasons}

    reasons.append("no material personal action gate crossed")
    return {"recommended_r_level": "R0", "readiness_gap": readiness_gap, "reasons": reasons}
