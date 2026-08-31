import copy
import tempfile
import unittest

from src.psrro.intelligence_memory import (
    JudgmentMemoryStore,
    claim_grade_changed,
    summarize_judgment_calibration,
)


def judgment(jid="jdg-1", outcome="unresolved", errors=None):
    return {
        "judgment_id": jid,
        "outcome_status": outcome,
        "error_types": errors or [],
        "current_finding": "synthetic",
    }


class AppendOnlyStoreTests(unittest.TestCase):
    def test_idempotent_replay_is_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = JudgmentMemoryStore(tmp)
            row = judgment()
            store.append_judgment(row)
            store.append_judgment(copy.deepcopy(row))
            self.assertEqual(store.get_judgment("jdg-1"), row)

    def test_same_id_with_changed_content_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = JudgmentMemoryStore(tmp)
            store.append_judgment(judgment())
            changed = judgment()
            changed["current_finding"] = "rewritten history"
            with self.assertRaises(ValueError):
                store.append_judgment(changed)

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
    def test_counts_resolved_and_error_types(self):
        rows = [
            judgment("jdg-1", "resolved", ["none"]),
            judgment("jdg-2", "resolved", ["overreaction", "timing_error"]),
            judgment("jdg-3", "unresolved", []),
            judgment("jdg-4", "partially_resolved", ["omitted_variable"]),
        ]
        result = summarize_judgment_calibration(rows)
        self.assertEqual(result["total_count"], 4)
        self.assertEqual(result["resolved_count"], 2)
        self.assertEqual(result["unresolved_count"], 1)
        self.assertEqual(result["partially_resolved_count"], 1)
        self.assertEqual(result["error_type_counts"]["overreaction"], 1)
        self.assertEqual(result["error_type_counts"]["timing_error"], 1)
        self.assertNotIn("accuracy_score", result)

    def test_duplicate_ids_do_not_change_total_observation_count(self):
        rows = [
            judgment("jdg-1", "resolved", ["none"]),
            judgment("jdg-1", "resolved", ["none"]),
        ]
        result = summarize_judgment_calibration(rows)
        self.assertEqual(result["total_count"], 2)
        self.assertEqual(result["judgment_ids"], ["jdg-1"])


if __name__ == "__main__":
    unittest.main()
