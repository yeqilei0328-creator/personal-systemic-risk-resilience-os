# Execution Router

## 1. Control and execution planes

Recommended operating split:

```text
GPT = Control Plane
Desktop = Default Local Execution Plane
Codex = Escalated Specialist Engineer
CI = Independent deterministic verification plane
External Research = read-only evidence plane unless separately authorized
```

The execution router does not determine authority. Authority is classified separately.

## 2. GPT_ONLY

Use for:
- architecture judgment;
- roadmap;
- governance;
- audit;
- product decision;
- Radar synthesis;
- Owner gate preparation;
- evidence interpretation.

## 3. GPT_DESKTOP

Default routine engineering:
- Git;
- terminal;
- file inspection;
- environment checks;
- existing tests;
- deterministic edits;
- config/scripts/logs;
- local evidence;
- branch/PR preparation.

Routine engineering should not escalate merely because a specialist agent exists.

## 4. GPT_DESKTOP_CODEX

Escalate when one or more are true:
- substantial multi-file code;
- complex feature;
- new test design;
- complex refactor;
- CI failure investigation;
- runtime/SDK/dependency bug;
- uncertain root cause;
- disciplined fix failed;
- same blocker repeated twice;
- cross-module behavior;
- architecture-sensitive implementation;
- long autonomous fix loop;
- conversational patch count exceeds two.

## 5. Model Router

Choose the lowest sufficient model:

```text
LUNA  = mechanical
TERRA = routine engineering
SOL   = complex professional engineering
ASTRA = hardest / unfamiliar / cross-layer
```

Reasoning effort:

```text
LIGHT
MEDIUM
HIGH
EXTREME
```

## 6. Router Header

For material work units:

```text
AUTHORITY_ROUTER = GREEN / AMBER / RED
EXECUTION_ROUTER = GPT_ONLY / GPT_DESKTOP / GPT_DESKTOP_CODEX
MODEL_ROUTER = LUNA / TERRA / SOL / ASTRA
REASONING_EFFORT = LIGHT / MEDIUM / HIGH / EXTREME
FALLBACK_ROUTER = <explicit route>
```

## 7. Fallback rules

- Environment/toolbox mismatch: diagnose environment first.
- Two disciplined patches without resolution: escalate execution tier and/or Technology Radar.
- External SDK/platform behavior with low root-cause confidence: Technology Radar before speculative widening.
- Authority changes during work: stop and re-run Authority Router.
- Reality failure: stop local speculation and evaluate Reality/Strategic Capture state.

Execution capability must never be used as a substitute for Owner authority.