import copy
import tempfile
import unittest

from src.psrro.intelligence_events import (
    EventClaimStateStore,
    detect_material_change,
    event_fingerprint,
    numeric_material_change,
)


def basis():
    return {
        "actors": ["Actor A"],
        "actions": ["Deploy"],
        "objects": ["System X"],
        "locations": ["Region 1"],
        "time_window_key": "2026-08-31",
        "consequences": ["Operational change"],
    }


def event(priority="P3", title="Headline A", markers=None, lifecycle="developing"):
    fp = event_fingerprint(basis())
    return {
        "event_id": "evt-synthetic",
        "display_title": title,
        "fingerprint": fp,
        "intelligence_priority": priority,
        "material_markers": markers or [],
        "lifecycle": lifecycle,
        "sensitivity": "public",
    }


class FingerprintTests(unittest.TestCase):
    def test_order_case_and_whitespace_do_not_change_fingerprint(self):
        left = basis()
        right = {
            "actors": ["  ACTOR   A "],
            "actions": ["deploy"],
            "objects": ["system x"],
            "locations": ["region 1"],
            "time_window_key": " 2026-08-31 ",
            "consequences": ["operational change"],
        }
        self.assertEqual(event_fingerprint(left), event_fingerprint(right))

    def test_display_title_is_not_part_of_fingerprint(self):
        self.assertEqual(event("P3", "Headline A")["fingerprint"], event("P3", "Totally different headline")["fingerprint"])

    def test_missing_actor_action_or_time_fails_closed(self):
        bad = basis()
        bad["actors"] = []
        with self.assertRaises(ValueError):
            event_fingerprint(bad)


class NumericMaterialityTests(unittest.TestCase):
    def test_absolute_threshold(self):
        policy = {"materiality_rule": "absolute", "absolute_delta": 10, "relative_delta": None}
        self.assertFalse(numeric_material_change(policy, 100, 105)[0])
        self.assertTrue(numeric_material_change(policy, 100, 110)[0])

    def test_relative_threshold(self):
        policy = {"materiality_rule": "relative", "absolute_delta": None, "relative_delta": 0.1}
        self.assertFalse(numeric_material_change(policy, 100, 105)[0])
        self.assertTrue(numeric_material_change(policy, 100, 111)[0])

    def test_relative_zero_baseline_fails_closed(self):
        policy = {"materiality_rule": "relative", "absolute_delta": None, "relative_delta": 0.1}
        result, reason = numeric_material_change(policy, 0, 10)
        self.assertFalse(result)
        self.assertIn("undefined", reason)

    def test_either_can_use_absolute_when_zero_baseline(self):
        policy = {"materiality_rule": "either", "absolute_delta": 5, "relative_delta": 0.1}
        self.assertTrue(numeric_material_change(policy, 0, 5)[0])


class MaterialChangeTests(unittest.TestCase):
    def test_title_only_update_is_not_material(self):
        old = event(title="Old title")
        new = event(title="New title")
        result = detect_material_change(old, new)
        self.assertFalse(result["material"])
        self.assertEqual(result["change_types"], ["non_material_update"])

    def test_p3_to_p2_is_material(self):
        result = detect_material_change(event("P3"), event("P2"))
        self.assertTrue(result["material"])
        self.assertIn("priority_change", result["change_types"])

    def test_threat_to_attack_marker_is_material(self):
        result = detect_material_change(
            event(markers=[]),
            event(markers=["threat_to_attack"]),
        )
        self.assertTrue(result["material"])
        self.assertIn("material_marker_added", result["change_types"])

    def test_numeric_change_ref_is_material(self):
        result = detect_material_change(
            event(),
            event(),
            numeric_change_refs=["cvo-2"],
            changed_claim_ids=["clm-1"],
        )
        self.assertTrue(result["material"])
        self.assertIn("numeric_material_change", result["change_types"])

    def test_fingerprint_drift_requires_reclustering(self):
        old = event()
        new = copy.deepcopy(old)
        changed_basis = basis()
        changed_basis["actors"] = ["Actor B"]
        new["fingerprint"] = event_fingerprint(changed_basis)
        with self.assertRaises(ValueError):
            detect_material_change(old, new)


class StoreTests(unittest.TestCase):
    def test_event_claim_and_dynamic_value_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = EventClaimStateStore(tmp)
            ev = {"event_id": "evt-1", "value": 1}
            cl = {"claim_id": "clm-1", "value": 2}
            val = {"value_observation_id": "cvo-1", "claim_id": "clm-1", "value": 3}
            store.put_event(ev)
            store.put_claim(cl)
            store.put_value_observation(val)
            self.assertEqual(store.get_event("evt-1"), ev)
            self.assertEqual(store.get_claim("clm-1"), cl)
            self.assertEqual(store.get_value_observation("clm-1", "cvo-1"), val)

    def test_unsafe_identifier_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = EventClaimStateStore(tmp)
            with self.assertRaises(ValueError):
                store.put_event({"event_id": "../escape"})


if __name__ == "__main__":
    unittest.main()
