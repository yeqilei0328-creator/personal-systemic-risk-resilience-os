#!/usr/bin/env python3
"""Owner-scoped PUBLIC R1 source gap proof from ten local official HTML originals.

The original R1 HTTPS acquisition has already completed in scratch.
This command never performs HTTP, uses no credentials and cannot write
to the official source stores, PRIVATE repository or forecasting state.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from psrro.intelligence_reviewed_macro_gap import export_r1_macro_gap_once


def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--existing-official-scratch",type=Path,required=True)
    p.add_argument("--new-output-scratch",type=Path,required=True)
    a=p.parse_args()
    try:
        result=export_r1_macro_gap_once(a.existing_official_scratch,a.new_output_scratch)
    except (ValueError,TypeError,KeyError,IndexError,OSError) as exc:
        print(json.dumps({"status":"FAIL_CLOSED","reason":str(exc)},ensure_ascii=False,sort_keys=True))
        return 2
    print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
