"""靜態拓撲的輸入驗證、局部亂數生成、表格與匯出。"""
from collections import Counter
from dataclasses import asdict
from pathlib import Path
import csv
import json
import math
import random

from .contracts import (FixedNodeConfig, Position2D, TagRecord, TagZone,
                        TopologyConfig, TopologySnapshot, UERecord)
from .plotting import plot_topology


def example_config(seed=42):
    """工程示例；固定站點不代表真實農場或通訊覆蓋已校準。"""
    positions = ((0, 0), (120, 0), (240, 0), (60, 120), (180, 120))
    return TopologyConfig(
        donor=FixedNodeConfig('Donor-1', Position2D(120, -120)),
        iab_nodes=tuple(FixedNodeConfig(f'Node-{i}', Position2D(*xy))
                        for i, xy in enumerate(positions, 1)),
        seed=seed,
    )


# Check this can handle finite numer?
# for cacluate
def _finite_number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(value)
    except OverflowError: # for prevent the hugle num
        return False

# Check the radis area is legitimate?
def _validate_radii(radii):
    if not isinstance(radii, tuple) or len(radii) != 3: # need type = (1,2,3)
        raise ValueError('zone_outer_radii_m must contain three radii')

    if any(not _finite_number(r) or r <= 0 for r in radii): # check the r is real number?
        raise ValueError('zone_outer_radii_m must be finite and positive')

    if not radii[0] < radii[1] < radii[2]: # need like = (10,30,50) if (30,50,10) is unpass.
        raise ValueError('zone_outer_radii_m must strictly increase')

# The destiance near mid fear
def classify_distance(distance, radii=(10.0, 30.0, 50.0)):
    """含外邊界、排除內邊界；這是部署分區，不是成功率判定。"""
    _validate_radii(radii)
    if not _finite_number(distance) or not 0 < distance <= radii[-1]:
        raise ValueError('distance must be positive and within deployment radius')

    return next(zone for zone, radius in zip(TagZone, radii) if distance <= radius)




# Check The hold node setting is legitimate?
def validate_config(config):
    """公開生成入口的輸入檢查；失敗不產生部分檔案或修改輸入。"""
    if not isinstance(config, TopologyConfig):
        raise ValueError('config must be TopologyConfig')

    if not isinstance(config.iab_nodes, tuple) or len(config.iab_nodes) != 5:
        raise ValueError('iab_nodes must contain exactly five nodes')

    stations = (config.donor,) + config.iab_nodes
    identifiers = [] #collection the node id

    # The every station need pass the check
    for station in stations:
        if not isinstance(station, FixedNodeConfig):
            raise ValueError('station must be FixedNodeConfig')

        if not isinstance(station.node_id, str) or not station.node_id.strip():
            raise ValueError('station ID must be a non-empty string')

        identifiers.append(station.node_id)

        if not isinstance(station.position, Position2D):
            raise ValueError('station position must be Position2D')

        if not all(_finite_number(v) for v in (station.position.x_m, station.position.y_m)):
            raise ValueError('station coordinates must be finite numbers')

    if len(set(identifiers)) != len(identifiers): # check have a duplication value
        raise ValueError('duplicate station ID')

    _validate_radii(config.zone_outer_radii_m)
    counts = config.zone_tag_counts

    if (not isinstance(counts, tuple) or len(counts) != 3
            or any(type(c) is not int or c < 0 for c in counts)):
        raise ValueError('zone_tag_counts must contain three non-negative integers')

    if type(config.min_tags_per_node) is not int or config.min_tags_per_node < 2:
        raise ValueError('min_tags_per_node must be an integer >= 2')

    # sum need over the node request
    if sum(counts) < len(config.iab_nodes) * config.min_tags_per_node:
        raise ValueError('zone_tag_counts total is below minimum required Tag count')

    if type(config.seed) is not int:
        raise ValueError('seed must be an integer')

    for identifier in identifiers:
        reserved_ue = identifier in {f'UE-{i}' for i in range(1, 6)}
        suffix = identifier.removeprefix('Tag-') # remove Tag- identify symbol
                                                 # for the instiance check , need number
        reserved_tag = (identifier.startswith('Tag-')
                        and suffix.isascii()
                        and suffix.isdigit()
                        and 1 <= int(suffix) <= sum(counts)
                        and identifier == f'Tag-{int(suffix):03d}') #03d -> 00n

        if reserved_ue or reserved_tag:
            raise ValueError(f'station ID collides with generated entity ID: {identifier}')

    # 部署幾何檢查；不代表射頻無干擾
    diameter = 2 * config.zone_outer_radii_m[-1]

    if not _finite_number(diameter):
        raise ValueError('deployment geometry cannot be represented')

    for index, left in enumerate(config.iab_nodes):
        for right in config.iab_nodes[index + 1:]:
            try:
                separation = math.hypot(left.position.x_m - right.position.x_m,
                                        left.position.y_m - right.position.y_m)
            except OverflowError as error:
                raise ValueError('node separation geometry cannot be represented') from error

            if not math.isfinite(separation):
                raise ValueError('node separation cannot be represented')

            if separation <= diameter: # 拒絕部署圓域重疊或相切
                raise ValueError(f'node regions overlap or touch: {left.node_id}, {right.node_id}')


