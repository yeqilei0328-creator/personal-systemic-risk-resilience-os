import copy
import tempfile
import unittest

from src.psrro.intelligence_memory import (
    JudgmentMemoryStore,
    claim_grade_changed,
    summarize_judgment_calibration,
)


def judgment(jid="jdg-1"):
    return {
        "judgment_id": jid,
        "current_finding": "synthetic",
    }


def outcome(
    oid="jot-1",
    jid="jdg-1",
    status="unresolved",
    errors=None,
    later=None,
    evaluated_at="2026-08-31T00:00:00Z",
):
    return {
        "outcome_id": oid,
        "judgment_id": jid,
        "evaluated_at": evaluated_at,
        "outcome_status": status,
        "error_types": errors or [],
        "later_result": later,
    }


class AppendOnlyStoreTests(unittest.TestCase):
    def test_idempotent_judgment_replay_is_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = JudgmentMemoryStore(tmp)
            row = judgment()
            store.append_judgment(row)
            store.append_judgment(copy.deepcopy(row))
            self.assertEqual(store.get_judgment("jdg-1"), row)

    def test_original_judgment_cannot_be_rewritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = JudgmentMemoryStore(tmp)
            store.append_judgment(judgment())
            changed = judgment()
            changed["current_finding"] = "rewritten history"
            with self.assertRaises(ValueError):
                store.append_judgment(changed)

    def test_later_result_is_appended_as_outcome_not_judgment_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = JudgmentMemoryStore(tmp)
            j = judgment()
            o = outcome(
                status="resolved",
                errors=["none"],
                later="synthetic result confirmed",
            )
            store.append_judgment(j)
            store.append_outcome(o)
            self.assertEqual(store.get_judgment("jdg-1"), j)
            self.assertEqual(store.get_outcome("jdg-1", "jot-1"), o)

    def test_outcome_is_append_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = JudgmentMemoryStore(tmp)
            store.append_outcome(outcome())
            changed = outcome()
            changed["outcome_status"] = "resolved"
            with self.assertRaises(ValueError):
                store.append_outcome(changed)

    def test_revision_is_append_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = JudgmentMemoryStore(tmp)
            rev = {"revision_id": "prv-1", "judgment_id": "jdg-1", "value": 1}
            store.append_revision(rev)
            with self.assertRaises(ValueError):
                store.append_revision({"revision_id": "prv-1", "judgment_id": "jdg-1", "value": 2})
            self.assertEqual(store.get_revision("jdg-1", "prv-1"), rev)

    def test_suppressed_alert_is_still_remembered(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = JudgmentMemoryStore(tmp)
            row = {
                "alert_history_id": "ahs-1",
                "outcome": "SUPPRESS",
                "decision_id": "ogd-1",
            }
            store.append_alert_history(row)
            self.assertEqual(store.get_alert_history("ahs-1"), row)

    def test_unsafe_identifier_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = JudgmentMemoryStore(tmp)
            with self.assertRaises(ValueError):
                store.append_judgment({"judgment_id": "../escape"})


class ClaimGradeTests(unittest.TestCase):
    def test_grade_function_only_checks_identity(self):
        self.assertTrue(claim_grade_changed("B", "A"))
        self.assertTrue(claim_grade_changed("D", "C"))
        self.assertFalse(claim_grade_changed("D", "D"))

    def test_d_is_not_numeric_lowest_grade(self):
        # No function exists to order grades; D may mean analysis/opinion/prediction.
        self.assertTrue(claim_grade_changed("D", "A"))


class CalibrationTests(unittest.TestCase):
    def test_counts_latest_supplied_outcomes_and_error_types(self):
        rows = [
            outcome("jot-1", "jdg-1", "resolved", ["none"], "confirmed"),
            outcome("jot-2", "jdg-2", "resolved", ["overreaction", "timing_error"], "wrong timing"),
            outcome("jot-3", "jdg-3", "unresolved", [], None),
            outcome("jot-4", "jdg-4", "partially_resolved", ["omitted_variable"], "partial"),
        ]
        result = summarize_judgment_calibration(rows)
        self.assertEqual(result["total_count"], 4)
        self.assertEqual(result["resolved_count"], 2)
        self.assertEqual(result["unresolved_count"], 1)
        self.assertEqual(result["partially_resolved_count"], 1)
        self.assertEqual(result["error_type_counts"]["overreaction"], 1)
        self.assertEqual(result["error_type_counts"]["timing_error"], 1)
        self.assertNotIn("accuracy_score", result)

    def test_latest_outcome_per_judgment_is_used_for_current_calibration(self):
        rows = [
            outcome(
                "jot-1",
                "jdg-1",
                "unresolved",
                [],
                None,
                "2026-08-31T00:00:00Z",
            ),
            outcome(
                "jot-2",
                "jdg-1",
                "partially_resolved",
                ["unknown"],
                "new evidence",
                "2026-08-31T01:00:00Z",
            ),
        ]
        result = summarize_judgment_calibration(rows)
        self.assertEqual(result["total_count"], 1)
        self.assertEqual(result["judgment_ids"], ["jdg-1"])
        self.assertEqual(result["outcome_ids"], ["jot-2"])
        self.assertEqual(result["partially_resolved_count"], 1)
        self.assertEqual(result["error_type_counts"]["unknown"], 1)

    def test_equal_latest_timestamps_fail_closed(self):
        rows = [
            outcome("jot-1", "jdg-1", evaluated_at="2026-08-31T01:00:00Z"),
            outcome("jot-2", "jdg-1", evaluated_at="2026-08-31T01:00:00Z"),
        ]
        with self.assertRaises(ValueError):
            summarize_judgment_calibration(rows)


if __name__ == "__main__":
    unittest.main()
