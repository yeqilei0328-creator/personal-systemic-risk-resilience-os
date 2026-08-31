import unittest

from src.psrro.energy import assess_energy_verification


def base_audit():
    return {
        "schema_version": "0.1.0",
        "energy_audit_id": "era-synthetic",
        "capability_id": "cap-synthetic-energy",
        "service_scope": "critical_loads",
        "grid": {
            "connection_status": "connected",
            "normal_operation_depends_on_grid": True,
        },
        "generation": {
            "pv_present": True,
            "pv_nameplate_kwp": 100,
            "pv_measured_peak_kw": None,
            "generator_present": False,
            "generator_rated_kw": None,
            "generator_measured_runtime_hours": None,
        },
        "storage": {
            "battery_present": None,
            "nameplate_kwh": None,
            "usable_kwh": None,
            "max_continuous_output_kw": None,
        },
        "conversion": {
            "inverter_present": True,
            "islanding_status": "unknown",
            "black_start_status": "unknown",
            "transfer_path_status": "unknown",
        },
        "loads": {
            "critical_loads_mapped": None,
            "critical_peak_kw": None,
            "critical_energy_kwh_per_day": None,
            "essential_circuits_tested": None,
        },
        "outage_test": {
            "status": "not_run",
            "duration_hours": None,
            "minimum_load_served_kw": None,
            "energy_served_kwh": None,
        },
        "dependencies": [],
        "single_points_of_failure": [],
        "maintenance_status": "unknown",
        "independent_review_completed": False,
        "evidence_refs": ["synthetic"],
        "updated_at": "2026-08-31T00:00:00Z",
        "data_sensitivity": "public",
    }


class EnergyVerificationTests(unittest.TestCase):
    def test_pv_nameplate_only_remains_stated(self):
        result = assess_energy_verification(base_audit())
        self.assertEqual(result["recommended_verification_status"], "stated")
        self.assertFalse(result["islanding_gate_passed"])
        self.assertIsNone(result["storage_autonomy_days"])

    def test_measured_storage_calculates_storage_autonomy_only(self):
        audit = base_audit()
        audit["storage"]["battery_present"] = True
        audit["storage"]["usable_kwh"] = 100
        audit["loads"]["critical_loads_mapped"] = True
        audit["loads"]["critical_energy_kwh_per_day"] = 50
        result = assess_energy_verification(audit)
        self.assertEqual(result["recommended_verification_status"], "measured")
        self.assertEqual(result["storage_autonomy_days"], 2.0)
        self.assertIsNone(result["minimum_demonstrated_continuity_days"])

    def test_grid_tied_pv_without_islanding_is_not_field_tested(self):
        audit = base_audit()
        audit["generation"]["pv_measured_peak_kw"] = 80
        audit["conversion"]["islanding_status"] = "not_capable"
        audit["conversion"]["black_start_status"] = "not_supported"
        audit["loads"]["critical_loads_mapped"] = True
        audit["loads"]["critical_energy_kwh_per_day"] = 50
        audit["loads"]["essential_circuits_tested"] = True
        audit["outage_test"]["status"] = "fail"
        result = assess_energy_verification(audit)
        self.assertEqual(result["recommended_verification_status"], "measured")
        self.assertFalse(result["renewable_sustaining_candidate"])

    def test_field_tested_requires_islanding_black_start_and_critical_loads(self):
        audit = base_audit()
        audit["generation"]["pv_measured_peak_kw"] = 80
        audit["storage"]["battery_present"] = True
        audit["storage"]["usable_kwh"] = 100
        audit["storage"]["max_continuous_output_kw"] = 40
        audit["conversion"]["islanding_status"] = "tested_pass"
        audit["conversion"]["black_start_status"] = "tested_pass"
        audit["conversion"]["transfer_path_status"] = "tested_pass"
        audit["loads"]["critical_loads_mapped"] = True
        audit["loads"]["critical_peak_kw"] = 20
        audit["loads"]["critical_energy_kwh_per_day"] = 50
        audit["loads"]["essential_circuits_tested"] = True
        audit["outage_test"]["status"] = "pass"
        audit["outage_test"]["duration_hours"] = 24
        audit["outage_test"]["minimum_load_served_kw"] = 10
        audit["outage_test"]["energy_served_kwh"] = 45
        result = assess_energy_verification(audit)
        self.assertEqual(result["recommended_verification_status"], "field_tested")
        self.assertEqual(result["storage_autonomy_days"], 2.0)
        self.assertEqual(result["minimum_demonstrated_continuity_days"], 1.0)
        self.assertTrue(result["renewable_sustaining_candidate"])

    def test_renewable_candidate_is_not_infinite_autonomy(self):
        audit = base_audit()
        audit["generation"]["pv_measured_peak_kw"] = 80
        audit["conversion"]["islanding_status"] = "tested_pass"
        audit["conversion"]["black_start_status"] = "tested_pass"
        audit["loads"]["critical_loads_mapped"] = True
        audit["loads"]["critical_energy_kwh_per_day"] = 40
        audit["loads"]["essential_circuits_tested"] = True
        audit["outage_test"]["status"] = "pass"
        audit["outage_test"]["duration_hours"] = 48
        audit["outage_test"]["energy_served_kwh"] = 60
        result = assess_energy_verification(audit)
        self.assertTrue(result["renewable_sustaining_candidate"])
        self.assertIsNone(result["storage_autonomy_days"])
        self.assertEqual(result["minimum_demonstrated_continuity_days"], 2.0)

    def test_audited_requires_review_maintenance_and_backed_dependencies(self):
        audit = base_audit()
        audit["storage"]["battery_present"] = True
        audit["storage"]["usable_kwh"] = 100
        audit["conversion"]["islanding_status"] = "tested_pass"
        audit["conversion"]["black_start_status"] = "tested_pass"
        audit["loads"]["critical_loads_mapped"] = True
        audit["loads"]["critical_energy_kwh_per_day"] = 50
        audit["loads"]["essential_circuits_tested"] = True
        audit["outage_test"]["status"] = "pass"
        audit["outage_test"]["duration_hours"] = 24
        audit["outage_test"]["energy_served_kwh"] = 40
        audit["maintenance_status"] = "current"
        audit["independent_review_completed"] = True
        audit["dependencies"] = [{
            "dependency_id": "critical-inverter",
            "kind": "inverter",
            "critical": True,
            "backup_status": "ready",
        }]
        result = assess_energy_verification(audit)
        self.assertEqual(result["recommended_verification_status"], "audited")


if __name__ == "__main__":
    unittest.main()
