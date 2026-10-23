# IAB Network Topology User Guide

[繁體中文](README.md)

## What does this feature do?

This feature creates a static network deployment map. It lets you inspect each Node's position, the Tags assigned to it, and their distances from that Node. You can view the results as tables and save both images and data files.

The current layout contains:

| Name | Role in this scenario | Number |
|---|---|---:|
| Donor | The upstream station connected to all IAB Nodes | 1 |
| IAB Node, called Node below | Connects to the Donor and reads its assigned Tags | 5 |
| UE | User equipment associated with a Node | 1 per Node |
| Tag | A label device randomly assigned and placed around a Node | Configurable; 30 in the default example |

Each Tag belongs to exactly one Node. A Node can have several Tags. Positions remain fixed during a simulation.

## Where to go next

- [Settings](01-settings.en.md)
- [Getting started](02-usage.en.md)
- [Reading the results](03-results.en.md)
- [Troubleshooting](04-troubleshooting.en.md)

## Scope and further reading

This feature currently describes positions and connections. It does not yet calculate signal quality, transmission success, battery levels or scheduling. Colours indicate distance zones rather than signal quality. Separate deployment circles do not establish that wireless interference is absent.

Integrating Tag reading into a Node is part of this research model. Its use within the IAB split base-station architecture is a research extension, not a claim of full standards compliance.

For the reasons behind the settings, read the [system model plan](../../Plan/R-01_System_Model_and_Baseline_Decision_Record.md). For implementation details, see the [IAB source files](../../../src/iab/).
