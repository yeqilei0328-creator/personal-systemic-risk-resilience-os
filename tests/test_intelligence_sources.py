import tempfile
import unittest

from src.psrro.intelligence_sources import (
    SourceStateStore,
    access_disclosure_required,
    assess_source_concentration,
    can_claim_full_text_verified,
)


def observation(
    oid,
    sid,
    *,
    claim_ref="claim-synthetic",
    relation="independent",
    group="group-a",
    access="full_access",
    full_text=True,
    origin=None,
):
    return {
        "schema_version": "0.1.0",
        "observation_id": oid,
        "source_id": sid,
        "claim_ref": claim_ref,
        "published_at": "2026-08-31T00:00:00Z",
        "retrieved_at": "2026-08-31T00:05:00Z",
        "access_status": access,
        "access_limit_note": None,
        "source_role": "original_report",
        "evidence_type": "document",
        "lineage": {
            "relation": relation,
            "origin_observation_id": origin,
            "independence_group_id": group,
            "shared_origin_note": None,
        },
        "anonymous_source": {"present": False, "origin_group_id": None},
        "provenance": {
            "full_text_verified": full_text,
            "primary_material_accessed": True,
            "source_locator": "synthetic",
        },
        "sensitivity": "public",
    }


class SourceConcentrationTests(unittest.TestCase):
    def test_two_reposts_of_one_origin_are_single_origin(self):
        rows = [
            observation("sob-1", "src-origin", relation="original", group="origin-1"),
            observation("sob-2", "src-repost-a", relation="repost", group="origin-1", origin="sob-1"),
            observation("sob-3", "src-repost-b", relation="syndication", group="origin-1", origin="sob-1"),
        ]
        result = assess_source_concentration(rows)
        self.assertEqual(result["unique_source_count"], 3)
        self.assertEqual(result["known_independence_group_count"], 1)
        self.assertEqual(result["derivative_observation_count"], 2)
        self.assertEqual(result["state"], "SINGLE_ORIGIN")
        self.assertTrue(result["single_source_bias"])

    def test_two_independent_groups_are_diverse(self):
        rows = [
            observation("sob-1", "src-a", group="group-a"),
            observation("sob-2", "src-b", group="group-b"),
        ]
        result = assess_source_concentration(rows)
        self.assertEqual(result["state"], "DIVERSE")
        self.assertFalse(result["single_source_bias"])

    def test_unknown_lineage_does_not_fake_independence(self):
        rows = [
            observation("sob-1", "src-a", relation="unknown", group=None),
            observation("sob-2", "src-b", relation="unknown", group=None),
        ]
        result = assess_source_concentration(rows)
        self.assertEqual(result["state"], "UNKNOWN")
        self.assertEqual(result["known_independence_group_count"], 0)

    def test_mixed_known_and_unknown_is_concentrated_not_diverse(self):
        rows = [
            observation("sob-1", "src-a", group="group-a"),
            observation("sob-2", "src-b", relation="unknown", group=None),
        ]
        result = assess_source_concentration(rows)
        self.assertEqual(result["state"], "CONCENTRATED")


class AccessTests(unittest.TestCase):
    def test_paywall_requires_disclosure(self):
        row = observation("sob-1", "src-a", access="paywall", full_text=False)
        self.assertTrue(access_disclosure_required(row))
        self.assertFalse(can_claim_full_text_verified(row))

    def test_metadata_only_cannot_claim_full_text(self):
        row = observation("sob-1", "src-a", access="metadata_only", full_text=False)
        self.assertTrue(access_disclosure_required(row))
        self.assertFalse(can_claim_full_text_verified(row))

    def test_full_access_plus_flag_can_claim_full_text(self):
        row = observation("sob-1", "src-a", access="full_access", full_text=True)
        self.assertFalse(access_disclosure_required(row))
        self.assertTrue(can_claim_full_text_verified(row))


class StoreTests(unittest.TestCase):
    def test_file_backed_store_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = SourceStateStore(tmp)
            source = {
                "source_id": "src-synthetic",
                "display_name": "Synthetic Source",
                "source_class": "other",
            }
            reputation = {
                "source_id": "src-synthetic",
                "domain": "global_risk",
                "claim_type": "causal",
                "sample_count": 3,
            }
            obs = observation("sob-1", "src-synthetic")

            store.upsert_source(source)
            store.upsert_reputation(reputation)
            store.put_observation(obs)

            self.assertEqual(store.get_source("src-synthetic"), source)
            self.assertEqual(
                store.get_reputation("src-synthetic", "global_risk", "causal"),
                reputation,
            )
            self.assertEqual(store.get_observation("sob-1"), obs)


if __name__ == "__main__":
    unittest.main()
