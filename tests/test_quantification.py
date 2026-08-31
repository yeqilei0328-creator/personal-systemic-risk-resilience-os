import unittest

from src.psrro.quantification import (
    buffer_snapshot,
    coupling_snapshot,
    recommend_edge_state,
    recommend_r_level,
)


def edge(edge_id, src, dst, state="H2", persistence="transient", common=False):
    return {
        "edge_id": edge_id,
        "state": state,
        "source_node": {"first_order_variable": src},
        "target_node": {"first_order_variable": dst},
        "persistence": persistence,
        "common_cause": {"present": common},
        "mechanism": "synthetic mechanism",
        "evidence_ids": ["evd-1", "evd-2", "evd-3"],
        "metrics": [{"latest_value": 1.0}],
    }


def evidence(eid, source, stance="supports", quality=0.8):
    return {
        "evidence_id": eid,
        "stance": stance,
        "source": {"name": source},
        "quality": {
            "provenance_score": quality,
            "independence_score": quality,
            "confidence": quality,
        },
    }


def scenario(impact=3, p_high=0.3, lead=90, velocity="medium"):
    return {
        "impact": impact,
        "probability": {"high": p_high},
        "lead_time": {"min_days": lead},
        "velocity": velocity,
    }


def exposure(gross=3, sensitivity=2, adaptive=2):
    dims = {
        "geography": 0, "assets": 0, "business": 0, "supply_chain": 0,
        "finance": 0, "family": 0, "infrastructure": gross,
    }
    return {
        "dimensions": dims,
        "sensitivity_score": sensitivity,
        "adaptive_capacity_score": adaptive,
    }


class CouplingTests(unittest.TestCase):
    def test_c0(self):
        self.assertEqual(coupling_snapshot([])["band"], "C0")

    def test_c1(self):
        edges = [edge("e1", "A", "B"), edge("e2", "B", "C")]
        self.assertEqual(coupling_snapshot(edges)["band"], "C1")

    def test_c2(self):
        edges = [
            edge("e1", "A", "B", persistence="persistent"),
            edge("e2", "B", "C", persistence="persistent"),
            edge("e3", "C", "A"),
            edge("e4", "A", "C"),
        ]
        self.assertEqual(coupling_snapshot(edges)["band"], "C2")

    def test_c3(self):
        edges = [
            edge("e1", "A", "B", state="H3", persistence="persistent"),
            edge("e2", "B", "C", state="H3", persistence="persistent"),
            edge("e3", "C", "D", persistence="persistent"),
            edge("e4", "D", "A", persistence="persistent"),
            edge("e5", "A", "C"),
            edge("e6", "B", "D"),
        ]
        result = coupling_snapshot(edges)
        self.assertEqual(result["band"], "C3")
        self.assertGreaterEqual(result["max_independent_path_length"], 3)

    def test_common_cause_not_counted_as_independent_pair(self):
        result = coupling_snapshot([
            edge("e1", "A", "B", common=True),
            edge("e2", "B", "C"),
        ])
        self.assertEqual(result["unique_validated_directed_pairs"], 2)
        self.assertEqual(result["independent_validated_directed_pairs"], 1)
        self.assertEqual(result["band"], "C0")


class BufferTests(unittest.TestCase):
    def buf(self, bid, current, baseline=100, floor=0, criticality=5, repl=0, burn=0):
        return {
            "buffer_id": bid,
            "criticality": criticality,
            "baseline_capacity": baseline,
            "current_capacity": current,
            "minimum_viable_capacity": floor,
            "replenishment_rate_per_day": repl,
            "depletion_rate_per_day": burn,
        }

    def test_b0(self):
        result = buffer_snapshot([self.buf("b1", 90), self.buf("b2", 85)])
        self.assertEqual(result["band"], "B0")

    def test_b1(self):
        result = buffer_snapshot([self.buf("b1", 65)])
        self.assertEqual(result["band"], "B1")

    def test_b2(self):
        result = buffer_snapshot([self.buf("b1", 40)])
        self.assertEqual(result["band"], "B2")

    def test_b3(self):
        result = buffer_snapshot([self.buf("b1", 5)])
        self.assertEqual(result["band"], "B3")

    def test_depletion_time(self):
        result = buffer_snapshot([self.buf("b1", 50, burn=5)])
        self.assertEqual(result["earliest_floor_days"], 10.0)


