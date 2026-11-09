"""PSRRO bounded PUBLIC two-edition PMI original-byte retrospective audit.

Requires two previously downloaded NBS primary HTML pages, two PSRRO
reviewed native Event/Claim/Source packets, and the already-approved Oct PMI
one-shot G1 sidecar. Does not do network I/O, mutate stores, produce forecasts,
or claim historical first-release copies or revisions have been authenticated.
"""
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any, Mapping

from .intelligence_reviewed_export import validate_reviewed_packet
from .intelligence_reviewed_macro import (
    _get_current_method_commit, _read_page, prepare_reviewed_macro
)

CONTRACT = "psrro-reviewed-pmi-cross-edition.v0.1"
SEPT_URL = "https://www.stats.gov.cn/zwfwck/sjfb/202609/t20260930_1965449.html"
OCT_URL = "https://www.stats.gov.cn/sj/zxfbhjd/202610/t20261031_1965718.html"
OCT_ORIGINAL_METHOD = "a9aabf049629e97f81fe6ec0d42c2ce1ad2b9c07"
_SPEC = {
    "2026-09": {
        "url": SEPT_URL, "label": "9", "publication_date": "2026-09-30",
        "publication_text": "发布时间：2026-09-30 09:30",
        "title": "2026年9月中国采购经理指数运行情况",
        "pmi": "50.1", "orders": "50.5", "production": "51.7",
    },
    "2026-10": {
        "url": OCT_URL, "label": "10", "publication_date": "2026-10-31",
        "publication_text": "2026/10/31 09:30",
        "title": "2026年10月中国采购经理指数运行情况",
        "pmi": "49.3", "orders": "49.4", "production": "49.8",
    },
}


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_native(packet: Mapping[str, Any], root: Path, expected_url: str) -> dict[str, Any]:
    proof = validate_reviewed_packet(packet)
    if len(packet["claims"]) != 1 or len(packet["source_observations"]) != 1:
        raise ValueError("one_native_original_claim_per_release_required")
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError("native_root_invalid")
    manifest_path = root / "review-manifest.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise ValueError("native_manifest_missing")
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    event, claim, src = (
        packet["event_state"], packet["claims"][0], packet["source_observations"][0]
    )
    if (manifest.get("packet_sha256") != proof["packet_sha256"]
            or manifest.get("event_id") != event["event_id"]
            or manifest.get("assessment_id") != proof["assessment_id"]
            or manifest.get("source_urls") != [expected_url]
            or manifest.get("review_mode") != "reviewed_public_sources"
            or manifest.get("reviewer_type") != packet["reviewer_type"]
            or manifest.get("evidence_reviewed_at") != packet["reviewed_at"]):
        raise ValueError("native_manifest_proof_mismatch")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or len(artifacts) != 4:
        raise ValueError("unexpected_native_artifacts")
    seen = set()
    for entry in artifacts:
        rel = entry["path"]
        if rel in seen or not re.fullmatch(r"(events|claims|observations)/[a-zA-Z0-9._-]+\.json|material-change/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+\.json", rel):
            raise ValueError("native_artifact_path_or_duplicate_invalid")
        seen.add(rel)
        f = root / rel
        if f.is_symlink() or not f.is_file() or not f.resolve().is_relative_to(root.resolve()):
            raise ValueError("native_artifact_missing")
        if _digest(f.read_bytes()) != entry["sha256"]:
            raise ValueError("native_artifact_hash_mismatch")
    if (event["domain"] != "macro"
            or claim["claim_kind"] != "quantity"
            or claim["epistemic_class"] != "fact"
            or claim["status"] != "accepted"
            or claim["claim_grade"] not in ("A", "B")
            or src["claim_ref"] != claim["claim_id"]
            or src["source_role"] not in ("original_document", "original_report")
            or src["access_status"] != "full_access"
            or src["lineage"]["relation"] != "original"
            or src["provenance"]["source_locator"] != expected_url
            or src["provenance"]["primary_material_accessed"] is not True
            or src["provenance"]["full_text_verified"] is not True
            or src["published_at"] is not None):
        raise ValueError("native_original_source_contract_invalid")
    return {
        "native_event_id": event["event_id"],
        "native_claim_id": claim["claim_id"],
        "native_source_observation_id": src["observation_id"],
        "native_assessment_id": proof["assessment_id"],
        "native_packet_sha256": proof["packet_sha256"],
        "native_review_manifest_sha256": _digest(manifest_bytes),
        "reviewer_type": packet["reviewer_type"],
        "reviewed_at": packet["reviewed_at"],
        "source_retrieved_at": src["retrieved_at"],
        "source_independence_group": src["lineage"]["independence_group_id"],
    }


