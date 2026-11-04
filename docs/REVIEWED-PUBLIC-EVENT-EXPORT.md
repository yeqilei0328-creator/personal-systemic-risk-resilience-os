# PSRRO Reviewed Public Event Export v0.1

Issue: https://github.com/yeqilei0328-creator/personal-systemic-risk-resilience-os/issues/53

## Scope

One-shot, offline operator-reviewed PUBLIC evidence packet -> standard PSRRO EventClaimStateStore and SourceStateStore native files.

This is a small producer for RIOS World Intelligence Issue #57. It is not a web scraper, narrative-to-event extractor, external provider, live listener, or automated news production service. The producer neither contacts nor authenticates article URLs. A human reviewer must check the claims and source status before preparing the packet.

Existing schemas and the existing library APIs are reused unchanged. The full JSON Schema validation uses the repository's existing development dependency jsonschema.

## Governance and authority

- User requested continuation on 2026-11-04 of the already defined real-source shadow gate. Engineering bounded to AMBER source-interface implementation, with GPT_DESKTOP / SOL / HIGH and fail-closed fallback.
- Public method code only; no private preparedness state and no production or restricted-data writes.
- Source-policy widening, live feed, automated fetch, alert transport and change of provider class are explicitly excluded.
- Contract baseline: 574b17ade4ee52628ccf5806e0f129e8fd267b0e.
- Technology Radar disposition: REUSE existing event/claim/assessment/observation schemas and stores; implement only the minimal reviewed packet adapter.
- An Event Store first-discovery material marker does not imply real-world systemic transmission.

## Input and validation

The operator-prepared JSON must contain:
- packet_version = psrro-reviewed-public-event.v0.1;
- review_mode = human_reviewed_public_sources; reviewed_at and review_notes;
- event_state, claims, source_observations and material_change using existing schemas.

The exporter validates full upstream schemas, event fingerprint recomputation, event/claim/source relationships, reference uniqueness, timing, public sensitivity, HTTPS source locators, source access honesty and an initial-event assessment. Unsupported or conflicting inputs fail before writing.

## Output and safety

The CLI accepts only a NEW directory under the system temporary location (/tmp also supported on macOS). It atomically publishes the export directory after validation and isolated generation. It refuses any preexisting destination; no overwrite or unsafe retry.

Native files:
- events/evt-*.json;
- claims/clm-*.json;
- material-change/evt-*/mca-*.json;
- observations/sob-*.json.

An additional review-manifest.json records the packet's canonical SHA256, per-file SHA256, published source locators and a list of limitations. The manifest does not include copied news text, a claim of article-body preservation, or a source independence score. The output status is NATIVE_REVIEWED_EXPORTED (human-reviewed, one-shot).

## Usage

From the PSRRO checkout, with the existing development requirements installed:

PYTHONPATH=src python scripts/export_reviewed_event.py --packet /tmp/reviewed-packet.json --scratch-output-root /tmp/psrro-reviewed-export-unique

A fresh directory is required. Confirm its manifest, then pass the new native-store root to RIOS read-only shadow_native.py. No automatic forecast, notification or global-systemic-risk transition occurs.

## Demonstration (2026-11-04, source-verified by operator)

The 2026-11-03 PBOC announcement of the future 2026-11-15 FX deposit reserve requirement ratio change (4% -> 6%) was corroborated from PBOC's statement reproduced by Xinhua and contemporaneous Reuters reporting. Both source observations ultimately refer to the same central-bank announcement; they are not treated as independent policy-origin events.

- Source 1: https://www.xinhuanet.com/fortune/20261103/80f848e7f7e547b2a7b72ef4c64c3262/c.html
- Source 2: https://www.reuters.com/world/asia-pacific/china-raise-forex-deposit-reserve-ratio-6-starting-november-15-2026-11-03/

The operator-curated packet was written to an external, untracked scratch file; it is not committed to this public method repository. The native export was read by RIOS and produced SHADOW_VALIDATED_NATIVE with first CREATED, then IDEMPOTENT, 5 source files hashed; forecast UNMATCHED, structural_delta_material false. The first observation is an actual public policy announcement, not a synthetic event, though its structured representation was manually produced.

## Evidence and reality limits

- This establishes a one-shot, reviewer-assisted real-public-event source path (first-real-signal trial), not a continuously operating native feed.
- Source URL presence and human review do NOT imply independent machine attestation, authenticated original web archive, or demonstrated predictive accuracy.
- The 2026-11-15 policy has not yet been observed in force as of the 2026-11-04 packet capture.
- No raw PDF/HTML/article text, private preparedness data or credentials are stored in this public method branch.
- Future automatic producer, trigger, scheduling, event source admission and ongoing calibration require separately reviewed work units.
