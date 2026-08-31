"""Preparedness baseline audit reference logic.

Public code, private operational state.
"""

from __future__ import annotations

from typing import Mapping, Sequence


def _is_confirmed(audit: Mapping) -> bool:
    return (
        audit.get("verification_status") in {"field_tested", "audited"}
        and audit.get("availability_status") in {"available", "degraded"}
    )


def _has_critical_single_point(audit: Mapping) -> bool:
    if audit.get("single_points_of_failure"):
        return True
    for dep in audit.get("dependencies", []):
        if dep.get("critical") and dep.get("backup_status") in {"none", "unknown"}:
            return True
    return False


def preparedness_snapshot(
    audits: Sequence[Mapping],
    required_domains: Sequence[str],
    *,
    snapshot_id: str = "prs-derived",
    as_of: str = "1970-01-01T00:00:00Z",
) -> dict:
    required = sorted(set(required_domains))
    by_domain: dict[str, list[Mapping]] = {}
    for audit in audits:
        by_domain.setdefault(audit["domain"], []).append(audit)

    covered = sorted(domain for domain in required if domain in by_domain)
    missing = sorted(domain for domain in required if domain not in by_domain)

    confirmed = sorted(
        domain
        for domain in required
        if any(_is_confirmed(a) for a in by_domain.get(domain, []))
    )
    unverified_domains = sorted(
        domain
        for domain in required
        if domain in by_domain
        and not any(_is_confirmed(a) for a in by_domain[domain])
        and not all(a.get("availability_status") == "unavailable" for a in by_domain[domain])
    )

    critical = [a for a in audits if int(a.get("criticality", 0)) >= 4]
    critical_unknown = [
        a for a in critical
        if a.get("availability_status") == "unknown"
        or (
            a.get("autonomy_days") is None
            and a.get("availability_status") != "unavailable"
        )
    ]
    critical_unavailable = [
        a for a in critical if a.get("availability_status") == "unavailable"
    ]
    critical_single_points = [a for a in critical if _has_critical_single_point(a)]

    readiness_gaps: list[str] = []
    if missing:
        readiness_gaps.append("missing required domains: " + ", ".join(missing))
    if critical_unknown:
        readiness_gaps.append(
            "critical capabilities with unknown availability/autonomy: "
            + ", ".join(a["capability_id"] for a in critical_unknown)
        )
    if critical_unavailable:
        readiness_gaps.append(
            "critical capabilities unavailable: "
            + ", ".join(a["capability_id"] for a in critical_unavailable)
        )
    if not critical:
        readiness_gaps.append("no critical capabilities designated")
    if critical_single_points:
        readiness_gaps.append(
            "critical single points of failure: "
            + ", ".join(a["capability_id"] for a in critical_single_points)
        )

    base_autonomy_days = None
    first_failure_capability_id = None
    first_failure_domain = None

    if missing:
        state = "INCOMPLETE"
    elif critical_unavailable:
        state = "DEGRADED"
        base_autonomy_days = 0.0
        first = sorted(critical_unavailable, key=lambda a: a["capability_id"])[0]
        first_failure_capability_id = first["capability_id"]
        first_failure_domain = first["domain"]
    elif critical_unknown or not critical:
        state = "UNKNOWN"
    else:
        state = "AUDITED"
        first = min(
            critical,
            key=lambda a: (float(a["autonomy_days"]), a["capability_id"]),
        )
        base_autonomy_days = float(first["autonomy_days"])
        first_failure_capability_id = first["capability_id"]
        first_failure_domain = first["domain"]

    return {
        "schema_version": "0.1.0",
        "snapshot_id": snapshot_id,
        "as_of": as_of,
        "required_domains": required,
        "covered_domains": covered,
        "missing_domains": missing,
        "confirmed_domains": confirmed,
        "unverified_domains": unverified_domains,
        "critical_capability_count": len(critical),
        "critical_unknown_count": len(critical_unknown),
        "critical_unavailable_count": len(critical_unavailable),
        "critical_single_point_count": len(critical_single_points),
        "base_autonomy_days": base_autonomy_days,
        "first_failure_capability_id": first_failure_capability_id,
        "first_failure_domain": first_failure_domain,
        "state": state,
        "readiness_gaps": readiness_gaps,
        "sensitivity": "public",
    }
