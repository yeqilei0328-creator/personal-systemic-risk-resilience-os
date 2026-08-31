# Source Registry & Evidence Persistence — Phase 3R-01 v0.1

## Purpose

V0.3 already defines strong source/evidence judgment rules. R1 makes those rules durable.

This phase does **not** decide which news is important and does not assign a universal source score.

It persists:
- who the source is;
- what role it played for a specific claim;
- whether the system actually read the material;
- whether several reports are independent or derivative;
- how a source has performed in a specific domain × claim type over time.

## 1. Source Registry

A source record captures durable publisher/source identity:

- source class;
- operating roles;
- canonical origin;
- ownership group when known;
- domain strengths;
- default access status.

This is source identity, not a fact-confidence decision.

## 2. Source Observation

Independence is claim/event specific.

A Source Observation therefore records:
- claim_ref;
- source_id;
- publication/retrieval time;
- access state;
- role in this claim;
- evidence type;
- lineage relation;
- independence group;
- anonymous-origin group;
- full-text verification state;
- primary-material access.

This prevents a publisher-level registry from pretending that every Reuters/AP/company/official item has the same evidentiary structure.

## 3. Access Failure

Canonical access states:
- full_access
- partial
- paywall
- robots_blocked
- unavailable
- metadata_only
- unknown

Hard rule:

> If full text was not actually accessed and verified, the state must not imply full-text verification.

The runtime may still use metadata/summary/discovery value, but it must disclose the limitation and reduce downstream confidence where relevant.

## 4. Source lineage

Lineage relations:
- original
- independent
- repost
- syndication
- shared_press_release
- shared_anonymous_origin
- unknown

The same claim repeated by multiple publishers only increases independent evidence when the underlying evidence origin is genuinely independent.

Example:

`Original wire report → portal repost → translated repost`

may be 3 publishers but still 1 independence group.

## 5. Source Concentration Gate

R1 outputs one of:
- UNKNOWN
- SINGLE_ORIGIN
- CONCENTRATED
- DIVERSE

It does not create a new risk/priority taxonomy.

### SINGLE_ORIGIN
All observed reports trace to one known evidence-origin group.

### CONCENTRATED
At least one known origin exists, but unresolved lineage prevents a diversity claim.

### DIVERSE
At least two known independence groups exist.

### UNKNOWN
Lineage is insufficient to establish independence.

Search-result count is never evidence count.

## 6. Source Reputation Ledger

Reputation is explicitly:

`source × domain × claim_type × time`

Not:

`source = 87/100 forever`

Tracked dimensions may include:
- original reporting ratio;
- later-confirmed ratio;
- correction frequency;
- anonymous-source dependence;
- headline exaggeration;
- battlefield-claim accuracy;
- PR-copy tendency;
- median lead time;
- directional/systematic error notes.

Metrics may be null when not applicable or insufficiently sampled.

No `global_score` field exists.

## 7. Claim Grade vs Risk Variable namespace

Use:
- Claim Grade A-D
- Risk Variable A-D

Never use bare A/B/C/D where the meaning could be ambiguous.

## 8. File-backed reference store

`SourceStateStore` provides deterministic local persistence primitives for:
- source records;
- reputation records;
- claim-level source observations.

This is a reference implementation, not a crawler or production database.

It deliberately does not:
- crawl the web;
- choose P0/P1/P2/P3;
- automatically route Physical AI;
- assign fact confidence;
- change risk state.

## 9. Phase boundary

R1 establishes provenance memory.

R2 will build Event Store / Claim Store and use these records as evidence lineage inputs.
