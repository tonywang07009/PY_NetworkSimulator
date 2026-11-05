# CFA Paging R2D configuration

Accepted fixed configuration: 2026-11-02, R-01 sections 60-63. The fixed batch-local timing convention below is current.
Use individual Paging for each selected Tag, with the accepted final batch-Paging response reference.

| Field | Accepted configuration |
|---|---|
| Addressing | Permanent ID; optional domain fields absent |
| Identification content | 32 bits |
| Permanent ID including ID Type | 40 bits |
| Complete Paging ID including outer type | 42 bits |
| Mandatory security parameter | Present, 128 bits; count airtime without claiming cryptographic implementation |
| Complete CFA Paging TB | 27 bytes |
| R2D chips per OFDM symbol | 24 for applicable R2D portions |
| Minimum PRBs | 3 for CAP/PRDCH/postamble/padding; separate SIP mapping |
| Subcarrier spacing | 15 kHz |
| Total R2D OFDM symbols | 24 per Paging, including the specified framing/padding |
| Inter-Paging gap | Zero |
| CP sequence | Continuous across messages in the batch |
| Batch-local CP phase | Long CP at symbol indices n modulo 7 = 0; first batch-local symbol n=0 |
| Seven-message Paging phase | Exactly 12 ms |
| Post-D2R Guard | 200 us = 0.2 ms = 200000 ns, once per nonempty batch |
| Recovery assumption | Reader/CW recovery finishes within the fixed Guard; not hardware-validated |

The ID profile is fixed simulator scenario configuration, not an extra Policy decision.
Keep unique full identifiers across the deployment; internal labels such as Tag-001 are not the encoded ID length.

## Complete field and chip calculation

MAC bits = 3+7+1+128+1+10+42+24 = 216 = 27 bytes.
CRC adds 16 bits; R2D line coding gives 2*(216+16)=464 chips.
CAP adds four chips and postamble adds four: 472 useful chips after SIP.
The 24-chip format reserves two positions per symbol, giving 22 useful positions.
ceil(472/22)=22 symbols, plus two SIP symbols = 24 OFDM symbols per Paging.

## CP-dependent time

Source: TS 38.291 V19.3.0 clause 6.2.7.
Each symbol is (2048+144)/30720000 seconds, with an extra 16/30720000 seconds at the long-CP phase modulo seven.
A 24-symbol interval contains three or four long CPs, depending on alignment.

| Case | Nominal physical duration |
|---|---:|
| One Paging, three long CPs | 1.714062500 ms |
| One Paging, four long CPs | 1.714583333... ms |
| Seven back-to-back Paging messages with a continuous CP phase | 12 ms exactly |

The user now accepts a fixed back-to-back configuration with continuous CP phase and zero inter-message gaps.
Use batch-local symbol index n=0 at the beginning of the first Paging and a long CP when n modulo 7 is zero.
Continue n across messages; do not restart the CP phase at each individual Paging.
This is the selected simulator timing convention. It does not establish alignment with an external NR frame clock.
Seven messages contain 168 symbols and 24 long CPs, giving exactly 12 ms.
For 1-6 selected Tags, send only that number of messages and use the corresponding table prefix.
Empty NO_OP sends no Paging. Do not reserve 12 ms for a smaller batch or use 12/7 ms per packet.

| Paging index | Long CP count | Exact message ms | Display message ms | Exact cumulative ms |
|---|---:|---|---:|---|
| 1 | 4 | 823/480 | 1.714583333 | 823/480 |
| 2 | 3 | 1097/640 | 1.714062500 | 6583/1920 |
| 3 | 4 | 823/480 | 1.714583333 | 1975/384 |
| 4 | 3 | 1097/640 | 1.714062500 | 6583/960 |
| 5 | 4 | 823/480 | 1.714583333 | 2743/320 |
| 6 | 3 | 1097/640 | 1.714062500 | 6583/640 |
| 7 | 3 | 1097/640 | 1.714062500 | 12 |

Use exact fractions in derivation; integer-ns conversion remains open under AP-06.
Do not round each OFDM symbol or display decimal independently.
Actual external NR in-band alignment and any resulting additional alignment wait require separate integration evidence.
No hidden alignment wait is included in the accepted 12 ms nominal Paging phase.

## Remaining batch construction

Let P_end be the selected table prefix end relative to the batch Paging start. Extra global alignment waits, if later required, must be explicitly accounted for.
Each Tag starts D2R at P_end plus its configured response offset under the accepted simulator reference abstraction.
The final D2R end is max_i(start_i + selected_D2R_duration_i).
Append one full 200-us Guard after that end. Turn CW off at the final D2R end; no Guard harvesting. Keep mode costs, window limits and each service deadline.
Guard is fixed by R-01 section 63. Response-delay table verification, external NR alignment and full batch/energy feasibility remain open.
This is not permission to add arbitrary physical timing constants or assume successful R2D reception.

Sources: TS 38.391 V19.4.0 clause 6.2.1.1; TS 23.003 V19.6.0 clauses 31.2/31.7;
TS 38.291 V19.3.0 clauses 4.3 and 6.2. Source links and history are in
[the batch timing evidence](../../AgentDoc/openspec/discuss/2026-11-02-batch-response-timing.md).

## Accepted occupancy conversion (2026-11-03)

R-01 section 68 selects the existing UE ceil-to-ms rule for scheduler occupancy.
Apply it to cumulative Paging prefix boundaries from the batch origin, not each message duration before summation.
Keep the exact nominal table and continuous CP sequence; seven messages remain 12 ms.
Fixed Guard stays 200000 ns. Boundary integration and runtime implementation remain pending.

## 2026-11-03 | RF hardware evidence and transition clarification

R-01 section 71 records the user-confirmed UE-end -> RF transition -> Tag-band procedure.
The transition is inside the 600-ms window, before Tag-band operations, and separate from the 200-us final Guard.
No duration is selected; no source-free harvesting credit or extra payload is assumed during transition.
ReferDoc/Plan/RF_Hardware_and_Frequency_Switching_Evidence.md records TMTT/NSDI hardware evidence and X310/SBX/AD9361 official links.
The future Notebook must show the transition interval, remaining Tag budget and evidence limits.
No simultaneous dual-band requirement or change to the equivalent 915-MHz profile is introduced. Influence stays 38.
