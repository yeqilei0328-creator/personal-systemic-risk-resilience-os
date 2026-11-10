"""Synthetic PBOC fixed one-shot source review negative controls."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from src.psrro.intelligence_reviewed_pboc_afre import (
    parse_pboc_original,build_pboc_afre_once,export_pboc_afre_once,
    PBOC_AFRE_URL,PBOC_SOURCE_SHA256,
)


def sample(
    stock="468.17", yoy="7.1", september="2026.9",
    october_stock="", october_yoy="",
):
    headers=[""]+[f"2026.{i}" for i in range(1,13)]+[""]
    headers[9]=september
    values=["社会融资规模存量 AFRE(stock)"]+["449.11","8.2"]*7+[
        "464.80","7.2",stock,yoy,october_stock,october_yoy,"","","","",""]
    assert len(headers)==14
    assert len(values)==26
    def tr(items):
        return "<tr>"+"".join("<td>"+x+"</td>" for x in items)+"</tr>"
    s=("<html><head><meta charset=gb2312></head><body>"
       "<p>社会融资规模存量统计表 单位：万亿元人民币 增速（%）</p>"
       "<table>"+tr(headers)+tr(values)+"</table></body></html>")
    return s.encode("gb18030")


class PBOCAFRETests(unittest.TestCase):
    def test_exact_sept_afre_and_aug_control(self):
        v=parse_pboc_original(sample())
        self.assertEqual(v["indicator_id"],"cn.credit.afre_stock.yoy")
        self.assertEqual((v["stock_amount"],v["value"]),("468.17","7.1"))
        self.assertEqual(v["previous_month_yoy"],"7.2")
        self.assertFalse(v["october_column_nonempty"])
        self.assertEqual((v["period_mode"],v["measure"]),("STOCK","YOY"))

    def test_september_growth_7_2_is_not_7_1(self):
        with self.assertRaisesRegex(ValueError,"growth_or_oct_future_empty_changed"):
            parse_pboc_original(sample(yoy="7.2"))

    def test_stock_is_not_growth(self):
        with self.assertRaisesRegex(ValueError,"growth_or_oct_future_empty_changed"):
            parse_pboc_original(sample(stock="7.1",yoy="468.17"))

    def test_2025_worksheet_refused(self):
        with self.assertRaisesRegex(ValueError,"official_title_year_or_table_missing"):
            parse_pboc_original(sample().replace(b"2026.9",b"2025.9"))

    def test_missing_month_header_denied(self):
        with self.assertRaisesRegex(ValueError,"official_title_year_or_table_missing|unique_year_header_and_afre_stock_row_required"):
            parse_pboc_original(sample(september="2026.8"))

    def test_future_month_10_fabrication_denied(self):
        with self.assertRaisesRegex(ValueError,"growth_or_oct_future_empty_changed"):
            parse_pboc_original(sample(october_stock="470.00",october_yoy="7.0"))

    def test_inconsistent_aug_guard_denied(self):
        with self.assertRaisesRegex(ValueError,"growth_or_oct_future_empty_changed"):
            parse_pboc_original(sample().replace(b"464.80",b"464.81"))

    def test_unrelated_not_stock_denied(self):
        with self.assertRaisesRegex(ValueError,"official_title_year_or_table_missing|unique_year_header_and_afre_stock_row_required"):
            parse_pboc_original(sample().replace(b"AFRE(stock)",b"AFRE(flow)"))

    def test_invalid_encoding_denied(self):
        with self.assertRaisesRegex(ValueError,"pboc_original_encoding_invalid"):
            parse_pboc_original(b"\x81")

    def test_disallow_wrong_raw_file_sha_even_if_numeric_valid(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            html=root/"source.html";html.write_bytes(sample())
            with self.assertRaisesRegex(ValueError,"original_bytes_hash_or_length_changed"):
                build_pboc_afre_once(html=html,reviewed_packet=root/"fake-packet.json",
                    native_root=root/"missing",source_receipt=root/"receipt.json",
                    producer_method_commit="a"*40)

    def test_disallow_non_scratch_output(self):
        with self.assertRaisesRegex(ValueError,"only_fresh_official_scratch_output_permitted"):
            export_pboc_afre_once(Path.home()/"not-allowed",html=Path("/not-there"),
                                  reviewed_packet=Path("/not-there"),native_root=Path("/not-there"),
                                  source_receipt=Path("/not-there"))

    def test_official_source_link_is_strict_2026_pbc(self):
        self.assertEqual(PBOC_AFRE_URL,
            "https://www.pbc.gov.cn/diaochatongjisi/attachDir/2026/10/2026101417444554195.htm")
        self.assertRegex(PBOC_SOURCE_SHA256,"^[0-9a-f]{64}$")


if __name__=="__main__":
    unittest.main()
