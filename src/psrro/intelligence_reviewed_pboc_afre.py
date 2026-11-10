"""WI-MACRO04: once-only PBOC 2026 AFRE(stock) native original-byte proof.

Reads an ALREADY downloaded official People's Bank of China HTML table and
a PSRRO reviewer-attributed native public Event/Claim/Source proof. Never
fetches or schedules sources, certifies first-online historic availability,
changes PSRRO PRIVATE, forecasts, or edits RIOS.
"""
from __future__ import annotations

from datetime import date, datetime
from html.parser import HTMLParser
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any,Mapping

from .intelligence_reviewed_export import read_packet
from .intelligence_reviewed_macro import _get_current_method_commit
from .intelligence_reviewed_pmi_joint import _load_native

PBOC_AFRE_URL = "https://www.pbc.gov.cn/diaochatongjisi/attachDir/2026/10/2026101417444554195.htm"
PBOC_PUBLISHER_INDEX = "https://www.pbc.gov.cn/diaochatongjisi/116219/116319/2026ntjsj/shrzgm/index.html"
PBOC_SOURCE_SHA256 = "8649f9da169e8c89985781bfb26f222f277adc59685315836c0c133dc0056794"
PBOC_BYTES = 57401
CONTRACT = "psrro-reviewed-pboc-afre-stock-one-shot.v0.1"
_REPO=Path(__file__).resolve().parents[2]


class _Cells(HTMLParser):
    """Extract actual Excel-HTML table cells; never infer column from prose."""
    def __init__(self)->None:
        super().__init__()
        self.rows:list[list[str]]=[]
        self.row:list[str]=[]
        self.cell:list[str]|None=None
    def handle_starttag(self,tag:str,attrs:list)->None:
        if tag=="tr":self.row=[]
        if tag in ("td","th"):self.cell=[]
    def handle_data(self,content:str)->None:
        if self.cell is not None:self.cell.append(content)
    def handle_endtag(self,tag:str)->None:
        if tag in ("td","th") and self.cell is not None:
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell=None
        if tag=="tr" and self.row:
            self.rows.append(self.row)
            self.row=[]


def parse_pboc_original(raw:bytes)->dict[str,str]:
    """Primary source HTML with original row and exact month/stock-growth pairing."""
    if not isinstance(raw,bytes) or not raw:
        raise ValueError("pboc_source_bytes_missing")
    try: page=raw.decode("gb18030")
    except UnicodeDecodeError as exc:
        raise ValueError("pboc_original_encoding_invalid") from exc
    if not ("社会融资规模存量统计表" in page and "AFRE(stock)" in page
            and "2026.9" in page):
        raise ValueError("pboc_afre_official_title_year_or_table_missing")
    p=_Cells()
    p.feed(page)
    headers=[r for r in p.rows if "2026.9" in r and "2026.10" in r]
    values=[r for r in p.rows if r and "AFRE(stock)" in r[0] and "社会融资规模存量" in r[0]]
    if len(headers)!=1 or len(values)!=1:
        raise ValueError("pboc_official_unique_year_header_and_afre_stock_row_required")
    head=headers[0]
    if (len(head)!=14 or head[:10]!=[""]+[f"2026.{n}" for n in range(1,10)]
            or head[10:13]!=["2026.10","2026.11","2026.12"]):
        raise ValueError("pboc_official_month_columns_wrong")
    row=values[0]
    if len(row)!=26:
        raise ValueError("pboc_afre_stock_growth_pair_columns_wrong")
    # Header positions count from index1. Each month has TWO columns
    # stock (trillion RMB) then YOY growth rate (%), not flow.
    if (row[15:19]!=["464.80","7.2","468.17","7.1"]
            or any(val.strip() for val in row[19:25])):
        raise ValueError("pboc_official_sep_stock_growth_or_oct_future_empty_changed")
    if "单位：万亿元人民币" not in page or "增速" not in page:
        raise ValueError("pboc_stock_units_or_growth_headers_missing")
    return {
        "indicator_id":"cn.credit.afre_stock.yoy",
        "geography":"CN",
        "statistical_period_start":"2026-09-01",
        "statistical_period_end":"2026-09-30",
        "period_mode":"STOCK",
        "measure":"YOY",
        "unit":"percent",
        "value":row[18],
        "stock_amount":row[17],
        "stock_amount_unit":"万亿元",
        "previous_month":"2026-08",
        "previous_month_stock":row[15],
        "previous_month_yoy":row[16],
        "october_column_nonempty":False,
    }


