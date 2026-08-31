import copy
import json
import unittest
from pathlib import Path

from src.psrro.intelligence_output import decide_output_gate, output_state_signature


SIGNALS = {
    "geopolitical_conflicts": {"direction": "neutral", "real_world_evidence": False},
    "energy_shipping": {"direction": "neutral", "real_world_evidence": False},
    "east_asia_security": {"direction": "neutral", "real_world_evidence": False},
    "extreme_weather_disasters": {"direction": "neutral", "real_world_evidence": False},
    "price_real_economy_transmission": {"direction": "neutral", "real_world_evidence": False},
}


def candidate(mode="interrupt_alert", priority="P1", material=True):
    return {
        "candidate_id": "ogc-synthetic",
        "subject_ref": "subject-synthetic",
        "event_ids": ["evt-synthetic"],
        "delivery_mode": mode,
        "intelligence_priority": priority,
        "material_change": material,
        "structural_delta_material": False,
        "observation_signals": copy.deepcopy(SIGNALS),
        "validated_cross_system_transmission": False,
        "major_system_event": False,
        "new_strong_edge": False,
        "hypothesis_falsified": False,
        "lead_time_compressed": False,
        "global_stage_change": False,
        "global_stage_direction": "unchanged",
        "personal_action_change": False,
        "common_cause_refs": [],
        "detected_at": "2026-08-31T00:00:00Z",
        "sensitivity": "public",
    }


def context(previous=None, last=None, cooldown=6, applicable=False, count=0, required=2, now="2026-08-31T12:00:00Z"):
    return {
        "previous_notified_state_signature": previous,
        "last_notified_at": last,
        "cooldown_hours": cooldown,
        "hysteresis": {
            "applicable": applicable,
            "persistence_count": count,
            "required_count": required,
        },
        "now": now,
    }


def worsen_three(row):
    for name in ("geopolitical_conflicts", "energy_shipping", "price_real_economy_transmission"):
        row["observation_signals"][name] = {"direction": "worsen", "real_world_evidence": True}
    return row


ROOT = Path(__file__).resolve().parents[1]


class ExampleContractTests(unittest.TestCase):
    def test_synthetic_example_decision_matches_reference_logic(self):
        candidate_obj = json.loads(
            (ROOT / "examples" / "synthetic" / "intelligence-output-candidate.json").read_text(encoding="utf-8")
        )
        context_obj = json.loads(
            (ROOT / "examples" / "synthetic" / "intelligence-output-gate-context.json").read_text(encoding="utf-8")
        )
        expected = json.loads(
            (ROOT / "examples" / "synthetic" / "intelligence-output-decision.json").read_text(encoding="utf-8")
        )
        actual = decide_output_gate(
            candidate_obj,
            context_obj,
            decision_id=expected["decision_id"],
        )
        self.assertEqual(actual, expected)


class ScheduledBriefTests(unittest.TestCase):
    def test_p2_material_item_emits_in_scheduled_brief(self):
        result = decide_output_gate(candidate(mode="scheduled_brief", priority="P2"), context())
        self.assertTrue(result["notify"])
        self.assertIn("SCHEDULED_MATERIAL_ITEM", result["trigger_codes"])

    def test_p3_is_silent_even_when_material(self):
        result = decide_output_gate(candidate(mode="scheduled_brief", priority="P3"), context())
        self.assertFalse(result["notify"])
        self.assertIn("P3_SILENT", result["suppression_codes"])

    def test_non_material_scheduled_item_is_suppressed(self):
        result = decide_output_gate(candidate(mode="scheduled_brief", material=False), context())
        self.assertFalse(result["notify"])
        self.assertIn("NO_SUBSTANTIVE_CHANGE", result["suppression_codes"])


