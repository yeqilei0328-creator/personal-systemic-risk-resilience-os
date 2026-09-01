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
    "energy_resilience_audit": ("schemas/energy-resilience-audit.schema.json", "examples/synthetic/energy-resilience-audit.json"),
    "energy_verification_assessment": ("schemas/energy-verification-assessment.schema.json", "examples/synthetic/energy-verification-assessment.json"),
    "source_registry_record": ("schemas/source-registry-record.schema.json", "examples/synthetic/source-registry-record.json"),
    "source_observation": ("schemas/source-observation.schema.json", "examples/synthetic/source-observation.json"),
    "source_reputation_record": ("schemas/source-reputation-record.schema.json", "examples/synthetic/source-reputation-record.json"),
    "source_concentration_assessment": ("schemas/source-concentration-assessment.schema.json", "examples/synthetic/source-concentration-assessment.json"),
    "event_state_record": ("schemas/event-state-record.schema.json", "examples/synthetic/event-state-record.json"),
    "claim_record": ("schemas/claim-record.schema.json", "examples/synthetic/claim-record.json"),
    "claim_value_observation": ("schemas/claim-value-observation.schema.json", "examples/synthetic/claim-value-observation.json"),
    "material_change_assessment": ("schemas/material-change-assessment.schema.json", "examples/synthetic/material-change-assessment.json"),
    "behavior_signal": ("schemas/behavior-signal.schema.json", "examples/synthetic/behavior-signal.json"),
    "costly_signal_assessment": ("schemas/costly-signal-assessment.schema.json", "examples/synthetic/costly-signal-assessment.json"),
    "rhetoric_action_gap": ("schemas/rhetoric-action-gap.schema.json", "examples/synthetic/rhetoric-action-gap.json"),
    "narrative_gap": ("schemas/narrative-gap.schema.json", "examples/synthetic/narrative-gap.json"),
    "hypothesis_assessment": ("schemas/hypothesis-assessment.schema.json", "examples/synthetic/hypothesis-assessment.json"),
    "structural_delta": ("schemas/structural-delta.schema.json", "examples/synthetic/structural-delta.json"),
    "intelligence_output_candidate": ("schemas/intelligence-output-candidate.schema.json", "examples/synthetic/intelligence-output-candidate.json"),
    "intelligence_output_gate_context": ("schemas/intelligence-output-gate-context.schema.json", "examples/synthetic/intelligence-output-gate-context.json"),
    "intelligence_output_decision": ("schemas/intelligence-output-decision.schema.json", "examples/synthetic/intelligence-output-decision.json"),
    "judgment_ledger_record": ("schemas/judgment-ledger-record.schema.json", "examples/synthetic/judgment-ledger-record.json"),
    "judgment_outcome_record": ("schemas/judgment-outcome-record.schema.json", "examples/synthetic/judgment-outcome-record.json"),
    "posterior_revision": ("schemas/posterior-revision.schema.json", "examples/synthetic/posterior-revision.json"),
    "alert_history_record": ("schemas/alert-history-record.schema.json", "examples/synthetic/alert-history-record.json"),
    "judgment_calibration_summary": ("schemas/judgment-calibration-summary.schema.json", "examples/synthetic/judgment-calibration-summary.json"),
    "chain_definition": ("schemas/chain-definition.schema.json", "chains/climate-food-energy-inflation-ai.json"),
    "chain_link_assessment": ("schemas/chain-link-assessment.schema.json", "examples/synthetic/chain-link-assessment.json"),
    "chain_watch_snapshot": ("schemas/chain-watch-snapshot.schema.json", "examples/synthetic/chain-watch-snapshot.json"),
    "replay_step_result": ("schemas/replay-step-result.schema.json", "examples/synthetic/replay-step-result.json"),
    "replay_suite_summary": ("schemas/replay-suite-summary.schema.json", "examples/synthetic/replay-suite-summary.json"),
    "communications_resilience_audit": ("schemas/communications-resilience-audit.schema.json", "examples/synthetic/communications-resilience-audit.json"),
    "communications_verification_assessment": ("schemas/communications-verification-assessment.schema.json", "examples/synthetic/communications-verification-assessment.json"),
    "food_resilience_audit": ("schemas/food-resilience-audit.schema.json", "examples/synthetic/food-resilience-audit.json"),
    "food_verification_assessment": ("schemas/food-verification-assessment.schema.json", "examples/synthetic/food-verification-assessment.json"),
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
    elif name == "energy_resilience_audit":
        storage = obj["storage"]
        if storage["nameplate_kwh"] is not None and storage["usable_kwh"] is not None:
            if storage["usable_kwh"] > storage["nameplate_kwh"]:
                errors.append("usable battery kWh cannot exceed nameplate kWh")
        if storage["battery_present"] is False:
            if any(storage[key] is not None for key in ("nameplate_kwh", "usable_kwh", "max_continuous_output_kw")):
                errors.append("battery_present=false conflicts with battery capacity values")
        generation = obj["generation"]
        if generation["pv_present"] is False and (
            generation["pv_nameplate_kwp"] is not None or generation["pv_measured_peak_kw"] is not None
        ):
            errors.append("pv_present=false conflicts with PV capacity values")
        if generation["generator_present"] is False and (
            generation["generator_rated_kw"] is not None or generation["generator_measured_runtime_hours"] is not None
        ):
            errors.append("generator_present=false conflicts with generator values")
        outage = obj["outage_test"]
        if outage["status"] == "pass":
            if not outage.get("duration_hours") or outage["duration_hours"] <= 0:
                errors.append("passed outage test requires positive duration_hours")
    elif name == "source_observation":
        if obj["provenance"]["full_text_verified"] and obj["access_status"] != "full_access":
            errors.append("full_text_verified requires full_access")
        if obj["lineage"]["relation"] in {"repost", "syndication", "shared_press_release", "shared_anonymous_origin"}:
            if not obj["lineage"].get("origin_observation_id"):
                errors.append("derivative lineage requires origin_observation_id")
    elif name == "source_concentration_assessment":
        if obj["known_independence_group_count"] > obj["unique_source_count"]:
            errors.append("known independence groups cannot exceed unique sources")
        if obj["derivative_observation_count"] > len(obj["observation_ids"]):
            errors.append("derivative count cannot exceed observation count")
        if obj["state"] == "SINGLE_ORIGIN":
            if obj["known_independence_group_count"] != 1 or obj["unknown_lineage_count"] != 0:
                errors.append("SINGLE_ORIGIN requires exactly one known group and no unknown lineage")
            if not obj["single_source_bias"]:
                errors.append("SINGLE_ORIGIN must set single_source_bias=true")
        if obj["state"] == "DIVERSE" and obj["known_independence_group_count"] < 2:
            errors.append("DIVERSE requires at least two known independence groups")
    elif name == "claim_record":
        policy = obj["dynamic_value_policy"]
        if policy is not None:
            rule = policy["materiality_rule"]
            if rule == "absolute" and policy["absolute_delta"] is None:
                errors.append("absolute materiality rule requires absolute_delta")
            if rule == "relative" and policy["relative_delta"] is None:
                errors.append("relative materiality rule requires relative_delta")
            if rule == "either" and policy["absolute_delta"] is None and policy["relative_delta"] is None:
                errors.append("either materiality rule requires at least one threshold")
    elif name == "material_change_assessment":
        if obj["material"] and "non_material_update" in obj["change_types"]:
            errors.append("material assessment cannot include non_material_update")
        if not obj["material"] and obj["change_types"] != ["non_material_update"]:
            errors.append("non-material assessment must contain only non_material_update")
        if "priority_change" in obj["change_types"] and obj["priority_from"] == obj["priority_to"]:
            errors.append("priority_change requires different from/to values")
    elif name == "costly_signal_assessment":
        if not obj["eligible"] and obj["strength"] != "NOT_APPLICABLE":
            errors.append("ineligible costly signal must be NOT_APPLICABLE")
        if obj["strength"] == "STRONG" and not obj["resource_commitment_present"]:
            errors.append("STRONG costly signal requires resource commitment")
    elif name == "rhetoric_action_gap":
        if obj["gap_direction"] == "aligned" and obj["rhetoric_direction"] != obj["behavior_direction"]:
            errors.append("aligned gap requires matching directions")
    elif name == "narrative_gap":
        if obj["gap_type"] == "NARRATIVE_ONLY":
            if obj["material_fact_disagreement"] or not obj["narrative_only_divergence"]:
                errors.append("NARRATIVE_ONLY requires narrative divergence without material fact disagreement")
        if obj["gap_type"] == "FACT_DISPUTE" and not obj["material_fact_disagreement"]:
            errors.append("FACT_DISPUTE requires material_fact_disagreement=true")
    elif name == "hypothesis_assessment":
        if obj["falsification_status"] == "triggered" and obj["posterior_direction"] != "falsified":
            errors.append("triggered falsification requires posterior_direction=falsified")
        if obj["posterior_direction"] == "falsified" and obj["falsification_status"] != "triggered":
            errors.append("posterior_direction=falsified requires triggered falsification")
    elif name == "intelligence_output_decision":
        if obj["notify"] != (obj["outcome"] == "EMIT"):
            errors.append("notify must match outcome")
        if obj["notify"] and obj["suppression_codes"]:
            errors.append("EMIT decision cannot contain suppression codes")
        if not obj["notify"] and not obj["suppression_codes"]:
            errors.append("SUPPRESS decision requires a suppression code")
        if obj["next_eligible_at"] is not None and "COOLDOWN" not in obj["suppression_codes"]:
            errors.append("next_eligible_at is only valid for cooldown suppression")
    elif name == "judgment_ledger_record":
        refs = obj["subject_refs"]
        if not any(refs.values()):
            errors.append("judgment must reference at least one event/claim/edge/scenario")
    elif name == "judgment_outcome_record":
        if obj["outcome_status"] == "resolved" and not obj["later_result"]:
            errors.append("resolved judgment outcome requires later_result")
        if "none" in obj["error_types"] and len(obj["error_types"]) > 1:
            errors.append("error_types=none cannot coexist with other errors")
        if obj["previous_outcome_id"] == obj["outcome_id"]:
            errors.append("previous_outcome_id cannot self-reference")
    elif name == "posterior_revision":
        if obj["direction"] == "falsified":
            if not obj["refuting_evidence_ids"] and not obj["counterevidence_assessment_ids"]:
                errors.append("falsified posterior requires refuting evidence or counterevidence assessment")
    elif name == "alert_history_record":
        if obj["outcome"] == "EMIT":
            if not obj["trigger_codes"]:
                errors.append("EMIT alert history requires trigger_codes")
            if obj["suppression_codes"]:
                errors.append("EMIT alert history cannot contain suppression_codes")
        else:
            if not obj["suppression_codes"]:
                errors.append("SUPPRESS alert history requires suppression_codes")
    elif name == "judgment_calibration_summary":
        total = obj["total_count"]
        if obj["resolved_count"] + obj["partially_resolved_count"] + obj["unresolved_count"] != total:
            errors.append("calibration outcome counts must sum to total_count")
        if len(obj["judgment_ids"]) != total:
            errors.append("calibration must contain one latest judgment_id per total_count")
        if len(obj["outcome_ids"]) != total:
            errors.append("calibration must contain one selected outcome_id per total_count")
    elif name == "chain_definition":
        node_ids = [node["node_id"] for node in obj["nodes"]]
        link_ids = [link["link_id"] for link in obj["links"]]
        if len(node_ids) != len(set(node_ids)):
            errors.append("chain node_id values must be unique")
        if len(link_ids) != len(set(link_ids)):
            errors.append("chain link_id values must be unique")
        if not all(link["required"] for link in obj["links"]):
            errors.append("v0.1 canonical linear chain requires every link to be required")
        node_set = set(node_ids)
        for link in obj["links"]:
            if link["source_node_id"] == link["target_node_id"]:
                errors.append("chain link cannot self-loop")
            if link["source_node_id"] not in node_set or link["target_node_id"] not in node_set:
                errors.append("chain link endpoints must reference defined nodes")
            latency = link["expected_latency_days"]
            if latency is not None and latency["min"] > latency["max"]:
                errors.append("chain expected latency min must be <= max")
        for left, right in zip(obj["links"], obj["links"][1:]):
            if left["target_node_id"] != right["source_node_id"]:
                errors.append("v0.1 canonical chain links must form an ordered contiguous path")
    elif name == "chain_link_assessment":
        counts = obj["epistemic_counts"]
        forecast_only = (
            counts["forecast"] > 0
            and counts["fact"] == 0
            and counts["correlation"] == 0
            and counts["causality"] == 0
        )
        if forecast_only and obj["h_state"] in {"H2", "H3"}:
            errors.append("forecast-only link cannot claim H2/H3 chain transmission")
        if counts["causality"] > 0 and not obj["supporting_evidence_ids"]:
            errors.append("causal evidence count requires supporting_evidence_ids")
        if obj["h_state"] == "Hx" and obj["direction"] != "falsified":
            errors.append("Hx link must use direction=falsified")
        if obj["direction"] == "falsified" and obj["h_state"] != "Hx":
            errors.append("direction=falsified requires Hx")
    elif name == "chain_watch_snapshot":
        total = obj["total_link_count"]
        required = obj["required_link_count"]
        if required > total:
            errors.append("required_link_count cannot exceed total_link_count")
        for field in (
            "supported_link_count",
            "h3_link_count",
            "forecast_only_link_count",
            "falsified_link_count",
            "falsified_required_link_count",
            "strengthening_link_count",
            "weakening_link_count",
            "material_link_count",
        ):
            if obj[field] > total:
                errors.append(f"{field} cannot exceed total_link_count")
        if obj["falsified_required_link_count"] > obj["falsified_link_count"]:
            errors.append("falsified required links cannot exceed all falsified links")
        if obj["longest_contiguous_supported_path"] > obj["supported_link_count"]:
            errors.append("longest contiguous path cannot exceed supported_link_count")
        if obj["full_chain_supported"] and obj["chain_state"] != "TRANSMITTING":
            errors.append("full_chain_supported requires TRANSMITTING")
        if obj["chain_state"] == "TRANSMITTING" and not obj["full_chain_supported"]:
            errors.append("TRANSMITTING requires full_chain_supported")
        if obj["chain_state"] == "BROKEN" and obj["falsified_required_link_count"] == 0:
            errors.append("BROKEN requires a falsified required link")
        if obj["chain_state"] == "BUILDING" and obj["longest_contiguous_supported_path"] < 2:
            errors.append("BUILDING requires a contiguous supported path of at least 2")
        if obj["chain_state"] == "FRAGMENTED":
            if obj["supported_link_count"] == 0 or obj["longest_contiguous_supported_path"] > 1:
                errors.append("FRAGMENTED requires isolated supported links")
    elif name == "replay_step_result":
        expected_notify = obj["expected_notify"]
        actual_notify = obj["actual_notify"]
        expected_code = obj["expected_code"]
        actual_codes = set(obj["actual_trigger_codes"]) | set(obj["actual_suppression_codes"])
        if expected_notify and not actual_notify:
            expected_error = "FALSE_NEGATIVE"
        elif not expected_notify and actual_notify:
            expected_error = "FALSE_POSITIVE"
        elif expected_code is not None and expected_code not in actual_codes:
            expected_error = "CODE_MISMATCH"
        else:
            expected_error = "NONE"
        if obj["error_class"] != expected_error:
            errors.append(f"replay error_class must be {expected_error}")
        if obj["passed"] != (expected_error == "NONE"):
            errors.append("replay passed must match error_class")
    elif name == "replay_suite_summary":
        if obj["passed_steps"] + obj["failed_steps"] != obj["total_steps"]:
            errors.append("replay passed_steps + failed_steps must equal total_steps")
        if len(obj["result_ids"]) != obj["total_steps"]:
            errors.append("replay result_ids length must equal total_steps")
        if obj["false_positive_count"] > obj["failed_steps"]:
            errors.append("false_positive_count cannot exceed failed_steps")
        if obj["false_negative_count"] > obj["failed_steps"]:
            errors.append("false_negative_count cannot exceed failed_steps")
        if obj["code_mismatch_count"] > obj["failed_steps"]:
            errors.append("code_mismatch_count cannot exceed failed_steps")
        classified_failures = (
            obj["false_positive_count"]
            + obj["false_negative_count"]
            + obj["code_mismatch_count"]
        )
        if classified_failures != obj["failed_steps"]:
            errors.append("all replay failed_steps must be classified as FP/FN/code mismatch")
        if obj["duplicate_control_failure_count"] > obj["failed_steps"]:
            errors.append("duplicate_control_failure_count cannot exceed failed_steps")
        if obj["deescalation_falsification_failure_count"] > obj["failed_steps"]:
            errors.append("deescalation/falsification failures cannot exceed failed_steps")
    elif name == "communications_resilience_audit":
        link_ids = [link["link_id"] for link in obj["external_links"]]
        if len(link_ids) != len(set(link_ids)):
            errors.append("external link_id values must be unique")
        if obj["power"]["power_outage_test"] == "pass":
            runtime = obj["power"]["tested_runtime_hours"]
            if runtime is None or runtime <= 0:
                errors.append("passed communications power outage test requires positive runtime")
        internal = obj["internal_network"]
        if internal["local_lan_status"] == "tested_pass" and internal["internet_loss_test"] != "pass":
            errors.append("tested_pass local LAN requires internet_loss_test=pass")
        for link in obj["external_links"]:
            if link["status"] == "tested_pass":
                if not link["independence_group_id"]:
                    errors.append(f"{link['link_id']}: tested external link requires independence_group_id")
                if link["bidirectional"] is not True:
                    errors.append(f"{link['link_id']}: tested external link must be bidirectional")
                if link["test_runtime_hours"] is None or link["test_runtime_hours"] <= 0:
                    errors.append(f"{link['link_id']}: tested external link requires positive runtime")
    elif name == "communications_verification_assessment":
        if obj["independent_external_path_count"] > obj["tested_external_path_count"]:
            errors.append("independent external paths cannot exceed tested paths")
        if obj["minimum_demonstrated_internal_continuity_days"] is not None and not obj["internal_lan_gate_passed"]:
            errors.append("internal continuity lower bound requires internal LAN gate")
        if obj["minimum_demonstrated_external_continuity_days"] is not None and not obj["external_redundancy_gate_passed"]:
            errors.append("external continuity lower bound requires external redundancy gate")
        if obj["degraded_local_operation_candidate"] and not (
            obj["internal_lan_gate_passed"]
            and obj["offline_compute_gate_passed"]
            and obj["power_gate_passed"]
        ):
            errors.append("degraded local candidate requires internal + offline compute + power gates")
    elif name == "food_resilience_audit":
        inv = obj["inventory"]
        demand = obj["demand"]
        if (
            inv["shelf_stable_calories_kcal"] is not None
            and inv["usable_calories_kcal"] is not None
            and inv["shelf_stable_calories_kcal"] > inv["usable_calories_kcal"]
        ):
            errors.append("shelf-stable calories cannot exceed total usable calories")
        if inv["inventory_count_status"] == "measured" and inv["usable_calories_kcal"] is None:
            errors.append("measured food inventory requires usable_calories_kcal")
        if demand["daily_calorie_demand_kcal"] is not None and demand["people_count"] is None:
            errors.append("daily calorie demand requires people_count context")
        path_ids = [path["path_id"] for path in obj["replenishment"]["supply_paths"]]
        if len(path_ids) != len(set(path_ids)):
            errors.append("food replenishment path_id values must be unique")
        for path in obj["replenishment"]["supply_paths"]:
            if path["status"] == "verified_available" and not path["independence_group_id"]:
                errors.append(f"{path['path_id']}: verified food path requires independence_group_id")
        repl = obj["replenishment"]
        if repl["local_production_status"] in {"measured_output", "field_tested"}:
            if repl["production_daily_calorie_equivalent"] is None or repl["production_daily_calorie_equivalent"] <= 0:
                errors.append("measured/field-tested food production requires positive calorie-equivalent output")
            if repl["production_inputs_mapped"] is not True:
                errors.append("measured/field-tested food production requires mapped inputs")
    elif name == "food_verification_assessment":
        if (
            obj["buffer_autonomy_days"] is not None
            and obj["shelf_stable_buffer_days"] is not None
            and obj["shelf_stable_buffer_days"] > obj["buffer_autonomy_days"]
        ):
            errors.append("shelf-stable buffer days cannot exceed total buffer days")
        if obj["production_support_candidate"] and obj["recommended_verification_status"] == "stated":
            errors.append("production support candidate cannot coexist with stated-only verification")
    elif name == "structural_delta":
        h_order = {"H0": 0, "H1": 1, "H2": 2, "H3": 3}
        c_order = {"C0": 0, "C1": 1, "C2": 2, "C3": 3}
        b_order = {"B0": 0, "B1": 1, "B2": 2, "B3": 3}
        for edge in obj["edge_changes"]:
            f, t, d = edge["from_state"], edge["to_state"], edge["direction"]
            expected = "unchanged" if f == t else (
                "falsified" if t == "Hx" else (
                    "recovered" if f == "Hx" else (
                        "strengthened" if h_order[t] > h_order[f] else "weakened"
                    )
                )
            )
            if d != expected:
                errors.append(f"edge delta {f}->{t} must be {expected}")
        coupling = obj["coupling_change"]
        cf, ct = coupling["from_band"], coupling["to_band"]
        c_expected = "unchanged" if cf == ct else ("denser" if c_order[ct] > c_order[cf] else "sparser")
        if coupling["direction"] != c_expected:
            errors.append(f"coupling delta {cf}->{ct} must be {c_expected}")
        buffer = obj["buffer_change"]
        bf, bt = buffer["from_band"], buffer["to_band"]
        if bf == bt:
            b_expected = "unchanged"
        elif "BU" in {bf, bt}:
            b_expected = "unknown"
        else:
            b_expected = "depleted" if b_order[bt] > b_order[bf] else "restored"
        if buffer["direction"] != b_expected:
            errors.append(f"buffer delta {bf}->{bt} must be {b_expected}")
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
