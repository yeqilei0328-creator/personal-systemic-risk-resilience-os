#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
PAIRS = {
    "event": ("schemas/event.schema.json", "examples/synthetic/event.json"),
    "evidence": ("schemas/evidence.schema.json", "examples/synthetic/evidence.json"),
    "edge": ("schemas/edge.schema.json", "examples/synthetic/edge.json"),
    "scenario": ("schemas/scenario.schema.json", "examples/synthetic/scenario.json"),
    "exposure": ("schemas/exposure.schema.json", "examples/synthetic/exposure.json"),
    "capability": ("schemas/capability.schema.json", "examples/synthetic/capability.json"),
    "alert": ("schemas/alert.schema.json", "examples/synthetic/alert.json"),
    "coupling_snapshot": ("schemas/coupling-snapshot.schema.json", "examples/synthetic/coupling-snapshot.json"),
    "buffer_state": ("schemas/buffer-state.schema.json", "examples/synthetic/buffer-state.json"),
    "buffer_snapshot": ("schemas/buffer-snapshot.schema.json", "examples/synthetic/buffer-snapshot.json"),
    "edge_assessment": ("schemas/edge-assessment.schema.json", "examples/synthetic/edge-assessment.json"),
    "r_level_assessment": ("schemas/r-level-assessment.schema.json", "examples/synthetic/r-level-assessment.json"),
    "capability_audit": ("schemas/capability-audit.schema.json", "examples/synthetic/capability-audit.json"),
    "preparedness_snapshot": ("schemas/preparedness-snapshot.schema.json", "examples/synthetic/preparedness-snapshot.json"),
    "water_resilience_audit": ("schemas/water-resilience-audit.schema.json", "examples/synthetic/water-resilience-audit.json"),
    "water_verification_assessment": ("schemas/water-verification-assessment.schema.json", "examples/synthetic/water-verification-assessment.json"),
}

def load(path):
    with (ROOT / path).open("r", encoding="utf-8") as f:
        return json.load(f)

def approx_equal(left, right, tol=1e-6):
    return abs(float(left) - float(right)) <= tol

def semantic_errors(name, obj):
    errors = []
    if name == "scenario":
        p = obj["probability"]
        if p["low"] > p["high"]:
            errors.append("probability.low must be <= probability.high")
        lead = obj["lead_time"]
        if lead["min_days"] > lead["max_days"]:
            errors.append("lead_time.min_days must be <= lead_time.max_days")
    elif name == "edge":
        if obj["source_node"]["node_id"] == obj["target_node"]["node_id"]:
            errors.append("source_node and target_node must differ")
        latency = obj.get("latency_days")
        if latency and latency["min"] > latency["max"]:
            errors.append("latency_days.min must be <= latency_days.max")
        common = obj["common_cause"]
        if common["present"] and not common.get("cause_id"):
            errors.append("common_cause.cause_id is required when present=true")
    elif name == "alert" and obj["notify"]:
        if not any(obj["basis"].values()):
            errors.append("notify=true requires at least one basis reference")
    elif name == "buffer_state":
        if obj["baseline_capacity"] <= obj["minimum_viable_capacity"]:
            errors.append("baseline_capacity must be > minimum_viable_capacity")
    elif name == "coupling_snapshot":
        if not approx_equal(obj["pair_density"], obj["unique_validated_directed_pairs"] / 12):
            errors.append("pair_density inconsistent with directed pair count")
        if not approx_equal(obj["independent_pair_density"], obj["independent_validated_directed_pairs"] / 12):
            errors.append("independent_pair_density inconsistent with directed pair count")
        if not approx_equal(obj["coactivation_breadth"], obj["active_variable_count"] / 4):
            errors.append("coactivation_breadth inconsistent with active variable count")
        if obj["independent_validated_directed_pairs"] > obj["unique_validated_directed_pairs"]:
            errors.append("independent pair count cannot exceed raw pair count")
    elif name == "water_resilience_audit":
        quality = obj["quality"]
        if quality["potability_status"] in {"lab_verified", "authority_verified"}:
            if not quality.get("evidence_date") or not quality.get("evidence_ref"):
                errors.append("verified potability requires evidence_date and evidence_ref")
        if quality["consumer_sensor_only"] and quality["potability_status"] in {"lab_verified", "authority_verified"}:
            errors.append("consumer_sensor_only cannot establish verified potability")
        continuity = obj["continuity"]
        if continuity["outage_test"] == "pass":
            if not continuity.get("field_test_duration_hours") or continuity["field_test_duration_hours"] <= 0:
                errors.append("passed outage test requires positive field_test_duration_hours")
    return errors

def main():
    failures = []
    for name, (schema_path, example_path) in PAIRS.items():
        schema = load(schema_path)
        example = load(example_path)
        try:
            Draft202012Validator.check_schema(schema)
            Draft202012Validator(schema, format_checker=FormatChecker()).validate(example)
            semantic = semantic_errors(name, example)
            if semantic:
                raise ValueError("; ".join(semantic))
            print(f"PASS {name}: {example_path}")
        except Exception as exc:
            failures.append((name, str(exc)))
            print(f"FAIL {name}: {exc}")
    if failures:
        raise SystemExit(1)
    print(f"PASS all: {len(PAIRS)}/{len(PAIRS)} schemas and examples validated")

if __name__ == "__main__":
    main()
