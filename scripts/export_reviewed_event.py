#!/usr/bin/env python3
"""Export a human-reviewed, PUBLIC-safe event packet into fresh PSRRO native scratch files.

No network access, no private source state, no scheduling, no notifications.
Requires the repository's existing dev dependency: jsonschema.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from psrro.intelligence_reviewed_export import export_reviewed_packet, read_packet


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--scratch-output-root", type=Path, required=True)
    args = parser.parse_args()
    try:
        packet = read_packet(args.packet)
        result = export_reviewed_packet(packet, args.scratch_output_root)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "FAIL_CLOSED", "reason": str(exc)}, ensure_ascii=False, sort_keys=True))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
