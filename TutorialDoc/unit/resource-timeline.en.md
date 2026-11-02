[English](resource-timeline.en.md) | [繁體中文](resource-timeline.zh-TW.md)

# Resource timeline unit

Use the [resource Notebook](../../notebooks/03_resource_timeline.ipynb) to generate and inspect UE and Tag resource intervals.
Complete the [quick start](../../README.md#quick-start) first. Open the Notebook from the project root or notebooks directory.

Run the cells from the beginning. The settings cell uses seed 42 and explicit synthetic starts at 0 and 800 ms.
Each outer window lasts 600 ms. Each Node has a UE prefix, followed by a Tag budget for Paging, D2R and Guard.
The tables and plot use the same generated snapshot; blank gaps are unavailable resource.

The Notebook demonstrates rounding, reproducibility, Node-order independence and a current-resource projection.
The caller supplies authoritative time to the projection; this is not a security sandbox against future queries.
Channel handoff uses the existing ChannelModel and does not implement a full engine or packet scheduler.

Export is disabled by default. Set EXPORT_RESULTS to True in the explicit export cell to write into notebooks/artifacts/resource-timeline.
It writes snapshot.json, resources.csv, timeline.png and timeline.svg. Export replaces named files and can leave partial files on failure.
Copy results that you want to keep before export.

The accepted core now lives in [src/timeline](../../src/timeline/). The Notebook imports that core. The 200 ms gap is a synthetic input, not a calibrated load distribution.
See the [resource design](../../docs/architecture/resource-timeline-design.md) and [decision record](../../ReferDoc/Plan/R-01_System_Model_and_Baseline_Decision_Record.md), §34.

Read the source in this order:

| Module | Responsibility |
|---|---|
| [contracts.py](../../src/timeline/contracts.py) | Frozen configuration, direction and snapshot records |
| [resource_timeline.py](../../src/timeline/resource_timeline.py) | Validation, sampling, generation, current projection and export |
| [plotting.py](../../src/timeline/plotting.py) | Plot the generated UE and Tag intervals |

The Notebook retains settings, explanations, HTML presentation and assertions.
User review comments moved with their corresponding source functions.
