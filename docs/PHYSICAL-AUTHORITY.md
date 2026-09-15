# Physical Execution Authority

## 1. Scope

Applies to real:
- camera / microphone;
- robot / drone / UGV;
- arm / PLC;
- vehicle;
- other physical device or actuator.

Physical AI remains defensive/non-weaponized in this project.

## 2. Physical Execution Authority Envelope

Before physical execution, define:

```text
device
operation
duration
environment
allowed_commands
forbidden_commands
stop_condition
retry_policy
evidence
exact_main_sha
exact_implementation_sha
gate_fingerprint
```

Missing/unknown/conflicting required fields cause `FAIL_CLOSED`.

## 3. Separation of concerns

Keep four states distinct:

```text
proposal
approval
execution
verification
```

A proposal is not approval. Approval is not execution. Execution is not verification.

## 4. Non-authoritative proposal pattern

AI-derived operational suggestions follow:

```text
Event
→ Incident
→ TaskProposal
```

`TaskProposal` defaults to:

```text
authoritative = false
execution_allowed = false
```

Only a canonical authorized task with a valid Physical Execution Authority Envelope may cross into physical execution.

## 5. RED consumption

The authorization record must define the precise consumption boundary, for example:
- before device connection/open: not consumed;
- after actual connection/open or command dispatch: consumed.

Once RED is consumed:

```text
automatic_retry = 0
```

A second real attempt requires diagnosis and fresh Owner authorization.

## 6. Evidence

Prefer sanitized metadata, hashes and aggregate outcomes. Do not persist raw secrets, local paths, raw camera identifiers, pixel/biometric traces or unnecessary sensitive deployment details.

## 7. Emergency/stop condition

The stop condition overrides mission continuation. A system unable to verify its own authority envelope or stop condition must fail closed.