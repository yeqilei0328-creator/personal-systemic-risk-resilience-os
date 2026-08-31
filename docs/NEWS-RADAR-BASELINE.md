# Existing News Radar Baseline — Phase 3R-00

## Status

Recovered operational baseline.

This document captures the already-working news recommendation and briefing logic before Phase 3R precision upgrades. It is a preservation baseline, not a redesign.

If an original Markdown specification is later supplied, reconcile it against this baseline and record differences explicitly.

## 1. Product role

The existing news conversation remains the primary user-facing intelligence surface.

It covers:
- domestic and international current affairs;
- geopolitical competition;
- military developments;
- regional conflict;
- macro / finance / trade / supply-chain developments;
- climate / disasters / resource constraints;
- Physical AI developments relevant to the user's project.

The front end should remain conversational and direct. The backend may be much more complex.

## 2. Recovered presentation behavior

Operational preferences recovered from prior use:

- primary delivery is a daily morning briefing around 08:00;
- avoid duplicative evening briefing as a second default digest;
- avoid a noisy hourly P0 presentation loop as a default user experience;
- front-end analysis is intentionally compressed;
- backend reasoning remains deep;
- top-level daily judgments remain tightly bounded, historically around no more than three major judgments;
- individual event items should emphasize:
  1. what happened;
  2. current judgment;
  3. why it matters;
  4. what to watch next.

These are preserved operating preferences, not hard-coded scheduling infrastructure in this repository.

## 3. P0 / P1 / P2

P0 / P1 / P2 is an **intelligence priority taxonomy**, not the global systemic-risk stage and not the personal R-Level.

### P0
Must-know information because it may:
- materially change model state;
- materially shorten Lead Time;
- alter a major scenario;
- change an action/playbook;
- invalidate an important assumption;
- represent a single major event with immediate systemic relevance.

P0 is not “dramatic headline”.

### P1
Important trend evidence worth retaining and incorporating into the model, but not necessarily requiring immediate interruption.

### P2
Background/context. Useful for state maintenance and understanding, but normally not worth interrupting the user.

## 4. Backend reasoning contract

The radar may use a full Evidence · Behavior · Systems reasoning chain internally.

### Evidence
- multi-source discovery;
- claim splitting;
- source quality / provenance;
- primary vs secondary;
- independent vs derivative sources;
- fact / forecast / correlation / causality / opinion;
- counterevidence;
- confidence and uncertainty.

### Behavior
For political/military/state actors:
- observable action may carry more evidentiary value than rhetoric;
- words-actions gap is explicit;
- logistics, mobilization, routing, procurement, deployment, regulation and market behavior may matter more than statements.

### Systems
- map events into first-order variables A/B/C/D;
- track transmission edges;
- avoid common-cause double counting;
- update Coupling Density;
- monitor feedback-loop candidates;
- track buffer depletion/restoration;
- update scenarios and Lead Time;
- map personal exposure only after global-system judgment.

## 5. Multi-risk resonance baseline

The radar is not a “bad news counter”.

A resonance alert becomes meaningful when:
- multiple distinct risk domains synchronously deteriorate; or
- one major event materially changes several downstream systems; or
- an important transmission edge is strengthened/validated; or
- a key buffer is depleted; or
- the global risk structure changes.

A prior operational threshold used “at least three risk categories visibly worsening together, or one major event”. Phase 3R may refine this into explicit structural-delta logic, but it should preserve the spirit: synchronized change matters more than headline count.

## 6. Front-end compression

The front end should not expose the entire backend reasoning chain.

Default user-facing output should emphasize:
- conclusion;
- material evidence;
- what changed;
- why it matters;
- uncertainty/counterevidence when decision-relevant;
- next trigger.

Detailed chain-of-thought style exposition is not required for normal alerts.

## 7. Physical AI Radar

Physical AI is a fixed intelligence module within the same user-facing news product.

Coverage includes:
- drones / UAVs;
- quadrupeds / robot dogs;
- UGVs;
- humanoids;
- manipulators;
- biomimetic / insect-scale / micro robots;
- AI vision / VLM / VLA / perception;
- world models;
- planning / control;
- multi-agent / swarm / one-to-many supervision;
- digital twins / simulation / data flywheels / RoboOps;
- edge/local AI;
- degraded/offline runtime;
- autonomous inspection / security;
- high-adversity field lessons from real unmanned systems, bounded to generalizable systems/robotics insight.

The Physical AI Radar is not a separate news product. It is one domain inside the broader intelligence product, with a specialized downstream engineering path into the Physical AI project's Technology Radar.

## 8. What Phase 3R may improve

Phase 3R should improve:
- source registry;
- source independence;
- event fingerprinting;
- clustering/dedup;
- novelty/change detection;
- behavior-vs-rhetoric;
- counterevidence/falsification;
- edge/coupling/buffer/scenario deltas;
- alert suppression/hysteresis;
- Chain Watch.

It should **not** casually replace:
- P0/P1/P2;
- the concise presentation style;
- the existing daily briefing experience;
- Physical AI Radar;
- the principle that no substantive change means no notification.

## 9. Reconciliation rule

If an original news-radar Markdown/spec is supplied:
1. parse it as a source artifact;
2. compare against this recovered baseline;
3. prefer later explicit user rules over older rules;
4. record conflicts;
5. preserve working behavior unless there is an explicit reason to change it;
6. update this document through review rather than silent replacement.
