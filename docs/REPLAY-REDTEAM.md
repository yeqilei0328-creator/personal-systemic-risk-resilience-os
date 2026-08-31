# Replay & Red Team — Phase 3R-07 v0.1

## Purpose

R7 is the final engineering gate for the Phase 3R Radar Precision Upgrade.

It does not add another intelligence model.

It tries to break the ones already built.

## 1. Synthetic replay scope

The v0.1 suite exercises failure modes that were explicitly identified during the V0.3 reconciliation and Phase 3R design:

- derivative-source multiplication;
- false multi-risk resonance;
- true multi-link resonance;
- duplicate re-alert;
- hysteresis;
- P3 silence;
- scheduled brief behavior;
- falsification;
- de-escalation/improvement;
- Chain Watch break/relaxation;
- title-only non-material updates;
- limited source access.

## 2. Replay result

Each replay step records:
- expected notify/suppress;
- actual notify/suppress;
- expected trigger/suppression code;
- actual codes;
- pass/fail;
- error class.

Error classes:
- NONE
- FALSE_POSITIVE
- FALSE_NEGATIVE
- CODE_MISMATCH

## 3. Suite summary

Summary reports counts only:
- total;
- passed/failed;
- false positives;
- false negatives;
- code mismatches;
- duplicate-control failures;
- de-escalation/falsification failures.

There is no aggregate `accuracy_score`.

The Phase 3R exit replay contains 13 required synthetic cases.

Passing 13/13 does not mean the system is 100% accurate in the real world. It only means the encoded synthetic failure modes behave as intended.

## 4. Cross-layer replay

R7 deliberately tests more than isolated functions.

### R1 → R4

Three publishers that trace to one original source remain:

`SINGLE_ORIGIN`

and do not magically create validated cross-system transmission.

### R6 → R4

A fully supported Chain Watch can provide a structured basis for a real resonance candidate.

A required Hx link yields:

`BROKEN`

and the associated hypothesis-falsification path may deserve an alert.

## 5. False-positive discipline

Expected silence is tested for:
- derivative-source multiplication;
- three worsening observation channels with no validated transmission;
- exact duplicate state;
- P3;
- title-only update;
- one-sample hysteresis crossing.

## 6. False-negative discipline

Expected emission is tested for:
- persistent true resonance;
- scheduled P2 material item;
- hypothesis falsification;
- improving Global Stage change.

A system that only catches worsening is incomplete.

## 7. Historical calibration boundary

This is not the historical backtest.

Historical calibration belongs to Phase 5 and will require real dated events, contemporaneous evidence sets, past predictions and outcome reconstruction.

R7 is synthetic engineering validation only.

## 8. Exit criterion

Phase 3R is engineering-complete only when:
- all R1-R7 tests pass;
- no unexplained CI failure remains;
- replay summary is deterministic;
- Roadmap/Project State are updated only after the final head is green.
