import unittest

from src.psrro.preparedness import preparedness_snapshot


def audit(
    capability_id,
    domain,
    *,
    criticality=5,
    verification="field_tested",
    availability="available",
    autonomy=30,
    spof=None,
    deps=None,
):
    return {
        "capability_id": capability_id,
        "domain": domain,
        "criticality": criticality,
        "verification_status": verification,
        "availability_status": availability,
        "autonomy_days": autonomy,
        "single_points_of_failure": spof or [],
        "dependencies": deps or [],
    }


class PreparednessSnapshotTests(unittest.TestCase):
    def test_missing_required_domain_is_incomplete(self):
        result = preparedness_snapshot(
            [audit("cap-water", "water")],
            ["water", "energy"],
        )
        self.assertEqual(result["state"], "INCOMPLETE")
        self.assertIsNone(result["base_autonomy_days"])
        self.assertEqual(result["missing_domains"], ["energy"])

    def test_unknown_critical_capability_blocks_autonomy_claim(self):
        result = preparedness_snapshot(
            [
                audit("cap-water", "water", availability="unknown", autonomy=None),
                audit("cap-energy", "energy", autonomy=20),
            ],
            ["water", "energy"],
        )
        self.assertEqual(result["state"], "UNKNOWN")
        self.assertIsNone(result["base_autonomy_days"])
        self.assertEqual(result["critical_unknown_count"], 1)

    def test_first_failure_point_sets_base_autonomy(self):
        result = preparedness_snapshot(
            [
                audit("cap-water", "water", autonomy=40),
                audit("cap-energy", "energy", autonomy=12),
                audit("cap-food", "food", autonomy=25),
            ],
            ["water", "energy", "food"],
        )
        self.assertEqual(result["state"], "AUDITED")
        self.assertEqual(result["base_autonomy_days"], 12.0)
        self.assertEqual(result["first_failure_capability_id"], "cap-energy")
        self.assertEqual(result["first_failure_domain"], "energy")

    def test_unavailable_critical_capability_sets_zero(self):
        result = preparedness_snapshot(
            [
                audit("cap-water", "water", autonomy=40),
                audit("cap-energy", "energy", availability="unavailable", autonomy=0),
            ],
            ["water", "energy"],
        )
        self.assertEqual(result["state"], "DEGRADED")
        self.assertEqual(result["base_autonomy_days"], 0.0)
        self.assertEqual(result["first_failure_capability_id"], "cap-energy")

    def test_single_point_of_failure_is_surfaced(self):
        result = preparedness_snapshot(
            [
                audit(
                    "cap-network",
                    "communications",
                    autonomy=10,
                    deps=[{
                        "dependency_id": "carrier-a",
                        "kind": "network",
                        "critical": True,
                        "backup_status": "none",
                    }],
                )
            ],
            ["communications"],
        )
        self.assertEqual(result["critical_single_point_count"], 1)
        self.assertTrue(any("critical single points" in x for x in result["readiness_gaps"]))

    def test_stated_only_domain_is_not_confirmed(self):
        result = preparedness_snapshot(
            [audit("cap-water", "water", verification="stated", autonomy=20)],
            ["water"],
        )
        self.assertEqual(result["confirmed_domains"], [])
        self.assertEqual(result["unknown_domains"], ["water"])


if __name__ == "__main__":
    unittest.main()
