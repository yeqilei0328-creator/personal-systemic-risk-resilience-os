"""Food resilience verification v0.1.

Food resilience separates current buffer, nutrition planning, storage/cooking
continuity, replenishment diversity, and local-production support.

Local production is never treated as infinite food autonomy. Inventory days
remain inventory days.
"""

from __future__ import annotations

from typing import Mapping


def _independent_replenishment_paths(audit: Mapping) -> int:
    groups: set[str] = set()
    for path in audit["replenishment"]["supply_paths"]:
        if (
            path["status"] == "verified_available"
            and path["independence_group_id"]
        ):
            groups.add(str(path["independence_group_id"]))
    return len(groups)


def assess_food_verification(audit: Mapping) -> dict:
    blockers: list[str] = []
    scope = audit["service_scope"]
    demand = audit["demand"]
    inventory = audit["inventory"]
    nutrition = audit["nutrition"]
    storage = audit["storage"]
    cooking = audit["cooking"]
    replenishment = audit["replenishment"]

    daily_kcal = demand["daily_calorie_demand_kcal"]
    usable_kcal = inventory["usable_calories_kcal"]
    shelf_kcal = inventory["shelf_stable_calories_kcal"]

    inventory_gate = bool(
        inventory["inventory_count_status"] == "measured"
        and usable_kcal is not None
        and daily_kcal is not None
        and daily_kcal > 0
    )

    nutrition_gate = bool(
        nutrition["plan_status"] == "reviewed"
        and nutrition["protein_sources_mapped"] is True
        and nutrition["fat_sources_mapped"] is True
        and nutrition["micronutrient_strategy_mapped"] is True
        and nutrition["dietary_constraints_mapped"] is True
        and demand["special_requirements_mapped"] is True
    )

    cold_chain_gate = (
        storage["cold_chain_dependency"] in {"none", "partial"}
        or (
            storage["cold_chain_dependency"] == "critical"
            and storage["cold_chain_outage_test"] == "pass"
        )
    )

    storage_gate = bool(
        storage["dry_storage_status"] in {"inspected_pass", "not_required"}
        and storage["pest_moisture_control_status"] in {"adequate", "not_required"}
        and cold_chain_gate
    )

    cooking_gate = bool(
        cooking["outage_cooking_test"] in {"pass", "not_required"}
        and cooking["backup_path_status"] in {"tested_pass", "not_required"}
    )

    independent_paths = _independent_replenishment_paths(audit)

    production_support = bool(
        replenishment["local_production_status"] in {"measured_output", "field_tested"}
        and replenishment["production_daily_calorie_equivalent"] is not None
        and replenishment["production_daily_calorie_equivalent"] > 0
        and replenishment["production_inputs_mapped"] is True
    )

    replenishment_gate = bool(independent_paths >= 2 or production_support)

    buffer_days = None
    shelf_days = None
    if usable_kcal is not None and daily_kcal is not None and daily_kcal > 0:
        buffer_days = usable_kcal / daily_kcal
    if shelf_kcal is not None and daily_kcal is not None and daily_kcal > 0:
        shelf_days = shelf_kcal / daily_kcal

    asset_present = bool(
        (usable_kcal is not None and usable_kcal > 0)
        or inventory["inventory_count_status"] in {"estimated", "measured"}
        or replenishment["supply_paths"]
        or replenishment["local_production_status"] not in {"unknown", "none"}
    )

    measured_evidence = bool(inventory_gate)

    if scope == "unknown":
        blockers.append("food service scope not defined")

    if not inventory_gate:
        blockers.append("measured food inventory and daily demand baseline incomplete")

    if not nutrition_gate:
        blockers.append("nutrition coverage plan incomplete")

    if not storage_gate:
        blockers.append("food storage resilience not demonstrated")

    if storage["cold_chain_dependency"] == "critical" and storage["cold_chain_outage_test"] != "pass":
        blockers.append("critical cold-chain continuity not demonstrated")

    if not cooking_gate:
        blockers.append("outage cooking path not demonstrated")

    if scope == "sustained_resilience" and not replenishment_gate:
        blockers.append("independent replenishment or measured local production not demonstrated")

    if shelf_kcal is not None and usable_kcal is not None and shelf_kcal > usable_kcal:
        blockers.append("shelf-stable calories cannot exceed total usable calories")

    if not asset_present:
        blockers.append("no food resilience asset confirmed")
        status = "stated"
    elif not measured_evidence:
        status = "stated"
    else:
        status = "measured"

    if scope == "emergency_buffer":
        field_gate = inventory_gate and nutrition_gate and storage_gate and cooking_gate
    elif scope == "sustained_resilience":
        field_gate = (
            inventory_gate
            and nutrition_gate
            and storage_gate
            and cooking_gate
            and replenishment_gate
        )
    else:
        field_gate = False

    if status == "measured" and field_gate:
        status = "field_tested"

    if (
        status == "field_tested"
        and audit["independent_review_completed"]
        and audit["maintenance_status"] == "current"
        and inventory["rotation_status"] == "tested"
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
        "assessment_id": f"fva-{audit['food_audit_id'][4:]}",
        "food_audit_id": audit["food_audit_id"],
        "recommended_verification_status": status,
        "inventory_gate_passed": inventory_gate,
        "nutrition_gate_passed": nutrition_gate,
        "storage_gate_passed": storage_gate,
        "cooking_gate_passed": cooking_gate,
        "replenishment_gate_passed": replenishment_gate,
        "buffer_autonomy_days": None if buffer_days is None else round(buffer_days, 6),
        "shelf_stable_buffer_days": None if shelf_days is None else round(shelf_days, 6),
        "independent_replenishment_path_count": independent_paths,
        "production_support_candidate": production_support,
        "blockers": sorted(set(blockers)),
        "as_of": audit["updated_at"],
        "sensitivity": audit["data_sensitivity"],
    }