def _from_original(html: Path, period: str) -> dict[str, Any]:
    spec = _SPEC[period]
    body, text = _read_page(html)
    if spec["title"] not in text or spec["publication_text"] not in text:
        raise ValueError("official_title_or_publication_label_missing")
    l = spec["label"]
    sentences = [
        (rf"{l}月份，制造业采购经理指数（PMI）为([0-9]{{2}}\.[0-9])%", "pmi"),
        (r"生产指数为([0-9]{2}\.[0-9])%", "production"),
        (r"新订单指数为([0-9]{2}\.[0-9])%", "orders"),
    ]
    # Only the first chapter (manufacturing) is relevant, not non-manufacturing.
    section = text.split("二、中国非制造业")[0]
    observed = {}
    for pattern, key in sentences:
        m = re.search(pattern, section)
        if not m:
            raise ValueError("official_monthly_statistic_missing_" + key)
        observed[key] = m.group(1)
    if any(observed[k] != spec[k] for k in observed):
        raise ValueError("official_value_changed_from_reviewed_20261109_anchor")
    if period == "2026-10":
        if "大型企业PMI为50.2%" not in section:
            raise ValueError("official_counterexample_large_enterprise_missing")
    if period == "2026-09":
        table_anchor = "2026年9月 50.1 51.7 50.5"
    else:
        table_anchor = "2026年10月 49.3 49.8 49.4"
    if table_anchor not in section:
        raise ValueError("official_table_and_text_conflict")
    return {
        "period": period,
        "statistical_period_start": period + "-01",
        "statistical_period_end": "2026-09-30" if period == "2026-09" else "2026-10-31",
        "publisher_release_date": spec["publication_date"],
        "publisher_displayed_release_clock": "09:30",
        "verified_historical_release_at": None,
        "source_url": spec["url"],
        "source_bytes_sha256": _digest(body),
        "source_bytes_length": len(body),
        "unit": "percent", "measure": "LEVEL",
        "pmi": observed["pmi"],
        "new_orders": observed["orders"],
        "production": observed["production"],
        "source_vintage": "CURRENT_RETRIEVAL_ONLY_NOT_HISTORICAL_ORIGINAL",
    }


