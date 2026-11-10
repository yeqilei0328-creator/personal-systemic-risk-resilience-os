"""WI-MACRO03 PSRRO-owned one-shot first-party macro source proof.

Exactly eight already-downloaded 2026 official primary source pages
(9 R2 indicators), and two 2024 annual GDP preliminary/final primary
pages with real same-period numerical revision. No HTTP, PBOC source
substitution, historical-time travel, generalized collector, scheduled
updates, source-state mutation, forecasting or private state writing.
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

from .intelligence_reviewed_export import read_packet
from .intelligence_reviewed_macro import _get_current_method_commit, _read_page
from .intelligence_reviewed_pmi_joint import _load_native

_REPO = Path(__file__).resolve().parents[2]
_SPEC_PATH = _REPO / "config/r1-macro03-official-source-proof.v0.1.json"
_CONTRACT = "psrro-r1-macro03-source-provenance.v0.1"
_NINE = frozenset({
    "cn.cpi.yoy", "cn.ppi.yoy", "cn.industrial.va.yoy",
    "cn.retail.sales.yoy", "cn.fai.ytd.yoy",
    "cn.realestate.investment.ytd.yoy", "cn.realestate.sales_area.ytd.yoy",
    "cn.industrial.profit.ytd.yoy", "cn.fiscal.land_use_revenue.ytd.yoy",
})
_GDP = "cn.gdp.annual.nominal"
_HASH = re.compile(r"^[0-9a-f]{64}$")


def _one_source_numeric(text: str, metric: Mapping[str, Any]) -> None:
    """Fail if source text does not support the exact signed, native-grain value."""
    pattern = metric["original_text_regex"]
    found = re.search(pattern, text)
    if not found or found.lastindex != 1:
        raise ValueError("original_contextual_numeric_anchor_missing")
    val = found.group(1)
    if bool(metric["negative_claim"]):
        val = "-" + val
    if val != metric["value"]:
        raise ValueError("source_number_or_negative_direction_changed")
    if (metric["indicator_id"] != _GDP
            and (metric["measure"] != "YOY" or metric["unit"] != "percent")):
        raise ValueError("yoy_grain_or_unit_invalid")
    if metric["indicator_id"] == _GDP and (
        metric["measure"] != "NOMINAL_LEVEL" or metric["unit"] != "亿元"
        or metric["negative_claim"]
    ):
        raise ValueError("gdp_nominal_level_unit_invalid")
    start, end = metric["statistical_period_start"], metric["statistical_period_end"]
    if not isinstance(start, str) or not isinstance(end, str) or start > end:
        raise ValueError("metric_statistical_interval_invalid")
    if metric["indicator_id"] != _GDP:
        if metric["indicator_id"].find(".ytd.") >= 0:
            if (start, end) != ("2026-01-01", "2026-09-30"):
                raise ValueError("ytd_period_misrepresented")
        elif (start,end) not in (("2026-09-01","2026-09-30"),("2026-10-01","2026-10-31")):
            raise ValueError("month_period_misrepresented")
    elif (start,end) != ("2024-01-01","2024-12-31"):
        raise ValueError("annual_gdp_period_invalid")


def _revision_proof(initial: Mapping[str,Any], final: Mapping[str,Any]) -> dict[str,Any]:
    if (initial["indicator_id"] != _GDP or final["indicator_id"] != _GDP
            or initial["statistical_period_start"] != final["statistical_period_start"]
            or initial["statistical_period_end"] != final["statistical_period_end"]
            or initial["value"] != "1349084" or final["value"] != "1348066"
            or initial["unit"] != final["unit"] or initial["unit"] != "亿元"
            or initial["measure"] != final["measure"] or initial["measure"] != "NOMINAL_LEVEL"):
        raise ValueError("official_gdp_revision_grain_or_values_invalid")
    delta = Decimal(final["value"])-Decimal(initial["value"])
    if delta != -1018:
        raise ValueError("official_gdp_revision_math_invalid")
    return {
        "indicator_id":_GDP,
        "statistical_period_start":"2024-01-01",
        "statistical_period_end":"2024-12-31",
        "unit":"亿元", "measure":"NOMINAL_LEVEL",
        "initial_value":initial["value"],
        "official_final_value":final["value"],
        "official_declared_revision_delta":"-1018",
        "initial_publisher_date_displayed":"2025-01-18",
        "final_publisher_date_displayed":"2025-12-26",
        "revision_kind":"OFFICIAL_PRELIMINARY_TO_FINAL_SAME_PERIOD_NUMERIC_REVISION",
        "original_first_release_bytes_at_historical_time_attested":False,
        "historical_asof_value_eligibility":"BLOCKED_UNATTESTED_ONLINE_FIRST_AVAILABILITY",
        "not_a_pmi_revision":True,
    }


def _verified_coverage(metrics: list[dict[str,Any]]) -> dict[str, Any]:
    names=[item["indicator_id"] for item in metrics]
    if len(names)!=9 or set(names)!=_NINE:
        raise ValueError("nine_original_macro_metric_ids_required_no_duplicates")
    # Existing two PMIs were separately attested, and not re-authenticated
    # by this report. PBOC/AFRE unverified -> 11/12 only after downstream
    # independent RIOS acceptance, not automatically from our count.
    return {
        "new_nine_official_primary_original_values":9,
        "existing_separate_pmi_core_ids":["cn.pmi.manufacturing","cn.pmi.new_orders"],
        "expected_core_universe_count":12,
        "not_provided_primary_id":"cn.credit.afre_stock.yoy",
        "reference_only_possible_combined_count":11,
        "downstream_r2_acceptance":"NOT_AUTO_GRANTED_FROM_R1_REVIEW",
    }


def _utc(v: Any) -> datetime:
    if not isinstance(v,str):raise ValueError("source_time_not_string")
    try:t=datetime.fromisoformat(v.replace("Z","+00:00"))
    except ValueError as exc:raise ValueError("source_time_invalid") from exc
    if t.tzinfo is None:raise ValueError("source_timezone_missing")
    return t


def _acquisition_receipt(receipt: Mapping[str,Any], spec: Mapping[str,Any], html: bytes) -> str:
    if (receipt.get("source_id")!=spec["source_id"]
            or receipt.get("url")!=spec["url"]
            or receipt.get("exit_code")!=0
            or not isinstance(receipt.get("http_response"),str)):
        raise ValueError("acquisition_receipt_id_or_url_wrong")
    response=receipt["http_response"]
    items=response.split(" ",3)
    if (len(items)!=4 or items[0]!="200" or items[1]!=str(len(html))
            or items[2]!=spec["url"] or items[3]!="text/html"):
        raise ValueError("source_http_outcome_or_redirect_invalid")
    if receipt.get("sha256")!=spec["source_original_sha256"] or receipt.get("length")!=len(html):
        raise ValueError("source_acquisition_hash_or_length_mismatch")
    t=receipt.get("local_observed_at_utc")
    moment=_utc(t)
    if moment.date()!=date(2026,11,10):
        raise ValueError("unexpected_retrieval_day_for_frozen_one_shot_scope")
    return t


def build_r1_macro_gap(root: Path, *,
                       producer_method_commit: str | None=None) -> dict[str,Any]:
    """Read a sealed, externally acquired scratch snapshot. No fetch or mutation."""
    root=Path(root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError("source_scratch_root_missing_or_symlink")
    spec=json.loads(_SPEC_PATH.read_text(encoding="utf-8"))
    if (spec.get("schema_version")!="psrro-r1-macro03-source-proof-spec.v0.1"
            or spec.get("automated_source_fetch") is not False
            or spec.get("historical_first_availability_attested") is not False
            or spec.get("unverified_credit_core_id")!="cn.credit.afre_stock.yoy"
            or len(spec.get("sources",[]))!=10):
        raise ValueError("frozen_r1_spec_invalid")
    receipts=json.loads((root/"one-shot-acquisition-receipt.json").read_text(encoding="utf-8"))
    if len(receipts)!=10 or len({x.get("source_id") for x in receipts})!=10:
        raise ValueError("source_receipt_count_or_duplicates")
    received={x["source_id"]:x for x in receipts}
    verified=[]; metrics=[]
    for item in spec["sources"]:
        name=item["source_id"]
        if not re.fullmatch(r"[a-z0-9_]{5,36}",name) or name not in received:
            raise ValueError("unapproved_source_id")
        page=root/(name+".html")
        if not page.is_file() or page.is_symlink():raise ValueError("raw_primary_source_missing")
        blob,text=_read_page(page)
        if hashlib.sha256(blob).hexdigest()!=item["source_original_sha256"] or len(blob)!=item["source_bytes_length"]:
            raise ValueError("original_source_bytes_sha_mismatch")
        if item["title_required"] not in text or item["publication_label_required"] not in text:
            raise ValueError("publisher_title_or_date_label_missing")
        timestamp=_acquisition_receipt(received[name],item,blob)
        packet_file=root/"reviewed-native"/name/"reviewed-packet.json"
        if packet_file.is_symlink() or not packet_file.is_file():
            raise ValueError("native_packet_missing")
        packet=read_packet(packet_file)
        native=_load_native(packet,root/"reviewed-native"/name/"native",item["url"])
        observed=_utc(native["source_retrieved_at"])
        reviewed=_utc(native["reviewed_at"])
        if (native["source_retrieved_at"]!=timestamp or reviewed<observed
                or observed.date()<=date.fromisoformat(item["claimed_publisher_release_date"])):
            raise ValueError("source_review_chronology_or_retrospective_claim_invalid")
        if native["reviewer_type"]!="ai_assistant":
            raise ValueError("reviewer_type_unexpected")
        claim=packet["claims"][0]["statement"]
        for stat in item["values"]:
            if stat["source_original_sha256"]!=item["source_original_sha256"]:
                raise ValueError("metric_source_digest_mismatch")
            _one_source_numeric(text,stat)
            if (stat["indicator_id"]+"="+stat["value"]) not in claim:
                raise ValueError("native_claim_does_not_report_verified_value")
            metrics.append({
                "indicator_id":stat["indicator_id"],
                "geography":"CN",
                "value":stat["value"],
                "measure":stat["measure"],"unit":stat["unit"],
                "statistical_period_start":stat["statistical_period_start"],
                "statistical_period_end":stat["statistical_period_end"],
                "period_mode":("ANNUAL" if stat["indicator_id"]==_GDP
                                else "YTD" if ".ytd." in stat["indicator_id"] else "MONTH"),
                "source_id":name, "publisher":item["publisher"],
                "original_primary_source_url":item["url"],
                "original_source_bytes_sha256":item["source_original_sha256"],
                "source_retrieved_at":timestamp,
                "publisher_release_date_displayed":item["claimed_publisher_release_date"],
                "historical_first_availability_timestamp_attested":False,
                "reviewed_native_event_id":native["native_event_id"],
                "reviewed_native_claim_id":native["native_claim_id"],
                "reviewed_native_manifest_sha256":native["native_review_manifest_sha256"],
            })
        verified.append({
            "source_id":name,"publisher":item["publisher"],
            "source_url":item["url"],
            "source_original_sha256":item["source_original_sha256"],
            "source_bytes_length":len(blob),
            "local_retrieved_at":timestamp,
            "publisher_displayed_release_date":item["claimed_publisher_release_date"],
            "reviewer_identity_declared":"ai_assistant",
            "native_manifest_sha256":native["native_review_manifest_sha256"],
            "native_packet_sha256":native["native_packet_sha256"],
            "event_id":native["native_event_id"],"claim_id":native["native_claim_id"],
            "source_observation_id":native["native_source_observation_id"],
            "source_independence_group":native["source_independence_group"],
            "source_file_still_exists_in_scratch":True,
            "historical_source_first_seen_independently_attested":False,
        })
    core=[x for x in metrics if x["indicator_id"]!=_GDP]
    coverage=_verified_coverage(core)
    prelim=next(x for x in metrics if x["source_id"]=="gdp2024_initial")
    final=next(x for x in metrics if x["source_id"]=="gdp2024_final")
    rev=_revision_proof(prelim,final)
    rev.update({
        "preliminary_original_page_sha256":prelim["original_source_bytes_sha256"],
        "final_original_page_sha256":final["original_source_bytes_sha256"],
        "preliminary_original_url":prelim["original_primary_source_url"],
        "final_original_url":final["original_primary_source_url"],
        "verified_same_official_statistical_period":True,
    })
    commit=producer_method_commit or _get_current_method_commit()
    if not isinstance(commit,str) or not re.fullmatch(r"[0-9a-f]{40}",commit):
        raise ValueError("producer_method_commit_invalid")
    return {
        "contract_version":_CONTRACT,
        "producer_repository":"yeqilei0328-creator/personal-systemic-risk-resilience-os",
        "producer_method_commit":commit,
        "product_scope":"R1_ONE_SHOT_PUBLIC_MACRO_GAP_AND_REAL_GDP_REVISION_RESEARCH_ONLY",
        "source_review_mode":"reviewed_public_sources",
        "reviewer_type":"ai_assistant",
        "reviewer_identity_attestation":"DECLARED_NOT_INDEPENDENTLY_ATTESTED",
        "source_original_pages_acquired_once":10,
        "new_core_metric_count":9,
        "target_core_count":12,
        "sources":verified,
        "core_metrics":core,
        "gdp_revision":rev,
        "coverage":coverage,
        "not_verified_r1_source_indicator":"cn.credit.afre_stock.yoy",
        "credit_reason":"NO_VERIFIED_CURRENT_PERIOD_FIRST_PARTY_PBOC_ORIGINAL_SOURCE",
        "official_same_period_revised_numeric_record":"GOVERNMENT_2024_ANNUAL_GDP_PRELIMINARY_TO_FINAL",
        "pmi_historical_revision_proof":False,
        "current_source_versions_only_as_retrieved":"2026-11-10",
        "historical_asof_backtest_authorized":False,
        "automatic_source_fetches_by_this_method":0,
        "private_or_production_writes":0,
        "forecasts_created":0,
    }


def export_r1_macro_gap_once(root: Path, destination: Path) -> dict[str,Any]:
    dest=Path(destination)
    temp_roots={Path(tempfile.gettempdir()).resolve(),Path("/tmp").resolve()}
    resolved=dest.resolve()
    repo=_REPO.resolve()
    if (dest.is_symlink() or dest.exists() or repo in resolved.parents
            or not any(t in resolved.parents for t in temp_roots)
            or not dest.parent.is_dir() or dest.parent.is_symlink()):
        raise ValueError("must_output_into_new_isolated_scratch_only")
    result=build_r1_macro_gap(root)
    from jsonschema import Draft202012Validator, FormatChecker
    schema=json.loads((_REPO/"schemas/psrro-r1-macro03-source-provenance.v0.1.schema.json").read_text(encoding="utf-8"))
    errors=list(Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(result))
    if errors:
        raise ValueError("r1_macro03_schema_invalid:"+errors[0].message)
    raw=(json.dumps(result,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode("utf-8")
    with tempfile.TemporaryDirectory(prefix="psrro-r1-macro03-",dir=dest.parent) as d:
        t=Path(d)
        (t/"reviewed-r1-macro-gap.json").write_bytes(raw)
        if dest.exists():raise ValueError("scratch_collision")
        os.rename(t,dest)
    return {
        "status":"R1_REVIEWED_NINE_CORE_AND_ONE_GDP_REVISION_ONE_SHOT_EXPORTED",
        "core_count":9,
        "gdp_revision_delta_yuan_100m":"-1018",
        "record_sha256":hashlib.sha256(raw).hexdigest(),
        "producer_method_commit":result["producer_method_commit"],
        "private_or_production_writes":0,
    }
