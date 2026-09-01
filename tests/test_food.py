import copy
import json
import unittest
from pathlib import Path

from src.psrro.food import assess_food_verification


ROOT = Path(__file__).resolve().parents[1]


def base_audit(scope="sustained_resilience"):
    return {
        "food_audit_id": "fra-synthetic",
        "service_scope": scope,
        "demand": {
            "people_count": 4,
            "daily_calorie_demand_kcal": 8000,
            "special_requirements_mapped": True,
        },
        "inventory": {
            "inventory_count_status": "measured",
            "usable_calories_kcal": 240000,
            "shelf_stable_calories_kcal": 160000,
            "rotation_status": "routine",
        },
        "nutrition": {
            "plan_status": "reviewed",
            "protein_sources_mapped": True,
            "fat_sources_mapped": True,
            "micronutrient_strategy_mapped": True,
            "dietary_constraints_mapped": True,
        },
        "storage": {
            "dry_storage_status": "inspected_pass",
            "pest_moisture_control_status": "adequate",
            "cold_chain_dependency": "partial",
            "cold_chain_outage_test": "not_run",
        },
        "cooking": {
            "primary_path": "mixed",
            "backup_path_status": "tested_pass",
            "outage_cooking_test": "pass",
        },
        "replenishment": {
            "supply_paths": [
                {
                    "path_id": "foodpath-a",
                    "independence_group_id": "group-a",
                    "status": "verified_available",
                    "critical": True,
                },
                {
                    "path_id": "foodpath-b",
                    "independence_group_id": "group-b",
                    "status": "verified_available",
                    "critical": True,
                },
            ],
            "local_production_status": "possible_unverified",
            "production_daily_calorie_equivalent": None,
            "production_inputs_mapped": None,
        },
        "dependencies": [],
        "single_points_of_failure": [],
        "maintenance_status": "unknown",
        "independent_review_completed": False,
        "evidence_refs": ["evidence/synthetic-food.md"],
        "updated_at": "2026-09-01T00:00:00Z",
        "data_sensitivity": "public",
    }


class ExampleContractTests(unittest.TestCase):
    def test_synthetic_audit_recomputes_assessment_fixture(self):
        audit = json.loads(
            (ROOT / "examples" / "synthetic" / "food-resilience-audit.json").read_text(
                encoding="utf-8"
            )
        )
        expected = json.loads(
            (ROOT / "examples" / "synthetic" / "food-verification-assessment.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(assess_food_verification(audit), expected)


class BufferTests(unittest.TestCase):
    def test_measured_inventory_days(self):
        result = assess_food_verification(base_audit())
        self.assertEqual(result["buffer_autonomy_days"], 30.0)
        self.assertEqual(result["shelf_stable_buffer_days"], 20.0)

    def test_no_daily_demand_means_no_days(self):
        audit = base_audit()
        audit["demand"]["daily_calorie_demand_kcal"] = None
        result = assess_food_verification(audit)
        self.assertIsNone(result["buffer_autonomy_days"])
        self.assertFalse(result["inventory_gate_passed"])

    def test_shelf_stable_cannot_exceed_total_without_blocker(self):
        audit = base_audit()
        audit["inventory"]["shelf_stable_calories_kcal"] = 300000
        result = assess_food_verification(audit)
        self.assertIn("shelf-stable calories cannot exceed total usable calories", result["blockers"])


class StorageCookingNutritionTests(unittest.TestCase):
    def test_critical_cold_chain_requires_outage_test(self):
        audit = base_audit()
        audit["storage"]["cold_chain_dependency"] = "critical"
        result = assess_food_verification(audit)
        self.assertFalse(result["storage_gate_passed"])
        self.assertIn("critical cold-chain continuity not demonstrated", result["blockers"])

    def test_nutrition_requires_complete_reviewed_map(self):
        audit = base_audit()
        audit["nutrition"]["micronutrient_strategy_mapped"] = False
        result = assess_food_verification(audit)
        self.assertFalse(result["nutrition_gate_passed"])

    def test_outage_cooking_requires_tested_backup(self):
        audit = base_audit()
        audit["cooking"]["backup_path_status"] = "present_unverified"
        result = assess_food_verification(audit)
        self.assertFalse(result["cooking_gate_passed"])


class ReplenishmentTests(unittest.TestCase):
    def test_two_independent_paths_pass(self):
        result = assess_food_verification(base_audit())
        self.assertTrue(result["replenishment_gate_passed"])
        self.assertEqual(result["independent_replenishment_path_count"], 2)

    def test_same_upstream_group_does_not_count_as_two(self):
        audit = base_audit()
        audit["replenishment"]["supply_paths"][1]["independence_group_id"] = "group-a"
        result = assess_food_verification(audit)
        self.assertFalse(result["replenishment_gate_passed"])
        self.assertEqual(result["independent_replenishment_path_count"], 1)

    def test_measured_local_production_can_support_replenishment(self):
        audit = base_audit()
        audit["replenishment"]["supply_paths"] = []
        audit["replenishment"]["local_production_status"] = "measured_output"
        audit["replenishment"]["production_daily_calorie_equivalent"] = 1500
        audit["replenishment"]["production_inputs_mapped"] = True
        result = assess_food_verification(audit)
        self.assertTrue(result["production_support_candidate"])
        self.assertTrue(result["replenishment_gate_passed"])
        self.assertEqual(result["buffer_autonomy_days"], 30.0)

    def test_unverified_agriculture_does_not_count(self):
        audit = base_audit()
        audit["replenishment"]["supply_paths"] = []
        audit["replenishment"]["local_production_status"] = "possible_unverified"
        audit["replenishment"]["production_daily_calorie_equivalent"] = None
        result = assess_food_verification(audit)
        self.assertFalse(result["production_support_candidate"])
        self.assertFalse(result["replenishment_gate_passed"])


class VerificationLadderTests(unittest.TestCase):
    def test_emergency_buffer_does_not_require_replenishment(self):
        audit = base_audit("emergency_buffer")
        audit["replenishment"]["supply_paths"] = []
        result = assess_food_verification(audit)
        self.assertEqual(result["recommended_verification_status"], "field_tested")
        self.assertFalse(result["replenishment_gate_passed"])

    def test_sustained_scope_requires_replenishment(self):
        audit = base_audit()
        audit["replenishment"]["supply_paths"] = []
        result = assess_food_verification(audit)
        self.assertEqual(result["recommended_verification_status"], "measured")

    def test_presence_without_measured_inventory_stays_stated(self):
        audit = base_audit()
        audit["inventory"]["inventory_count_status"] = "estimated"
        audit["inventory"]["usable_calories_kcal"] = None
        audit["inventory"]["shelf_stable_calories_kcal"] = None
        result = assess_food_verification(audit)
        self.assertEqual(result["recommended_verification_status"], "stated")

    def test_audited_requires_review_rotation_dependencies_and_no_spof(self):
        audit = base_audit()
        audit["independent_review_completed"] = True
        audit["maintenance_status"] = "current"
        audit["inventory"]["rotation_status"] = "tested"
        audit["dependencies"] = [
            {
                "dependency_id": "food-water",
                "kind": "water",
                "critical": True,
                "backup_status": "ready",
            }
        ]
        result = assess_food_verification(audit)
        self.assertEqual(result["recommended_verification_status"], "audited")

        bad = copy.deepcopy(audit)
        bad["dependencies"][0]["backup_status"] = "unknown"
        self.assertEqual(
            assess_food_verification(bad)["recommended_verification_status"],
            "field_tested",
        )


if __name__ == "__main__":
    unittest.main()
