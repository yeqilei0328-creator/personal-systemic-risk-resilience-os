# ADR-0006: Preserve Existing News Radar and Integrate Physical AI by Handoff

Status: Accepted

## Decision

Preserve the existing news-push conversation as the user-facing intelligence product.

Phase 3R upgrades the backend precision engine rather than replacing the presentation model.

Physical AI remains a module inside the news product, but project-relevant Physical AI signals are handed off into the existing Physical AI Technology Radar rather than creating a second technical-radar authority.

## Interface

`News Radar / Physical AI module`
→ verify / dedup / cluster / compress
→ project-relevant handoff
→ `TECH-RADAR-04 Observation Packet + human-reviewed admission`
→ existing TECH-RADAR-01/02/03 governance

## Invariants

- P0/P1/P2 remains news attention priority.
- TECH-RADAR-01 ASSESS/TRIAL/ADOPT/HOLD remains engineering decision state.
- TECH-RADAR-04 REJECT/DEFER/WATCH/PROMOTE_TO_V1_RESEARCH/PROJECT_EVIDENCE_RECONCILIATION remains upstream admission routing.
- WATCH is not ADOPT and is not a TECH-RADAR-01 state.
- News discovery cannot grant engineering/physical authority.
- Raw news streams do not enter the Physical AI engineering repository.
- Existing front-end briefing behavior is preserved unless explicitly changed.
- Future MD/spec reconciliation may refine this baseline without silent replacement.
