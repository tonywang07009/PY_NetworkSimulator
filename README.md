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

These steps use Linux and Bash. Start with Python 3.10 or later and a local copy of this project.
Package installation needs network access.
Run the commands from the project root, which contains this README and `src/`.

### 1. Prepare a Python environment

Create an isolated environment for this project:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install matplotlib numpy scipy jupyterlab ipykernel pytest
python -m pip check
```

Matplotlib provides plots; NumPy and SciPy support channel calculations.
JupyterLab and ipykernel provide the Notebook interface and Python kernel. Pytest runs the tests.
The packages are installed in `.venv/`.
If `.venv/` already contains your project environment, start with the activation command.
In each new terminal, activate the environment before running project commands.

Make sure that Python uses this environment:

```bash
python -c 'import sys; print(sys.executable)'
```

The path must end with `/.venv/bin/python`. `pip check` must report `No broken requirements found.`
If environment creation reports that `venv` or `ensurepip` is unavailable, install your distribution's matching Python venv package.
Then repeat environment creation.
If package installation fails, resolve the reported error before continuing.
If an import reports `ModuleNotFoundError`, make sure the environment is active and repeat the installation command.

The examples use `PYTHONPATH=src` to find the source modules without installing this project as a package.
After your session, use `deactivate` to leave the environment.

### 2. Build the example topology

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

### 3. Examine the results

With the environment active, start JupyterLab:

```bash
python -m jupyterlab
```

Open the printed local URL in your browser if it does not open automatically.
Open a Notebook from the file browser.
Select the Python kernel from the environment above.
Run its cells from the beginning:

- [Topology Notebook](notebooks/01_iab_topology.ipynb): examine the settings, Node and Tag tables, and deployment plot. You can change the example settings and run the cells again.
- [Channel Notebook](notebooks/02_channel_model.ipynb): examine link calculations and packet reception for a topology.

For settings, operation, and troubleshooting, use the [IAB topology guide](ReferDoc/Implementation/IABTopology/README.en.md) and the [channel guide in Traditional Chinese](ReferDoc/Implementation/ChannelModel/README.md). The [guide index](ReferDoc/Implementation/README.md) lists the module documents.

The topology export replaces files with the same names.
A failed or interrupted export can leave partial files.
Before export, copy the results that you need to keep.

## Architecture and data flow

Topology settings produce a network snapshot. The channel model uses it to calculate link quality and packet reception.
[Architecture and data flow](TutorialDoc/architecture.en.md) explains the module relationships and research limits.

## Module units

See the [tutorial index](TutorialDoc/README.md) for the recommended reading order.

- [IAB topology](TutorialDoc/unit/iab-topology.en.md): settings, zones, and input limits.
- [Channel model](TutorialDoc/unit/channel-model.en.md): formulas, research rules, and the reception flow.

## Validation

From the project root, use the existing test environment:

```bash
MPLBACKEND=Agg python -m pytest tests/iab/test_topology_notebook.py tests/iab/test_topology_extraction.py -q
python -m pytest tests/iab -q
python -m pytest tests/channel -q
```

For a clean-kernel run, use the [topology Notebook runner](tests/iab/execute_topology_notebook.py).
The channel guide describes its runner and environment.

The setup commands were tested in a new temporary environment on Linux with Python 3.12.12.
Package installation and `pip check` passed. The topology command produced `5 30`; a channel link query also succeeded.
JupyterLab 4.6.5 was available, but browser operation and Notebook execution were not tested.
Other Python versions remain unverified. Package versions are not pinned, so later installations can select different versions.
Six existing focused tests passed for power-table classes, floating-point tails, and packet sampling during the reception-flow update.
The full test commands above were not rerun. Mermaid rendering and visual layout remain unverified.
