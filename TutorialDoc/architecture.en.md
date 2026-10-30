[English](architecture.en.md) | [繁體中文](architecture.zh-TW.md)

# System architecture and data flow

In the example, one Donor is the upstream station for five IAB Nodes.
Each Node has one logically associated UE and reads its assigned Tags.
Tags are placed around their assigned Nodes.
The topology remains fixed during a simulation.

1. **Topology:** Node positions, Tag counts, and a random seed produce a topology snapshot, tables, and a deployment plot. The snapshot records the Nodes, Tags, and their relationships.
2. **Channel:** The snapshot, channel settings, and window power provide the inputs for received power, SNR, SINR, and packet reception calculations. SNR compares signal power with noise; SINR also includes interference.
3. **Results:** The Notebooks show the settings and calculations. The topology module can also export plots and data as PNG, SVG, JSON, and CSV.

The topology's near, middle, and far zones describe distance.
They do not establish RF coverage, absence of interference, or measured signal quality.

The channel model uses research assumptions. One assumption is that a packet is ready to transmit.
Its results do not guarantee outdoor performance.
The [channel guide](../ReferDoc/Implementation/ChannelModel/README.md) explains the assumptions and parameter sources.
Tag reading within the IAB split architecture is a research extension, not a claim of full standards compliance.

## Module units and further reading

- [Topology unit](unit/iab-topology.en.md)
- [Channel model unit](unit/channel-model.en.md)

The core modules are [src/iab](../src/iab/) for topology and [src/channel](../src/channel/) for channel calculations. Their corresponding tests are in [tests/iab](../tests/iab/) and [tests/channel](../tests/channel/).

- [System architecture](../docs/architecture/system.html)
- [IAB topology architecture](../docs/architecture/iab-topology.html) and [design notes](../docs/architecture/iab-topology-design.md)
- [Channel architecture](../docs/architecture/channel-model.html)

