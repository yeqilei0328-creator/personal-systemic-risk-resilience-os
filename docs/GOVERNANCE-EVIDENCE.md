# Governance Evidence Contract

## 1. Rules / State / Evidence

Keep these separate.

### Rules
Define what should happen: authority, routers, gates, retry/stop policies.

### State
Defines the current position: branch/head, attempt state, authority consumed state, blocker, next authorized node.

### Evidence
Proves the state: SHA, tests, CI, logs/fingerprints, runtime/tool versions, review state and bounded real-world evidence.

A rule is not evidence. A claim in chat is not durable state.

## 2. Durable locations

Use as appropriate:
- Issue / PR body or comments;
- `docs/PROJECT-STATE.md`;
- evidence JSON/artifacts;
- closeout report;
- CI/status records.

Do not turn one file into an unstructured dumping ground.

## 3. Minimum closeout record

```text
result
exact_sha
tested_head
pr_head
origin_main
merge_base
focused_test_result
full_regression_result
static_integrity_result
ci_result
authority_level
authority_granted_state
authority_consumed_state
retry_state
radar_verdict
reality_level
known_unknowns
next_authorized_node
```

Not every field applies to every task, but missing required fields must be explicit rather than guessed.

## 4. Evidence fingerprint

For critical decisions/trials/gates:

```text
canonical JSON
→ SHA-256
```

The fingerprint can bind:
- gate contract;
- exact main/tool SHA;
- exact authority envelope;
- evidence bundle.

A filename alone is not a content identity.

## 5. Exact-head evidence

Before merge:

```text
tested_head == pr_head
origin_main = current intended base
merge_base = known
```

If the head changes, prior exact-head evidence is stale and CI/gates must be rerun.

## 6. Test layers

Record separately:
- Focused;
- Full Regression;
- Static / Integrity;
- CI.

Do not treat one focused test as repository-wide evidence.

## 7. Post-merge evidence

A merged PR is not a completed work unit.

Post-merge evidence records:
- merged `main` SHA;
- expected content present;
- required focused/full/static checks after merge;
- Project State/Issue closeout updated only after verification.

Final durable state:

```text
MERGED
+
POST_MERGE_VERIFIED
```

## 8. Privacy / secret discipline

Repository evidence must not contain:
- tokens/authorization headers/passwords/private keys/recovery codes;
- personal local paths;
- raw camera/microphone identifiers;
- unnecessary pixel/biometric traces;
- sensitive operational topology in PUBLIC.

Prefer hashes, generic classes, aggregate statistics and sanitized metadata.