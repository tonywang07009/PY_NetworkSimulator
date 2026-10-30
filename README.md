[English](README.md) | [繁體中文](README.zh-TW.md)

# PY_NetworkSimulator

This Python project supports Ambient IoT research in an IAB network.
The current local modules build a static network topology and calculate radio-link quality.
Use the Notebooks to inspect settings, calculations, and results.

## System overview

| Module | Input | Output |
|---|---|---|
| IAB topology | Node positions, Tag counts, and a random seed | A topology snapshot, distance tables, and deployment plots |
| Channel model | The topology snapshot, channel settings, and window power | Received power, SNR, SINR, and packet reception results |

The topology snapshot connects these two modules.
The channel model is available in the local worktree; its remote delivery is still pending.

## Choose a reading path

| Goal | Start here |
|---|---|
| Run a small example | [Quick start](#quick-start) |
| Understand the system | [Architecture and data flow](#architecture-and-data-flow) |

## Quick start

### Prerequisites

For the topology module, use Python 3.10 or later and Matplotlib.
Channel calculations also need NumPy and SciPy. Notebook examples need a working Jupyter kernel.
Tests need pytest. Use the existing project environment.

### Run the topology example

From the project root, run:

```bash
PYTHONPATH=src python -c 'from iab.topology import build_topology, example_config; snapshot = build_topology(example_config()); print(len(snapshot.ues), len(snapshot.tags))'
```

Expected output:

```text
5 30
```

These values are the UE count and Tag count in the example.
With this `PYTHONPATH` invocation, you do not need to install the project as a package.

### Continue in a Notebook

- [Topology Notebook](notebooks/01_iab_topology.ipynb): edit settings, inspect tables, and display the deployment plot.
- [Channel Notebook](notebooks/02_channel_model.ipynb): inspect channel calculations and packet reception.

Run cells from the beginning in the selected environment.
Both Notebooks import their core modules; settings, demonstrations, and scenarios remain in the Notebooks.

For topology settings and operation, read the [English IAB guide](ReferDoc/Implementation/IABTopology/README.en.md).
For channel operation, read the [channel guide in Traditional Chinese](ReferDoc/Implementation/ChannelModel/README.md).
The [guide index](ReferDoc/Implementation/README.md) lists available module documents.

## Topology configuration

The static two-dimensional example has one Donor and five Nodes, with one UE per Node.
UE association is logical. Tag counts are configurable; the example has 30 Tags.
The module provides exact three-zone quotas, tables, and PNG/SVG/JSON/CSV export.

Three `TopologyConfig` collection fields require tuples:

| Field | Format or example |
|---|---|
| `iab_nodes` | `(node_1, node_2, node_3, node_4, node_5)` |
| `zone_outer_radii_m` | `(10.0, 30.0, 50.0)`; near/middle/far outer boundaries in metres |
| `zone_tag_counts` | `(10, 13, 7)`; near/middle/far Tag counts across the whole scene |

Lists are rejected. No automatic format conversion occurs.
`frozen=True` blocks field reassignment. Tuples block adding, removing, or replacing collection items.
Together, these rules keep the configuration fixed; they do not replace the separate ID uniqueness validation.

Type annotations do not perform runtime input validation.
`build_topology(config)` rejects list inputs and other invalid settings with a `ValueError` that explains the reason.
No additional `__post_init__` conversion is needed.

```python
zone_tag_counts = (10, 13, 7)  # Accepted: tuple
# zone_tag_counts = [10, 13, 7]  # Rejected: list
```

## Architecture and data flow

The source and tests are grouped by module:

```text
src/
├── iab/
│   ├── __init__.py
│   ├── contracts.py       # Shared dataclasses and TagZone
│   ├── topology.py        # Validation, generation, tables, and export
│   └── plotting.py        # Deployment plot with equal axis scaling
└── channel/
    ├── __init__.py
    ├── contracts.py       # Channel configuration, data types, and enums
    └── channel_model.py   # Channel calculations, windows, and packet reception
```

- [System architecture](docs/architecture/system.html)
- [IAB topology architecture](docs/architecture/iab-topology.html)
- [IAB design notes](docs/architecture/iab-topology-design.md)
- [Channel architecture](docs/architecture/channel-model.html)
- [Topology tests](tests/iab/) and [channel tests](tests/channel/)

## Validation commands

From the project root, use the existing test environment:

```bash
MPLBACKEND=Agg python -m pytest tests/iab/test_topology_notebook.py tests/iab/test_topology_extraction.py -q
python -m pytest tests/iab -q
python -m pytest tests/channel -q
```

The existing clean-kernel topology runner is [execute_topology_notebook.py](tests/iab/execute_topology_notebook.py).
The channel guide gives its corresponding kernel runner and environment.
The quick-start command produced 5 30 on Python 3.12.12 during this README update.
The test commands above were not rerun for this documentation change.

## Limits

This guide covers the current topology and channel modules. Energy and scheduling remain future work.
Geometric zones do not establish RF coverage, absence of interference, or SNR quality.
The channel guide records model assumptions and parameter sources.

Export replaces files with the same names. An interrupted or failed export can leave partial files.
Copy earlier results before export if you need to keep them.