class InterruptGateTests(unittest.TestCase):
    def test_three_bad_headlines_without_transmission_do_not_alert(self):
        row = worsen_three(candidate())
        row["structural_delta_material"] = True
        result = decide_output_gate(row, context())
        self.assertFalse(result["notify"])
        self.assertIn("NO_TRIGGER", result["suppression_codes"])

    def test_trigger_a_requires_real_transmission(self):
        row = worsen_three(candidate())
        row["structural_delta_material"] = True
        row["validated_cross_system_transmission"] = True
        result = decide_output_gate(row, context())
        self.assertTrue(result["notify"])
        self.assertIn("TRIGGER_A_RESONANCE", result["trigger_codes"])

    def test_hysteresis_suppresses_one_sample_threshold_crossing(self):
        row = worsen_three(candidate())
        row["structural_delta_material"] = True
        row["validated_cross_system_transmission"] = True
        result = decide_output_gate(row, context(applicable=True, count=1, required=2))
        self.assertFalse(result["notify"])
        self.assertIn("HYSTERESIS", result["suppression_codes"])

    def test_hysteresis_allows_persistent_resonance(self):
        row = worsen_three(candidate())
        row["structural_delta_material"] = True
        row["validated_cross_system_transmission"] = True
        result = decide_output_gate(row, context(applicable=True, count=2, required=2))
        self.assertTrue(result["notify"])

    def test_cooldown_suppresses_repeated_low_level_resonance(self):
        row = worsen_three(candidate())
        row["structural_delta_material"] = True
        row["validated_cross_system_transmission"] = True
        result = decide_output_gate(
            row,
            context(last="2026-08-31T10:00:00Z", cooldown=6, now="2026-08-31T12:00:00Z"),
        )
        self.assertFalse(result["notify"])
        self.assertIn("COOLDOWN", result["suppression_codes"])
        self.assertEqual(result["next_eligible_at"], "2026-08-31T16:00:00Z")

    def test_major_event_bypasses_low_level_cooldown(self):
        row = candidate(priority="P1")
        row["major_system_event"] = True
        result = decide_output_gate(
            row,
            context(last="2026-08-31T10:00:00Z", cooldown=6, applicable=True, count=0, required=3),
        )
        self.assertTrue(result["notify"])
        self.assertIn("TRIGGER_B_MAJOR_EVENT", result["trigger_codes"])

    def test_p0_material_event_alerts_without_resonance(self):
        result = decide_output_gate(candidate(priority="P0"), context())
        self.assertTrue(result["notify"])
        self.assertIn("P0_MATERIAL", result["trigger_codes"])

    def test_hypothesis_falsification_alerts(self):
        row = candidate()
        row["hypothesis_falsified"] = True
        result = decide_output_gate(row, context())
        self.assertTrue(result["notify"])
        self.assertIn("HYPOTHESIS_FALSIFIED", result["trigger_codes"])

    def test_improving_global_stage_change_can_emit(self):
        row = candidate()
        row["global_stage_change"] = True
        row["global_stage_direction"] = "improve"
        result = decide_output_gate(row, context())
        self.assertTrue(result["notify"])
        self.assertIn("GLOBAL_STAGE_CHANGE", result["trigger_codes"])

    def test_material_update_without_trigger_is_silent(self):
        result = decide_output_gate(candidate(), context())
        self.assertFalse(result["notify"])
        self.assertIn("NO_TRIGGER", result["suppression_codes"])


class DuplicateTests(unittest.TestCase):
    def test_exact_same_gate_state_does_not_realert(self):
        row = candidate(priority="P0")
        sig = output_state_signature(row)
        result = decide_output_gate(row, context(previous=sig))
        self.assertFalse(result["notify"])
        self.assertIn("DUPLICATE_STATE", result["suppression_codes"])

    def test_signature_ignores_detection_timestamp_and_notes(self):
        left = candidate(priority="P0")
        right = copy.deepcopy(left)
        right["detected_at"] = "2026-09-01T00:00:00Z"
        right["notes"] = "wording changed"
        self.assertEqual(output_state_signature(left), output_state_signature(right))


if __name__ == "__main__":
    unittest.main()
