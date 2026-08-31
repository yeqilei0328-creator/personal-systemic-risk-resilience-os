# Event / Claim State — Phase 3R-02 v0.1

## Purpose

R1 remembers where evidence came from.

R2 remembers **what event/claim the system thought it was looking at**, how that state changed, and whether an update was materially new.

It implements the V0.3 Candidate Event Pool / Event Cluster / Atomic Claim / Material Change / dynamic-number discipline without introducing automatic semantic extraction.

## 1. Event compatibility

The existing Phase 1 `Event` remains valid.

Compatibility updates:
- `intelligence_priority` now supports P0-P3.
- P3 is stored/background and remains non-push by default.

R2 adds `Event State Record` for stateful clustering/persistence.

## 2. Event fingerprint

V0.3 cluster basis:

`Actor + Action + Object + Location + Time Window + Consequence`

R2 stores an immutable first-seen canonical `fingerprint_basis` and SHA-256 fingerprint.

Display title is deliberately excluded.

Therefore:
- headline rewrites do not create a new event;
- canonical identity changes require explicit re-clustering rather than silently mutating one event.

The fingerprint function normalizes case/whitespace and list order. Upstream semantic normalization is still required; this v0.1 function does not know that “US” and “United States” are synonyms.

## 3. Claim Store

Each atomic Claim stores:
- V0.3 claim kind;
- epistemic class;
- statement;
- **Claim Grade A-D**;
- source-observation refs;
- evidence refs;
- status/supersession;
- optional dynamic-value policy.

Claim Grade A-D is epistemic confidence and must never be confused with Risk Variable A-D.

## 4. Dynamic numbers

Changing numbers such as casualties, missing people, strike counts, order values or financing values are stored as separate timestamped observations:

`value + unit + as_of + recorded_at + source refs + Claim Grade`

Old and new numbers are not overwritten into one timeless field.

## 5. Claim-specific numeric materiality

There is no global “10% means material” rule.

A dynamic Claim may define:
- none
- any_change
- absolute
- relative
- either absolute/relative

This allows casualty counts, oil prices, order values and financing amounts to use different materiality logic.

Relative change from a zero baseline fails closed unless an absolute threshold also exists.

## 6. Material Change

The detector ignores title/source-list noise and recognizes structural change through:
- new event;
- P-level change;
- V0.3 material markers;
- qualifying lifecycle change;
- material Claim Grade change;
- claim-specific numeric material change.

Representable V0.3 transitions include:
- threat → attack
- declaration → budget
- budget → procurement
- procurement → delivery
- demo → deployment
- test → scaled production
- shipping risk → actual suspension
- expectation → real price transmission

The detector does not invent these transitions from prose. Upstream analysis must supply the semantic marker.

## 7. Evidence compatibility

The Phase 1 Evidence schema now allows `target_type=claim`.

This lets future Evidence Graph records attach directly to atomic Claims instead of forcing all evidence to point only at an Event/Edge/Scenario.

## 8. File-backed state

`EventClaimStateStore` persists:
- events
- claims
- dynamic claim values
- material-change assessments

It is deterministic reference storage, not a production database or crawler.

## 9. Phase boundary

R2 establishes event/claim memory.

R3 will add:
- Costly Signal
- Rhetoric–Action Gap
- Narrative Gap
- Counterevidence/falsification
- Risk Variable / Edge / Coupling / Buffer / Scenario deltas
