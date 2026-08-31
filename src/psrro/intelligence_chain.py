"""Phase 3R-06 Chain Watch.

A chain is only as strong as its actual directed links. Forecast/correlation
can inform a link but cannot by themselves establish causal transmission.
"""

from __future__ import annotations

from typing import Mapping, Sequence


SUPPORTED_H_STATES = {"H2", "H3"}


def is_forecast_only(assessment: Mapping) -> bool:
    counts = assessment["epistemic_counts"]
    return (
        counts["forecast"] > 0
        and counts["fact"] == 0
        and counts["correlation"] == 0
        and counts["causality"] == 0
    )


def is_chain_supported_link(assessment: Mapping) -> bool:
    """Chain support requires H2/H3 plus explicit causal evidence."""
    return (
        assessment["h_state"] in SUPPORTED_H_STATES
        and assessment["epistemic_counts"]["causality"] > 0
        and bool(assessment.get("supporting_evidence_ids"))
        and assessment["direction"] != "falsified"
    )


def longest_contiguous_supported_path(
    definition: Mapping,
    assessments_by_link: Mapping[str, Mapping],
) -> int:
    longest = 0
    current = 0
    for link in definition["links"]:
        assessment = assessments_by_link[link["link_id"]]
        if is_chain_supported_link(assessment):
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return longest


def build_chain_snapshot(
    definition: Mapping,
    assessments: Sequence[Mapping],
    *,
    snapshot_id: str = "chs-derived",
    as_of: str = "1970-01-01T00:00:00Z",
    previous_snapshot: Mapping | None = None,
    sensitivity: str = "public",
) -> dict:
    """Derive a descriptive chain state without creating a chain risk score."""

    if not definition["links"]:
        raise ValueError("chain definition must contain at least one link")
    if any(not link["required"] for link in definition["links"]):
        raise ValueError("v0.1 linear Chain Watch requires every canonical link to be required")

    link_ids = [link["link_id"] for link in definition["links"]]
    assessment_map: dict[str, Mapping] = {}

    for assessment in assessments:
        if assessment["chain_id"] != definition["chain_id"]:
            raise ValueError("assessment chain_id does not match definition")
        link_id = assessment["link_id"]
        if link_id in assessment_map:
            raise ValueError(f"duplicate assessment for link {link_id}")
        assessment_map[link_id] = assessment

    if set(assessment_map) != set(link_ids):
        missing = sorted(set(link_ids) - set(assessment_map))
        extra = sorted(set(assessment_map) - set(link_ids))
        raise ValueError(f"assessment coverage mismatch missing={missing} extra={extra}")

    # Validate assessment endpoints against the definition.
    for link in definition["links"]:
        assessment = assessment_map[link["link_id"]]
        if assessment["source_node_id"] != link["source_node_id"]:
            raise ValueError(f"source node mismatch for {link['link_id']}")
        if assessment["target_node_id"] != link["target_node_id"]:
            raise ValueError(f"target node mismatch for {link['link_id']}")

    ordered = [assessment_map[link_id] for link_id in link_ids]

    supported = [is_chain_supported_link(a) for a in ordered]
    supported_count = sum(supported)
    h3_count = sum(a["h_state"] == "H3" and is_chain_supported_link(a) for a in ordered)
    forecast_only_count = sum(is_forecast_only(a) for a in ordered)
    falsified_count = sum(a["h_state"] == "Hx" for a in ordered)
    falsified_required_count = sum(
        link["required"] and assessment_map[link["link_id"]]["h_state"] == "Hx"
        for link in definition["links"]
    )
    strengthening_count = sum(a["direction"] == "strengthening" for a in ordered)
    weakening_count = sum(a["direction"] == "weakening" for a in ordered)
    material_count = sum(bool(a["material_delta"]) for a in ordered)

    longest = longest_contiguous_supported_path(definition, assessment_map)

    required_links = [
        link["link_id"] for link in definition["links"] if link["required"]
    ]
    if not required_links:
        raise ValueError("chain definition must contain at least one required link")
    full_chain_supported = all(
        is_chain_supported_link(assessment_map[link_id])
        for link_id in required_links
    )

    if falsified_required_count:
        chain_state = "BROKEN"
    elif full_chain_supported:
        chain_state = "TRANSMITTING"
    elif (
        previous_snapshot is not None
        and previous_snapshot["chain_state"] in {"BUILDING", "TRANSMITTING"}
        and weakening_count > strengthening_count
    ):
        chain_state = "RELAXING"
    elif longest >= 2:
        chain_state = "BUILDING"
    elif supported_count > 0:
        chain_state = "FRAGMENTED"
    else:
        chain_state = "UNKNOWN"

    return {
        "schema_version": "0.1.0",
        "snapshot_id": snapshot_id,
        "chain_id": definition["chain_id"],
        "previous_snapshot_id": (
            None if previous_snapshot is None else previous_snapshot["snapshot_id"]
        ),
        "as_of": as_of,
        "ordered_link_assessment_ids": [a["assessment_id"] for a in ordered],
        "total_link_count": len(ordered),
        "required_link_count": len(required_links),
        "supported_link_count": supported_count,
        "h3_link_count": h3_count,
        "forecast_only_link_count": forecast_only_count,
        "falsified_link_count": falsified_count,
        "falsified_required_link_count": falsified_required_count,
        "strengthening_link_count": strengthening_count,
        "weakening_link_count": weakening_count,
        "material_link_count": material_count,
        "longest_contiguous_supported_path": longest,
        "full_chain_supported": full_chain_supported,
        "chain_state": chain_state,
        "sensitivity": sensitivity,
    }
