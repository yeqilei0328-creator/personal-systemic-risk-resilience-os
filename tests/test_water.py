import unittest

from src.psrro.water import assess_water_verification


def base_audit():
    return {
        "schema_version": "0.1.0",
        "water_audit_id": "wra-synthetic",
        "capability_id": "cap-synthetic-water",
        "service_scope": "potable",
        "source": {
            "source_type": "well",
            "presence_confirmed": True,
            "source_verification": "stated",
            "notes": None,
        },
        "hydraulics": {"flow_test": None, "usable_storage_liters": None},
        "power": {
            "extraction_requires_power": True,
            "primary_power": "grid",
            "backup_power_status": "unknown",
            "outage_extraction_test": "not_run",
        },
        "treatment": {"required": True, "system_status": "unknown"},
        "quality": {
            "potability_status": "unknown",
            "evidence_date": None,
            "evidence_ref": None,
            "consumer_sensor_only": False,
        },
        "continuity": {
            "daily_demand_liters": None,
            "outage_test": "not_run",
            "field_test_duration_hours": None,
        },
        "dependencies": [],
        "single_points_of_failure": [],
        "maintenance_status": "unknown",
        "independent_review_completed": False,
        "evidence_refs": ["synthetic"],
        "updated_at": "2026-08-31T00:00:00Z",
        "data_sensitivity": "public",
    }


class WaterVerificationTests(unittest.TestCase):
    def test_source_only_remains_stated(self):
        result = assess_water_verification(base_audit())
        self.assertEqual(result["recommended_verification_status"], "stated")
        self.assertIsNone(result["storage_autonomy_days"])

    def test_measured_storage_does_not_become_field_tested(self):
        audit = base_audit()
        audit["hydraulics"]["usable_storage_liters"] = 1000
        audit["continuity"]["daily_demand_liters"] = 100
        result = assess_water_verification(audit)
        self.assertEqual(result["recommended_verification_status"], "measured")
        self.assertEqual(result["storage_autonomy_days"], 10.0)

    def test_consumer_sensor_does_not_establish_potability(self):
        audit = base_audit()
        audit["hydraulics"]["usable_storage_liters"] = 1000
        audit["quality"]["consumer_sensor_only"] = True
        result = assess_water_verification(audit)
        self.assertFalse(result["potability_gate_passed"])
        self.assertIn("consumer sensors do not establish potability", result["blockers"])

    def test_field_test_requires_outage_and_potability_gate(self):
        audit = base_audit()
        audit["hydraulics"]["flow_test"] = {
            "method": "metered",
            "duration_minutes": 60,
            "sustained_flow_lpm": 10,
            "recovery_minutes": None,
            "notes": None,
        }
        audit["power"]["outage_extraction_test"] = "pass"
        audit["power"]["backup_power_status"] = "ready"
        audit["treatment"]["system_status"] = "operational_tested"
        audit["quality"]["potability_status"] = "lab_verified"
        audit["quality"]["evidence_date"] = "2026-08-30"
        audit["quality"]["evidence_ref"] = "synthetic-lab"
        audit["continuity"]["outage_test"] = "pass"
        audit["continuity"]["field_test_duration_hours"] = 24
        result = assess_water_verification(audit)
        self.assertEqual(result["recommended_verification_status"], "field_tested")
        self.assertEqual(result["minimum_demonstrated_continuity_days"], 1.0)
        self.assertTrue(result["continuous_source_candidate"])

    def test_continuous_source_candidate_is_not_infinite_autonomy(self):
        audit = base_audit()
        audit["hydraulics"]["flow_test"] = {
            "method": "pump_test",
            "duration_minutes": 120,
            "sustained_flow_lpm": 20,
            "recovery_minutes": 30,
            "notes": None,
        }
        audit["power"]["outage_extraction_test"] = "pass"
        audit["treatment"]["system_status"] = "operational_tested"
        audit["quality"]["potability_status"] = "authority_verified"
        audit["continuity"]["outage_test"] = "pass"
        audit["continuity"]["field_test_duration_hours"] = 48
        result = assess_water_verification(audit)
        self.assertTrue(result["continuous_source_candidate"])
        self.assertEqual(result["minimum_demonstrated_continuity_days"], 2.0)
        self.assertIsNone(result["storage_autonomy_days"])

    def test_audited_requires_review_and_no_critical_unbacked_dependencies(self):
        audit = base_audit()
        audit["hydraulics"]["usable_storage_liters"] = 1000
        audit["continuity"]["daily_demand_liters"] = 100
        audit["power"]["outage_extraction_test"] = "pass"
        audit["treatment"]["system_status"] = "operational_tested"
        audit["quality"]["potability_status"] = "lab_verified"
        audit["continuity"]["outage_test"] = "pass"
        audit["continuity"]["field_test_duration_hours"] = 24
        audit["maintenance_status"] = "current"
        audit["independent_review_completed"] = True
        audit["dependencies"] = [{
            "dependency_id": "backup-power",
            "kind": "power",
            "critical": True,
            "backup_status": "ready",
        }]
        result = assess_water_verification(audit)
        self.assertEqual(result["recommended_verification_status"], "audited")


if __name__ == "__main__":
    unittest.main()
