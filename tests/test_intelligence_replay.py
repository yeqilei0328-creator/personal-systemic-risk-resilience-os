import copy
import json
import unittest
from pathlib import Path

from src.psrro.intelligence_chain import build_chain_snapshot
from src.psrro.intelligence_events import detect_material_change, event_fingerprint
from src.psrro.intelligence_output import decide_output_gate, output_state_signature
from src.psrro.intelligence_replay import evaluate_replay_step, summarize_replay_suite
from src.psrro.intelligence_sources import (
    assess_source_concentration,
    can_claim_full_text_verified,
)


ROOT = Path(__file__).resolve().parents[1]
SIGNAL_NAMES = (
    "geopolitical_conflicts",
    "energy_shipping",
    "east_asia_security",
    "extreme_weather_disasters",
    "price_real_economy_transmission",
)


def base_candidate(mode="interrupt_alert", priority="P1", material=True):
    return {
        "candidate_id": "ogc-replay",
        "subject_ref": "replay-subject",
        "event_ids": ["evt-replay"],
        "delivery_mode": mode,
        "intelligence_priority": priority,
        "material_change": material,
        "structural_delta_material": False,
        "observation_signals": {
            name: {"direction": "neutral", "real_world_evidence": False}
            for name in SIGNAL_NAMES
        },
        "validated_cross_system_transmission": False,
        "major_system_event": False,
        "new_strong_edge": False,
        "hypothesis_falsified": False,
        "lead_time_compressed": False,
        "global_stage_change": False,
        "global_stage_direction": "unchanged",
        "personal_action_change": False,
        "common_cause_refs": [],
        "sensitivity": "public",
    }


def context(
    *,
    previous=None,
    last=None,
    now="2026-08-31T12:00:00Z",
    cooldown=6,
    applicable=False,
    count=0,
    required=2,
):
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
    for name in (
        "geopolitical_conflicts",
        "energy_shipping",
        "price_real_economy_transmission",
    ):
        row["observation_signals"][name] = {
            "direction": "worsen",
            "real_world_evidence": True,
        }
    return row


def source_observation(oid, sid, relation, group, origin=None):
    return {
        "observation_id": oid,
        "source_id": sid,
        "claim_ref": "claim-replay",
        "access_status": "full_access",
        "lineage": {
            "relation": relation,
            "origin_observation_id": origin,
            "independence_group_id": group,
        },
    }


def chain_definition():
    return json.loads(
        (ROOT / "chains" / "climate-food-energy-inflation-ai.json").read_text(
            encoding="utf-8"
        )
    )


def chain_assessments(h="H2", causality=1, direction="strengthening"):
    d = chain_definition()
    rows = []
    for idx, link in enumerate(d["links"], start=1):
        rows.append(
            {
                "assessment_id": f"cla-replay-{idx}",
                "chain_id": d["chain_id"],
                "link_id": link["link_id"],
                "source_node_id": link["source_node_id"],
                "target_node_id": link["target_node_id"],
                "h_state": h,
                "epistemic_counts": {
                    "fact": 1,
                    "forecast": 0,
                    "correlation": 0,
                    "causality": causality,
                    "counterevidence": 0,
                },
                "supporting_evidence_ids": ["evd-replay"] if causality else [],
                "direction": direction,
                "material_delta": True,
            }
        )
    return rows


def replay_result(decision, idx, category, expected_notify, expected_code):
    return evaluate_replay_step(
        decision,
        result_id=f"rpr-redteam-{idx:02d}",
        case_id=f"rpc-redteam-{idx:02d}",
        step_id=f"step-{idx:02d}",
        category=category,
        expected_notify=expected_notify,
        expected_code=expected_code,
        notes="synthetic red-team case",
    )


