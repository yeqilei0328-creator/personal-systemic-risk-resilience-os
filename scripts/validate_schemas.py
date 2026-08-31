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

def main():
    failures = []
    for name, (schema_path, example_path) in PAIRS.items():
        schema = load(schema_path)
        example = load(example_path)
        try:
            Draft202012Validator.check_schema(schema)
            Draft202012Validator(schema, format_checker=FormatChecker()).validate(example)
            print(f"PASS {name}: {example_path}")
        except Exception as exc:
            failures.append((name, str(exc)))
            print(f"FAIL {name}: {exc}")
    if failures:
        raise SystemExit(1)
    print(f"PASS all: {len(PAIRS)}/{len(PAIRS)} schemas and examples validated")

if __name__ == "__main__":
    main()
