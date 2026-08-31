"""Water-resilience verification v0.1.

This module deliberately avoids claiming indefinite water autonomy from the
mere existence of a well. It reports measured storage autonomy and minimum
demonstrated continuity separately.
"""

from __future__ import annotations

from typing import Mapping


def assess_water_verification(audit: Mapping) -> dict:
    blockers: list[str] = []

    source = audit["source"]
    hydraulics = audit["hydraulics"]
    power = audit["power"]
    treatment = audit["treatment"]
    quality = audit["quality"]
    continuity = audit["continuity"]
    scope = audit["service_scope"]

    source_present = bool(source["presence_confirmed"])
    measured_supply = (
        hydraulics.get("flow_test") is not None
        or hydraulics.get("usable_storage_liters") is not None
    )

    potability_required = scope in {"potable", "mixed"}
    potability_gate = (
        not potability_required
        or quality["potability_status"] in {"lab_verified", "authority_verified"}
    )

    if quality.get("consumer_sensor_only") and potability_required:
        blockers.append("consumer sensors do not establish potability")

    extraction_requires_power = power["extraction_requires_power"]
    if extraction_requires_power is None:
        blockers.append("extraction power requirement unknown")
        extraction_power_gate = False
    else:
        extraction_power_gate = (
            not extraction_requires_power
            or power["outage_extraction_test"] == "pass"
            or power["primary_power"] == "manual"
        )
    outage_gate = continuity["outage_test"] == "pass" and extraction_power_gate

    if extraction_requires_power is True and power["outage_extraction_test"] != "pass":
        blockers.append("outage extraction path not demonstrated")

    if potability_required and not potability_gate:
        blockers.append("potability not independently verified")

    if potability_required and treatment["required"] is None:
        blockers.append("treatment requirement unknown")
    if potability_required and treatment["required"] is True and treatment["system_status"] != "operational_tested":
        blockers.append("required treatment path not operationally tested")

    storage = hydraulics.get("usable_storage_liters")
    demand = continuity.get("daily_demand_liters")
    storage_days = None
    if storage is not None and demand is not None:
        storage_days = storage / demand

    field_hours = continuity.get("field_test_duration_hours")
    demonstrated_days = None
    if outage_gate and field_hours is not None:
        demonstrated_days = field_hours / 24.0

    flow = hydraulics.get("flow_test")
    continuous_candidate = bool(
        flow
        and flow.get("sustained_flow_lpm", 0) > 0
        and outage_gate
        and (potability_gate or not potability_required)
    )

    if not source_present:
        blockers.append("water source presence not confirmed")
        status = "stated"
    elif not measured_supply:
        blockers.append("no measured flow or usable storage")
        status = "stated"
    else:
        status = "measured"

    treatment_gate = (
        not potability_required
        or (
            treatment["required"] is False
            or (
                treatment["required"] is True
                and treatment["system_status"] == "operational_tested"
            )
        )
    )

    if status == "measured" and outage_gate and (potability_gate or not potability_required) and treatment_gate:
        status = "field_tested"

    if (
        status == "field_tested"
        and audit.get("independent_review_completed")
        and audit.get("maintenance_status") == "current"
        and audit.get("evidence_refs")
        and not audit.get("single_points_of_failure")
        and all(
            dep.get("backup_status") not in {"none", "unknown"}
            for dep in audit.get("dependencies", [])
            if dep.get("critical")
        )
    ):
        status = "audited"

    return {
        "schema_version": "0.1.0",
        "assessment_id": f"wva-{audit['water_audit_id'][4:]}",
        "water_audit_id": audit["water_audit_id"],
        "recommended_verification_status": status,
        "potability_gate_passed": potability_gate,
        "outage_gate_passed": outage_gate,
        "storage_autonomy_days": None if storage_days is None else round(storage_days, 6),
        "minimum_demonstrated_continuity_days": None if demonstrated_days is None else round(demonstrated_days, 6),
        "continuous_source_candidate": continuous_candidate,
        "blockers": sorted(set(blockers)),
        "as_of": audit["updated_at"],
        "sensitivity": audit["data_sensitivity"],
    }
