"""Two primary NBS document shapes: synthetic R1 joint-proof tests only."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tests.test_intelligence_reviewed_export import fixture
from src.psrro.intelligence_events import event_fingerprint
from src.psrro.intelligence_reviewed_export import export_reviewed_packet
from src.psrro.intelligence_reviewed_macro import prepare_reviewed_macro
from src.psrro.intelligence_reviewed_pmi_joint import (
    build_pmi_joint, export_pmi_joint_once, OCT_ORIGINAL_METHOD, SEPT_URL, OCT_URL,
)

SEPT_HTML = (
    "<html><title>2026年9月中国采购经理指数运行情况</title>"
    "<body><div>发布时间：2026-09-30 09:30</div>"
    "<p>9月份，制造业采购经理指数（PMI）为50.1%</p>"
    "<p>生产指数为51.7%</p><p>新订单指数为50.5%</p>"
    "<div>2026年9月 50.1 51.7 50.5</div></body></html>"
)
OCT_HTML = (
    "<html><title>2026年10月中国采购经理指数运行情况</title>"
    "<body><div>2026/10/31 09:30</div>"
    "<p>10月份，制造业采购经理指数（PMI）为49.3%</p>"
    "<p>大型企业PMI为50.2%</p>"
    "<p>生产指数为49.8%</p><p>新订单指数为49.4%</p>"
    "<div>2026年9月 50.1 51.7 50.5</div>"
    "<div>2026年10月 49.3 49.8 49.4</div></body></html>"
)


def reviewed_packet(period: str):
    x=fixture()
    is_sep=period=="2026-09"
    val,orders=("50.1","50.5") if is_sep else ("49.3","49.4")
    url=SEPT_URL if is_sep else OCT_URL
    viewed="2026-11-09T14:21:00Z"
    x["reviewed_at"]="2026-11-09T15:01:00Z"
    ev=x["event_state"]
    ev["domain"]="macro"
    ev["first_seen"]=viewed
    ev["last_updated"]=viewed
    ev["fingerprint_basis"]={
        "actors":["NBS"],"actions":["publish manufacturing PMI"],
        "objects":[period+" manufacturing PMI"],"locations":["CN"],
        "time_window_key":period,"consequences":[],
    }
    ev["fingerprint"]=event_fingerprint(ev["fingerprint_basis"])
    c=x["claims"][0]
    c["claim_kind"]="quantity"
    c["status"]="accepted"
    c["claim_grade"]="B"
    c["statement"]="NBS "+period+" manufacturing PMI "+val+"% and new orders "+orders+"%."
    c["last_updated"]=viewed
    c["grade_updated_at"]=viewed
    src=x["source_observations"][0]
    src["retrieved_at"]=viewed
    src["published_at"]=None
    src["access_status"]="full_access"
    src["source_role"]="original_document"
    src["provenance"]["source_locator"]=url
    src["provenance"]["full_text_verified"]=True
    src["provenance"]["primary_material_accessed"]=True
    src["lineage"]["relation"]="original"
    src["lineage"]["independence_group_id"]="ind-nbs-"+period
    x["material_change"]["assessed_at"]="2026-11-09T14:45:00Z"
    return x


class ReviewedPMIJointTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        root=Path(self.t.name)
        self.sept_html=root/"sep.html"
        self.oct_html=root/"oct.html"
        self.sept_html.write_text(SEPT_HTML,encoding="utf-8")
        self.oct_html.write_text(OCT_HTML,encoding="utf-8")
        self.sept_packet=reviewed_packet("2026-09")
        self.oct_packet=reviewed_packet("2026-10")
        self.sept_native=root/"sept-native"
        self.oct_native=root/"oct-native"
        export_reviewed_packet(self.sept_packet,self.sept_native)
        export_reviewed_packet(self.oct_packet,self.oct_native)
        self.oct_record=prepare_reviewed_macro(
            self.oct_packet,self.oct_native,self.oct_html,
            method_commit=OCT_ORIGINAL_METHOD,
        )
        self.oct_sha=hashlib.sha256(
            (json.dumps(self.oct_record,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode("utf-8")
        ).hexdigest()
        self.destination=root/"joint-out"

    def run_joint(self):
        return build_pmi_joint(
            september_packet=self.sept_packet,
            september_native_root=self.sept_native,
            september_html=self.sept_html,
            october_packet=self.oct_packet,
            october_native_root=self.oct_native,
            october_html=self.oct_html,
            october_g1_record=self.oct_record,
            october_g1_sha256=self.oct_sha,
            producer_method_commit="a"*40,
        )

    def test_two_original_editions_and_business_boundary(self):
        out=self.run_joint()
        self.assertEqual(out["sources"][0]["pmi"],"50.1")
        self.assertEqual(out["sources"][1]["pmi"],"49.3")
        self.assertEqual(out["sources"][0]["new_orders"],"50.5")
        self.assertEqual(out["sources"][1]["new_orders"],"49.4")
        self.assertEqual(out["descriptive_deltas_pp"]["manufacturing_pmi"],"-0.8")
        self.assertEqual(out["descriptive_deltas_pp"]["new_orders"],"-1.1")
        self.assertTrue(out["same_period_202609_cross_editions"]["reported_values_match"])
        self.assertFalse(out["same_period_202609_cross_editions"]["historical_original_release_bytes_at_publication_time_attested"])
        self.assertEqual(out["historical_revision_lineage"],"NOT_ATTESTED")
        self.assertIsNone(out["authoritative_macro_cycle_stage"])
        self.assertEqual(out["chain_h_causality"],"UNKNOWN")
        self.assertEqual(out["source_fetches_by_exporter"],0)

    def test_repeat_is_deterministic(self):
        self.assertEqual(self.run_joint(),self.run_joint())

    def test_september_primary_value_mismatch_rejected(self):
        self.sept_html.write_text(SEPT_HTML.replace("50.1%","50.2%"))
        with self.assertRaisesRegex(ValueError,"official_value_changed_from"):
            self.run_joint()

    def test_october_orders_mismatch_rejected(self):
        self.oct_html.write_text(OCT_HTML.replace("49.4%","49.3%"))
        with self.assertRaisesRegex(ValueError,"official_value_changed_from"):
            self.run_joint()

    def test_later_report_must_show_prior_september_row(self):
        self.oct_html.write_text(OCT_HTML.replace("2026年9月 50.1 51.7 50.5","2026年9月 50.2 51.7 50.5"))
        with self.assertRaisesRegex(ValueError,"prior_october_g1_record_and_original_bytes_conflict|later_release_does_not_match_prior_month_table"):
            self.run_joint()

    def test_same_source_identity_disallowed(self):
        self.sept_packet["source_observations"][0]["provenance"]["source_locator"]=OCT_URL
        with self.assertRaisesRegex(ValueError,"native_manifest_proof_mismatch|native_original_source_contract_invalid"):
            self.run_joint()

    def test_corrupt_psrro_native_manifest_hash_denied(self):
        path=next((self.sept_native/"claims").glob("*.json"))
        path.write_text(path.read_text().replace('"fact"','"opinion"'))
        with self.assertRaisesRegex(ValueError,"native_artifact_hash_mismatch"):
            self.run_joint()

    def test_fabricated_published_at_denied(self):
        self.sept_packet["source_observations"][0]["published_at"]="2026-09-30T01:30:00Z"
        with self.assertRaisesRegex(ValueError,"native_manifest_proof_mismatch"):
            self.run_joint()

    def test_october_previous_g1_method_or_value_rejected(self):
        self.oct_record["value"]="49.4"
        self.oct_sha=hashlib.sha256((json.dumps(self.oct_record,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode()).hexdigest()
        with self.assertRaisesRegex(ValueError,"prior_october_g1_record_and_original_bytes_conflict"):
            self.run_joint()

    def test_export_one_shot_and_no_replacement(self):
        params=dict(
            september_packet=self.sept_packet,september_native_root=self.sept_native,
            september_html=self.sept_html,october_packet=self.oct_packet,
            october_native_root=self.oct_native,october_html=self.oct_html,
            october_g1_record=self.oct_record,october_g1_sha256=self.oct_sha,
            destination=self.destination,
        )
        with patch("src.psrro.intelligence_reviewed_pmi_joint._get_current_method_commit",return_value="a"*40):
            v=export_pmi_joint_once(**params)
            self.assertEqual(v["status"],"R1_REVIEWED_PMI_TWO_EDITION_SNAPSHOT_EXPORTED")
            f=self.destination/"reviewed-pmi-joint.json"
            self.assertEqual(hashlib.sha256(f.read_bytes()).hexdigest(),v["record_sha256"])
            with self.assertRaisesRegex(ValueError,"fresh_tmp_output_only"):
                export_pmi_joint_once(**params)

    def test_non_tmp_output_denied(self):
        with self.assertRaisesRegex(ValueError,"fresh_tmp_output_only"):
            export_pmi_joint_once(destination=Path.home()/"pmi-joint-not-allowed")


if __name__=="__main__":
    unittest.main()
