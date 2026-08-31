import unittest

from src.psrro.intelligence_behavior import (
    assess_costly_signal,
    classify_buffer_delta,
    classify_coupling_delta,
    classify_h_state_delta,
    classify_rhetoric_action_gap,
    classify_scenario_delta,
)


def behavior(kind="budget", observable=True, resource="high", persistence="sustained", reversibility="hard"):
    return {
        "behavior_id": "beh-synthetic",
        "behavior_kind": kind,
        "observable_action": observable,
        "resource_commitment": {
            "money": resource,
            "military_assets": "none",
            "foreign_exchange": "none",
            "capacity": "none",
            "personnel": "none",
            "political_capital": "none",
            "time": "medium",
        },
        "persistence": persistence,
        "reversibility": reversibility,
        "sensitivity": "public",
    }


def scenario(sid="scn-synthetic", low=0.2, high=0.4, velocity="medium", lead_min=90, lead_max=180):
    return {
        "scenario_id": sid,
        "probability": {"low": low, "high": high},
        "velocity": velocity,
        "lead_time": {"min_days": lead_min, "max_days": lead_max},
    }


class CostlySignalTests(unittest.TestCase):
    def test_speech_cannot_establish_costly_signal(self):
        result = assess_costly_signal(behavior(kind="speech", observable=False))
        self.assertFalse(result["eligible"])
        self.assertEqual(result["strength"], "NOT_APPLICABLE")

    def test_high_resource_sustained_hard_to_reverse_is_strong(self):
        result = assess_costly_signal(behavior())
        self.assertTrue(result["eligible"])
        self.assertEqual(result["strength"], "STRONG")

    def test_low_one_off_easy_action_is_weak(self):
        result = assess_costly_signal(
            behavior(resource="low", persistence="one_off", reversibility="easy")
        )
        self.assertEqual(result["strength"], "WEAK")

    def test_unknown_resources_fail_to_unknown_not_strong(self):
        row = behavior(resource="unknown")
        row["resource_commitment"] = {k: "unknown" for k in row["resource_commitment"]}
        result = assess_costly_signal(row)
        self.assertEqual(result["strength"], "UNKNOWN")


class RhetoricActionTests(unittest.TestCase):
    def test_behavior_can_be_more_intensifying_than_rhetoric(self):
        self.assertEqual(
            classify_rhetoric_action_gap("easing", "intensifying"),
            "behavior_more_intensifying",
        )

    def test_rhetoric_can_be_more_intensifying_than_behavior(self):
        self.assertEqual(
            classify_rhetoric_action_gap("intensifying", "easing"),
            "rhetoric_more_intensifying",
        )

    def test_aligned(self):
        self.assertEqual(classify_rhetoric_action_gap("neutral", "neutral"), "aligned")

    def test_unknown_fails_closed(self):
        self.assertEqual(classify_rhetoric_action_gap("unknown", "intensifying"), "unknown")


class StructuralDeltaTests(unittest.TestCase):
    def test_h2_to_h3_strengthens(self):
        self.assertEqual(classify_h_state_delta("H2", "H3"), "strengthened")

    def test_h3_to_hx_is_falsified_not_stronger(self):
        self.assertEqual(classify_h_state_delta("H3", "Hx"), "falsified")

    def test_hx_to_h1_is_recovered(self):
        self.assertEqual(classify_h_state_delta("Hx", "H1"), "recovered")

    def test_coupling_can_densify_and_relax(self):
        self.assertEqual(classify_coupling_delta("C1", "C2"), "denser")
        self.assertEqual(classify_coupling_delta("C3", "C2"), "sparser")

    def test_buffer_can_deplete_and_restore(self):
        self.assertEqual(classify_buffer_delta("B1", "B2"), "depleted")
        self.assertEqual(classify_buffer_delta("B2", "B1"), "restored")
        self.assertEqual(classify_buffer_delta("BU", "B1"), "unknown")

    def test_scenario_worsening(self):
        prev = scenario()
        curr = scenario(low=0.3, high=0.5, velocity="fast", lead_min=60, lead_max=120)
        result = classify_scenario_delta(prev, curr)
        self.assertEqual(result["direction"], "worse")
        self.assertLess(result["lead_time_min_days_delta"], 0)

    def test_scenario_improvement(self):
        prev = scenario()
        curr = scenario(low=0.1, high=0.3, velocity="slow", lead_min=120, lead_max=240)
        result = classify_scenario_delta(prev, curr)
        self.assertEqual(result["direction"], "improved")

    def test_scenario_mixed(self):
        prev = scenario()
        curr = scenario(low=0.3, high=0.5, velocity="slow", lead_min=120, lead_max=240)
        result = classify_scenario_delta(prev, curr)
        self.assertEqual(result["direction"], "mixed")


if __name__ == "__main__":
    unittest.main()