class LayerIntegrationTests(unittest.TestCase):
    def test_three_reposts_remain_single_origin_and_do_not_validate_transmission(self):
        rows = [
            source_observation("sob-1", "src-origin", "original", "origin-1"),
            source_observation("sob-2", "src-copy-a", "repost", "origin-1", "sob-1"),
            source_observation("sob-3", "src-copy-b", "syndication", "origin-1", "sob-1"),
        ]
        concentration = assess_source_concentration(rows)
        self.assertEqual(concentration["state"], "SINGLE_ORIGIN")

        candidate = worsen_three(base_candidate())
        candidate["structural_delta_material"] = True
        candidate["validated_cross_system_transmission"] = False
        decision = decide_output_gate(candidate, context())
        result = replay_result(decision, 1, "derivative_source", False, "NO_TRIGGER")
        self.assertTrue(result["passed"])

    def test_full_chain_can_feed_true_resonance_gate(self):
        d = chain_definition()
        snapshot = build_chain_snapshot(
            d,
            chain_assessments(),
            snapshot_id="chs-replay-transmitting",
        )
        self.assertEqual(snapshot["chain_state"], "TRANSMITTING")

        candidate = worsen_three(base_candidate())
        candidate["structural_delta_material"] = True
        candidate["validated_cross_system_transmission"] = True
        decision = decide_output_gate(
            candidate,
            context(applicable=True, count=2, required=2),
        )
        result = replay_result(
            decision,
            2,
            "true_resonance",
            True,
            "TRIGGER_A_RESONANCE",
        )
        self.assertTrue(result["passed"])

    def test_chain_break_maps_to_falsification_alert_path(self):
        d = chain_definition()
        rows = chain_assessments()
        rows[2]["h_state"] = "Hx"
        rows[2]["direction"] = "falsified"
        rows[2]["epistemic_counts"]["causality"] = 0
        rows[2]["supporting_evidence_ids"] = []
        snapshot = build_chain_snapshot(
            d,
            rows,
            snapshot_id="chs-replay-broken",
        )
        self.assertEqual(snapshot["chain_state"], "BROKEN")

        candidate = base_candidate()
        candidate["hypothesis_falsified"] = True
        decision = decide_output_gate(candidate, context())
        result = replay_result(
            decision,
            3,
            "chain_break",
            True,
            "HYPOTHESIS_FALSIFIED",
        )
        self.assertTrue(result["passed"])

    def test_previous_chain_relaxes(self):
        d = chain_definition()
        previous = build_chain_snapshot(
            d,
            chain_assessments(),
            snapshot_id="chs-replay-previous",
        )
        current_rows = chain_assessments(h="H1", causality=0, direction="weakening")
        snapshot = build_chain_snapshot(
            d,
            current_rows,
            snapshot_id="chs-replay-relaxing",
            previous_snapshot=previous,
        )
        self.assertEqual(snapshot["chain_state"], "RELAXING")


class GateRedTeamTests(unittest.TestCase):
    def test_false_resonance_suppressed(self):
        candidate = worsen_three(base_candidate())
        candidate["structural_delta_material"] = True
        decision = decide_output_gate(candidate, context())
        self.assertTrue(
            replay_result(decision, 4, "false_resonance", False, "NO_TRIGGER")["passed"]
        )

    def test_hysteresis_then_persistent_resonance(self):
        candidate = worsen_three(base_candidate())
        candidate["structural_delta_material"] = True
        candidate["validated_cross_system_transmission"] = True

        first = decide_output_gate(
            candidate,
            context(applicable=True, count=1, required=2),
        )
        self.assertTrue(
            replay_result(first, 5, "hysteresis", False, "HYSTERESIS")["passed"]
        )

        second = decide_output_gate(
            candidate,
            context(applicable=True, count=2, required=2),
        )
        self.assertTrue(
            replay_result(
                second,
                6,
                "true_resonance",
                True,
                "TRIGGER_A_RESONANCE",
            )["passed"]
        )

    def test_exact_duplicate_suppressed(self):
        candidate = base_candidate(priority="P0")
        signature = output_state_signature(candidate)
        decision = decide_output_gate(candidate, context(previous=signature))
        self.assertTrue(
            replay_result(
                decision,
                7,
                "duplicate",
                False,
                "DUPLICATE_STATE",
            )["passed"]
        )

    def test_p3_silent(self):
        decision = decide_output_gate(
            base_candidate(mode="scheduled_brief", priority="P3"),
            context(),
        )
        self.assertTrue(
            replay_result(decision, 8, "p3_silent", False, "P3_SILENT")["passed"]
        )

    def test_p2_material_in_scheduled_brief(self):
        decision = decide_output_gate(
            base_candidate(mode="scheduled_brief", priority="P2"),
            context(),
        )
        self.assertTrue(
            replay_result(
                decision,
                9,
                "scheduled_brief",
                True,
                "SCHEDULED_MATERIAL_ITEM",
            )["passed"]
        )

    def test_hypothesis_falsification_emits(self):
        candidate = base_candidate()
        candidate["hypothesis_falsified"] = True
        decision = decide_output_gate(candidate, context())
        self.assertTrue(
            replay_result(
                decision,
                10,
                "falsification",
                True,
                "HYPOTHESIS_FALSIFIED",
            )["passed"]
        )

    def test_improving_stage_change_emits(self):
        candidate = base_candidate()
        candidate["global_stage_change"] = True
        candidate["global_stage_direction"] = "improve"
        decision = decide_output_gate(candidate, context())
        self.assertTrue(
            replay_result(
                decision,
                11,
                "improvement",
                True,
                "GLOBAL_STAGE_CHANGE",
            )["passed"]
        )


