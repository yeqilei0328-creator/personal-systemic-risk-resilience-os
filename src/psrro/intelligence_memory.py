"""Phase 3R-05 append-only judgment memory.

This module records judgments and revisions. It intentionally does not assign
numeric meaning to Claim Grade A/B/C/D and does not mutate source reputation.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Mapping, Sequence

SAFE_COMPONENT = re.compile(r"^[A-Za-z0-9._-]+$")
ERROR_TYPES = (
    "none",
    "source_error",
    "overreaction",
    "underreaction",
    "timing_error",
    "omitted_variable",
    "correlation_as_causality",
    "rhetoric_overweight",
    "technology_maturity_overestimate",
    "execution_delay",
    "unknown",
)


def _safe(value: str, label: str) -> str:
    if not SAFE_COMPONENT.fullmatch(value) or value in {".", ".."}:
        raise ValueError(f"unsafe {label}: {value!r}")
    return value


def _canonical_payload(obj: Mapping) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _append_only_write(path: Path, obj: Mapping) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    new_payload = _canonical_payload(obj)
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        if _canonical_payload(existing) != new_payload:
            raise ValueError(f"append-only record collision at {path}")
        return path
    path.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class JudgmentMemoryStore:
    """Append-only reference store with idempotent replay."""

    def __init__(self, root: str | Path):
        self.root = Path(root)

    def append_judgment(self, record: Mapping) -> Path:
        jid = _safe(str(record["judgment_id"]), "judgment_id")
        return _append_only_write(self.root / "judgments" / f"{jid}.json", record)

    def get_judgment(self, judgment_id: str) -> dict:
        jid = _safe(judgment_id, "judgment_id")
        return _load(self.root / "judgments" / f"{jid}.json")

    def append_revision(self, record: Mapping) -> Path:
        rid = _safe(str(record["revision_id"]), "revision_id")
        jid = _safe(str(record["judgment_id"]), "judgment_id")
        return _append_only_write(
            self.root / "revisions" / jid / f"{rid}.json",
            record,
        )

    def get_revision(self, judgment_id: str, revision_id: str) -> dict:
        jid = _safe(judgment_id, "judgment_id")
        rid = _safe(revision_id, "revision_id")
        return _load(self.root / "revisions" / jid / f"{rid}.json")

    def append_alert_history(self, record: Mapping) -> Path:
        aid = _safe(str(record["alert_history_id"]), "alert_history_id")
        return _append_only_write(self.root / "alerts" / f"{aid}.json", record)

    def get_alert_history(self, alert_history_id: str) -> dict:
        aid = _safe(alert_history_id, "alert_history_id")
        return _load(self.root / "alerts" / f"{aid}.json")


def summarize_judgment_calibration(
    judgments: Sequence[Mapping],
    *,
    summary_id: str = "jcs-derived",
    generated_at: str = "1970-01-01T00:00:00Z",
    sensitivity: str = "public",
) -> dict:
    """Count outcomes/errors without manufacturing one aggregate accuracy score."""
    status_counts = {
        "resolved": 0,
        "partially_resolved": 0,
        "unresolved": 0,
    }
    error_counts = {name: 0 for name in ERROR_TYPES}

    ids = []
    for judgment in judgments:
        ids.append(judgment["judgment_id"])
        status_counts[judgment["outcome_status"]] += 1
        for error_type in judgment.get("error_types", []):
            if error_type not in error_counts:
                raise ValueError(f"unsupported error type: {error_type}")
            error_counts[error_type] += 1

    return {
        "schema_version": "0.1.0",
        "summary_id": summary_id,
        "judgment_ids": sorted(set(ids)),
        "total_count": len(judgments),
        "resolved_count": status_counts["resolved"],
        "partially_resolved_count": status_counts["partially_resolved"],
        "unresolved_count": status_counts["unresolved"],
        "error_type_counts": error_counts,
        "generated_at": generated_at,
        "sensitivity": sensitivity,
    }


def claim_grade_changed(prior_grade: str | None, posterior_grade: str | None) -> bool:
    """Identity comparison only. No A/B/C/D numeric ordering exists here."""
    return prior_grade != posterior_grade
