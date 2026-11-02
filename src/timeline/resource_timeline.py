"""Generate, query and export the accepted 600 ms resource profile."""
from dataclasses import asdict
from pathlib import Path
import csv
import hashlib
import json
import math
import random

from .contracts import WINDOW_NS, CurrentResource, NodeResource, ResourceConfig, ResourceWindow, UEDirection
from .plotting import plot_resources

def validate_resource_config(config):
    if not isinstance(config, ResourceConfig): # The ResourceConfig is The data type
        raise ValueError('config must be ResourceConfig')

    if not isinstance(config.scenario_id, str) or not config.scenario_id.strip():
        raise ValueError('scenario_id must be a non-empty string')

    if type(config.seed) is not int or config.seed < 0:
        raise ValueError('seed must be a non-negative integer')

    if type(config.node_ids) is not tuple or not config.node_ids:
        raise ValueError('node_ids must be a non-empty tuple')

    if any(not isinstance(node_id, str) or not node_id.strip() for node_id in config.node_ids):
        raise ValueError('node_ids must contain non-empty strings')

    if len(set(config.node_ids)) != len(config.node_ids):
        raise ValueError('node_ids must be unique')

    window_starts_ns = config.window_starts_ns
    if type(window_starts_ns) is not tuple or not window_starts_ns: # The start duration time is different
        raise ValueError('window_starts_ns must be a non-empty tuple')

    if any(type(window_start_ns) is not int or window_start_ns < 0 for window_start_ns in window_starts_ns):
        raise ValueError('window_starts_ns must contain non-negative integer ns')

    if window_starts_ns[0] != 0:
        raise ValueError('first window start must be zero')

    if any(next_window_start_ns < previous_window_start_ns + WINDOW_NS for previous_window_start_ns, next_window_start_ns in zip(window_starts_ns, window_starts_ns[1:])):
        raise ValueError('window_starts_ns must increase without overlap')


# The dump snapshort
def resource_rng(config, node_id, window_id, kind):
    identity = [config.seed, config.scenario_id, node_id, window_id, kind]
    digest = hashlib.sha256(json.dumps(identity, ensure_ascii=False).encode('utf-8')).digest()
    return random.Random(int.from_bytes(digest, 'big'))
    # int.from_bytes(digest, 'big') -> hash transformet intergration

# The ue attent du time control
def round_ue_duration_ns(duration_ms):
    if type(duration_ms) not in (int, float):
        raise ValueError('duration_ms must be finite numeric milliseconds')

    if not 360 <= duration_ms <= 450:
        raise ValueError('duration_ms must be between 360 and 450 ms')

    return math.ceil(duration_ms) * 1_000_000
    # 1_000_000 is nano second


def build_timeline(config):
    validate_resource_config(config)
    resource_windows = []
    for window_id, window_start_ns in enumerate(config.window_starts_ns):
        node_resources = []
        for node_id in config.node_ids:
            ue_ratio = resource_rng(config, node_id, window_id, 'duration').uniform(0.60, 0.75)
            raw_duration_ms = 600 * ue_ratio
            ue_duration_ns = round_ue_duration_ns(raw_duration_ms) # The ue time transformer
            direction_draw = resource_rng(config, node_id, window_id, 'direction').random()
            ue_direction = UEDirection.UL if direction_draw < 0.5 else UEDirection.DL
            node_resources.append(NodeResource(node_id, window_id, window_start_ns, window_start_ns + ue_duration_ns,
                                        window_start_ns + WINDOW_NS, ue_direction, raw_duration_ms))
        resource_windows.append(ResourceWindow(window_id, window_start_ns, window_start_ns + WINDOW_NS, tuple(node_resources), config.scenario_id, config.seed))
    return tuple(resource_windows)


def resource_rows(windows):
    return [dict(window_id=window.window_id, node_id=node_resource.node_id, direction=node_resource.direction.value,
                 start_ns=node_resource.start_ns, ue_end_ns=node_resource.ue_end_ns, end_ns=node_resource.end_ns,
                 raw_duration_ms=node_resource.raw_duration_ms,
                 ue_duration_ms=(node_resource.ue_end_ns-node_resource.start_ns)//1_000_000,
                 tag_budget_ms=(node_resource.end_ns-node_resource.ue_end_ns)//1_000_000)
            for window in windows for node_resource in window.nodes]


def current_resource(windows, node_id, now_ns):
    if type(now_ns) is not int or now_ns < 0:
        raise ValueError('now_ns must be a non-negative integer')

    if not isinstance(node_id, str) or not node_id.strip():
        raise ValueError('node_id must be a non-empty string')

    if not windows or node_id not in {node_resource.node_id for window in windows for node_resource in window.nodes}:
        raise ValueError('unknown node_id or empty timeline')

    for window in windows:
        if window.start_ns <= now_ns < window.end_ns:
            node_resource = next(node_resource for node_resource in window.nodes if node_resource.node_id == node_id)
            resource_status = 'UE_OCCUPIED' if now_ns < node_resource.ue_end_ns else 'TAG_AVAILABLE' # The Du status now display
            return CurrentResource(node_id, now_ns, resource_status, node_resource.window_id,
                                   node_resource.ue_end_ns, node_resource.end_ns)
    return CurrentResource(node_id, now_ns, 'NO_WINDOW')


def export_resources(windows, destination):
    destination = Path(destination)
    resource_table_rows = resource_rows(windows)
    if not resource_table_rows:
        raise ValueError('cannot export an empty resource timeline')

    import matplotlib.pyplot as plt

    destination.mkdir(parents=True, exist_ok=True)
    snapshot_payload = {'scenario_id': windows[0].scenario_id, 'seed': windows[0].seed,
               'node_ids': [node_resource.node_id for node_resource in windows[0].nodes],
               'window_starts_ns': [window.start_ns for window in windows],
               'profile': 'ue-600ms-uniform-ceil-ms-v1',
               'windows': [asdict(window) for window in windows]}

    (destination/'snapshot.json').write_text(json.dumps(snapshot_payload, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

    with (destination/'resources.csv').open('w', newline='', encoding='utf-8-sig') as csv_stream:
        csv_writer = csv.DictWriter(csv_stream, fieldnames=tuple(resource_table_rows[0]))
        csv_writer.writeheader()
        csv_writer.writerows(resource_table_rows)

    figure = plot_resources(windows)
    try:
        figure.savefig(destination/'timeline.png', dpi=150)
        figure.savefig(destination/'timeline.svg')
    finally:
        plt.close(figure)

