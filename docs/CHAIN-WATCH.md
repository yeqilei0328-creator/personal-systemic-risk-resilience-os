# Chain Watch — Phase 3R-06 v0.1

## Purpose

Chain Watch answers:

> Are the links in a hypothesized systemic transmission chain actually becoming connected?

It does not infer a full causal chain from simultaneous headlines.

## First canonical chain

`Climate / El Niño`
→ `Food & Energy Pressure`
→ `Inflation / Inflation Expectations`
→ `Fed / Monetary Policy`
→ `UST 10Y / 30Y + Financial Conditions / Fiscal Pressure`
→ `AI CapEx / Tech Valuation / Financing Stress`

This is a watch hypothesis, not a declared causal fact.

## 1. Chain Definition

A Chain Definition stores:
- ordered nodes;
- ordered directed links;
- mechanism per link;
- expected latency where useful;
- persistence notes;
- observation domains;
- Risk Variable mapping.

Order matters.

## 2. Link Assessment

Every directed link stores distinct epistemic counts:

- Fact
- Forecast
- Correlation
- Causality
- Counterevidence

It also stores:
- H0/H1/H2/H3/Hx;
- direction;
- Material Delta;
- supporting/refuting evidence;
- hypothesis/counterevidence refs;
- common-cause refs.

## 3. Causal support rule

For Chain Watch v0.1, a link counts as connected transmission only when:

- `H2` or `H3`; and
- at least one explicit `causality` evidence item exists;
- at least one supporting Evidence reference is attached; and
- the link is not falsified.

Therefore:

- Forecast-only H2 does not count.
- Correlation-only H2 does not count.
- A downstream fact does not automatically validate upstream causality.

This is deliberately conservative.

## 4. Chain state

Chain state is descriptive and separate from Global Stage I-IV.

### UNKNOWN
Insufficient connected causal links.

### FRAGMENTED
At least one supported link exists, but supported links do not yet create a multi-link contiguous path.

### BUILDING
At least two contiguous required links are supported, but the full chain is incomplete.

### TRANSMITTING
Every required ordered link is supported.

### RELAXING
A previously BUILDING/TRANSMITTING chain is losing support and weakening dominates, without a required link being formally falsified.

### BROKEN
At least one required link is Hx.

### v0.1 linear-chain constraint

The canonical v0.1 Chain Watch is a single ordered linear path. Every link in that path is required.

Branching, alternative mechanisms and auxiliary links are deliberately deferred to a future schema version rather than pretending a skipped middle link still forms a continuous path.

## 5. Longest contiguous supported path

This is more informative than raw supported-link count.

Example:

`L1 supported, L2 unsupported, L3 supported`

has:
- supported count = 2;
- longest contiguous path = 1;
- state = FRAGMENTED.

It is not a connected three-stage transmission.

## 6. No chain score

R6 does not output:
- 73/100 risk;
- 82% chain certainty;
- a new global danger index.

It reports structure.

Snapshots therefore expose both:
- total link count;
- required link count;
- all falsified links;
- falsified required links.

## 7. Relationship to R4

R6 does not notify.

A material Chain Watch state change may later become an R4 candidate:
- BUILDING → TRANSMITTING;
- new link H3;
- required link → Hx;
- major Lead Time compression.

The output gate remains authoritative for interruption decisions.

## 8. Relationship to R5

Chain Watch snapshots and link assessments can be referenced by Judgment Ledger entries.

That makes it possible to record:
- when the chain was believed to be BUILDING;
- which links were still missing;
- what later evidence confirmed/falsified them.

## 9. Anti-doom discipline

The chain may weaken.

The chain may break.

A forecast may fail.

Counterevidence is not an inconvenience; it is part of the data model.

A useful Chain Watch must be equally capable of saying:

> the hypothesized resonance is not closing.
