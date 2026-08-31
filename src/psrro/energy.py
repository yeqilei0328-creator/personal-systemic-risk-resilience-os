"""Energy resilience verification v0.1.

Nameplate assets are not outage capability. This module separates measured
capacity, islanding, black-start, critical-load knowledge and demonstrated
continuity. Renewable generation never becomes an infinite-autonomy claim.
"""

from __future__ import annotations

from typing import Mapping


def assess_energy_verification(audit: Mapping) -> dict:
    blockers: list[str] = []
    generation = audit["generation"]
    storage = audit["storage"]
    conversion = audit["conversion"]
    loads = audit["loads"]
    outage = audit["outage_test"]

    asset_present = any(
        value is True
        for value in (
            generation["pv_present"],
            generation["generator_present"],
            storage["battery_present"],
            conversion["inverter_present"],
        )
    )

    measured_capacity = any(
        value is not None
        for value in (
            generation["pv_measured_peak_kw"],
            storage["usable_kwh"],
            storage["max_continuous_output_kw"],
            loads["critical_peak_kw"],
            loads["critical_energy_kwh_per_day"],
            outage["energy_served_kwh"],
        )
    )

    islanding_gate = conversion["islanding_status"] in {"tested_pass", "not_applicable"}
    black_start_gate = conversion["black_start_status"] in {"tested_pass", "not_applicable"}
    critical_load_gate = (
        loads["critical_loads_mapped"] is True
        and loads["critical_energy_kwh_per_day"] is not None
    )

    if conversion["islanding_status"] in {"unknown", "capable_unverified"}:
        blockers.append("islanding capability not demonstrated")
    elif conversion["islanding_status"] in {"not_capable", "tested_fail"}:
        blockers.append("islanding capability unavailable or failed")

    if conversion["black_start_status"] in {"unknown", "unverified"}:
        blockers.append("black-start capability not demonstrated")
    elif conversion["black_start_status"] in {"not_supported", "tested_fail"}:
        blockers.append("black-start capability unavailable or failed")

    if not critical_load_gate:
        blockers.append("critical-load demand baseline incomplete")

    if loads["essential_circuits_tested"] is not True:
        blockers.append("essential circuits not field tested")

    storage_days = None
    if storage["usable_kwh"] is not None and loads["critical_energy_kwh_per_day"] is not None:
        storage_days = storage["usable_kwh"] / loads["critical_energy_kwh_per_day"]

    demonstrated_days = None
    if outage["status"] == "pass" and outage["duration_hours"] is not None:
        demonstrated_days = outage["duration_hours"] / 24.0

    renewable_candidate = bool(
        generation["pv_present"] is True
        and generation["pv_measured_peak_kw"] is not None
        and generation["pv_measured_peak_kw"] > 0
        and islanding_gate
        and black_start_gate
        and outage["status"] == "pass"
        and critical_load_gate
    )

    backup_generation_candidate = bool(
        generation["generator_present"] is True
        and generation["generator_rated_kw"] is not None
        and generation["generator_rated_kw"] > 0
        and outage["status"] == "pass"
        and black_start_gate
    )

    if not asset_present:
        blockers.append("no resilience energy asset confirmed")
        status = "stated"
    elif not measured_capacity:
        blockers.append("no measured usable capacity or critical-load demand")
        status = "stated"
    else:
        status = "measured"

    outage_gate = (
        outage["status"] == "pass"
        and outage["duration_hours"] is not None
        and outage["duration_hours"] > 0
        and islanding_gate
        and black_start_gate
        and critical_load_gate
        and loads["essential_circuits_tested"] is True
    )

    if status == "measured" and outage_gate:
        status = "field_tested"

    if (
        status == "field_tested"
        and audit["independent_review_completed"]
        and audit["maintenance_status"] == "current"
        and audit["evidence_refs"]
        and not audit["single_points_of_failure"]
        and all(
            dep["backup_status"] not in {"none", "unknown"}
            for dep in audit["dependencies"]
            if dep["critical"]
        )
    ):
        status = "audited"

    return {
        "schema_version": "0.1.0",
        "assessment_id": f"eva-{audit['energy_audit_id'][4:]}",
        "energy_audit_id": audit["energy_audit_id"],
        "recommended_verification_status": status,
        "islanding_gate_passed": islanding_gate,
        "black_start_gate_passed": black_start_gate,
        "critical_load_gate_passed": critical_load_gate,
        "storage_autonomy_days": None if storage_days is None else round(storage_days, 6),
        "minimum_demonstrated_continuity_days": None if demonstrated_days is None else round(demonstrated_days, 6),
        "renewable_sustaining_candidate": renewable_candidate,
        "backup_generation_candidate": backup_generation_candidate,
        "blockers": sorted(set(blockers)),
        "as_of": audit["updated_at"],
        "sensitivity": audit["data_sensitivity"],
    }
