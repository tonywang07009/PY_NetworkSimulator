# RF hardware capabilities and frequency-switching evidence

Recorded: 2026-11-03. Scope: traceable hardware support for a system-level simulation assumption.
This record separates measured research results, manufacturer specifications and simulator assumptions.
It does not select a board, fix switching latency or establish complete 3GPP conformance.

## Conclusion for the system model

A configurable RF front end can switch between communication and Tag operating frequencies.
An explicit transition interval between UE communication and Tag access is supported by existing hardware mechanisms.
Concurrent multiband transmission is also documented, but it is not required by this time-separated model.
The cited evidence supports architectural plausibility, not a measured end-to-end 3.5-GHz-to-915-MHz transition bound.

## Recorded hardware characteristics

| ID | Source and type | Hardware characteristics | What can be cited |
|---|---|---|---|
| HW-01 | Chung et al., IEEE TMTT 63(2), 598-613, 2015; peer-reviewed prototype | Two GaN Class-D power amplifiers and a Chireix combiner; concurrent 240/500-MHz LTE signals with 15-MHz aggregate bandwidth; reported out-of-band emissions -30/-37 dBc. | Non-contiguous multiband transmission is physically implemented. These frequencies and emissions are not our hardware parameters. |
| HW-02 | Katanbaf, Weinand and Talla, NSDI 2021, 955-972; peer-reviewed backscatter system | Commodity LoRa components, hybrid coupler and tunable impedance network; reported 78-dB carrier cancellation. | Co-located carrier transmission and backscatter reception can be implemented with explicit isolation/cancellation. The result is not a universal isolation requirement. |
| HW-03 | Ettus X310/SBX; official manufacturer documentation | X310 has two compatible RF daughterboard slots. SBX covers 400 MHz-4.4 GHz, supports 40/120-MHz variants and independent TX/RX synthesizers. | Candidate RF hardware can cover both 915 MHz and 3.5 GHz. Tuning range does not establish a complete-system switching time or every simultaneous configuration. |
| HW-04 | AD9361 Rev. G and UG-570 Rev. A; official manufacturer documentation | TX 47 MHz-6 GHz, RX 70 MHz-6 GHz; TDD/FDD support. Fast-lock memory stores eight RX and eight TX frequency profiles including VCO calibration results. Profiles can be recalled through SPI or control pins. | Frequency reconfiguration and pre-calibrated profile switching are explicit hardware functions. Two TX channels do not by themselves prove arbitrary independent simultaneous TX carriers. |
| HW-05 | AD9361 Frequency Hopping Example Design; official implementation example | Describes PLL unlock/recalibration during tuning and invalid data until relock. Fast-lock example reports approximately 15-25 us LO locking, depending on configuration and frequency. | A finite settling interval is justified. The example is not a worst-case 3.5-GHz/915-MHz hop or an end-to-end DU/Reader bound. |

## Direct source links

