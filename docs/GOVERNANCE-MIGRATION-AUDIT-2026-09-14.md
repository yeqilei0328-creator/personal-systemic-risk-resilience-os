# Governance Migration Audit — 2026-09-14

## Baseline

PUBLIC main at audit start: `ce747f993d88336ea8f30edcae03400ae540d4a2`.

Existing draft governance PR #51 head at audit start: `505b46c97a9f8f083b1ae342cddcc6f5014ca0e5`.

PRIVATE main was read-only observed at `fb333b54f2e6b0cccb3061f544ea840e39f560cc`. PRIVATE PR #24 remains outside this work unit.

## Preserved strengths

Existing repository governance already provides:
- dual-repository authority boundary;
- GitHub `main` truth hierarchy;
- mandatory Fresh Read;
- fail-closed domain evidence;
- method-pin discipline;
- branch/PR/final-head CI;
- stale-branch reconciliation;
- public/private security boundary;
- defensive Physical AI constraint.

PR #51 additionally provides a permanent Technology Radar gate and is retained as part of this governance migration.

## Gaps found

Missing or incomplete on the audit baseline:
- deterministic GREEN / AMBER / RED Authority Router;
- RED freeze / consumed boundary / one-shot retry semantics;
- Execution Router and model escalation;
- machine-readable governance contract;
- deterministic Radar trigger implementation;
- Commercial/Ecosystem Radar separation;
- Reality-First / Reality Debt / Reality Spike;
- Strategic Capture stop-loss;
- Physical Execution Authority Envelope;
- canonical evidence fingerprint;
- explicit focused/full/static test layers;
- complete exact-head evidence bundle;
- mandatory post-merge verification;
- PR template carrying router/evidence fields.

## Namespace conflict resolved

The source governance manual uses `R0-R6` for Reality Ladder, but this project already owns `R0-R5` as Personal Action Level. Reality maturity is therefore renamed `RL0-RL6`.

This is a compatibility requirement, not a cosmetic preference.

## Maturity interpretation

The repository has isolated higher-level controls, but maturity is capped by missing lower-level governance contracts. This migration establishes the missing control-plane foundation and deterministic checks rather than claiming maturity from individual features.

## Authority

This migration is `AMBER`.

No RED authorization is created or consumed. No private operational-state write, credential/account change, procurement/payment, device access/control, physical dispatch or destructive action is included.

## Merge disposition

Draft PR only. Merge remains a separate gate requiring exact-head CI/review and post-merge verification.