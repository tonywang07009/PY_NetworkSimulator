[English](iab-topology.en.md) | [繁體中文](iab-topology.zh-TW.md)

# IAB topology unit

This unit explains topology settings and input limits. Complete the [quick start](../../README.md#quick-start) first.

## Topology settings

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

See the [topology guide](../../ReferDoc/Implementation/IABTopology/README.en.md) and [architecture and data flow](../architecture.en.md).
