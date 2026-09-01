import json
import unittest
from pathlib import Path
from src.psrro.mobility import assess_mobility_verification

ROOT=Path(__file__).resolve().parents[1]

def base(scope="evacuation_and_logistics"):
    return {
        "mobility_audit_id":"mra-synthetic",
        "service_scope":scope,
        "mission":{"people_capacity_required":4,"cargo_capacity_kg_required":100,"target_distance_km":200,"route_requirements_mapped":True},
        "vehicles":[{"vehicle_id":"vehicle-a","availability":"tested_ready","energy_type":"plug_in_hybrid","demonstrated_range_km":500,"people_capacity":5,"cargo_capacity_kg":300,"degraded_mission_test":"pass","critical":True}],
        "energy_paths":[
            {"path_id":"mobenergy-a","kind":"grid_charging","independence_group_id":"energy-a","status":"tested_available","critical":True},
            {"path_id":"mobenergy-b","kind":"fuel_station","independence_group_id":"energy-b","status":"tested_available","critical":True}
        ],
        "routes":[
            {"route_id":"route-a","independence_group_id":"route-group-a","status":"tested_pass","critical":True},
            {"route_id":"route-b","independence_group_id":"route-group-b","status":"tested_pass","critical":True}
        ],
        "maintenance":{"status":"current","tires_checked":True,"critical_spares_mapped":True,"repair_tools_ready":True,"service_dependency_mapped":True},
        "navigation":{"online_dependency":"partial","offline_maps_status":"tested_access"},
        "mission_test":{"status":"pass","distance_km":250,"people_count":4,"cargo_kg":100},
        "dependencies":[],
        "single_points_of_failure":[],
        "independent_review_completed":False,
        "evidence_refs":["evidence/synthetic-mobility.md"],
        "updated_at":"2026-09-01T00:00:00Z",
        "data_sensitivity":"public"
    }

class Contract(unittest.TestCase):
    def test_fixture(self):
        audit=json.loads((ROOT/"examples/synthetic/mobility-resilience-audit.json").read_text())
        expected=json.loads((ROOT/"examples/synthetic/mobility-verification-assessment.json").read_text())
        self.assertEqual(assess_mobility_verification(audit),expected)

class Gates(unittest.TestCase):
    def test_full(self):
        r=assess_mobility_verification(base())
        self.assertEqual(r["recommended_verification_status"],"field_tested")
        self.assertEqual(r["independent_energy_path_count"],2)
        self.assertEqual(r["independent_route_count"],2)
        self.assertEqual(r["minimum_demonstrated_mission_km"],250)

    def test_same_energy_group_fails_redundancy(self):
        a=base(); a["energy_paths"][1]["independence_group_id"]="energy-a"
        r=assess_mobility_verification(a)
        self.assertFalse(r["energy_replenishment_gate_passed"])

    def test_same_route_group_fails_redundancy(self):
        a=base(); a["routes"][1]["independence_group_id"]="route-group-a"
        self.assertFalse(assess_mobility_verification(a)["route_gate_passed"])

    def test_brochure_presence_without_mission_stays_stated(self):
        a=base(); a["mission"]={"people_capacity_required":None,"cargo_capacity_kg_required":None,"target_distance_km":None,"route_requirements_mapped":None}
        a["vehicles"][0]["availability"]="present_unverified"
        a["vehicles"][0]["demonstrated_range_km"]=None
        a["vehicles"][0]["people_capacity"]=None
        a["vehicles"][0]["cargo_capacity_kg"]=None
        a["vehicles"][0]["degraded_mission_test"]="not_run"
        r=assess_mobility_verification(a)
        self.assertEqual(r["recommended_verification_status"],"stated")

    def test_online_only_navigation_blocks(self):
        a=base(); a["navigation"]["online_dependency"]="critical"; a["navigation"]["offline_maps_status"]="absent"
        self.assertFalse(assess_mobility_verification(a)["offline_navigation_gate_passed"])

    def test_local_scope_needs_one_path(self):
        a=base("local_continuity")
        a["energy_paths"]=a["energy_paths"][:1]
        a["routes"]=a["routes"][:1]
        r=assess_mobility_verification(a)
        self.assertTrue(r["energy_replenishment_gate_passed"])
        self.assertTrue(r["route_gate_passed"])

if __name__=="__main__":
    unittest.main()
