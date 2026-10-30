[English](README.md) | [繁體中文](README.zh-TW.md)

# PY_NetworkSimulator

PY_NetworkSimulator is a Python research project for Ambient IoT in an Integrated Access and Backhaul (IAB) network.
It helps readers study a network deployment and the radio links between its Nodes and Tags.

The current modules create a static network topology.
They also calculate link quality and packet reception for that topology.
The channel model is available in the local worktree; its remote delivery is still pending.
Energy, access, scheduling, and a complete simulation timeline are not yet integrated.

## Choose a reading path

- [Quick start](#quick-start): run the example, then examine its deployment plot and channel calculations in the Notebooks.
- [Architecture and data flow](#architecture-and-data-flow): understand the inputs, modules, outputs, and research limits.

## Quick start

### Prerequisites

For the topology example, use Python 3.10 or later and Matplotlib.
Channel calculations also need NumPy and SciPy.
To run the Notebooks, use an environment with Jupyter and a working Python kernel.
Tests need pytest.
If the existing project environment has these packages, use that environment.

Run the commands below from the project root.
The `PYTHONPATH` setting makes the source modules available without installing this project as a package.
The third-party packages above are still required.

### 1. Build the example topology

```bash
PYTHONPATH=src python -c 'from iab.topology import build_topology, example_config; snapshot = build_topology(example_config()); print(len(snapshot.ues), len(snapshot.tags))'
```

Expected output:

```text
5 30
```

The example has five user equipment devices (UEs) and 30 Tags.
This output shows that the example topology was built.
The command does not run the channel model or display a plot.

### 2. Inspect the results

Open a Notebook in the environment above.
Run its cells from the beginning:

- [Topology Notebook](notebooks/01_iab_topology.ipynb): examine the settings, Node and Tag tables, and deployment plot. You can change the example settings and run the cells again.
- [Channel Notebook](notebooks/02_channel_model.ipynb): examine link calculations and packet reception for a topology.

For settings, operation, and troubleshooting, use the [IAB topology guide](ReferDoc/Implementation/IABTopology/README.en.md) and the [channel guide in Traditional Chinese](ReferDoc/Implementation/ChannelModel/README.md). The [guide index](ReferDoc/Implementation/README.md) lists the module documents.

The topology export replaces files with the same names.
A failed or interrupted export can leave partial files.
Before export, copy the results that you need to keep.

## Architecture and data flow

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
The [channel guide](ReferDoc/Implementation/ChannelModel/README.md) explains the assumptions and parameter sources.
Tag reading within the IAB split architecture is a research extension, not a claim of full standards compliance.

### Topology settings

The example has one Donor, five Nodes, one UE per Node, and 30 Tags. Tag counts are configurable. Use tuples for these three `TopologyConfig` collection fields:

| Field | Example and meaning |
|---|---|
| `iab_nodes` | `(node_1, node_2, node_3, node_4, node_5)` |
| `zone_outer_radii_m` | `(10.0, 30.0, 50.0)`; near, middle, and far outer boundaries in metres |
| `zone_tag_counts` | `(10, 13, 7)`; Tag counts across the whole scene for the three zones |

The module rejects lists and does not convert them automatically.
`frozen=True` prevents field reassignment; tuples prevent adding, removing, or replacing collection items.
The module checks ID uniqueness separately.

Type annotations do not validate inputs at runtime.
For invalid settings, `build_topology(config)` raises a `ValueError` with the reason.

```python
zone_tag_counts = (10, 13, 7)  # Accepted: tuple
# zone_tag_counts = [10, 13, 7]  # Rejected: list
```

### Source and further reading

The core modules are [src/iab](src/iab/) for topology and [src/channel](src/channel/) for channel calculations. Their corresponding tests are in [tests/iab](tests/iab/) and [tests/channel](tests/channel/).

- [System architecture](docs/architecture/system.html)
- [IAB topology architecture](docs/architecture/iab-topology.html) and [design notes](docs/architecture/iab-topology-design.md)
- [Channel architecture](docs/architecture/channel-model.html)

## Validation

From the project root, use the existing test environment:

```bash
MPLBACKEND=Agg python -m pytest tests/iab/test_topology_notebook.py tests/iab/test_topology_extraction.py -q
python -m pytest tests/iab -q
python -m pytest tests/channel -q
```

For a clean-kernel run, use the [topology Notebook runner](tests/iab/execute_topology_notebook.py).
The channel guide describes its runner and environment.

The quick-start command produced `5 30` during this README update.
The test commands and Notebooks were not rerun for this documentation change.
