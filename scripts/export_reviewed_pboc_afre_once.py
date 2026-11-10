#!/usr/bin/env python3
"""One-off PBOC 2026 September stock-growth first-party original export.

No HTTP, login, source polling, persistent source database or production write.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from psrro.intelligence_reviewed_pboc_afre import export_pboc_afre_once


def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--official-original-html",required=True,type=Path)
    p.add_argument("--reviewed-packet",required=True,type=Path)
    p.add_argument("--native-root",required=True,type=Path)
    p.add_argument("--source-receipt",required=True,type=Path)
    p.add_argument("--new-output",required=True,type=Path)
    a=p.parse_args()
    try:
        r=export_pboc_afre_once(
            a.new_output,
            html=a.official_original_html,
            reviewed_packet=a.reviewed_packet,
            native_root=a.native_root,
            source_receipt=a.source_receipt,
        )
    except (ValueError,TypeError,KeyError,IndexError,OSError) as exc:
        print(json.dumps({"status":"FAIL_CLOSED","reason":str(exc)},ensure_ascii=False))
        return 2
    print(json.dumps(r,ensure_ascii=False,indent=2,sort_keys=True))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