def _reviewed_pboc_native(packet:Mapping[str,Any],root:Path,source:Mapping[str,Any])->dict[str,Any]:
    proof=_load_native(packet,root,PBOC_AFRE_URL)
    src=packet["source_observations"][0]
    claim=packet["claims"][0]["statement"]
    if (packet["reviewer_type"]!="ai_assistant"
            or src["source_id"]!="src-pboc-afre-stock-202609"
            or proof["native_event_id"]!="evt-r1-pboc-afre-stock-202609"
            or proof["native_claim_id"]!="clm-r1-pboc-afre-stock-growth-202609"
            or proof["native_source_observation_id"]!="sob-r1-pboc-afre-202609-official"
            or proof["native_assessment_id"]!="mca-r1-pboc-afre-202609"
            or proof["source_independence_group"]!="ind-pboc-2026-afre-stock-original"
            or "cn.credit.afre_stock.yoy=7.1 YOY/percent" not in claim
            or "stock=468.17万亿元" not in claim):
        raise ValueError("pboc_native_claim_source_identity_and_values_invalid")
    try:
        received=datetime.fromisoformat(proof["source_retrieved_at"].replace("Z","+00:00"))
        reviewed=datetime.fromisoformat(proof["reviewed_at"].replace("Z","+00:00"))
    except (TypeError,ValueError) as exc:
        raise ValueError("pboc_review_time_invalid") from exc
    if (received.tzinfo is None or reviewed.tzinfo is None or
            received.date()!=date(2026,11,10) or reviewed<received
            or received.isoformat()!=source["retrieved_at"]):
        raise ValueError("pboc_actual_retrieval_and_review_time_invalid")
    return proof


