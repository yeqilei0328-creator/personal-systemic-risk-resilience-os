# Precision Output / Alert Gate — Phase 3R-04 v0.1

## Purpose

R4 answers one question:

> Does this new state deserve to reach the user now?

It does not discover news and does not send notifications.

## 1. Two delivery modes

### scheduled_brief

China Morning Intelligence Brief.

Rules:
- P0-P2 may emit when there is Material Change;
- P3 remains stored/background;
- duplicate gate state is suppressed;
- no quota filling.

Scheduled brief does **not** require Global Risk Trigger A/B/C.

### interrupt_alert

Global Risk Resonance / must-know state change.

Requires an explicit interrupt trigger.

This distinction prevents the morning brief from becoming empty and prevents the condition watch from becoming a second news feed.

## 2. Trigger A — resonance compatibility

Preserve V0.3's five observation channels:
1. geopolitical conflicts
2. energy/shipping
3. East Asia security
4. extreme weather/disasters
5. price/real-economy transmission

Trigger A requires:
- at least 3 channels with `direction=worsen`;
- each counted channel has real-world behavior/data evidence;
- Structural Delta is material;
- validated cross-system transmission exists.

Therefore “three scary headlines” is insufficient.

The five channels are observation channels, not five independent causal votes. `common_cause_refs` remain part of state and are handled upstream in structural/coupling logic.

## 3. Trigger B

One newly material major system-changing event.

Examples in V0.3 include a durable Hormuz closure, direct major-power entry, major East Asia conflict or global financial accident.

R4 does not decide that an event is major. It consumes the structured boolean from upstream analysis.

## 4. Trigger C

A newly material strong transmission/coupling edge.

Again, R4 consumes an already validated structural state; it does not manufacture causality from headlines.

## 5. Additional interrupt triggers

- P0 material event
- hypothesis falsified
- material Lead Time compression
- Global Stage change in either direction
- personal action/playbook change

De-escalation is allowed to notify when it materially changes the model. A radar that never tells you risk improved is merely a siren with commitment issues.

## 6. Suppression order

1. P3 silent
2. no Material Change
3. exact gate-state duplicate
4. delivery-mode logic
5. no interrupt trigger
6. resonance-only hysteresis
7. resonance-only cooldown
8. emit

## 7. Duplicate state signature

The deterministic state signature excludes:
- detection timestamp
- prose notes

It includes gate-relevant state only.

Therefore headline wording/time-of-check changes cannot create alert novelty.

## 8. Hysteresis

Hysteresis applies to low-level Trigger-A-only threshold crossings.

A one-sample crossing can be held until the configured persistence count is met.

Urgent triggers such as:
- P0
- major event
- new strong edge
- hypothesis falsification
- Lead Time compression
- Stage/action change

are not hidden behind low-level hysteresis.

## 9. Cooldown

Cooldown also applies only to Trigger-A-only repeated resonance.

A genuinely new urgent trigger bypasses that low-level cooldown.

Exact duplicate state is still suppressed regardless.

## 10. Silence remains output

Suppression reasons are persisted:
- P3_SILENT
- NO_SUBSTANTIVE_CHANGE
- DUPLICATE_STATE
- NO_TRIGGER
- COOLDOWN
- HYSTERESIS

This is important for later replay/audit.

## 11. Phase boundary

R4 makes the output decision.

R5 will remember those decisions over time:
- Judgment Ledger
- Alert History
- Posterior Revision
- source/judgment calibration
