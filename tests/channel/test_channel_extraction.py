"""正式模組必須保留人工接受前的分窗與接收結果。"""
from dataclasses import asdict, replace
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
BASELINE = json.loads((ROOT / 'tests/channel/fixtures/channel-before-extraction.json').read_text())


@pytest.mark.parametrize('case', BASELINE['cases'], ids=['default-seeds', 'alternate-seeds'])
def test_python_module_preserves_accepted_windows_and_receptions(case):
    source_root = str(ROOT / 'src')
    sys.path.insert(0, source_root)
    try:
        from channel.channel_model import ChannelModel
        from channel.contracts import ChannelConfig, PowerLevel
        from iab.topology import build_topology, example_config

        config = replace(ChannelConfig(), channel_seed=case['channel_seed'], phy_seed=case['phy_seed'])
        model = ChannelModel(config, build_topology(example_config(BASELINE['topology_seed'])))
        actual = []
        for expected_window in case['windows']:
            window_id = expected_window['snapshot']['window_id']
            power = PowerLevel(expected_window['snapshot']['power_level'])
            window = model.window(window_id, power)
            records = [asdict(model.receive(window_id, tag_id, 'baseline-packet'))
                       for tag_id in case['tag_ids']]
            actual.append(dict(snapshot=asdict(window), records=records))
        assert json.loads(json.dumps(actual, allow_nan=False)) == case['windows']
    finally:
        sys.path.remove(source_root)
