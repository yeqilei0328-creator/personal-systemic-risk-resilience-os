"""WI-MACRO03 narrow official macro one-shot validation (synthetic text only)."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import unittest

from src.psrro.intelligence_reviewed_macro_gap import (
    _SPEC_PATH, _acquisition_receipt, _one_source_numeric,
    _revision_proof, _verified_coverage, _utc, export_r1_macro_gap_once,
)


class R1Macro03Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config=json.loads(_SPEC_PATH.read_text(encoding="utf-8"))
        cls.lookup={s["source_id"]:s for s in cls.config["sources"]}

    def metric(self,name,index=0):
        return copy.deepcopy(self.lookup[name]["values"][index])

    def test_exactly_ten_official_urls_and_nine_missing_macro_candidates(self):
        self.assertEqual(len(self.config["sources"]),10)
        self.assertEqual(len(set(x["url"] for x in self.config["sources"])),10)
        metrics=[copy.deepcopy(v) for row in self.config["sources"] if not row["source_id"].startswith("gdp") for v in row["values"]]
        self.assertEqual(len(metrics),9)
        self.assertEqual(_verified_coverage(metrics)["not_provided_primary_id"],"cn.credit.afre_stock.yoy")

    def test_original_monthly_yoy_cpi_anchor_pass(self):
        _one_source_numeric("2026年10月份，全国居民消费价格同比上涨0.7%。",self.metric("cpi_202610"))

    def test_original_ytd_negative_fai_anchor_pass(self):
        _one_source_numeric("1—9月份，全国固定资产投资（不含农户）334115亿元，同比下降7.2%。",self.metric("fai_2026ytd09"))

    def test_ytd_negative_direction_not_a_positive_yoy(self):
        m=self.metric("fai_2026ytd09")
        m["negative_claim"]=False
        with self.assertRaisesRegex(ValueError,"source_number_or_negative_direction_changed"):
            _one_source_numeric("1—9月份，全国固定资产投资（不含农户）334115亿元，同比下降7.2%。",m)

    def test_ytd_month_not_interchangeable(self):
        m=self.metric("fai_2026ytd09")
        m["statistical_period_start"]="2026-09-01"
        with self.assertRaisesRegex(ValueError,"ytd_period_misrepresented"):
            _one_source_numeric("1—9月份，全国固定资产投资（不含农户）334115亿元，同比下降7.2%。",m)

    def test_yoy_not_level(self):
        m=self.metric("cpi_202610")
        m["measure"]="LEVEL"
        with self.assertRaisesRegex(ValueError,"yoy_grain_or_unit_invalid"):
            _one_source_numeric("2026年10月份，全国居民消费价格同比上涨0.7%。",m)

    def test_wrong_value_or_missing_anchored_text_denied(self):
        with self.assertRaisesRegex(ValueError,"original_contextual_numeric_anchor_missing"):
            _one_source_numeric("2026年10月份，工业生产者出厂价格上涨0.7%。",self.metric("cpi_202610"))

    def test_gdp_preliminary_nominal_level_primary(self):
        _one_source_numeric("2024年四季度和全年GDP初步核算数据 GDP 373726 1349084 5.4 5.0",self.metric("gdp2024_initial"))

    def test_gdp_final_explicit_revision_acknowledgement_required(self):
        _one_source_numeric("经最终核实，2024年，GDP现价总量为1348066亿元，比初步核算数减少1018亿元；",self.metric("gdp2024_final"))
        with self.assertRaisesRegex(ValueError,"original_contextual_numeric_anchor_missing"):
            _one_source_numeric("GDP现价总量为1348066亿元。",self.metric("gdp2024_final"))

    def test_actual_same_period_revision_delta(self):
        a=self.metric("gdp2024_initial")
        b=self.metric("gdp2024_final")
        p=_revision_proof(a,b)
        self.assertEqual(p["official_declared_revision_delta"],"-1018")
        self.assertEqual(p["initial_value"],"1349084")
        self.assertEqual(p["official_final_value"],"1348066")
        self.assertFalse(p["original_first_release_bytes_at_historical_time_attested"])
        self.assertTrue(p["not_a_pmi_revision"])

    def test_gdp_other_grain_rejected_as_revision(self):
        a=self.metric("gdp2024_initial")
        b=self.metric("gdp2024_final")
        b["statistical_period_start"]="2025-01-01"
        with self.assertRaisesRegex(ValueError,"official_gdp_revision_grain_or_values_invalid"):
            _revision_proof(a,b)

    def test_gdp_no_fabricated_revision(self):
        a=self.metric("gdp2024_initial")
        b=self.metric("gdp2024_final")
        b["value"]="1349084"
        with self.assertRaisesRegex(ValueError,"official_gdp_revision_grain_or_values_invalid"):
            _revision_proof(a,b)

    def test_missing_core_metric_refuses_nine_claim(self):
        rows=[copy.deepcopy(v) for row in self.config["sources"] if not row["source_id"].startswith("gdp") for v in row["values"]]
        rows.pop()
        with self.assertRaisesRegex(ValueError,"nine_original_macro_metric_ids_required"):
            _verified_coverage(rows)

    def test_duplicate_core_metric_refuses_coverage(self):
        rows=[copy.deepcopy(v) for row in self.config["sources"] if not row["source_id"].startswith("gdp") for v in row["values"]]
        rows[-1]=rows[0]
        with self.assertRaisesRegex(ValueError,"nine_original_macro_metric_ids_required"):
            _verified_coverage(rows)

    def test_acquisition_receipt_http_and_sha(self):
        raw=b'example synthetic official source'
        h=hashlib.sha256(raw).hexdigest()
        spec={"source_id":"cpi_202610","url":"https://www.stats.gov.cn/synthetic","source_original_sha256":h}
        receipt={"source_id":"cpi_202610","url":spec["url"],"exit_code":0,
                 "http_response":f"200 {len(raw)} {spec['url']} text/html",
                 "sha256":h,"length":len(raw),"local_observed_at_utc":"2026-11-10T02:00:00+00:00"}
        self.assertEqual(_acquisition_receipt(receipt,spec,raw),"2026-11-10T02:00:00+00:00")
        receipt["http_response"]=f"403 {len(raw)} {spec['url']} text/html"
        with self.assertRaisesRegex(ValueError,"source_http_outcome_or_redirect_invalid"):
            _acquisition_receipt(receipt,spec,raw)

    def test_forbid_implicit_past_asof_from_current_source(self):
        with self.assertRaisesRegex(ValueError,"unexpected_retrieval_day_for_frozen_one_shot_scope"):
            raw=b'raw'
            spec={"source_id":"s","url":"https://www.stats.gov.cn/s","source_original_sha256":hashlib.sha256(raw).hexdigest()}
            rec={"source_id":"s","url":spec["url"],"exit_code":0,"http_response":f"200 3 {spec['url']} text/html",
                 "sha256":spec["source_original_sha256"],"length":3,
                 "local_observed_at_utc":"2025-01-18T00:00:00Z"}
            _acquisition_receipt(rec,spec,raw)

    def test_timezone_required(self):
        with self.assertRaisesRegex(ValueError,"source_timezone_missing"):
            _utc("2026-11-10T01:00:00")

    def test_only_fresh_scratch_output(self):
        with self.assertRaisesRegex(ValueError,"must_output_into_new_isolated_scratch_only"):
            export_r1_macro_gap_once(Path("/tmp/does-not-matter"),Path.home()/"not-allowed-macro03")


if __name__=="__main__":
    unittest.main()