def build_pboc_afre_once(
    *,
    html:Path,reviewed_packet:Path,native_root:Path,
    source_receipt:Path,producer_method_commit:str|None=None,
)->dict[str,Any]:
    rawpath=Path(html)
    if not rawpath.is_file() or rawpath.is_symlink():
        raise ValueError("source_original_html_missing_or_symlink")
    raw=rawpath.read_bytes()
    digest=hashlib.sha256(raw).hexdigest()
    if digest!=PBOC_SOURCE_SHA256 or len(raw)!=PBOC_BYTES:
        raise ValueError("pboc_official_original_bytes_hash_or_length_changed")
    receipt=json.loads(Path(source_receipt).read_text(encoding="utf-8"))
    if (receipt.get("source_url")!=PBOC_AFRE_URL
            or receipt.get("http_status")!=200
            or receipt.get("source_bytes_length")!=PBOC_BYTES
            or receipt.get("source_sha256")!=PBOC_SOURCE_SHA256
            or receipt.get("publisher")!="中国人民银行"
            or receipt.get("first_available_history")!="NOT_ATTESTED"):
        raise ValueError("pboc_official_acquisition_receipt_invalid")
    metric=parse_pboc_original(raw)
    if receipt.get("period")!="2026-09" or receipt.get("value")!=metric["value"] or receipt.get("stock")!=metric["stock_amount"]:
        raise ValueError("pboc_acquisition_value_or_grain_conflict")
    native=_reviewed_pboc_native(read_packet(Path(reviewed_packet)),Path(native_root),receipt)
    if native["native_review_manifest_sha256"]!=receipt["native_review_manifest_sha256"]:
        raise ValueError("pboc_review_manifest_checksum_mismatch")
    commit=producer_method_commit or _get_current_method_commit()
    if not isinstance(commit,str) or not re.fullmatch("[0-9a-f]{40}",commit):
        raise ValueError("pboc_producer_method_commit_invalid")
    return {
        "contract_version":CONTRACT,
        "producer_repository":"yeqilei0328-creator/personal-systemic-risk-resilience-os",
        "producer_method_commit":commit,
        "product_scope":"R1_ONE_OFF_PUBLIC_PBOC_AFRE_202609_SOURCE_REVIEW_ONLY",
        "source_review_mode":"reviewed_public_sources",
        "source_publisher":"中国人民银行",
        "source_role":"original_document",
        "source_url":PBOC_AFRE_URL,
        "source_index_url":PBOC_PUBLISHER_INDEX,
        "original_source_sha256":digest,
        "original_source_bytes_length":len(raw),
        "publisher_document_filename_date_hint":"2026-10-14",
        "actual_source_retrieved_at":native["source_retrieved_at"],
        "source_vintage":"CURRENT_RETRIEVAL_ON_NOV10_ONLY",
        "historical_first_availability_attested":False,
        "original_source_fetched_by_this_exporter":0,
        "original_source_stored_in_git":False,
        "reviewer_identity":"ai_assistant",
        "reviewer_signature_verified":False,
        "native_event_id":native["native_event_id"],
        "native_claim_id":native["native_claim_id"],
        "native_assessment_id":native["native_assessment_id"],
        "native_source_observation_id":native["native_source_observation_id"],
        "native_packet_sha256":native["native_packet_sha256"],
        "native_review_manifest_sha256":native["native_review_manifest_sha256"],
        "native_reviewed_at":native["reviewed_at"],
        "native_source_independence_group":native["source_independence_group"],
        "verified_metric":metric,
        "afre_flow_and_stock_not_interchangeable":True,
        "historical_asof_backtesting_authorized":False,
        "macro_cycle_stage":None,
        "psrro_causal_H":"UNKNOWN",
        "private_or_production_writes":0,
        "forecast_created":0,
    }


def export_pboc_afre_once(destination:Path,**kwargs:Any)->dict[str,Any]:
    dest=Path(destination)
    resolved=dest.resolve()
    roots={Path(tempfile.gettempdir()).resolve(),Path("/tmp").resolve()}
    if (dest.exists() or dest.is_symlink() or not any(root in resolved.parents for root in roots)
            or _REPO.resolve() in resolved.parents
            or not dest.parent.is_dir() or dest.parent.is_symlink()):
        raise ValueError("only_fresh_official_scratch_output_permitted")
    result=build_pboc_afre_once(**kwargs)
    from jsonschema import Draft202012Validator, FormatChecker
    schema=json.loads((_REPO/"schemas/psrro-reviewed-pboc-afre-one-shot.v0.1.schema.json").read_text(encoding="utf-8"))
    errors=list(Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(result))
    if errors:raise ValueError("r1_afre_schema_failed:"+errors[0].message)
    raw=(json.dumps(result,sort_keys=True,ensure_ascii=False,separators=(",",":"),allow_nan=False)+"\n").encode("utf-8")
    with tempfile.TemporaryDirectory(dir=dest.parent,prefix="psrro-afre-") as scratch:
        f=Path(scratch)/"r1-reviewed-pboc-afre.json"
        f.write_bytes(raw)
        if dest.exists():raise ValueError("output_collision")
        os.rename(scratch,dest)
    return {
        "status":"R1_PBOC_FIRST_PARTY_202609_AFRE_REVIEWED_ONE_SHOT_EXPORTED",
        "contract_version":CONTRACT,
        "producer_method_commit":result["producer_method_commit"],
        "record_sha256":hashlib.sha256(raw).hexdigest(),
        "indicator_id":result["verified_metric"]["indicator_id"],
        "value":result["verified_metric"]["value"],
        "private_or_production_writes":0,
    }
