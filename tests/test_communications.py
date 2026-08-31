import copy
import json
import unittest
from pathlib import Path

from src.psrro.communications import assess_communications_verification


ROOT = Path(__file__).resolve().parents[1]


class ExampleContractTests(unittest.TestCase):
    def test_synthetic_audit_recomputes_assessment_fixture(self):
        audit = json.loads(
            (ROOT / "examples" / "synthetic" / "communications-resilience-audit.json").read_text(
                encoding="utf-8"
            )
        )
        expected = json.loads(
            (ROOT / "examples" / "synthetic" / "communications-verification-assessment.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(assess_communications_verification(audit), expected)


def base_audit(scope="full_resilient_stack"):
    return {
        "communications_audit_id": "cra-synthetic",
        "service_scope": scope,
        "power": {
            "critical_power_path_mapped": True,
            "backup_power_status": "ready",
            "power_outage_test": "pass",
            "tested_runtime_hours": 24,
        },
        "internal_network": {
            "topology_mapped": True,
            "critical_backbone_medium": "wired",
            "local_lan_status": "tested_pass",
            "internet_loss_test": "pass",
            "local_control_path_without_internet": True,
        },
        "external_links": [
            {
                "link_id": "comlink-a",
                "medium": "fiber",
                "independence_group_id": "group-a",
                "status": "tested_pass",
                "bidirectional": True,
                "test_runtime_hours": 12,
                "critical": True,
            },
            {
                "link_id": "comlink-b",
                "medium": "cellular",
                "independence_group_id": "group-b",
                "status": "tested_pass",
                "bidirectional": True,
                "test_runtime_hours": 8,
                "critical": True,
            },
        ],
        "offline_compute": {
            "local_compute_present": True,
            "critical_workloads_identified": True,
            "local_runtime_status": "tested_pass",
            "cloud_dependency_status": "partial",
            "offline_data_status": "tested_access",
        },
        "dependencies": [],
        "single_points_of_failure": [],
        "maintenance_status": "unknown",
        "independent_review_completed": False,
        "evidence_refs": ["evidence/synthetic.md"],
        "updated_at": "2026-08-31T00:00:00Z",
        "data_sensitivity": "public",
    }


class ExternalRedundancyTests(unittest.TestCase):
    def test_two_independent_tested_paths_pass(self):
        result = assess_communications_verification(base_audit("external_communications"))
        self.assertTrue(result["external_redundancy_gate_passed"])
        self.assertEqual(result["independent_external_path_count"], 2)
        self.assertEqual(result["recommended_verification_status"], "field_tested")

    def test_same_independence_group_does_not_pass(self):
        audit = base_audit("external_communications")
        audit["external_links"][1]["independence_group_id"] = "group-a"
        result = assess_communications_verification(audit)
        self.assertFalse(result["external_redundancy_gate_passed"])
        self.assertEqual(result["independent_external_path_count"], 1)
        self.assertEqual(result["recommended_verification_status"], "measured")

    def test_unverified_satellite_does_not_count(self):
        audit = base_audit("external_communications")
        audit["external_links"][1] = {
            "link_id": "comlink-sat",
            "medium": "satellite",
            "independence_group_id": "group-sat",
            "status": "present_unverified",
            "bidirectional": None,
            "test_runtime_hours": None,
            "critical": True,
        }
        result = assess_communications_verification(audit)
        self.assertFalse(result["external_redundancy_gate_passed"])
        self.assertEqual(result["tested_external_path_count"], 1)

    def test_external_continuity_uses_best_per_group_then_min(self):
        audit = base_audit("external_communications")
        audit["external_links"].append({
            "link_id": "comlink-a2",
            "medium": "cellular",
            "independence_group_id": "group-a",
            "status": "tested_pass",
            "bidirectional": True,
            "test_runtime_hours": 20,
            "critical": False,
        })
        result = assess_communications_verification(audit)
        self.assertEqual(result["tested_external_path_count"], 3)
        self.assertEqual(result["independent_external_path_count"], 2)
        self.assertEqual(result["minimum_demonstrated_external_continuity_days"], round(8/24, 6))


class InternalAndOfflineTests(unittest.TestCase):
    def test_internal_only_can_field_test_without_external_paths(self):
        audit = base_audit("internal_network")
        audit["external_links"] = []
        audit["offline_compute"] = {
            "local_compute_present": None,
            "critical_workloads_identified": None,
            "local_runtime_status": "unknown",
            "cloud_dependency_status": "unknown",
            "offline_data_status": "unknown",
        }
        result = assess_communications_verification(audit)
        self.assertTrue(result["internal_lan_gate_passed"])
        self.assertFalse(result["external_redundancy_gate_passed"])
        self.assertEqual(result["recommended_verification_status"], "field_tested")

    def test_power_unknown_blocks_internal_field_test(self):
        audit = base_audit("internal_network")
        audit["external_links"] = []
        audit["power"] = {
            "critical_power_path_mapped": None,
            "backup_power_status": "unknown",
            "power_outage_test": "not_run",
            "tested_runtime_hours": None,
        }
        result = assess_communications_verification(audit)
        self.assertFalse(result["power_gate_passed"])
        self.assertEqual(result["recommended_verification_status"], "measured")
        self.assertIn("critical communications power resilience not demonstrated", result["blockers"])

    def test_full_stack_requires_offline_compute(self):
        audit = base_audit()
        audit["offline_compute"]["local_runtime_status"] = "present_unverified"
        result = assess_communications_verification(audit)
        self.assertFalse(result["offline_compute_gate_passed"])
        self.assertEqual(result["recommended_verification_status"], "measured")

    def test_cloud_critical_dependency_blocks_offline_gate(self):
        audit = base_audit()
        audit["offline_compute"]["cloud_dependency_status"] = "critical"
        result = assess_communications_verification(audit)
        self.assertFalse(result["offline_compute_gate_passed"])
        self.assertIn("critical workload remains cloud-dependent", result["blockers"])

    def test_degraded_local_candidate_requires_internal_offline_and_power(self):
        result = assess_communications_verification(base_audit())
        self.assertTrue(result["degraded_local_operation_candidate"])
        self.assertEqual(result["minimum_demonstrated_internal_continuity_days"], 1.0)


class VerificationLadderTests(unittest.TestCase):
    def test_presence_only_remains_stated(self):
        audit = base_audit()
        audit["power"]["tested_runtime_hours"] = None
        audit["power"]["power_outage_test"] = "not_run"
        audit["internal_network"]["local_lan_status"] = "present_unverified"
        audit["internal_network"]["internet_loss_test"] = "not_run"
        for link in audit["external_links"]:
            link["status"] = "present_unverified"
            link["bidirectional"] = None
            link["test_runtime_hours"] = None
        audit["offline_compute"]["local_runtime_status"] = "present_unverified"
        result = assess_communications_verification(audit)
        self.assertEqual(result["recommended_verification_status"], "stated")
        self.assertIn("no measured/tested communications continuity evidence", result["blockers"])

    def test_full_stack_can_be_field_tested(self):
        result = assess_communications_verification(base_audit())
        self.assertEqual(result["recommended_verification_status"], "field_tested")
        self.assertTrue(result["internal_lan_gate_passed"])
        self.assertTrue(result["external_redundancy_gate_passed"])
        self.assertTrue(result["offline_compute_gate_passed"])
        self.assertTrue(result["power_gate_passed"])

    def test_audited_requires_review_maintenance_and_backed_dependencies(self):
        audit = base_audit()
        audit["independent_review_completed"] = True
        audit["maintenance_status"] = "current"
        audit["dependencies"] = [
            {
                "dependency_id": "critical-router",
                "kind": "router_switch",
                "critical": True,
                "backup_status": "ready",
            }
        ]
        result = assess_communications_verification(audit)
        self.assertEqual(result["recommended_verification_status"], "audited")

        bad = copy.deepcopy(audit)
        bad["dependencies"][0]["backup_status"] = "unknown"
        result_bad = assess_communications_verification(bad)
        self.assertEqual(result_bad["recommended_verification_status"], "field_tested")


if __name__ == "__main__":
    unittest.main()
