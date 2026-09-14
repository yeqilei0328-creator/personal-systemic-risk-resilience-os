from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "governance.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"GOVERNANCE_VALIDATION_FAIL: {message}")


def main() -> None:
    data = json.loads(CONFIG.read_text(encoding="utf-8"))

    require(data["governance_version"] == "1.0.0", "unexpected governance version")
    require(data["source_of_truth"]["engineering"] == "github_main", "main must be engineering truth")
    require(data["source_of_truth"]["chat_memory_authoritative"] is False, "chat cannot be authoritative")

    authority = data["authority_router"]
    require(authority["levels"] == ["GREEN", "AMBER", "RED"], "authority levels drifted")
    require(authority["red_requires_fresh_owner_authorization"] is True, "RED must require fresh Owner authorization")
    require(authority["red_granted_not_equal_consumed"] is True, "RED granted/consumed boundary missing")
    require(authority["red_one_shot_automatic_retry"] == 0, "RED auto retry must be zero")

    radar = data["radar_router"]
    require(
        set(radar["verdicts"])
        == {
            "NO_RADAR",
            "TECH_RADAR_BLOCKER",
            "TECH_RADAR_DECISION",
            "COMMERCIAL_RADAR_DISCOVERY",
            "COMMERCIAL_RADAR_VALIDATION",
            "DUAL_RADAR_MAJOR_DECISION",
        },
        "Radar verdict contract drifted",
    )
    require(radar["authority_widened"] is False, "Radar must never widen authority")
    require(
        radar["triggered_disposition"]
        == "STOP_LOCAL_SPECULATION_ALLOW_READONLY_EVIDENCE",
        "triggered Radar must stop local speculation",
    )

    reality = data["reality_first"]
    require(reality["namespace"] == "RL", "Reality namespace must avoid R0-R5 collision")
    require(reality["levels"] == [f"RL{i}" for i in range(7)], "Reality levels drifted")
    require(reality["personal_action_namespace_reserved"] == "R0-R5", "Personal Action namespace guard missing")

    require(data["evidence"]["post_merge_verify_required"] is True, "post-merge verification is mandatory")

    missing = [path for path in data["required_docs"] if not (ROOT / path).exists()]
    require(not missing, f"required governance docs missing: {missing}")

    print("GOVERNANCE_VALIDATION_PASS")
    print(f"required_docs={len(data['required_docs'])}")
    print(f"radar_verdicts={len(radar['verdicts'])}")
    print(f"reality_levels={len(reality['levels'])}")


if __name__ == "__main__":
    main()