"""Mobility resilience verification v0.1."""

from __future__ import annotations
from typing import Mapping


def _independent_count(rows: list[Mapping], pass_status: str) -> int:
    return len({
        str(row["independence_group_id"])
        for row in rows
        if row["status"] == pass_status and row["independence_group_id"]
    })


def assess_mobility_verification(audit: Mapping) -> dict:
    blockers: list[str] = []
    scope = audit["service_scope"]
    mission = audit["mission"]
    maintenance = audit["maintenance"]
    navigation = audit["navigation"]
    mission_test = audit["mission_test"]

    mission_gate = bool(
        mission["people_capacity_required"] is not None
        and mission["cargo_capacity_kg_required"] is not None
        and mission["target_distance_km"] is not None
        and mission["route_requirements_mapped"] is True
    )

    ready = [v for v in audit["vehicles"] if v["availability"] == "tested_ready"]
    tested_ready_count = len(ready)

    eligible = []
    if mission_gate:
        for vehicle in ready:
            if (
                vehicle["demonstrated_range_km"] is not None
                and vehicle["demonstrated_range_km"] >= mission["target_distance_km"]
                and vehicle["people_capacity"] is not None
                and vehicle["people_capacity"] >= mission["people_capacity_required"]
                and vehicle["cargo_capacity_kg"] is not None
                and vehicle["cargo_capacity_kg"] >= mission["cargo_capacity_kg_required"]
                and vehicle["degraded_mission_test"] == "pass"
            ):
                eligible.append(vehicle)
    vehicle_gate = bool(eligible)

    independent_energy = _independent_count(audit["energy_paths"], "tested_available")
    independent_routes = _independent_count(audit["routes"], "tested_pass")

    if scope == "local_continuity":
        energy_gate = independent_energy >= 1
        route_gate = independent_routes >= 1
    elif scope == "evacuation_and_logistics":
        energy_gate = independent_energy >= 2
        route_gate = independent_routes >= 2
    else:
        energy_gate = False
        route_gate = False

    maintenance_gate = bool(
        maintenance["status"] == "current"
        and maintenance["tires_checked"] is True
        and maintenance["critical_spares_mapped"] is True
        and maintenance["repair_tools_ready"] is True
        and maintenance["service_dependency_mapped"] is True
    )

    offline_nav_gate = bool(
        navigation["online_dependency"] in {"none", "partial"}
        and navigation["offline_maps_status"] in {"tested_access", "not_required"}
    )

    if scope == "unknown":
        blockers.append("mobility service scope not defined")
    if not mission_gate:
        blockers.append("mobility mission baseline incomplete")
    if not vehicle_gate:
        blockers.append("no tested-ready vehicle demonstrates required mission")
    if not energy_gate:
        blockers.append("required independent mobility energy paths not demonstrated")
    if not route_gate:
        blockers.append("required independent route paths not demonstrated")
    if not maintenance_gate:
        blockers.append("mobility maintenance/spares readiness incomplete")
    if not offline_nav_gate:
        blockers.append("offline navigation continuity not demonstrated")

    asset_present = any(v["availability"] != "unknown" for v in audit["vehicles"])
    measured_evidence = bool(
        mission_gate
        and any(
            v["demonstrated_range_km"] is not None
            or v["people_capacity"] is not None
            or v["cargo_capacity_kg"] is not None
            for v in audit["vehicles"]
        )
    )

    if not asset_present:
        blockers.append("no mobility asset confirmed")
        status = "stated"
    elif not measured_evidence:
        status = "stated"
    else:
        status = "measured"

    mission_test_gate = bool(
        mission_test["status"] == "pass"
        and mission_test["distance_km"] is not None
        and mission_gate
        and mission_test["distance_km"] >= mission["target_distance_km"]
        and mission_test["people_count"] is not None
        and mission_test["people_count"] >= mission["people_capacity_required"]
        and mission_test["cargo_kg"] is not None
        and mission_test["cargo_kg"] >= mission["cargo_capacity_kg_required"]
    )

    full_gate = (
        mission_gate and vehicle_gate and energy_gate and route_gate
        and maintenance_gate and offline_nav_gate and mission_test_gate
    )
    if status == "measured" and full_gate:
        status = "field_tested"

    if (
        status == "field_tested"
        and audit["independent_review_completed"]
        and audit["evidence_refs"]
        and not audit["single_points_of_failure"]
        and all(
            dep["backup_status"] not in {"none", "unknown"}
            for dep in audit["dependencies"]
            if dep["critical"]
        )
    ):
        status = "audited"

    demonstrated_km = (
        float(mission_test["distance_km"])
        if mission_test_gate else None
    )

    return {
        "schema_version": "0.1.0",
        "assessment_id": f"mva-{audit['mobility_audit_id'][4:]}",
        "mobility_audit_id": audit["mobility_audit_id"],
        "recommended_verification_status": status,
        "mission_gate_passed": mission_gate,
        "vehicle_gate_passed": vehicle_gate,
        "energy_replenishment_gate_passed": energy_gate,
        "route_gate_passed": route_gate,
        "maintenance_gate_passed": maintenance_gate,
        "offline_navigation_gate_passed": offline_nav_gate,
        "tested_ready_vehicle_count": tested_ready_count,
        "independent_energy_path_count": independent_energy,
        "independent_route_count": independent_routes,
        "minimum_demonstrated_mission_km": demonstrated_km,
        "blockers": sorted(set(blockers)),
        "as_of": audit["updated_at"],
        "sensitivity": audit["data_sensitivity"],
    }