def build_pmi_joint(
    *,
    september_packet: Mapping[str, Any],
    september_native_root: Path,
    september_html: Path,
    october_packet: Mapping[str, Any],
    october_native_root: Path,
    october_html: Path,
    october_g1_record: Mapping[str, Any],
    october_g1_sha256: str,
    producer_method_commit: str | None = None,
) -> dict[str, Any]:
    """Produce a bounded cross-edition retrospective evidence object."""
    sources = []
    for period, packet, root, html in (
        ("2026-09", september_packet, september_native_root, september_html),
        ("2026-10", october_packet, october_native_root, october_html),
    ):
        original = _from_original(html, period)
        native = _load_native(packet, root, original["source_url"])
        retrieved = datetime.fromisoformat(native["source_retrieved_at"].replace("Z", "+00:00"))
        reviewed = datetime.fromisoformat(native["reviewed_at"].replace("Z", "+00:00"))
        if (retrieved.tzinfo is None or reviewed.tzinfo is None or retrieved > reviewed
                or retrieved.date() <= date.fromisoformat(original["publisher_release_date"])):
            raise ValueError("original_source_retrieval_asof_invalid")
        claim = packet["claims"][0]["statement"]
        if (original["pmi"] + "%" not in claim
                or (period == "2026-09" and original["new_orders"] + "%" not in claim)):
            raise ValueError("native_claim_does_not_support_reported_official_value")
        # October's existing frozen G1 Claim carries PMI only. October's other
        # subindexes are verified against the SAME primary HTML raw bytes,
        # never falsely attributed to the older original Claim statement.
        sources.append({**original, **native})

    if (not re.fullmatch("[0-9a-f]{64}", october_g1_sha256)
            or _digest((json.dumps(october_g1_record, ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode("utf-8")) != october_g1_sha256):
        raise ValueError("prior_october_g1_record_digest_invalid")
    earlier_oct = prepare_reviewed_macro(
        october_packet, october_native_root, october_html,
        method_commit=OCT_ORIGINAL_METHOD,
    )
    if october_g1_record != earlier_oct:
        raise ValueError("prior_october_g1_record_and_original_bytes_conflict")
    if sources[1]["pmi"] != october_g1_record["value"]:
        raise ValueError("prior_october_g1_pmi_value_conflict")
    # A later monthly release REPUBLISHED the earlier September values, but
    # contemporaneous first-release original bytes/time have NOT been attested.
    _, october_text = _read_page(october_html)
    table = "2026年9月 50.1 51.7 50.5"
    if table not in october_text:
        raise ValueError("later_release_does_not_match_prior_month_table")
    if sources[0]["source_url"] == sources[1]["source_url"]:
        raise ValueError("different_months_must_reference_different_official_releases")
    method = producer_method_commit or _get_current_method_commit()
    if not re.fullmatch("[0-9a-f]{40}", method):
        raise ValueError("producer_method_commit_invalid")

    return {
        "contract_version": CONTRACT,
        "producer_repository": "yeqilei0328-creator/personal-systemic-risk-resilience-os",
        "producer_method_commit": method,
        "review_mode": "reviewed_public_sources",
        "product_scope": "R2_G2_G3_JOINT_RETROSPECTIVE_ONE_SHOT_ONLY",
        "metric_ids": ["cn.pmi.manufacturing","cn.pmi.new_orders"],
        "sources": sources,
        "prior_october_g1_record_sha256": october_g1_sha256,
        "same_period_202609_cross_editions": {
            "first_release_reported": {"pmi": sources[0]["pmi"],"new_orders":sources[0]["new_orders"],"production": sources[0]["production"]},
            "later_october_reprint": {"pmi": "50.1","new_orders":"50.5","production":"51.7"},
            "reported_values_match": True,
            "historical_original_release_bytes_at_publication_time_attested": False,
            "documented_true_numeric_revision_between_editions": False,
            "status": "NO_CONFLICT_VISIBLE_IN_CURRENTLY_RETRIEVED_COPIES_NOT_PROOF_OF_NO_REVISION",
        },
        "descriptive_deltas_pp": {
            "manufacturing_pmi": "-0.8",
            "new_orders": "-1.1",
            "production": "-1.9",
        },
        "counterevidence": {
            "october_large_enterprises_pmi": "50.2",
            "interpretation": "large_manufacturers_above_50_despite_aggregate_below_50",
            "source_index": 1,
        },
        "data_grain": "monthly_diffusion_index_level_percent",
        "asof_limit": "BOTH_WEBPAGES_ONLY_RETRIEVED_2026_11_09",
        "historical_revision_lineage": "NOT_ATTESTED",
        "authoritative_macro_cycle_stage": None,
        "chain_h_causality": "UNKNOWN",
        "source_fetches_by_exporter": 0,
        "private_or_production_writes": 0,
        "forecasts_created": 0,
    }


def export_pmi_joint_once(*, destination: Path, **kwargs: Any) -> dict[str, Any]:
    destination = Path(destination)
    scratch_roots = {Path(tempfile.gettempdir()).resolve(), Path("/tmp").resolve()}
    resolved = destination.resolve()
    repo = Path(__file__).resolve().parents[2].resolve()
    if (destination.exists() or destination.is_symlink()
            or not any(root in resolved.parents for root in scratch_roots)
            or repo in resolved.parents
            or not destination.parent.is_dir() or destination.parent.is_symlink()):
        raise ValueError("fresh_tmp_output_only")
    payload = build_pmi_joint(**kwargs)
    from jsonschema import Draft202012Validator, FormatChecker
    schema_file = repo / "schemas/psrro-reviewed-pmi-cross-edition.v0.1.schema.json"
    schema = json.loads(schema_file.read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(payload))
    if errors:
        raise ValueError("pmi_joint_schema_invalid:" + errors[0].message)
    raw = (json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode("utf-8")
    with tempfile.TemporaryDirectory(prefix="psrro-pmi-joint-",dir=destination.parent) as t:
        tmp=Path(t);(tmp/"reviewed-pmi-joint.json").write_bytes(raw)
        if destination.exists():
            raise ValueError("destination_collision")
        os.rename(tmp,destination)
    return {
        "status": "R1_REVIEWED_PMI_TWO_EDITION_SNAPSHOT_EXPORTED",
        "record_sha256": _digest(raw),
        "producer_method_commit": payload["producer_method_commit"],
        "metric_ids": payload["metric_ids"],
        "historical_revision_lineage": payload["historical_revision_lineage"],
        "private_or_production_writes": 0,
    }
