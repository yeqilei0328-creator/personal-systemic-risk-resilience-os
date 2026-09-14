# Engineering Autonomy Governance

## 1. Principle

`capability != authority`

An agent being technically able to perform an action does not authorize that action.

Authority is classified per **next action**.

## 2. GREEN

GREEN covers bounded, reversible engineering actions with no protected real-world side effect:
- read repository/files;
- search code;
- local tests;
- deterministic edits;
- create branch;
- generate reports/evidence;
- dry-run/simulation;
- read-only API;
- CI diagnosis;
- public-safe synthetic work.

GREEN can proceed continuously while scope remains stable.

## 3. AMBER

AMBER covers governance, scope, architecture and reduced-reversibility changes:
- governance/workflow change;
- critical schema change;
- permission router change;
- dependency widening;
- architecture widening;
- security boundary change;
- method-pin contract change.

AMBER requires explicit review/approval before acceptance/merge. It does not grant RED authority.

## 4. RED

RED covers protected or real-world mutation:
- production write;
- sensitive/private operational-state write outside an already approved bounded transaction;
- credential/account mutation;
- payment/procurement;
- camera/microphone/device access or control;
- robot/drone/UGV/arm/PLC/vehicle control;
- mission start / physical dispatch;
- destructive action.

RED requires fresh Owner authorization with:

```text
exact main SHA
exact tool / implementation SHA
exact gate fingerprint
exact operation/scope
exact environment
exact duration/bounds
exact retry policy
exact evidence-retention policy
exact exclusions
```

A vague `continue` is not a RED authorization.

## 5. RED granted != RED consumed

Every RED gate defines a consumption boundary.

Examples:
- before opening a camera/device connection: not consumed;
- after the device is actually opened/commanded: consumed;
- a preflight failure before the protected boundary does not consume RED unless the authorization contract says otherwise.

Evidence must record whether RED was `GRANTED_NOT_CONSUMED` or `CONSUMED`.

## 6. One-shot semantics

After RED is consumed:

```text
automatic_retry = 0
```

A later attempt requires:

```text
diagnose
→ prepare exact new gate
→ fresh Owner authorization
```

No retry loop, Radar result, CI result or prior approval can widen this.

## 7. Authority precedence

If an action matches multiple levels, highest risk wins:

```text
RED > AMBER > GREEN
```

If required facts are unknown or conflicting: `FAIL_CLOSED`.

## 8. Merge authority

Implementation permission is not merge permission.

Merge requires the repository merge gate regardless of GREEN/AMBER implementation authority. Governance PRs are at least AMBER because their acceptance changes future authority/workflow.

## 9. Radar boundary

Technology or Commercial/Ecosystem Radar may recommend:

`REUSE / ADAPT / EXTEND / BUILD / SUBSTITUTE / REBASELINE / STOP`

It never grants:
- merge;
- RED;
- production;
- credential/account action;
- procurement/payment;
- device/physical access.

## 10. Physical execution

Any RED physical action also requires `docs/PHYSICAL-AUTHORITY.md`.

Proposal, approval, execution and verification are separate records.