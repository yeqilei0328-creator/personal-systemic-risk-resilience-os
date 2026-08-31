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
}

def load(path):
    with (ROOT / path).open("r", encoding="utf-8") as f:
        return json.load(f)

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
