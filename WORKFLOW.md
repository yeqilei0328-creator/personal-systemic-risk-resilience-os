# WORKFLOW.md — Canonical Work-Unit Lifecycle

## 1. Purpose

This file is the executable human/agent workflow for the Personal Systemic Risk & Resilience OS.

`AGENTS.md` defines the mandatory entry behavior. `docs/PROJECT-ENGINE.md` defines the project-specific operating engine. This file binds them to deterministic governance gates.

## 2. Work-unit lifecycle

```text
READ
→ INHERIT PARENT DECISION
→ RADAR TRIGGER CHECK
→ AUTHORITY ROUTER
→ EXECUTION ROUTER
→ PLAN
→ IMPLEMENT
→ FOCUSED TEST
→ FULL REGRESSION
→ STATIC / INTEGRITY
→ SELF-AUDIT
→ PR
→ CI
→ EXACT-HEAD GATE
→ MERGE
→ POST-MERGE VERIFY
→ DURABLE CLOSEOUT
→ NEXT AUTHORIZED WORK UNIT
```

If any stage observes `UNKNOWN`, `MISSING`, `DRIFTED`, `STALE`, `UNVERIFIED`, `UNAUTHORIZED`, `CONFLICTING_EVIDENCE`, material blocker, authority change or reality failure, stop the affected path and re-enter routing.

## 3. READ

Fresh-read current authoritative state:
- PUBLIC `main` SHA;
- PRIVATE `main` SHA when in scope and authorized;
- AGENTS / Project Engine / governance docs;
- Project State / Roadmap;
- active Issue / PR;
- branch / HEAD / merge-base;
- relevant CI;
- current-domain contracts.

Never substitute chat memory for this phase.

## 4. INHERIT PARENT DECISION

Recover durable decisions already made by the parent Issue/PR/ADR/Radar result. Do not silently widen them.

## 5. RADAR TRIGGER CHECK

Run the deterministic trigger contract before substantial implementation.

Possible verdicts:
- `NO_RADAR`
- `TECH_RADAR_BLOCKER`
- `TECH_RADAR_DECISION`
- `COMMERCIAL_RADAR_DISCOVERY`
- `COMMERCIAL_RADAR_VALIDATION`
- `DUAL_RADAR_MAJOR_DECISION`

When triggered:

```text
gpt_handoff_required = true
local_execution_disposition = STOP_LOCAL_SPECULATION_ALLOW_READONLY_EVIDENCE
resume_condition = RADAR_RESULT_RECONCILED_BY_GPT_CONTROL_PLANE
```

Radar never widens authority.

## 6. AUTHORITY ROUTER

Classify the next action, not the whole project.

- `GREEN`: bounded engineering/research with no real-world or protected mutation.
- `AMBER`: governance/workflow/schema/architecture/security-boundary change requiring explicit review/approval.
- `RED`: production/private sensitive writes, credentials/accounts, payment/procurement, real device/physical control or destructive action requiring fresh bounded Owner authorization.

RED is frozen to exact scope/gate/environment/duration/retry/evidence. If consumed, automatic retry is zero.

## 7. EXECUTION ROUTER

Choose the lowest sufficient execution tier:

- `GPT_ONLY`: architecture, roadmap, governance, audit, product decision, Radar synthesis, evidence interpretation.
- `GPT_DESKTOP`: routine Git/terminal/files/env/tests/deterministic edits/config/scripts/logs/branch/PR preparation.
- `GPT_DESKTOP_CODEX`: substantial multi-file implementation, complex refactor/test design, CI/runtime/SDK blocker, uncertain root cause, repeated blocker or architecture-sensitive work.

Model route: `LUNA / TERRA / SOL / ASTRA`.
Reasoning: `LIGHT / MEDIUM / HIGH / EXTREME`.

## 8. Router Header

Every material work unit binds:

```text
AUTHORITY_ROUTER = ...
EXECUTION_ROUTER = ...
MODEL_ROUTER = ...
REASONING_EFFORT = ...
FALLBACK_ROUTER = ...
```

## 9. PLAN / IMPLEMENT

Implementation must stay within Issue scope, authority and Radar decision.

A Technology Radar `BUILD` decision does not authorize dependency installation, private writes, procurement or real device access.

Do not patch the same blocker indefinitely. Repeated disciplined failure routes to Technology Radar and/or Strategic Capture.

## 10. Tests

### Focused
Test the changed work unit directly.

### Full regression
Run the repository-wide suite.

### Static / integrity
As applicable:
- `compileall`;
- `git diff --check`;
- JSON parse;
- schema validation;
- secret audit;
- local-path audit;
- scope audit;
- governance contract validation.

Environment/toolbox failures are classified before invoking Radar.

## 11. SELF-AUDIT

Confirm:
- scope;
- public/private boundary;
- secret/privacy safety;
- authority classification;
- Radar state;
- Reality state;
- stop-loss state;
- durable evidence completeness.

## 12. PR / CI

A PR records:
- exact base;
- Issue;
- scope / non-goals;
- Router Header;
- Radar verdict / evidence;
- Reality level if relevant;
- test commands/results;
- authority granted/consumed state;
- acceptance and stop conditions.

CI must validate the current final head.

## 13. EXACT-HEAD GATE

Record:

```text
tested_head
pr_head
origin_main
merge_base
```

Require:

```text
tested_head == pr_head
base reconciled
focused PASS
full regression PASS
static/integrity PASS
CI exact-head PASS
mergeable CLEAN
reviews/threads resolved
scope/privacy/secret/authority clean
```

If head changes, the gate resets.

## 14. MERGE

Merge is a separate authority gate. Do not infer merge approval from implementation permission.

Use expected head SHA where available.

## 15. POST-MERGE VERIFY

After merge:
1. fresh-read merged `main`;
2. confirm expected merge SHA/files;
3. rerun the relevant focused validation;
4. run full regression / compile/static checks as required;
5. update Project State / Issue closeout only if the merged state is true;
6. record durable evidence.

Completion requires:

```text
MERGED + POST_MERGE_VERIFIED
```

## 16. DURABLE CLOSEOUT

Record:
- result;
- exact SHA;
- test counts;
- CI result;
- authority consumed/not consumed;
- retry state;
- Reality/Radar state;
- evidence fingerprint;
- known unknowns;
- next authorized node.

## 17. Project-specific namespace guards

- Personal Action: `R0-R5`.
- Reality Ladder: `RL0-RL6`.
- Systemic-Risk Radar is a product engine.
- Technology Radar is an engineering control.
- Commercial/Ecosystem Radar is an external market/vendor reality control.

Do not collapse these namespaces.