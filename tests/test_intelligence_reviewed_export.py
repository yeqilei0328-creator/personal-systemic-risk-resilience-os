"""Deterministic fail-closed one-shot reviewed event export tests."""

from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from src.psrro.intelligence_events import event_fingerprint
from src.psrro.intelligence_reviewed_export import export_reviewed_packet, read_packet, validate_reviewed_packet

ROOT = Path(__file__).resolve().parents[1]


def fixture() -> dict:
    event = json.loads((ROOT / "examples/synthetic/event-state-record.json").read_text())
    claim = json.loads((ROOT / "examples/synthetic/claim-record.json").read_text())
    obs = json.loads((ROOT / "examples/synthetic/source-observation.json").read_text())
    event["claim_ids"] = [claim["claim_id"]]
    event["source_observation_ids"] = [obs["observation_id"]]
    event["fingerprint"] = event_fingerprint(event["fingerprint_basis"])
    obs["claim_ref"] = claim["claim_id"]
    obs["provenance"]["source_locator"] = "https://example.org/synthetic-source"
    obs["retrieved_at"] = "2026-08-31T00:05:00Z"
    obs["published_at"] = "2026-08-31T00:00:00Z"
    claim["event_id"] = event["event_id"]
    claim["source_observation_ids"] = [obs["observation_id"]]
    claim["last_updated"] = "2026-08-31T01:00:00Z"
    assessment = {
        "schema_version": "0.1.0",
        "assessment_id": "mca-synthetic-reviewed",
        "event_id": event["event_id"],
        "previous_state_ref": None,
        "current_state_ref": "reviewed-initial-state",
        "material": True,
        "change_types": ["new_event"],
        "changed_claim_ids": [claim["claim_id"]],
        "numeric_change_refs": [],
        "priority_from": None,
        "priority_to": event["intelligence_priority"],
        "reasons": ["Synthetic initial discovery; not global-risk transmission"],
        "assessed_at": "2026-08-31T01:15:00Z",
        "sensitivity": "public",
    }
    return {
        "packet_version": "psrro-reviewed-public-event.v0.1",
        "review_mode": "reviewed_public_sources",
        "reviewer_type": "ai_assistant",
        "reviewed_at": "2026-08-31T02:00:00Z",
        "review_notes": ["Entirely synthetic test material"],
        "event_state": event,
        "claims": [claim],
        "material_change": assessment,
        "source_observations": [obs],
    }


class ReviewedExportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.destination = self.root / "first-export"

    def test_schema_and_native_export_success(self):
        packet = fixture()
        result = export_reviewed_packet(packet, self.destination)
        self.assertEqual(result["status"], "NATIVE_REVIEWED_EXPORTED")
        self.assertEqual(result["claim_count"], 1)
        self.assertTrue((self.destination / "events" / (packet["event_state"]["event_id"] + ".json")).is_file())
        self.assertTrue((self.destination / "observations" / (packet["source_observations"][0]["observation_id"] + ".json")).is_file())
        m = json.loads((self.destination / "review-manifest.json").read_text())
        self.assertEqual(m["packet_sha256"], result["packet_sha256"])
        self.assertEqual(hashlib.sha256((self.destination / "review-manifest.json").read_bytes()).hexdigest(), result["manifest_sha256"])
        self.assertEqual(len(m["artifacts"]), 4)
        for item in m["artifacts"]:
            p = self.destination / item["path"]
            self.assertEqual(item["sha256"], hashlib.sha256(p.read_bytes()).hexdigest())
        self.assertIn("reviewed_sources_not_automated_news_ingestion", m["limitations"])
        self.assertEqual(m["reviewer_type"], "ai_assistant")

    def test_no_overwrite(self):
        p = fixture()
        export_reviewed_packet(p, self.destination)
        with self.assertRaisesRegex(ValueError, "scratch_output_already_exists"):
            export_reviewed_packet(p, self.destination)

    def test_reject_non_tmp_destination(self):
        with self.assertRaisesRegex(ValueError, "scratch_output_must_be_under_system_tmp"):
            export_reviewed_packet(fixture(), Path.home() / "psrro-wi03-outside-tmp")

    def test_reject_output_within_method_repo(self):
        with self.assertRaisesRegex(ValueError, "scratch_output_inside_method_repo_denied"):
            export_reviewed_packet(fixture(), ROOT / "event-export-denied")
        self.assertFalse((ROOT / "event-export-denied").exists())

    def test_reject_duplicate_json_keys(self):
        path = self.root / "duplicate.json"
        path.write_text('{"packet_version":"a","packet_version":"b"}')
        with self.assertRaisesRegex(ValueError, "duplicate_json_key"):
            read_packet(path)

    def test_reject_symlink_packet(self):
        original = self.root / "packet.json"
        original.write_text(json.dumps(fixture()))
        alias = self.root / "alias.json"
        alias.symlink_to(original)
        with self.assertRaisesRegex(ValueError, "packet_path_or_size_invalid"):
            read_packet(alias)

    def test_reject_bad_fingerprint_without_writing(self):
        p = fixture()
        p["event_state"]["fingerprint"] = "a" * 64
        with self.assertRaisesRegex(ValueError, "event_fingerprint_mismatch"):
            export_reviewed_packet(p, self.destination)
        self.assertFalse(self.destination.exists())

    def test_reject_source_reference_conflict(self):
        p = fixture()
        p["source_observations"][0]["claim_ref"] = "clm-wrong"
        with self.assertRaisesRegex(ValueError, "observation_claim_or_privacy_mismatch"):
            export_reviewed_packet(p, self.destination)

    def test_reject_claim_after_assessment(self):
        p = fixture()
        p["claims"][0]["last_updated"] = "2026-08-31T02:30:00Z"
        with self.assertRaisesRegex(ValueError, "claim_updated_after_assessment"):
            export_reviewed_packet(p, self.destination)

    def test_reject_retrieval_after_review(self):
        p = fixture()
        p["source_observations"][0]["retrieved_at"] = "2026-09-01T00:00:00Z"
        with self.assertRaisesRegex(ValueError, "observation_review_chronology_invalid"):
            export_reviewed_packet(p, self.destination)

    def test_reject_non_public_claim(self):
        p = fixture()
        p["claims"][0]["sensitivity"] = "restricted"
        with self.assertRaisesRegex(ValueError, "claim_event_or_privacy_mismatch"):
            export_reviewed_packet(p, self.destination)

    def test_reject_http_source(self):
        p = fixture()
        p["source_observations"][0]["provenance"]["source_locator"] = "http://example.org/source"
        with self.assertRaisesRegex(ValueError, "invalid_source_locator"):
            export_reviewed_packet(p, self.destination)

    @staticmethod
    def _with_claims(count: int) -> dict:
        packet = fixture()
        base_claim = packet["claims"][0]
        base_obs = packet["source_observations"][0]
        claims, observations = [], []
        for index in range(count):
            claim = copy.deepcopy(base_claim)
            obs = copy.deepcopy(base_obs)
            claim["claim_id"] = f"clm-reviewed-{index}"
            obs["observation_id"] = f"sob-reviewed-{index}"
            obs["claim_ref"] = claim["claim_id"]
            claim["source_observation_ids"] = [obs["observation_id"]]
            claims.append(claim)
            observations.append(obs)
        packet["claims"] = claims
        packet["source_observations"] = observations
        packet["event_state"]["claim_ids"] = [c["claim_id"] for c in claims]
        packet["event_state"]["source_observation_ids"] = [o["observation_id"] for o in observations]
        packet["material_change"]["changed_claim_ids"] = [c["claim_id"] for c in claims]
        return packet

    def test_superseded_claim_must_point_to_existing_claim(self):
        p = self._with_claims(2)
        p["claims"][0]["status"] = "superseded"
        p["claims"][0]["superseded_by_claim_id"] = "clm-not-in-packet"
        with self.assertRaisesRegex(ValueError, "supersession_successor_not_in_packet"):
            export_reviewed_packet(p, self.destination)
        self.assertFalse(self.destination.exists())

    def test_superseded_claim_cannot_point_to_self(self):
        p = self._with_claims(2)
        p["claims"][0]["status"] = "superseded"
        p["claims"][0]["superseded_by_claim_id"] = p["claims"][0]["claim_id"]
        with self.assertRaisesRegex(ValueError, "self_supersession_denied"):
            validate_reviewed_packet(p)

    def test_supersession_cycle_denied(self):
        p = self._with_claims(2)
        for i, j in ((0, 1), (1, 0)):
            p["claims"][i]["status"] = "superseded"
            p["claims"][i]["superseded_by_claim_id"] = p["claims"][j]["claim_id"]
        with self.assertRaisesRegex(ValueError, "supersession_cycle_denied"):
            validate_reviewed_packet(p)

    def test_accepted_claim_cannot_have_successor(self):
        p = self._with_claims(2)
        p["claims"][0]["status"] = "accepted"
        p["claims"][0]["superseded_by_claim_id"] = p["claims"][1]["claim_id"]
        with self.assertRaisesRegex(ValueError, "non_superseded_claim_with_successor"):
            validate_reviewed_packet(p)

    def test_valid_multi_version_chain_is_allowed(self):
        p = self._with_claims(3)
        for i in (0, 1):
            p["claims"][i]["status"] = "superseded"
            p["claims"][i]["superseded_by_claim_id"] = p["claims"][i + 1]["claim_id"]
        p["claims"][2]["status"] = "accepted"
        proof = validate_reviewed_packet(p)
        self.assertEqual(proof["claim_count"], 3)
        result = export_reviewed_packet(p, self.destination)
        self.assertEqual(result["status"], "NATIVE_REVIEWED_EXPORTED")

    def test_valid_convergent_supersession_chain_allowed(self):
        p = self._with_claims(3)
        for i in (0, 1):
            p["claims"][i]["status"] = "superseded"
            p["claims"][i]["superseded_by_claim_id"] = p["claims"][2]["claim_id"]
        p["claims"][2]["status"] = "accepted"
        self.assertEqual(validate_reviewed_packet(p)["claim_count"], 3)

    def test_reject_unknown_schema_key(self):
        p = fixture()
        p["event_state"]["unknown"] = "not allowed"
        with self.assertRaisesRegex(ValueError, "event_state_schema_invalid"):
            export_reviewed_packet(p, self.destination)

    def test_no_fake_material_to_nonmaterial(self):
        p = fixture()
        p["material_change"]["material"] = False
        with self.assertRaisesRegex(ValueError, "new_event_assessment_inconsistent"):
            export_reviewed_packet(p, self.destination)

    def test_reject_untruthful_or_unknown_reviewer_type(self):
        p = fixture()
        p["reviewer_type"] = "unknown"
        with self.assertRaisesRegex(ValueError, "reviewer_type_invalid"):
            export_reviewed_packet(p, self.destination)

    def test_reject_absent_review_notes(self):
        p = fixture()
        p["review_notes"] = []
        with self.assertRaisesRegex(ValueError, "review_notes_missing"):
            export_reviewed_packet(p, self.destination)


if __name__ == "__main__":
    unittest.main()
