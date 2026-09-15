# Strategic Capture Guard

## 1. Purpose

Prevent infinite patching, tuning and Reality retries when a route is no longer proving the project claim.

## 2. Trigger

Enter `STRATEGIC_CAPTURE` when one or more are true:
- same failure class repeats twice after disciplined fixes;
- a route consumes the configured Reality Spike budget (default maximum `3` unless a stricter work-unit limit exists);
- timing/tracking/runtime mechanics are already repaired but the product/capability claim still is not demonstrated;
- continued tuning is no longer materially increasing understanding;
- Technology Radar evidence indicates a different route is likely superior.

RED actions are stricter: after one consumed RED attempt, automatic retry remains `0` regardless of the generic spike budget.

## 3. Required questions

Before another implementation attempt, answer:

```text
What exact claim are we proving?
Is the current path the lowest-cost valid proof?
Is this an implementation failure or contract/reality failure?
Should we REUSE / ADAPT / SUBSTITUTE / REBASELINE / STOP?
What new evidence would justify resuming this route?
```

## 4. Stop-loss

Each Reality route should define before execution:
- maximum attempts;
- maximum repeated failure class;
- maximum tuning cycles;
- time/cost/authority envelope as applicable;
- evidence needed to justify another attempt.

Do not create `Attempt N+1` merely because `Attempt N` failed.

## 5. Allowed activity in Strategic Capture

Allowed:
- preserve logs/evidence;
- read-only inspection;
- bounded Radar research;
- compare alternatives;
- reframe claim/contract;
- prepare a new decision record.

Not allowed without a new authorized decision:
- another speculative implementation loop;
- architecture/dependency widening;
- RED retry;
- procurement/device execution.

## 6. Exit

Exit `STRATEGIC_CAPTURE` only with a durable decision:
- resume existing route with new evidence/constraint;
- REUSE;
- ADAPT;
- SUBSTITUTE;
- REBASELINE;
- STOP.

Record the decision and reconsideration trigger.