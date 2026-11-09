"""One-shot, offline PSRRO-owned PUBLIC macro review projection.

Strictly one official NBS October-2026 manufacturing PMI source and one
already-reviewed native PSRRO Event/Claim/Source packet. No HTTP, scheduler,
existing state mutation, private values, generic series provider or backfill.
"""
from __future__ import annotations

from datetime import date, datetime
from html.parser import HTMLParser
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

from .intelligence_reviewed_export import read_packet, validate_reviewed_packet

_REPO = Path(__file__).resolve().parents[2]
_URL = "https://www.stats.gov.cn/sj/zxfbhjd/202610/t20261031_1965718.html"
_SCHEMA = "psrro-reviewed-macro-one-shot.v0.1"
_NUM = re.compile(r"10月份，制造业采购经理指数（PMI）为([0-9]{2}\.[0-9])%")
_TITLE = "2026年10月中国采购经理指数运行情况"
_PUBLISHED = "2026/10/31 09:30"
_MAX_HTML = 1_000_000


class _VisibleText(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.text: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag in ("script", "style"):
            self.skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style") and self.skip:
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.text.append(data)


def _read_page(path: Path) -> tuple[bytes, str]:
    path = Path(path)
    if path.is_symlink() or not path.is_file() or not 1 <= path.stat().st_size <= _MAX_HTML:
        raise ValueError("source_html_file_size_or_symlink_invalid")
    b = path.read_bytes()
    try:
        decoded = b.decode("utf-8-sig")
        parser = _VisibleText()
        parser.feed(decoded)
        text = re.sub(r"[\s\u00a0\u2002\u2003]+", " ", "".join(parser.text))
    except (UnicodeError, ValueError) as exc:
        raise ValueError("source_html_decode_invalid") from exc
    return b, text


def _get_current_method_commit() -> str:
    # Exact checkout of PSRRO method code, not historical publisher identity.
    result = subprocess.run(
        ["git", "-C", str(_REPO), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    )
    sha = result.stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError("method_commit_invalid")
    status = subprocess.run(
        ["git", "-C", str(_REPO), "status", "--porcelain"],
        capture_output=True, text=True, check=True,
    )
    if status.stdout.strip():
        raise ValueError("producer_method_worktree_not_clean")
    return sha


def prepare_reviewed_macro(
    reviewed_event_packet: dict,
    native_root: Path,
    html_path: Path,
    *,
    method_commit: str | None = None,
) -> dict:
    """Return data-only one-shot projection, no mutation or network access."""
    proof = validate_reviewed_packet(reviewed_event_packet)
    event = reviewed_event_packet["event_state"]
    sources = reviewed_event_packet["source_observations"]
    claims = reviewed_event_packet["claims"]
    if len(sources) != 1 or len(claims) != 1:
        raise ValueError("single_primary_event_and_claim_required")
    src, claim = sources[0], claims[0]
    if (src["provenance"]["source_locator"] != _URL
            or src["source_role"] not in ("original_document", "original_report")
            or src["access_status"] != "full_access"
            or src["lineage"]["relation"] != "original"
            or not src["provenance"]["full_text_verified"]
            or not src["provenance"]["primary_material_accessed"]
            or src["claim_ref"] != claim["claim_id"]
            or event["domain"] != "macro" or claim["claim_kind"] != "quantity"):
        raise ValueError("official_primary_reviewed_source_contract_invalid")
    if src["published_at"] is not None:
        # An HTML display clock is not authenticated source-history availability.
        raise ValueError("unverified_exact_publication_time_fabricated")
    if Path(native_root).is_symlink():
        raise ValueError("native_root_symlink_invalid")
    manifest_file = Path(native_root) / "review-manifest.json"
    if manifest_file.is_symlink() or not manifest_file.is_file():
        raise ValueError("native_review_manifest_missing")
    manifest_bytes = manifest_file.read_bytes()
    manifest = json.loads(manifest_bytes)
    if (manifest["packet_sha256"] != proof["packet_sha256"]
            or manifest["event_id"] != event["event_id"]
            or manifest["assessment_id"] != proof["assessment_id"]
            or manifest["review_mode"] != "reviewed_public_sources"
            or manifest["reviewer_type"] != reviewed_event_packet["reviewer_type"]
            or manifest["source_urls"] != [_URL]):
        raise ValueError("native_packet_manifest_identity_mismatch")
    expected = {e["path"]: e["sha256"] for e in manifest["artifacts"]}
    if len(expected) != len(manifest["artifacts"]):
        raise ValueError("native_duplicate_artifact_manifest")
    for rel, digest in expected.items():
        p = Path(native_root) / rel
        if p.is_symlink() or not p.is_file() or not p.resolve().is_relative_to(Path(native_root).resolve()):
            raise ValueError("native_artifact_missing_or_symlink")
        if hashlib.sha256(p.read_bytes()).hexdigest() != digest:
            raise ValueError("native_artifact_hash_mismatch")
    if len(expected) != 4:
        raise ValueError("native_source_count_invalid")

    b, text = _read_page(html_path)
    match = _NUM.search(text)
    if _TITLE not in text or _PUBLISHED not in text or not match:
        raise ValueError("official_primary_value_or_release_not_observed_in_source_bytes")
    value = match.group(1)
    if value != "49.3":
        raise ValueError("official_value_changed_from_20261109_review_anchor")
    reviewed_at = datetime.fromisoformat(reviewed_event_packet["reviewed_at"].replace("Z", "+00:00"))
    retrieved_at = datetime.fromisoformat(src["retrieved_at"].replace("Z", "+00:00"))
    if retrieved_at.tzinfo is None or reviewed_at.tzinfo is None or not retrieved_at <= reviewed_at:
        raise ValueError("retrieval_review_chronology_invalid")
    if retrieved_at.date() <= date(2026, 10, 31):
        raise ValueError("source_retrieval_historical_availability_unproven")
    method_sha = method_commit or _get_current_method_commit()
    if not re.fullmatch(r"[0-9a-f]{40}", method_sha):
        raise ValueError("method_commit_invalid")

    return {
        "contract_version": _SCHEMA,
        "producer_repository": "yeqilei0328-creator/personal-systemic-risk-resilience-os",
        "producer_method_commit": method_sha,
        "producer_review_mode": "reviewed_public_sources",
        "reviewer_type": reviewed_event_packet["reviewer_type"],
        "reviewer_identity_attestation": "DECLARED_NOT_INDEPENDENTLY_ATTESTED",
        "reviewed_at": reviewed_event_packet["reviewed_at"],
        "native_event_id": event["event_id"],
        "native_assessment_id": proof["assessment_id"],
        "native_claim_id": claim["claim_id"],
        "native_source_observation_id": src["observation_id"],
        "native_packet_sha256": proof["packet_sha256"],
        "native_review_manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "indicator_id": "cn.pmi.manufacturing",
        "geography": "CN",
        "statistical_period_start": "2026-10-01",
        "statistical_period_end": "2026-10-31",
        "period_mode": "MONTH",
        "measure": "LEVEL",
        "unit": "percent",
        "value": value,
        "publisher": "国家统计局",
        "publisher_release_date": "2026-10-31",
        "publisher_displayed_clock": "09:30",
        "original_release_time_independently_attested": False,
        "verified_historical_availability_timestamp": None,
        "source_url": _URL,
        "source_role": "official_primary",
        "source_retrieved_at": src["retrieved_at"],
        "retrieval_time_attestation": "OPERATOR_DECLARED_NOT_INDEPENDENTLY_TIMESTAMPED",
        "original_source_http_attestation": "HTTPS_200_OPERATOR_RECORDED_NOT_DIGITALLY_SIGNED",
        "source_bytes_sha256": hashlib.sha256(b).hexdigest(),
        "source_bytes_length": len(b),
        "source_contents_checked_against_bytes": True,
        "source_license_scope": "ONE_SHOT_PUBLIC_RESEARCH_ONLY",
        "vintage_status": "CURRENT_RETRIEVAL_ONLY_NO_HISTORICAL_VINTAGE",
        "supersedes_vintage": None,
        "source_independence_group": src["lineage"]["independence_group_id"],
        "automatic_source_fetch": False,
        "source_writes": 0,
        "forecast_created": False,
    }


def export_reviewed_macro_once(
    reviewed_event_packet: dict, native_root: Path, html_path: Path, destination: Path
) -> dict:
    """Atomic, new scratch-only sidecar; existing PSRRO native root read-only."""
    destination = Path(destination)
    scratch_roots = {Path(tempfile.gettempdir()).resolve(), Path("/tmp").resolve()}
    resolved = destination.resolve()
    if (_REPO.resolve() in resolved.parents or resolved == _REPO.resolve()
            or not any(root in resolved.parents for root in scratch_roots)
            or destination.exists() or destination.is_symlink()):
        raise ValueError("fresh_scratch_root_required")
    if not destination.parent.is_dir() or destination.parent.is_symlink():
        raise ValueError("scratch_parent_invalid")
    record = prepare_reviewed_macro(reviewed_event_packet, native_root, html_path)
    from jsonschema import Draft202012Validator, FormatChecker
    schema_path = _REPO / "schemas/psrro-reviewed-macro-one-shot.v0.1.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record))
    if errors:
        raise ValueError("one_shot_macro_schema_invalid:" + errors[0].message)
    payload = (json.dumps(record, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")
    with tempfile.TemporaryDirectory(prefix="psrro-macro-one-", dir=destination.parent) as tmp:
        path = Path(tmp)
        (path / "reviewed-macro.json").write_bytes(payload)
        if destination.exists():
            raise ValueError("scratch_output_collision")
        os.rename(path, destination)
    return {
        "status": "R1_REVIEWED_MACRO_ONE_SHOT_EXPORTED",
        "indicator_id": record["indicator_id"],
        "value": record["value"],
        "statistical_period_end": record["statistical_period_end"],
        "record_sha256": hashlib.sha256(payload).hexdigest(),
        "method_commit": record["producer_method_commit"],
        "producer_writes": 0,
    }
