# Energy Resilience Verification v0.1

## Core principle

`PV present ≠ outage power`  
`Battery nameplate ≠ usable energy`  
`Inverter present ≠ islanding`  
`Islanding ≠ black-start`

Energy resilience is the ability to keep **defined critical loads** operating after normal external power is lost.

## Verification chain

`Generation → Storage → Conversion/Transfer → Critical Loads → Islanding → Black Start → Outage Test → Maintenance/Spares`

## Verification ladder

### stated
Assets are reported/present, but there is no defensible measured usable capacity or load baseline.

### measured
At least one relevant usable quantity is measured:
- PV delivered/peak output;
- usable battery kWh;
- battery continuous output;
- critical peak load;
- critical daily energy;
- measured outage energy served.

Nameplate-only PV/battery figures are not enough to establish resilience.

### field_tested
Requires:
- outage test passes for a positive duration;
- islanding is tested or genuinely not applicable;
- black-start is tested or genuinely not applicable;
- critical loads are mapped;
- critical daily energy is known;
- essential circuits are actually tested.

### audited
Field-tested plus:
- evidence complete;
- maintenance current;
- independent review;
- no unresolved SPOF;
- critical dependencies have a ready/not-required backup.

## Storage autonomy

When usable battery energy and critical daily demand are both defensible:

`storage_autonomy_days = usable_kWh / critical_kWh_per_day`

This is storage-only autonomy. It does not include future solar production unless the scenario model explicitly validates generation and weather assumptions.

## Renewable sustaining candidate

PV can be marked as a sustaining candidate only when:
- measured PV output exists;
- islanding works;
- black-start works;
- outage test passes;
- critical loads are known.

Even then, the system does not assign infinite autonomy. Renewable output varies with weather, season, equipment condition and load.

## Field evidence

Collect:
1. PV/inverter/battery/generator inventory and nameplates
2. actual system topology
3. islanding capability
4. black-start capability
5. usable battery kWh and power limit
6. critical-load inventory and measured demand
7. generator/fuel path if present
8. controlled outage-test result
9. inverter/BMS/controller/network dependencies
10. spares and maintenance

Electrical-panel inspection, switching and controlled grid-loss tests should be performed by qualified personnel under a safe site procedure.
