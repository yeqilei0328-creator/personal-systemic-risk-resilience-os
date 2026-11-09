#!/usr/bin/env python3
"""PSRRO offline one-shot NBS October 2026 PMI reviewer-backed macro export.

Requires an existing PSRRO reviewed PUBLIC native event/Claim/Source bundle
and a previously obtained original HTML file. Does not make HTTP requests.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from psrro.intelligence_reviewed_export import read_packet
from psrro.intelligence_reviewed_macro import export_reviewed_macro_once


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--reviewed-event-packet", type=Path, required=True)
    p.add_argument("--existing-native-root", type=Path, required=True)
    p.add_argument("--original-html", type=Path, required=True)
    p.add_argument("--scratch-output-root", type=Path, required=True)
    a = p.parse_args()
    try:
        packet = read_packet(a.reviewed_event_packet)
        out = export_reviewed_macro_once(
            packet, a.existing_native_root, a.original_html, a.scratch_output_root
        )
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(json.dumps({"status": "FAIL_CLOSED", "reason": str(exc)}, sort_keys=True, ensure_ascii=False))
        return 2
    print(json.dumps(out, sort_keys=True, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
