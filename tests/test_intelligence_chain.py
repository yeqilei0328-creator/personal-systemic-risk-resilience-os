import copy
import json
import unittest
from pathlib import Path

from src.psrro.intelligence_chain import (
    build_chain_snapshot,
    is_chain_supported_link,
    is_forecast_only,
)


ROOT = Path(__file__).resolve().parents[1]


def definition():
    return json.loads(
        (ROOT / "chains" / "climate-food-energy-inflation-ai.json").read_text(
            encoding="utf-8"
        )
    )


def assessment(link, idx, h="H1", causality=0, forecast=0, direction="stable", material=False):
    return {
        "assessment_id": f"cla-chain-{idx}",
        "chain_id": "chn-climate-food-energy-inflation-ai-v0.1",
        "link_id": link["link_id"],
        "source_node_id": link["source_node_id"],
        "target_node_id": link["target_node_id"],
        "h_state": h,
        "supporting_evidence_ids": ["evd-chain-synthetic"] if causality > 0 else [],
        "epistemic_counts": {
            "fact": 0,
            "forecast": forecast,
            "correlation": 0,
            "causality": causality,
            "counterevidence": 0,
        },
        "direction": direction,
        "material_delta": material,
    }


def all_assessments(h="H1", causality=0, direction="stable"):
    d = definition()
    return [
        assessment(link, idx, h=h, causality=causality, direction=direction)
        for idx, link in enumerate(d["links"], start=1)
    ]


class ExampleContractTests(unittest.TestCase):
    def test_full_transmitting_snapshot_matches_fixture(self):
        d = definition()
        rows = all_assessments(h="H2", causality=1, direction="strengthening")
        for row in rows:
            row["material_delta"] = True
        expected = json.loads(
            (ROOT / "examples" / "synthetic" / "chain-watch-snapshot.json").read_text(
                encoding="utf-8"
            )
        )
        actual = build_chain_snapshot(
            d,
            rows,
            snapshot_id=expected["snapshot_id"],
            as_of=expected["as_of"],
            sensitivity=expected["sensitivity"],
        )
        self.assertEqual(actual, expected)


class LinkSupportTests(unittest.TestCase):
    def test_forecast_only_is_not_chain_support(self):
        row = assessment(definition()["links"][0], 1, h="H2", forecast=2)
        self.assertTrue(is_forecast_only(row))
        self.assertFalse(is_chain_supported_link(row))

    def test_h2_with_causal_evidence_is_supported(self):
        row = assessment(definition()["links"][0], 1, h="H2", causality=1)
        self.assertTrue(is_chain_supported_link(row))

    def test_causal_count_without_evidence_ref_fails_closed(self):
        row = assessment(definition()["links"][0], 1, h="H2", causality=1)
        row["supporting_evidence_ids"] = []
        self.assertFalse(is_chain_supported_link(row))


class SnapshotTests(unittest.TestCase):
    def test_full_h2_causal_chain_is_transmitting(self):
        d = definition()
        rows = all_assessments(h="H2", causality=1, direction="strengthening")
        result = build_chain_snapshot(d, rows)
        self.assertEqual(result["chain_state"], "TRANSMITTING")
        self.assertTrue(result["full_chain_supported"])
        self.assertEqual(
            result["longest_contiguous_supported_path"],
            len(d["links"]),
        )

    def test_required_hx_breaks_chain(self):
        d = definition()
        rows = all_assessments(h="H2", causality=1)
        rows[2]["h_state"] = "Hx"
        rows[2]["direction"] = "falsified"
        result = build_chain_snapshot(d, rows)
        self.assertEqual(result["chain_state"], "BROKEN")
        self.assertFalse(result["full_chain_supported"])

    def test_isolated_supported_links_are_fragmented(self):
        d = definition()
        rows = all_assessments()
        rows[0]["h_state"] = "H2"
        rows[0]["epistemic_counts"]["causality"] = 1
        rows[2]["h_state"] = "H2"
        rows[2]["epistemic_counts"]["causality"] = 1
        result = build_chain_snapshot(d, rows)
        self.assertEqual(result["chain_state"], "FRAGMENTED")
        self.assertEqual(result["longest_contiguous_supported_path"], 1)

    def test_two_contiguous_supported_links_are_building(self):
        d = definition()
        rows = all_assessments()
        for idx in (1, 2):
            rows[idx]["h_state"] = "H2"
            rows[idx]["epistemic_counts"]["causality"] = 1
            rows[idx]["direction"] = "strengthening"
        result = build_chain_snapshot(d, rows)
        self.assertEqual(result["chain_state"], "BUILDING")
        self.assertEqual(result["longest_contiguous_supported_path"], 2)

    def test_previous_active_chain_can_relax(self):
        d = definition()
        previous_rows = all_assessments(h="H2", causality=1)
        previous = build_chain_snapshot(
            d,
            previous_rows,
            snapshot_id="chs-previous",
        )
        current_rows = all_assessments()
        current_rows[0]["h_state"] = "H2"
        current_rows[0]["epistemic_counts"]["causality"] = 1
        current_rows[0]["direction"] = "weakening"
        current_rows[1]["direction"] = "weakening"
        result = build_chain_snapshot(
            d,
            current_rows,
            previous_snapshot=previous,
        )
        self.assertEqual(result["chain_state"], "RELAXING")
        self.assertEqual(result["previous_snapshot_id"], "chs-previous")

    def test_order_of_input_assessments_does_not_change_output_order(self):
        d = definition()
        rows = all_assessments(h="H2", causality=1)
        forward = build_chain_snapshot(d, rows)
        reverse = build_chain_snapshot(d, list(reversed(rows)))
        self.assertEqual(
            forward["ordered_link_assessment_ids"],
            reverse["ordered_link_assessment_ids"],
        )

    def test_missing_link_assessment_fails_closed(self):
        d = definition()
        rows = all_assessments()
        with self.assertRaises(ValueError):
            build_chain_snapshot(d, rows[:-1])

    def test_duplicate_link_assessment_fails_closed(self):
        d = definition()
        rows = all_assessments()
        rows.append(copy.deepcopy(rows[0]))
        rows[-1]["assessment_id"] = "cla-duplicate"
        with self.assertRaises(ValueError):
            build_chain_snapshot(d, rows)


if __name__ == "__main__":
    unittest.main()
