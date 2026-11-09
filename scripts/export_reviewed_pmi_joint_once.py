#!/usr/bin/env python3
"""Bounded R1-only offline cross-edition PMI proof. No HTTP or state writes."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from psrro.intelligence_reviewed_export import read_packet
from psrro.intelligence_reviewed_pmi_joint import export_pmi_joint_once


def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    for key in ("september_packet","september_native_root","september_html",
                "october_packet","october_native_root","october_html",
                "october_g1_record","october_g1_sha256","destination"):
        p.add_argument("--"+key.replace("_","-"),required=True)
    args=p.parse_args()
    try:
        result=export_pmi_joint_once(
            september_packet=read_packet(Path(args.september_packet)),
            september_native_root=Path(args.september_native_root),
            september_html=Path(args.september_html),
            october_packet=read_packet(Path(args.october_packet)),
            october_native_root=Path(args.october_native_root),
            october_html=Path(args.october_html),
            october_g1_record=json.loads(Path(args.october_g1_record).read_text(encoding="utf-8")),
            october_g1_sha256=args.october_g1_sha256,
            destination=Path(args.destination),
        )
    except (ValueError,TypeError,KeyError,OSError) as exc:
        print(json.dumps({"status":"FAIL_CLOSED","reason":str(exc)},ensure_ascii=False,sort_keys=True))
        return 2
    print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
