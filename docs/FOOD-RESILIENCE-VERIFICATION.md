# Food Resilience Verification v0.1

## Core principle

Food resilience is not a pile of groceries.

It is six separate questions:

1. **Buffer** — how many measured usable food-days exist now?
2. **Nutrition** — is the stored plan nutritionally complete enough to be defensible?
3. **Storage** — what survives without refrigeration and how is spoilage controlled?
4. **Cooking** — can stored food still be prepared during a utility outage?
5. **Replenishment** — can food be replaced through independent supply paths?
6. **Production support** — can local production contribute measured output?

The model deliberately prevents these concepts from collapsing into one claim.

## 1. Inventory buffer

Measured buffer days are:

`usable food calories / measured daily calorie demand`

Shelf-stable buffer days are calculated separately.

No daily demand baseline → no food-days claim.

The method does not prescribe the user's dietary intake. Private demand values must be established from the actual household/base plan.

## 2. Nutrition gate

Calories alone are not enough.

The v0.1 nutrition gate requires a reviewed plan that maps:
- protein sources;
- fat sources;
- micronutrient strategy;
- dietary constraints;
- special requirements.

This is an audit completeness gate, not medical nutrition advice.

## 3. Storage gate

Storage resilience considers:
- dry storage;
- pest/moisture control;
- cold-chain dependence.

If food is critically dependent on refrigeration, cold-chain outage continuity must be demonstrated.

Shelf-stable calories are therefore a particularly useful buffer metric.

## 4. Cooking gate

Food that cannot be safely prepared during an outage may not be a usable buffer.

The gate separates:
- normal cooking path;
- backup path;
- outage cooking test.

The method does not prescribe a specific fuel technology.

## 5. Replenishment diversity

Two shops do not necessarily mean two supply chains.

A replenishment path counts only when:
- it is verified available; and
- its independence group is known.

Two verified paths sharing one independence group count as one.

For `sustained_resilience`, the replenishment gate requires:
- at least two independent verified supply paths; or
- measured local production support.

## 6. Local production / conversion

Local production is tracked separately from inventory.

A production-support candidate requires:
- measured/field-tested output;
- positive daily calorie equivalent;
- production inputs mapped.

Land ownership, soil availability or a planting idea do not satisfy this gate.

Most importantly:

> local production does not increase current inventory buffer days.

This prevents an unverified garden from turning into imaginary infinite autonomy.

## 7. Verification ladder

### stated
Food presence/gap may be known, but measured inventory + daily demand are incomplete.

### measured
Measured inventory and daily demand establish a defensible buffer.

### field_tested
For `emergency_buffer`:
- inventory
- nutrition
- storage
- outage cooking

must pass.

For `sustained_resilience`, replenishment must also pass.

### audited
Field-tested plus:
- independent review;
- rotation tested;
- maintenance current;
- evidence present;
- no unresolved SPOF;
- critical dependencies backed/not-required.

## 8. Preparation architecture

A practical preparation sequence is:

### Layer 1 — shelf-stable buffer
Build a rotating stock that does not require the cold chain.

### Layer 2 — nutrition completeness
Ensure the buffer is not merely starch.

### Layer 3 — storage / cooking continuity
Protect inventory and make sure it remains usable during utility loss.

### Layer 4 — replenishment diversity
Avoid one supplier/logistics dependency.

### Layer 5 — production conversion
Only after the buffer is sound, audit land/soil/water/inputs/time/skills for supplementary production.

This is intentionally less cinematic than "become self-sufficient". It is also much more likely to work.