| ID | Publication or official source | Location |
|---|---|---|
| HW-01 | [MERL publication record](https://www.merl.com/publications/TR2015-004), [author PDF](https://www.merl.com/publications/docs/TR2015-004.pdf), DOI 10.1109/TMTT.2014.2387845 | Abstract and prototype measurements |
| HW-02 | [NSDI proceedings record](https://www.usenix.org/conference/nsdi21/presentation/katanbaf), [author manuscript](https://arxiv.org/html/2011.03952) | Abstract; sections 2-4 |
| HW-03 | [X310 official documentation](https://kb.ettus.com/X300/X310), [SBX official documentation](https://kb.ettus.com/SBX) | Device overview; features; RF specifications |
| HW-04 | [AD9361 data sheet](https://www.analog.com/media/en/technical-documentation/data-sheets/AD9361.pdf), [UG-570 reference manual](https://www.analog.com/media/en/technical-documentation/user-guides/ad9361.pdf) | Data sheet page 1; UG-570 pages 22-23, Fast Lock Profiles |
| HW-05 | [Frequency Hopping Example Design](https://wiki.analog.com/resources/eval/user-guides/adrv936x_rfsom/tutorials/frequency_hopping) | AD9361 Fastlock for Fast Frequency Hopping |

The 15-25-us value is vendor implementation evidence, not a peer-reviewed result or a selected model constant.
The 78-dB value concerns carrier cancellation, not frequency-switching latency.
The TMTT concurrent-transmitter paper does not establish a retuning gap.

## User-confirmed transition structure

The user states that the system model already includes an interval after UE transmission for frequency switching.
Record this clarified requirement explicitly; do not claim it already exists in simulator code.

```text
UE communication ends
    -> RF frequency/mode transition and settling interval T_switch
    -> Tag-band access (existing individual Paging sequence)
    -> CW and parallel D2R responses
    -> existing 200-us batch-end Guard
```

T_switch occurs at the UE-to-Tag phase transition, not once per Tag or per later Tag batch without another RF transition.
Keep it separate from the 200-us post-D2R Guard and the Paging-to-D2R response offsets.
Count the transition interval inside the 600-ms window and reduce the available Tag-phase time accordingly.
Do not start a Tag-band operation before the required RF configuration is ready.
Do not count useful payload or assume harvested energy without an active compatible source during transition.
Preserve applicable Tag mode consumption and stored-energy admission.
The numerical transition duration is unspecified; do not silently assign zero, 200 us or the vendor's PLL-only example.
The first-version equivalent 915-MHz abstraction does not eliminate physical RF/mode-switching overhead.
The 3.5-GHz/915-MHz pair remains a motivating hardware example, not a newly accepted carrier profile.
No simultaneous UE communication and Tag response is required by this clarification.

## Defensible research wording

The model assumes a reconfigurable reader RF front end that time-shares UE communication and Tag access.
It reserves a nonzero transition interval for frequency reconfiguration and settling before Tag-band operations.
Frequency-agile transceiver documentation supports this architecture; the transition duration remains an explicit model parameter.
Results should identify the selected parameter and its evidence or sensitivity range.
The model does not claim a measured switching bound or a validated implementation of a specific frequency pair.

Peer-reviewed papers support related multiband and backscatter architectures.
Primary manufacturer documentation directly supports the retuning mechanism.
Together they provide a defensible basis for a stated system-level abstraction; they do not guarantee publication acceptance.
Standards conformance and hardware feasibility for a selected complete implementation remain separate claims.

## Notebook and verification notes

The future Notebook must show this phase boundary, T_switch units, source links and the remaining Tag-window budget.
It must distinguish nominal PHY durations, rounded occupancy, RF transition time, response offsets and the final Guard.
No numerical switching value, actual hardware purchase, simulator implementation or publication is authorized by this record.
Source and Markdown diff checks only; no RF measurement or runtime tests. Exact transition performance remains [Needs Verification].

## RedCap and SUL source-profile evidence (2026-11-03)

These entries concern standards and a research extension, not measured retuning hardware.

- [TS 38.300 V19.4.0](https://www.etsi.org/deliver/etsi_ts/138300_138399/138300/19.04.00_60/ts_138300v190400p.pdf), clauses 5.4.2/6.9 and Annex B.1: SUL supplements the normal uplink; the network selects transmission on normal UL or SUL, not both simultaneously under the described single-cell model.
- [TS 38.331 V19.4.0](https://www.etsi.org/deliver/etsi_ts/138300_138399/138331/19.04.00_60/ts_138331v190400p.pdf), clause 5.2.2.4.2, local PDF printed pp.70-71: SUL configuration depends on supported bands, emissions, bandwidth and applicable (e)RedCap duplex conditions. Local original verified; web PDF parser failed.
- [TS 38.101-1 V18.10.0](https://www.etsi.org/deliver/etsi_ts/138100_138199/13810101/18.10.00_60/ts_13810101v181000p.pdf), Table 5.2-1: n81 spans 880-915 MHz and is UL-only SUL. The specification contains SUL_n78-n81 requirements. This does not establish support in every RedCap product.
- [Saafi et al., ICC Workshops 2022](https://researchportal.tuni.fi/en/publications/enhancing-uplink-performance-of-nr-redcap-in-industrial-5gb5g-sys/), pp.520-525, DOI 10.1109/ICCWorkshops53468.2022.9814497: peer-reviewed study of RedCap UL improvement with SUL and other research options. Repository metadata/abstract verified; author PDF returned HTTP 403. Do not treat all investigated options as standard RedCap features.

A supported SUL transmission can be a communication-RF harvesting source by the declared model assumption.
SUL does not imply fixed/maximum power, a continuous CW waveform, automatic frequency support or adequate harvested energy.
915 MHz is the upper edge of n81, not automatically a valid center for a finite-bandwidth NR carrier.
A real SUL profile must fit its occupied channel within the selected band and use compatible harvesting hardware.
The first-version equivalent-frequency abstraction is unchanged pending a separate explicit carrier-profile revision.
