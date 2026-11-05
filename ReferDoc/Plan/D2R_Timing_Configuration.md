# Accepted D2R timing configuration

Accepted: 2026-11-02. Authority: R-01 sections 55-58 and the existing simulator interview.
Use this table for nominal D2R airtime at the selected complete-TB byte values.
This is an accepted simulator timing configuration, not an implemented runtime interface or complete PHY validation.

## Fixed configuration

| Field | Accepted value |
|---|---|
| Procedure | CFA |
| Modulation | BPSK |
| Bit duration | tau = 400/3 microseconds = 2,000,000/15,000 microseconds |
| Channel coding | FEC enabled |
| Block repetition | 1 |
| CRC for these TB sizes | 16 bits |
| Preamble/midamble | Short, seven bits |
| Midamble interval | 96 bits (S*48 with S=2) |
| Additional midamble | Absent |
| Complete-TB Policy choices | tbs_bytes in {8,16,32,64} |
| Nonempty batch limit | Seven distinct Tags |
| Fixed SFS pool | {1,2,4,8,16,32,64} |
| Assignment | Stable Tag-ID order to ascending SFS entries |

## Nominal D2R duration table

SDU capacity is the maximum application payload with the accepted two-byte MAC format.
Actual SDU can be shorter; unused capacity is padding. Neither changes the chosen complete-TB airtime.
FEC redundancy, CRC and ambles do not supply useful application data.

| TB bytes | Maximum SDU bytes | Coded E bits | Transmitted V bits | Exact duration, ms | Display duration, ms |
|---|---:|---:|---:|---|---:|
| 8 | 6 | 240 | 261 | 174/5 | 34.800000 |
| 16 | 14 | 432 | 467 | 934/15 | 62.266667 |
| 32 | 30 | 816 | 879 | 586/5 | 117.200000 |
| 64 | 62 | 1584 | 1703 | 3406/15 | 227.066667 |

## Derivation and precision

For complete-TB size N bytes:

```text
A = 8*N
B = A + 16
E = 3*B
V = E + (1 + floor(E/96))*7
T_D2R_us = V*400/3
T_D2R_ns = V*400000/3
```

Keep exact rational durations through derivation. Display decimals are not scheduling constants.
R-01 section 68 selects UE-style ceil-to-ms scheduler occupancy. This table retains exact nominal PHY durations.
At fixed BD, the SFS chip count and chip duration cancel in this nominal duration expression.
The timing applies independently to each packet; do not sum all packet durations when their intervals overlap.
The batch end still follows the latest actual D2R end and its full Guard.

## Scope and remaining evidence

Included: the complete TB, CRC, FEC and all configured preamble/midamble bits.
Excluded: Paging airtime, R2D-to-D2R response offset and Guard.
Validate full-batch time, startup and mode energy separately; pure D2R fitting a window does not establish batch feasibility.
FEC protection does not guarantee successful reception. Receiver/FBL mapping and measured coding gain remain [Needs Verification].
Use seven fixed SFS resources {1,2,4,8,16,32,64} at tau, with at most seven Tags per batch.
Assign stable Tag-ID order to ascending SFS entries. Keep ideal mutual orthogonality and parallel responses.
The numerical pool now matches the batch limit. This does not establish measured orthogonality or receiver performance.

Sources checked for the preceding profile decisions:
- TS 38.391 V19.4.0 Table 6.2.1.6-1: local ReferDoc/Spec/A_IoT/TS_138_391_v19.4.0.pdf.
- TS 38.291 V19.3.0 clauses 6.1.2-6.1.4 and 7.1.1: local ReferDoc/Spec/A_IoT/TS38291_PHY.pdf.
- [Historical candidates and exact derivations](../../AgentDoc/openspec/discuss/2026-11-02-fixed-d2r-profile-candidates.md).

No source code, runtime configuration, energy parameters or receiver model is changed by this document.

## Accepted external Guard (2026-11-03)

R-01 section 63 fixes one 200-us Guard after the last D2R in a nonempty batch.
It is excluded from the individual packet durations above. Reader/CW recovery within that interval is an explicit unverified hardware assumption.
No Guard harvesting occurs; include its mode consumption and full interval in batch validation.

## Required Notebook explanation: stored-energy admission (2026-11-03)

The user requested this explanation in the future Jupyter Notebook; no Notebook implementation is started by this request.

- Explain that selecting a TBS requires enough stored energy for the complete planned operation, including applicable startup, waiting and mode costs.
- Show the D2R duration lookup and transmission-energy calculation with explicit units.
- The accepted D2R duration already includes CRC, FEC and ambles. Do not multiply the duration or energy by three again.
- Assume no energy harvesting during D2R. External CW enables reflection; it does not make Tag circuitry consume zero energy.
- Reject a TBS whose full operation exceeds stored energy. A smaller legal TBS or a later feasible opportunity can be used.
- A completed transmission consumes its full modeled energy even if reception fails; failed data earns no service credit and remains available.
- Separate illustrative power values from source-backed Tag parameters. Actual support for the longest packet remains [Needs Verification] until parameters are selected.

This documentation request does not resolve Q-INFLUENCE-36's CRC/FBL interpretation. Influence remains 36.

## Accepted scheduler occupancy conversion (2026-11-03)

R-01 section 68 applies ceil(duration_ms)*1000000 to each complete D2R operation.
For 8/16/32/64 bytes, occupancy is 35/63/118/228 ms; nominal physical times above remain unchanged.
Do not round individual chips or multiply FEC overhead again. Fixed Guard remains 200000 ns.
Track rounding slack explicitly in the event and mode-energy derivation. Runtime implementation remains pending.