# check node middle fornt , distance and angle
# calus the tad cooditonate
def _position_in_ring(centre, radius, angle, inner, outer):
    def point_at(r): # Polar coordinates transformer
        return Position2D(centre.x_m + r * math.cos(angle),
                          centre.y_m + r * math.sin(angle))

    position = point_at(radius) # radius tag for node taget range.
    distance = math.hypot(position.x_m - centre.x_m, position.y_m - centre.y_m)

    if inner < distance <= outer:
        return position

    # 只修正座標運算的端點捨入；不重抽、不放寬實際分區。
    # 微調目標距離　tag
    tolerance = 8 * max(math.ulp(float(centre.x_m)),
                        math.ulp(float(centre.y_m)),
                        math.ulp(outer))

    near_boundary = min(abs(distance - inner),
                        abs(distance - outer)) <= tolerance

    if tolerance < (outer - inner) / 2 and near_boundary:
        position = point_at(min(outer - tolerance, max(inner + tolerance, radius)))
        distance = math.hypot(position.x_m - centre.x_m, position.y_m - centre.y_m)

        if inner < distance <= outer:
            return position
    raise ValueError('generated geometry loses distance to float precision')


def build_topology(config):
    """由設定建立靜態快照；只使用局部亂數，不改全域RNG。"""
    validate_config(config)
    rng = random.Random(config.seed) # setting the seed for random

    zones = [zone for zone, count in zip(TagZone, config.zone_tag_counts)
             for _ in range(count)]

    rng.shuffle(zones)
    nodes = config.iab_nodes
    owners = [node for node in nodes # This sure the node have unless two tag asigend
              for _ in range(config.min_tags_per_node)]
    rng.shuffle(owners)   # 亂數
    owners.extend(rng.choice(nodes)
                  for _ in range(len(zones) - len(owners)))
    tags = []

    for index, (zone, node) in enumerate(zip(zones, owners), 1):

        # first get the zone range.
        zone_index = list(TagZone).index(zone)
        # setting range
        inner = 0.0 if zone_index == 0 else config.zone_outer_radii_m[zone_index - 1]
        outer = config.zone_outer_radii_m[zone_index]

        u = 1.0 - rng.random()  # (0,1]排除中心與環帶內邊界。

        # 環帶按面積均勻取樣，因此對平方距離取樣後開根號。
        radius = outer * math.sqrt((inner / outer)**2 + u * (1 - (inner / outer)**2))
        angle = rng.uniform(0.0, math.tau)

        # calus tag coordinate
        position = _position_in_ring(node.position, radius, angle, inner, outer)

        # input the tag data
        tags.append(TagRecord(f'Tag-{index:03d}',
                              node.node_id,
                              zone,
                              position))

    ues = tuple(UERecord(f'UE-{i}', node.node_id)
                for i, node in enumerate(nodes, 1))

    return TopologySnapshot(config, ues, tuple(tags))


def topology_tables(snapshot):
    """表格只推導同一快照，不重新抽樣或保存另一套真值。"""
    config = snapshot.config
    counts = Counter((tag.parent_node_id, tag.zone) for tag in snapshot.tags)
    nodes = []
    for node, ue in zip(config.iab_nodes, snapshot.ues):
        near, mid, far = (counts[node.node_id, zone] for zone in TagZone)
        nodes.append(dict(node_id=node.node_id,
                          x_m=node.position.x_m,
                          y_m=node.position.y_m,
                          donor_id=config.donor.node_id,
                          ue_id=ue.ue_id,
                          near=near,
                          mid=mid,
                          far=far,
                          total=near + mid + far))
    positions = {node.node_id: node.position for node in config.iab_nodes}
    # key -> node.id value -> position
    tags = []

    for tag in snapshot.tags:
        owner = positions[tag.parent_node_id]
        distance = math.hypot(tag.position.x_m - owner.x_m, tag.position.y_m - owner.y_m)
        tags.append(dict(tag_id=tag.tag_id,
                         parent_node_id=tag.parent_node_id,
                         x_m=tag.position.x_m,
                         y_m=tag.position.y_m,
                         distance_m=distance,
                         zone=tag.zone.value))

    # recode backhul
    links = [dict(kind='BACKHAUL',
                  source=config.donor.node_id,
                  target=n.node_id)
             for n in config.iab_nodes]

    # node -> ue link
    links += [dict(kind='UE_ASSOCIATION',
                   source=u.parent_node_id,
                   target=u.ue_id)
              for u in snapshot.ues]

    # node -> tag link
    links += [dict(kind='TAG_ACCESS',
                   source=t.parent_node_id,
                   target=t.tag_id)
              for t in snapshot.tags]

    # the setting data sturct
    settings = [dict(parameter='seed', value=config.seed),
                dict(parameter='zone_outer_radii_m', value=config.zone_outer_radii_m),
                dict(parameter='zone_tag_counts', value=config.zone_tag_counts),
                dict(parameter='min_tags_per_node', value=config.min_tags_per_node),
                dict(parameter='donor', value=asdict(config.donor)),
                dict(parameter='iab_nodes', value=[asdict(n) for n in config.iab_nodes])]

    return dict(settings=settings, nodes=nodes, tags=tags, links=links)




def export_topology(snapshot, output_dir):
    """匯出同一快照及其圖表，供人工核對與跨版本保存。"""
    from matplotlib import pyplot as plt
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {'snapshot': output_dir / 'snapshot.json'}
    payload = dict(schema_version=1, config=asdict(snapshot.config),
                   ues=[asdict(u) for u in snapshot.ues], tags=[asdict(t) for t in snapshot.tags])
    paths['snapshot'].write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + '\n',
                                 encoding='utf-8')
    for name, rows in topology_tables(snapshot).items():
        path = output_dir / f'{name}.csv'
        with path.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        paths[name] = path
    fig, _ = plot_topology(snapshot)
    try:
        for format in ('png', 'svg'):
            path = output_dir / f'deployment.{format}'
            fig.savefig(path, dpi=160)
            paths[format] = path
    finally:
        plt.close(fig)
    return paths
