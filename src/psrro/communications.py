"""Communications / Network / Offline Compute resilience verification v0.1.

Internet availability, internal LAN survival, external path diversity, local
runtime, and power continuity are deliberately separate gates.
"""

from __future__ import annotations

from typing import Mapping


def _tested_external_links(audit: Mapping) -> list[Mapping]:
    return [
        link
        for link in audit["external_links"]
        if link["status"] == "tested_pass"
        and link["bidirectional"] is True
        and link["test_runtime_hours"] is not None
        and link["test_runtime_hours"] > 0
        and link["independence_group_id"]
    ]


def _external_redundancy_metrics(audit: Mapping) -> tuple[int, int, float | None]:
    tested = _tested_external_links(audit)
    group_best: dict[str, float] = {}
    for link in tested:
        group = str(link["independence_group_id"])
        runtime = float(link["test_runtime_hours"])
        group_best[group] = max(group_best.get(group, 0.0), runtime)

    independent_count = len(group_best)
    continuity_hours = min(group_best.values()) if independent_count >= 2 else None
    return len(tested), independent_count, continuity_hours


def assess_communications_verification(audit: Mapping) -> dict:
    blockers: list[str] = []
    scope = audit["service_scope"]
    power = audit["power"]
    internal = audit["internal_network"]
    offline = audit["offline_compute"]

    tested_paths, independent_paths, external_hours = _external_redundancy_metrics(audit)

    internal_gate = bool(
        internal["local_lan_status"] == "tested_pass"
        and internal["internet_loss_test"] == "pass"
        and internal["local_control_path_without_internet"] is True
    )

    external_gate = bool(tested_paths >= 2 and independent_paths >= 2)

    offline_gate = bool(
        offline["local_compute_present"] is True
        and offline["critical_workloads_identified"] is True
        and offline["local_runtime_status"] == "tested_pass"
        and offline["cloud_dependency_status"] in {"none", "partial"}
        and offline["offline_data_status"] in {"tested_access", "not_required"}
    )

    power_gate = bool(
        power["critical_power_path_mapped"] is True
        and power["backup_power_status"] in {"ready", "not_required"}
        and power["power_outage_test"] in {"pass", "not_required"}
    )

    asset_present = bool(
        internal["local_lan_status"] not in {"unknown", "not_capable"}
        or audit["external_links"]
        or offline["local_compute_present"] is True
    )

    measured_evidence = bool(
        (power["tested_runtime_hours"] is not None and power["tested_runtime_hours"] > 0)
        or tested_paths > 0
        or internal["internet_loss_test"] == "pass"
    )

    if scope == "unknown":
        blockers.append("communications service scope not defined")

    if scope in {"internal_network", "full_resilient_stack"}:
        if internal["topology_mapped"] is not True:
            blockers.append("internal network topology not mapped")
        if not internal_gate:
            blockers.append("internal LAN under internet loss not demonstrated")
        if internal["local_control_path_without_internet"] is not True:
            blockers.append("local control path without internet not demonstrated")

    if scope in {"external_communications", "full_resilient_stack"} and not external_gate:
        blockers.append("two independent tested external communication paths not demonstrated")

    if scope == "full_resilient_stack":
        if not offline_gate:
            blockers.append("offline/local compute continuity not demonstrated")
        if offline["cloud_dependency_status"] == "critical":
            blockers.append("critical workload remains cloud-dependent")

    if scope in {"internal_network", "external_communications", "full_resilient_stack"} and not power_gate:
        blockers.append("critical communications power resilience not demonstrated")

    if not asset_present:
        blockers.append("no communications resilience asset confirmed")
        status = "stated"
    elif not measured_evidence:
        blockers.append("no measured/tested communications continuity evidence")
        status = "stated"
    else:
        status = "measured"

    if scope == "internal_network":
        field_gate = internal_gate and power_gate
    elif scope == "external_communications":
        field_gate = external_gate and power_gate
    elif scope == "full_resilient_stack":
        field_gate = internal_gate and external_gate and offline_gate and power_gate
    else:
        field_gate = False

    if status == "measured" and field_gate:
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

    internal_days = None
    if (
        internal_gate
        and power_gate
        and power["tested_runtime_hours"] is not None
        and power["tested_runtime_hours"] > 0
    ):
        internal_days = float(power["tested_runtime_hours"]) / 24.0

    external_days = None
    if external_gate and external_hours is not None:
        external_days = external_hours / 24.0

    degraded_local_candidate = bool(internal_gate and offline_gate and power_gate)

    return {
        "schema_version": "0.1.0",
        "assessment_id": f"cva-{audit['communications_audit_id'][4:]}",
        "communications_audit_id": audit["communications_audit_id"],
        "recommended_verification_status": status,
        "internal_lan_gate_passed": internal_gate,
        "external_redundancy_gate_passed": external_gate,
        "offline_compute_gate_passed": offline_gate,
        "power_gate_passed": power_gate,
        "tested_external_path_count": tested_paths,
        "independent_external_path_count": independent_paths,
        "minimum_demonstrated_internal_continuity_days": (
            None if internal_days is None else round(internal_days, 6)
        ),
        "minimum_demonstrated_external_continuity_days": (
            None if external_days is None else round(external_days, 6)
        ),
        "degraded_local_operation_candidate": degraded_local_candidate,
        "blockers": sorted(set(blockers)),
        "as_of": audit["updated_at"],
        "sensitivity": audit["data_sensitivity"],
    }
