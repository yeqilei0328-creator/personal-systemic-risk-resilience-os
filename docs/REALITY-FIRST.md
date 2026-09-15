# Reality-First Governance

## 1. Namespace guard

The generic governance manual uses `R0-R6` for a Reality Ladder, but this project already uses `R0-R5` for **Personal Action Level**.

This repository therefore uses:

```text
RL0 assumption
RL1 mock
RL2 simulated integration
RL3 local integration
RL4 first real signal
RL5 repeatable real signal
RL6 operational confidence
```

`R0-R5` remains reserved for Personal Action Level.

## 2. Reality is not code coverage

A green unit test does not establish:
- hardware behavior;
- third-party runtime behavior;
- field availability;
- network continuity;
- device observability;
- vendor availability;
- user/market demand.

Do not promote Reality level from software evidence alone when the claim concerns the external world.

## 3. Reality Debt

`REALITY_DEBT` increases when implementation accumulates on unverified external assumptions.

Examples:
- assuming an SDK works as documented;
- assuming hardware supports a required operation;
- assuming an API exposes real data;
- assuming a network path survives degradation;
- assuming a sensor can observe the target event;
- assuming a vendor/platform behaves as claimed.

Reality Debt is not a moral score. It is a queue of external assumptions that can invalidate downstream work.

## 4. Reality Spike

First real contact should be a minimum bounded spike:

```text
one device/path
one event
one environment
one attempt
one evidence bundle
```

The exact envelope may differ, but widening must be explicit and authorized.

If the spike crosses a RED boundary, `docs/ENGINEERING-AUTONOMY-GOVERNANCE.md` and, for physical work, `docs/PHYSICAL-AUTHORITY.md` apply.

## 5. Advancement

Move Reality level only with evidence supporting the new level.

Suggested interpretation:
- `RL0`: hypothesis/assumption only;
- `RL1`: deterministic mock/fixture evidence;
- `RL2`: simulated integration across components;
- `RL3`: local non-production integration;
- `RL4`: first bounded real signal;
- `RL5`: repeated real signals across the defined envelope;
- `RL6`: operationally repeatable, monitored and maintainable within the defined scope.

A level is always scoped. `RL6` for one device/environment does not mean global confidence.

## 6. Failure

A failed Reality Spike is evidence. Do not bury it under another patch.

Classify:
- implementation failure;
- environment/toolbox failure;
- external contract failure;
- observation/evidence failure;
- unknown.

Repeated failures route to `docs/STRATEGIC-CAPTURE.md` and/or Technology Radar.