# Judgment Memory & Posterior Learning — Phase 3R-05 v0.1

## Purpose

V0.3 requires the system to remember:
- what it knew then;
- what it did not know;
- what it predicted;
- what signals would prove/disprove it;
- what happened later;
- how the judgment changed.

R5 makes that memory durable.

## 1. Append-only principle

Judgments are historical records.

They must not be silently rewritten after outcomes become known.

`JudgmentMemoryStore` therefore permits:
- first append;
- exact idempotent replay.

It rejects:
- same ID + changed content.

Posterior revisions and Alert History use the same rule.

## 2. Judgment Ledger

A record captures the V0.3 concepts:
- timestamp;
- Event/Claim/Edge/Scenario refs;
- initial Claim Grade where applicable;
- P0-P3;
- system-state refs;
- current finding;
- predicted paths;
- tail risk;
- watch / falsification signals;
- source set;
- source limitations;
- later result;
- outcome status;
- error types;
- posterior revision refs.

`later_result` does not replace `current_finding`.

## 3. Predicted paths

Predictions use semantic likelihood bands:
- remote
- possible
- plausible
- likely
- unknown

v0.1 does not invent a universal numerical probability model.

## 4. Posterior Revision

Conceptual contract:

`Prior + New Evidence + Source Reliability + Counter Evidence → Posterior`

Persist:
- prior semantic state;
- posterior semantic state;
- supporting/new evidence;
- refuting evidence;
- Source Reputation refs;
- Counterevidence Assessment refs;
- direction;
- rationale.

Direction:
- strengthen
- weaken
- unchanged
- falsified
- reclassified
- unknown

## 5. Claim Grade discipline

Claim Grade A/B/C/D is not a numeric ordinal score.

Especially:
- D = analysis/opinion/prediction.

R5 therefore has no:
- A=4/B=3/C=2/D=1 mapping;
- automatic average confidence;
- grade arithmetic.

A revision may record B→A or D→D or D→C, but semantics/rationale remain explicit.

## 6. Alert History

Every R4 gate decision can be remembered, including suppression.

This matters because:
- duplicate suppression needs history;
- replay needs to know what the system chose not to send;
- false-positive/late/early review requires historical decisions.

Transport status is separate because R4/R5 do not implement notification delivery.

## 7. Calibration

`summarize_judgment_calibration` counts:
- resolved / partially resolved / unresolved;
- error types.

Supported error examples:
- source_error
- overreaction
- underreaction
- timing_error
- omitted_variable
- correlation_as_causality
- rhetoric_overweight
- technology_maturity_overestimate
- execution_delay
- none / unknown

There is deliberately no single `accuracy_score`.

## 8. Dual calibration

### Source Ledger
Who is reliable in what domain / Claim type?

### Judgment Ledger
Where does the system itself systematically fail?

These must remain separate.

## 9. Phase boundary

R5 adds memory and learning records.

R6 will use that persistent state to maintain the first explicit Chain Watch:
Climate / El Niño
→ Food & Energy
→ Inflation
→ Fed
→ UST / Financial Conditions
→ AI CapEx / Valuation / Financing Stress.
