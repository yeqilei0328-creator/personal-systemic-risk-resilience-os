# Technology Radar Gate — External Reality & Prior-Art Control

## Status

Permanent Project Engine control.

This is not a project phase, a one-time research task, or an optional note. It remains active throughout the life of the Personal Systemic Risk & Resilience OS.

## Mission

Prevent two recurring engineering failures:

1. **closed-world design** — making major technical decisions without checking the best available external answers;
2. **blocker tunnelling** — repeatedly attempting custom fixes while mature prior art, known failure modes, or reusable implementations already exist.

Core rule:

> Build last. Reuse first.

Decision order:

`REUSE → ADAPT → EXTEND → BUILD`

## Trigger A — Major Decision Gate

Mandatory before materially committing to or changing:

- architecture or subsystem boundaries;
- technical direction or strategy;
- hardware/platform family;
- protocol or communications architecture;
- major algorithm/model family;
- foundational third-party dependency;
- deployment/runtime approach;
- substantial custom implementation of a capability that may have mature prior art.

The gate asks:

> What are the best-supported current external answers to this capability under our project constraints, and what should we reuse rather than reinvent?

## Trigger B — Major Blocker Escape Gate

Mandatory when any of the following becomes true:

- a material engineering path is blocked;
- repeated attempts fail without materially increasing understanding;
- an unfamiliar error/failure mode is likely to have external prior art;
- hardware/software integration behaves unexpectedly;
- a dependency, protocol, platform, toolchain or deployment issue becomes a bottleneck;
- continued custom debugging is likely to cost more than bounded external research.

When triggered, stop blind iteration before adding another speculative custom fix.

The gate asks:

> Has this failure already been encountered, explained, fixed, worked around, or designed out elsewhere?

## Mandatory workflow

```text
TRIGGER CHECK
    |
    +-- no trigger --> normal Project Engine execution
    |
    +-- trigger --> STOP affected implementation path
                     |
                     v
               PROBLEM CONTRACT
                     |
                     v
             EXTERNAL REALITY SCAN
                     |
                     v
              PRIOR-ART MAP
                     |
                     v
        REUSE -> ADAPT -> EXTEND -> BUILD
                     |
                     v
             EXPLICIT DECISION
                     |
                     v
             RESUME ENGINEERING
```

## Problem contract

Before searching, define:

- exact capability or failure;
- current project constraints;
- what has already been tried when relevant;
- required safety/security/offline/degraded-mode properties;
- what evidence would materially change the decision.

Do not search for vague inspiration when the engineering question can be stated precisely.

## External source coverage

Use the sources appropriate to the problem. Coverage may include:

- official project/vendor documentation;
- GitHub repositories, releases, Issues, Discussions and pull requests;
- standards/specifications;
- academic papers and author/research-primary material;
- credible independent benchmarks/reproductions;
- mature downstream deployments and integration examples;
- hardware manufacturer documentation and ecosystem references;
- engineering forums, Stack Overflow, community reports and videos for discovery/failure evidence;
- security advisories and supply-chain information when relevant.

Community evidence may reveal candidates and failure modes. It does not automatically outrank official, reproducible or independently verified evidence.

## Minimum decision record

A triggered gate must leave enough durable evidence to reconstruct the decision:

### QUESTION
What exact problem was evaluated?

### EXTERNAL ANSWERS
What credible existing approaches were found?

### EVIDENCE
What supports or weakens each material approach?

### REUSE MAP
What can be reused directly, adapted, extended, or only learned from?

### DECISION
Exactly one primary strategy: `REUSE`, `ADAPT`, `EXTEND`, or `BUILD`.

### WHY
Why is that strategy preferred under project constraints?

### RECONSIDER WHEN
What upstream release, evidence, project constraint, failure, cost, license, security or ecosystem change should reopen the decision?

## No silent BUILD

A material `BUILD` decision must explicitly explain why:

1. REUSE is insufficient;
2. ADAPT is insufficient;
3. EXTEND is insufficient.

If that reasoning is absent, the gate has not passed.

BUILD is not forbidden. Unexamined BUILD is.

## Bounded research and stop rule

Technology Radar must accelerate engineering, not become research theatre.

Stop when:

1. the major credible candidate families are represented;
2. relevant official/primary evidence has been checked where available;
3. known strong prior art has been evaluated;
4. further searching is unlikely to change the decision or its uncertainty materially.

Record unresolved uncertainty instead of pretending the internet has been exhausted.

## Relationship to authorization

Radar research and a Radar decision do not automatically authorize:

- dependency installation;
- model or binary execution;
- production changes;
- private operational-state writes;
- credential/secret changes;
- device connections;
- real-world actuation or physical control.

Existing Project Engine authorization, branch, PR, CI, security and physical-safety rules remain in force.

## Relationship to risk Radar

This Technology Radar is distinct from the systemic-risk Radar.

- **Systemic-risk Radar** asks what is changing in the world and what it means for risk/lead time.
- **Technology Radar** asks what the external engineering world already knows, has built, or has learned about a capability/problem.

Both are external-reality mechanisms, but they serve different decisions.

## Permanent invariant

Every substantial engineering session must be able to answer:

1. Was a Major Decision Trigger present?
2. Was a Major Blocker Trigger present?
3. If yes, where is the Radar decision/evidence?
4. If BUILD was selected, where is the rejection reasoning for REUSE/ADAPT/EXTEND?

A triggered gate without a decision is an incomplete workflow state.