class EdgeAssessmentTests(unittest.TestCase):
    def assessment(self, **overrides):
        base = {
            "falsification_triggered": False,
            "mechanism_documented": True,
            "temporal_ordering_confirmed": True,
            "metric_observed": True,
            "common_cause_resolved": False,
            "counterevidence_resolved": False,
            "persistence_observations": 0,
        }
        base.update(overrides)
        return base

    def test_h0(self):
        e = edge("e", "A", "B")
        self.assertEqual(recommend_edge_state(e, [], self.assessment())["recommended_state"], "H0")

    def test_h1(self):
        e = edge("e", "A", "B")
        ev = [evidence("evd-1", "source-1")]
        self.assertEqual(recommend_edge_state(e, ev, self.assessment())["recommended_state"], "H1")

    def test_h2(self):
        e = edge("e", "A", "B")
        ev = [evidence("evd-1", "source-1"), evidence("evd-2", "source-2")]
        self.assertEqual(recommend_edge_state(e, ev, self.assessment())["recommended_state"], "H2")

    def test_h3(self):
        e = edge("e", "A", "B", persistence="persistent")
        ev = [
            evidence("evd-1", "source-1"),
            evidence("evd-2", "source-2"),
            evidence("evd-3", "source-3"),
        ]
        result = recommend_edge_state(e, ev, self.assessment(persistence_observations=3))
        self.assertEqual(result["recommended_state"], "H3")

    def test_hx(self):
        e = edge("e", "A", "B")
        result = recommend_edge_state(e, [], self.assessment(falsification_triggered=True))
        self.assertEqual(result["recommended_state"], "Hx")

    def test_common_cause_caps_at_h1_until_resolved(self):
        e = edge("e", "A", "B", common=True)
        ev = [evidence("evd-1", "source-1"), evidence("evd-2", "source-2")]
        self.assertEqual(recommend_edge_state(e, ev, self.assessment())["recommended_state"], "H1")


class RLevelTests(unittest.TestCase):
    def test_r0(self):
        self.assertEqual(
            recommend_r_level(scenario(impact=1, p_high=0.05), exposure(gross=1))["recommended_r_level"],
            "R0",
        )

    def test_r1(self):
        self.assertEqual(
            recommend_r_level(scenario(impact=2, p_high=0.15), exposure(gross=2))["recommended_r_level"],
            "R1",
        )

    def test_r2(self):
        self.assertEqual(
            recommend_r_level(scenario(impact=3, p_high=0.3), exposure(gross=3))["recommended_r_level"],
            "R2",
        )

    def test_r3(self):
        self.assertEqual(
            recommend_r_level(
                scenario(impact=5, p_high=0.6, lead=20, velocity="fast"),
                exposure(gross=4, adaptive=1),
                preparation_latency_days=40,
            )["recommended_r_level"],
            "R3",
        )

    def test_r4(self):
        self.assertEqual(
            recommend_r_level(
                scenario(impact=5, p_high=0.8, lead=5, velocity="acute"),
                exposure(gross=4),
                local_disruption=True,
            )["recommended_r_level"],
            "R4",
        )

    def test_r5(self):
        self.assertEqual(
            recommend_r_level(
                scenario(impact=5, p_high=1.0, lead=0, velocity="acute"),
                exposure(gross=5),
                life_safety_failure=True,
            )["recommended_r_level"],
            "R5",
        )


if __name__ == "__main__":
    unittest.main()