class MaterialityAndAccessTests(unittest.TestCase):
    def test_title_only_update_stays_non_material(self):
        basis = {
            "actors": ["Actor A"],
            "actions": ["Deploy"],
            "objects": ["System X"],
            "locations": ["Region 1"],
            "time_window_key": "2026-08-31",
            "consequences": ["Operational change"],
        }
        fp = event_fingerprint(basis)
        previous = {
            "event_id": "evt-replay",
            "display_title": "Old headline",
            "fingerprint": fp,
            "intelligence_priority": "P2",
            "material_markers": [],
            "lifecycle": "developing",
            "sensitivity": "public",
        }
        current = copy.deepcopy(previous)
        current["display_title"] = "New headline wording"
        material = detect_material_change(previous, current)
        self.assertFalse(material["material"])

        candidate = base_candidate(mode="scheduled_brief", priority="P2", material=False)
        decision = decide_output_gate(candidate, context())
        self.assertTrue(
            replay_result(
                decision,
                12,
                "materiality",
                False,
                "NO_SUBSTANTIVE_CHANGE",
            )["passed"]
        )

    def test_metadata_only_source_cannot_claim_full_text(self):
        observation = {
            "access_status": "metadata_only",
            "provenance": {"full_text_verified": False},
        }
        self.assertFalse(can_claim_full_text_verified(observation))


class ReplaySummaryTests(unittest.TestCase):
    def test_summary_counts_fp_fn_and_code_mismatch(self):
        results = [
            {
                "result_id": "rpr-1",
                "category": "duplicate",
                "passed": False,
                "error_class": "FALSE_POSITIVE",
            },
            {
                "result_id": "rpr-2",
                "category": "falsification",
                "passed": False,
                "error_class": "FALSE_NEGATIVE",
            },
            {
                "result_id": "rpr-3",
                "category": "scheduled_brief",
                "passed": False,
                "error_class": "CODE_MISMATCH",
            },
            {
                "result_id": "rpr-4",
                "category": "improvement",
                "passed": True,
                "error_class": "NONE",
            },
        ]
        summary = summarize_replay_suite(results)
        self.assertEqual(summary["total_steps"], 4)
        self.assertEqual(summary["passed_steps"], 1)
        self.assertEqual(summary["failed_steps"], 3)
        self.assertEqual(summary["false_positive_count"], 1)
        self.assertEqual(summary["false_negative_count"], 1)
        self.assertEqual(summary["code_mismatch_count"], 1)
        self.assertEqual(summary["duplicate_control_failure_count"], 1)
        self.assertEqual(summary["deescalation_falsification_failure_count"], 1)
        self.assertNotIn("accuracy_score", summary)

    def test_all_pass_synthetic_suite_matches_fixture(self):
        # Build a compact deterministic pass suite from gate outcomes.
        cases = []

        c1 = base_candidate(mode="scheduled_brief", priority="P2")
        cases.append(replay_result(
            decide_output_gate(c1, context()),
            21,
            "scheduled_brief",
            True,
            "SCHEDULED_MATERIAL_ITEM",
        ))

        c2 = base_candidate(mode="scheduled_brief", priority="P3")
        cases.append(replay_result(
            decide_output_gate(c2, context()),
            22,
            "p3_silent",
            False,
            "P3_SILENT",
        ))

        c3 = base_candidate()
        c3["hypothesis_falsified"] = True
        cases.append(replay_result(
            decide_output_gate(c3, context()),
            23,
            "falsification",
            True,
            "HYPOTHESIS_FALSIFIED",
        ))

        expected = json.loads(
            (ROOT / "examples" / "synthetic" / "replay-suite-summary.json").read_text(
                encoding="utf-8"
            )
        )
        actual = summarize_replay_suite(
            cases,
            suite_id=expected["suite_id"],
            generated_at=expected["generated_at"],
            sensitivity=expected["sensitivity"],
        )
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
