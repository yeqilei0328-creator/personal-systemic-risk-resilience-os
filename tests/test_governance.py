import unittest

from src.psrro.governance import (
    evidence_fingerprint,
    fail_closed,
    route_authority,
    route_radar,
)


class GovernanceRouterTests(unittest.TestCase):
    def test_no_radar(self):
        result = route_radar({})
        self.assertEqual(result["verdict"], "NO_RADAR")
        self.assertFalse(result["authority_widened"])

    def test_blocker_radar_stops_speculation(self):
        result = route_radar({"repeated_failure_class": True})
        self.assertEqual(result["verdict"], "TECH_RADAR_BLOCKER")
        self.assertEqual(
            result["next_action_handoff"]["local_execution_disposition"],
            "STOP_LOCAL_SPECULATION_ALLOW_READONLY_EVIDENCE",
        )

    def test_dual_radar_has_precedence(self):
        result = route_radar(
            {
                "major_architecture_decision": True,
                "repeated_failure_class": True,
            }
        )
        self.assertEqual(result["verdict"], "DUAL_RADAR_MAJOR_DECISION")

    def test_commercial_contradiction_is_validation(self):
        result = route_radar({"commercial_thesis_contradiction": True})
        self.assertEqual(result["verdict"], "COMMERCIAL_RADAR_VALIDATION")

    def test_authority_green(self):
        self.assertEqual(route_authority({})["authority"], "GREEN")

    def test_authority_amber(self):
        result = route_authority({"governance_change": True})
        self.assertEqual(result["authority"], "AMBER")
        self.assertTrue(result["explicit_review_required"])

    def test_authority_red(self):
        result = route_authority({"device_access_or_control": True})
        self.assertEqual(result["authority"], "RED")
        self.assertTrue(result["fresh_owner_authorization_required"])
        self.assertFalse(result["authorization_granted_equals_consumed"])
        self.assertEqual(result["automatic_retry_after_consumption"], 0)

    def test_red_precedes_amber(self):
        result = route_authority(
            {"governance_change": True, "production_write": True}
        )
        self.assertEqual(result["authority"], "RED")

    def test_fail_closed(self):
        result = fail_closed(["STALE", "KNOWN"])
        self.assertTrue(result["fail_closed"])
        self.assertEqual(result["matched_states"], ["STALE"])

    def test_fingerprint_is_order_stable(self):
        left = evidence_fingerprint({"b": 2, "a": 1})
        right = evidence_fingerprint({"a": 1, "b": 2})
        self.assertEqual(left, right)


if __name__ == "__main__":
    unittest.main()