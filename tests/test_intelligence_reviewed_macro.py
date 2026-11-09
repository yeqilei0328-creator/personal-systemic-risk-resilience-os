"""PSRRO WI-MACRO01: no-network single-reviewed NBS-PMI proof tests."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tests.test_intelligence_reviewed_export import fixture
from src.psrro.intelligence_reviewed_export import export_reviewed_packet
from src.psrro.intelligence_reviewed_macro import prepare_reviewed_macro, export_reviewed_macro_once

_URL = "https://www.stats.gov.cn/sj/zxfbhjd/202610/t20261031_1965718.html"
_HTML = ("<html><title>2026年10月中国采购经理指数运行情况</title>"
         "<body><div>2026/10/31 09:30</div>"
         "<p>10月份，制造业采购经理指数（PMI）为49.3%</p></body></html>")


class MacroOneShotTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.html = self.root / "original.html"
        self.html.write_text(_HTML, encoding="utf-8")
        self.native = self.root / "native"
        self.output = self.root / "macro-output"
        self.packet = fixture()
        p = self.packet
        p["reviewed_at"] = "2026-11-09T16:00:00Z"
        e = p["event_state"]
        e["domain"] = "macro"
        e["first_seen"] = "2026-11-09T14:00:00Z"
        e["last_updated"] = "2026-11-09T14:00:00Z"
        c = p["claims"][0]
        c["claim_kind"] = "quantity"
        c["last_updated"] = "2026-11-09T14:00:00Z"
        c["grade_updated_at"] = "2026-11-09T14:00:00Z"
        s = p["source_observations"][0]
        s["retrieved_at"] = "2026-11-09T14:00:00Z"
        s["published_at"] = None
        s["access_status"] = "full_access"
        s["source_role"] = "original_document"
        s["lineage"]["relation"] = "original"
        s["provenance"]["source_locator"] = _URL
        s["provenance"]["full_text_verified"] = True
        s["provenance"]["primary_material_accessed"] = True
        a = p["material_change"]
        a["assessed_at"] = "2026-11-09T15:00:00Z"
        export_reviewed_packet(p, self.native)

    def run_prep(self):
        return prepare_reviewed_macro(
            self.packet, self.native, self.html, method_commit="a"*40,
        )

    def test_actual_original_bytes_normalization_and_correct_period(self):
        record = self.run_prep()
        self.assertEqual(record["indicator_id"], "cn.pmi.manufacturing")
        self.assertEqual(record["value"], "49.3")
        self.assertEqual(record["unit"], "percent")
        self.assertEqual(record["measure"], "LEVEL")
        self.assertEqual(record["statistical_period_end"], "2026-10-31")
        self.assertEqual(record["source_bytes_sha256"], hashlib.sha256(self.html.read_bytes()).hexdigest())
        self.assertEqual(record["reviewer_identity_attestation"], "DECLARED_NOT_INDEPENDENTLY_ATTESTED")
        self.assertFalse(record["original_release_time_independently_attested"])
        self.assertIsNone(record["verified_historical_availability_timestamp"])

    def test_wrong_value_from_different_raw_bytes_denied(self):
        self.html.write_text(_HTML.replace("49.3%", "49.4%"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "official_value_changed_from"):
            self.run_prep()

    def test_missing_title_denied(self):
        self.html.write_text(_HTML.replace("2026年10月中国采购经理指数运行情况", "random blog"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "official_primary_value_or_release"):
            self.run_prep()

    def test_missing_release_date_denied(self):
        self.html.write_text(_HTML.replace("2026/10/31", "2026/11/02"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "official_primary_value_or_release"):
            self.run_prep()

    def test_fake_primary_url_denied(self):
        self.packet["source_observations"][0]["provenance"]["source_locator"] = "https://example.org/repost"
        with self.assertRaisesRegex(ValueError, "official_primary_reviewed_source"):
            self.run_prep()

    def test_unverified_full_text_not_admitted(self):
        self.packet["source_observations"][0]["provenance"]["full_text_verified"] = False
        with self.assertRaisesRegex(ValueError, "official_primary_reviewed_source"):
            self.run_prep()

    def test_invented_precise_publisher_clock_denied(self):
        self.packet["source_observations"][0]["published_at"] = "2026-10-31T01:30:00Z"
        with self.assertRaisesRegex(ValueError, "unverified_exact_publication_time"):
            self.run_prep()

    def test_tampered_psrro_native_claim_denied_even_with_same_manifest(self):
        f = next((self.native / "claims").glob("*.json"))
        f.write_text(f.read_text().replace('"fact"', '"opinion"'), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "native_artifact_hash_mismatch"):
            self.run_prep()

    def test_symlink_original_file_denied(self):
        alias = self.root / "alias.html"
        alias.symlink_to(self.html)
        with self.assertRaisesRegex(ValueError, "source_html_file_size_or_symlink"):
            prepare_reviewed_macro(self.packet, self.native, alias, method_commit="b"*40)

    def test_export_is_one_shot_and_cannot_overwrite(self):
        with patch("src.psrro.intelligence_reviewed_macro._get_current_method_commit", return_value="a"*40):
            first = export_reviewed_macro_once(self.packet, self.native, self.html, self.output)
            self.assertEqual(first["status"], "R1_REVIEWED_MACRO_ONE_SHOT_EXPORTED")
            result = json.loads((self.output/"reviewed-macro.json").read_text())
            self.assertEqual(result["native_claim_id"], self.packet["claims"][0]["claim_id"])
            self.assertEqual(first["record_sha256"], hashlib.sha256((self.output/"reviewed-macro.json").read_bytes()).hexdigest())
            with self.assertRaisesRegex(ValueError, "fresh_scratch_root_required"):
                export_reviewed_macro_once(self.packet, self.native, self.html, self.output)

    def test_prevents_non_tmp_output(self):
        with self.assertRaisesRegex(ValueError, "fresh_scratch_root_required"):
            export_reviewed_macro_once(self.packet, self.native, self.html, Path.home()/"bad-r1-macro-output")

    def test_same_source_same_period_has_stable_review_projection(self):
        self.assertEqual(self.run_prep(), self.run_prep())


if __name__ == "__main__":
    unittest.main()
