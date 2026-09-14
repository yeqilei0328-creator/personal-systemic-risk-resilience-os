# Commercial / Ecosystem Radar

## 1. Purpose

This control validates external commercial/ecosystem assumptions that can materially change an engineering, procurement or preparedness decision.

It is **not** the Systemic-Risk Radar and it is **not** the Technology Radar.

Examples:
- vendor/product availability;
- platform/service commercial viability;
- procurement lead time/cost assumptions;
- market support for a capability;
- ecosystem maturity;
- customer/field evidence when a product claim depends on real adoption.

## 2. Modes

### DISCOVERY
Use when the project needs an initial bounded view of vendors, products, market/economic availability or ecosystem options.

### VALIDATION
Use when an existing commercial thesis/evidence has changed or is contradicted.

### DECISION
For a major product/architecture/capability decision, pair with Technology Radar as `DUAL_RADAR_MAJOR_DECISION` where technical and commercial reality are both material.

## 3. Trigger families

Discovery triggers include:
- `market_assumption_change`;
- `commercial_debt_change`.

Validation triggers include:
- `commercial_evidence_change`;
- `customer_zero_evidence_change`;
- `external_m2_or_higher_evidence_change`;
- `commercial_thesis_contradiction`.

Dual triggers include:
- `major_product_decision`;
- `major_architecture_decision`;
- `next_major_technical_iteration`;
- `critical_path_rebaseline`;
- `new_capability_family`;
- `new_industry_pack`.

## 4. Evidence separation

Internal preference is not external validation.

```text
CUSTOMER_ZERO != EXTERNAL_M2
```

A user/Owner preference can guide constraints but cannot be silently promoted into vendor/market/customer evidence.

## 5. Triggered disposition

When triggered:

```text
gpt_handoff_required = true
local_execution_disposition = STOP_LOCAL_SPECULATION_ALLOW_READONLY_EVIDENCE
resume_condition = RADAR_RESULT_RECONCILED_BY_GPT_CONTROL_PLANE
```

Permitted while stopped:
- read-only research;
- evidence preservation;
- state capture;
- comparison/decision analysis.

Not permitted by Radar alone:
- purchase/payment;
- contract acceptance;
- account/credential mutation;
- dependency installation with material side effects;
- production/private writes;
- device/physical execution.

## 6. Output

A commercial/ecosystem decision record should capture:
- question;
- constraints;
- evidence and date;
- source quality/independence;
- options;
- contradiction/counterevidence;
- decision;
- confidence/known unknowns;
- reconsideration trigger;
- authority required for the next action.