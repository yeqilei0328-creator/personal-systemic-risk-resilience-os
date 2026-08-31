"""Phase 3R-07 replay/red-team helpers.

This module evaluates expected vs actual synthetic decisions. It does not
estimate real-world accuracy and deliberately exposes FP/FN counts instead of
inventing one aggregate accuracy score.
"""

from __future__ import annotations

from typing import Mapping, Sequence


DEESCALATION_OR_FALSIFICATION = {
    "falsification",
    "improvement",
    "chain_break",
    "chain_relaxation",
}


def evaluate_replay_step(
    decision: Mapping,
    *,
    result_id: str,
    case_id: str,
    step_id: str,
    category: str,
    expected_notify: bool,
    expected_code: str | None = None,
    notes: str | None = None,
    sensitivity: str = "public",
) -> dict:
    actual_notify = bool(decision["notify"])
    actual_trigger_codes = list(decision.get("trigger_codes", []))
    actual_suppression_codes = list(decision.get("suppression_codes", []))
    actual_codes = set(actual_trigger_codes) | set(actual_suppression_codes)

    if expected_notify and not actual_notify:
        error_class = "FALSE_NEGATIVE"
        passed = False
    elif not expected_notify and actual_notify:
        error_class = "FALSE_POSITIVE"
        passed = False
    elif expected_code is not None and expected_code not in actual_codes:
        error_class = "CODE_MISMATCH"
        passed = False
    else:
        error_class = "NONE"
        passed = True

    return {
        "schema_version": "0.1.0",
        "result_id": result_id,
        "case_id": case_id,
        "step_id": step_id,
        "category": category,
        "expected_notify": expected_notify,
        "actual_notify": actual_notify,
        "expected_code": expected_code,
        "actual_trigger_codes": actual_trigger_codes,
        "actual_suppression_codes": actual_suppression_codes,
        "passed": passed,
        "error_class": error_class,
        "notes": notes,
        "sensitivity": sensitivity,
    }


def summarize_replay_suite(
    results: Sequence[Mapping],
    *,
    suite_id: str = "rps-derived",
    generated_at: str = "1970-01-01T00:00:00Z",
    sensitivity: str = "public",
) -> dict:
    passed = sum(bool(result["passed"]) for result in results)
    failed = len(results) - passed
    false_positive = sum(result["error_class"] == "FALSE_POSITIVE" for result in results)
    false_negative = sum(result["error_class"] == "FALSE_NEGATIVE" for result in results)
    code_mismatch = sum(result["error_class"] == "CODE_MISMATCH" for result in results)
    duplicate_failures = sum(
        result["category"] == "duplicate" and not result["passed"]
        for result in results
    )
    deescalation_failures = sum(
        result["category"] in DEESCALATION_OR_FALSIFICATION and not result["passed"]
        for result in results
    )

    return {
        "schema_version": "0.1.0",
        "suite_id": suite_id,
        "result_ids": [result["result_id"] for result in results],
        "total_steps": len(results),
        "passed_steps": passed,
        "failed_steps": failed,
        "false_positive_count": false_positive,
        "false_negative_count": false_negative,
        "code_mismatch_count": code_mismatch,
        "duplicate_control_failure_count": duplicate_failures,
        "deescalation_falsification_failure_count": deescalation_failures,
        "generated_at": generated_at,
        "sensitivity": sensitivity,
    }
