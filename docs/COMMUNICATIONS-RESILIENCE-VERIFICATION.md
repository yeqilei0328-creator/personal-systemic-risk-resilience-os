# Communications / Network / Offline Compute Verification v0.1

## Core principle

`Internet available ≠ resilient communications`

`Wi-Fi present ≠ internal control survives internet loss`

`two links ≠ two independent links`

The communications domain is split into four gates:

1. **Internal LAN**
2. **External Communications**
3. **Offline / Local Compute**
4. **Power**

A fifth layer, **degraded-mode testing**, is what converts architecture claims into demonstrated resilience.

## 1. Internal LAN

Questions:
- Is the internal topology mapped?
- Is there a critical backbone?
- Can the LAN remain usable after external internet loss?
- Can local control paths operate without cloud reachability?

A router showing green lights is not evidence that local control/auth/time/data dependencies continue to work.

## 2. External communication paths

External links may include:
- fiber
- cellular
- satellite
- radio
- other appropriate paths

The method does not assume any technology is legally or operationally available in a particular jurisdiction. Deployment-time evidence decides that.

### Independence

Two tested links count as redundant only when they belong to at least two distinct `independence_group_id` values.

This prevents false redundancy such as:
- two logical links sharing one upstream;
- two SIMs that ultimately depend on the same infrastructure;
- a primary and backup path with the same critical power/control dependency.

The method records independence groups; it does not guess them.

## 3. External continuity lower bound

For each independence group:
- take the best demonstrated tested runtime.

Then:
- take the minimum across at least two independent groups.

This becomes the demonstrated redundant external-continuity lower bound.

It is not an infinite-autonomy claim.

## 4. Offline / local compute

For the full resilient stack:
- local compute must be present;
- critical workloads must be identified;
- local runtime must be tested;
- cloud dependency cannot remain critical;
- required offline data/knowledge must be locally accessible.

Principle:

> 云端可增强，本地可独立降级运行。

## 5. Power gate

Critical networking/compute assets require a known power path.

The gate requires:
- critical power path mapped;
- backup power ready/not-required;
- outage test pass/not-required.

A UPS box in a rack is not enough. Runtime must be demonstrated where backup power is actually required.

## 6. Verification ladder

### stated
Assets/topology are reported, but no measured/tested continuity exists.

### measured
At least one meaningful continuity measurement/test exists, but required service-scope gates are incomplete.

### field_tested
All gates required by the chosen service scope pass.

Scopes:
- `internal_network`
- `external_communications`
- `full_resilient_stack`

### audited
Field-tested plus:
- independent review;
- maintenance current;
- evidence present;
- no unresolved SPOF;
- critical dependencies backed/not-required.

## 7. Full resilient stack

Requires all four:
- Internal LAN gate
- External Redundancy gate
- Offline Compute gate
- Power gate

This is the basis for graceful degradation:

`Internet Down ≠ System Down`

## 8. Security boundary

This public method repository stores:
- schemas
- algorithms
- synthetic examples
- audit rules

It must not store:
- real network topology
- real provider identities
- radio/satellite identifiers
- credentials
- IP plans
- security access details
- exact private runtime capacities

Those belong in the private operational-state layer.
