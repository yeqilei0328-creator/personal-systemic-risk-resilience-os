# Behavior / Counterevidence / Structural Delta — Phase 3R-03 v0.1

## Purpose

V0.3 says:

> 语言是低成本信号，行为是高价值信号。

R3 persists that distinction and connects verified behavior/counterevidence to the existing systemic-risk state model.

It does not infer intent from rhetoric and does not generate one aggregate risk score.

## 1. Behavior Signal

A Behavior Signal records observable action separately from speech.

Fields include:
- actor;
- behavior kind;
- observable_action;
- direction;
- resource commitment;
- persistence;
- reversibility;
- Claim/Evidence/Source Observation refs.

Capability, Intent, Action and Outcome remain separate concepts.

## 2. Costly Signal

A speech/non-observable signal cannot become a Costly Signal merely because it sounds serious.

Costly-signal strength is based on:
- real resource commitment;
- persistence;
- reversal cost.

Output:
- NOT_APPLICABLE
- UNKNOWN
- WEAK
- MODERATE
- STRONG

This is evidence-value structure, not an event-priority or risk-level taxonomy.

## 3. Rhetoric–Action Gap

Both directions matter.

Possible results:
- rhetoric_more_intensifying
- behavior_more_intensifying
- aligned
- mixed
- unknown

Example:
“不会升级” + real deployment/logistics escalation
→ behavior_more_intensifying.

The reverse is equally important:
alarming rhetoric + easing behavior
→ rhetoric_more_intensifying.

## 4. Narrative Gap

Narrative disagreement is separated from factual disagreement.

The system records:
- interpretations;
- verified facts;
- disputed facts;
- whether divergence is narrative-only;
- whether material facts themselves differ.

Different adjectives do not create different facts.

## 5. Counterevidence / Falsification

Each material Claim/Edge/Scenario hypothesis can persist:
- supporting evidence;
- refuting evidence;
- alternative explanations;
- omitted variables;
- falsification condition;
- falsification status;
- posterior direction.

If a falsification condition is triggered, the posterior direction must be `falsified`.

This makes downshift a first-class result rather than a reluctant footnote.

## 6. Structural Delta

R3 stores explicit changes to:
- Risk Variable A-D
- Edge H-state
- Coupling C0-C3
- Buffer BU/B0-B3
- Scenario probability / velocity / Lead Time

### Hx discipline

`Hx` means falsified/rejected transmission hypothesis.

It is **not** numerically above H3.

Examples:
- H2 → H3 = strengthened
- H3 → Hx = falsified
- Hx → H1 = recovered/reopened evidence

### Improvements are first-class

The engine must represent:
- Coupling becoming sparser;
- buffers restoring;
- scenario probability falling;
- velocity slowing;
- Lead Time expanding;
- Risk Variable improving.

A radar that only records deterioration is not a risk model. It is a mood disorder with JSON.

## 7. Common cause

Structural Delta preserves `common_cause_refs`.

The existence of several downstream symptoms does not make them independent causal votes.

## 8. Phase boundary

R3 creates behavior/system delta state.

R4 will decide whether a delta deserves to interrupt the user:
- P0-P3 gate
- V0.3 Trigger A/B/C compatibility
- duplicate suppression
- cooldown
- hysteresis
- no substantive change = no notification
