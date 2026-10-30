"""往返路損、BPSK有限碼長、分窗品質與接收結果。

公式與研究假設：ReferDoc/Implementation/ChannelModel/README.md、Plan/channel-entry-pack.md。
"""
from dataclasses import asdict
import hashlib # handle safe hash message
import json
import math
import random
import warnings

import numpy as np
from scipy.integrate import quad, IntegrationWarning
from scipy.special import log_ndtr

from iab.contracts import TagZone, TopologySnapshot, TagRecord, Position2D
from iab.topology import classify_distance, validate_config
from .contracts import (PowerLevel, ChannelConfig, LinkBudget, FBLReference,
                        LinkResult, ReceptionResult, WindowSnapshot)


def finite_number(value):
    if type(value) not in (int, float):
        return False
    try:
        return math.isfinite(value)
    except OverflowError: # prevent immense value
        return False


def validate_channel_config(config):
    if not isinstance(config, ChannelConfig):
        raise ValueError('config must be ChannelConfig')

    for name in ('interference_dbm', 'cw_power_dbm', 'offset_range_db'):
        if type(getattr(config, name)) is not tuple: #get data attbute
            raise ValueError(f'{name} must be tuple')

    canonical = ChannelConfig()
    for name, expected in asdict(canonical).items():
        value = getattr(config, name)
        if name in ('channel_seed', 'phy_seed'):
            if type(value) is not int:
                raise ValueError(f'{name} must be integer')
            continue

        if isinstance(expected, tuple):
            valid = len(value) == len(expected) and all(finite_number(v) for v in value)
        elif isinstance(expected, str):
            valid = type(value) is str
        else:
            valid = finite_number(value)

        if not valid or value != expected:
            raise ValueError(f'{name} does not match accepted profile')

    if config.channel_seed == config.phy_seed:
        raise ValueError('channel_seed and phy_seed must differ')


def require_positive_int(value, name):
    if type(value) is not int or value <= 0:
        raise ValueError(f'{name} must be a positive integer')


def require_id(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{name} must be a non-empty string')


def link_budget(config, distance_m, power_level, offset_db, node_index):
    validate_channel_config(config)
    if not finite_number(distance_m) or not config.min_distance_m <= distance_m <= config.max_distance_m:
        raise ValueError('distance must be within [1, 50] m; Tag is not moved')

    if not isinstance(power_level, PowerLevel):
        raise ValueError('power_level must be PowerLevel')

    if not finite_number(offset_db) or not config.offset_range_db[0] <= offset_db <= config.offset_range_db[1]:
        raise ValueError('offset_db must be within [-3, 3] dB')

    if type(node_index) is not int or not 0 <= node_index < len(config.interference_dbm):
        raise ValueError('node_index must identify one configured node')

    # Cacluse the cw dbm power and power level
    level_index = list(PowerLevel).index(power_level)
    cw_dbm = config.cw_power_dbm[level_index]
    gain_db = 10 * math.log10(config.reference_gain_linear) - 10 * config.path_loss_exponent * math.log10(distance_m / config.reference_distance_m)

    # The reciver (reader) recive power caluse for tag refect
    received_dbm = cw_dbm + 10 * math.log10(config.reflection_power_coefficient) + 2 * gain_db + offset_db
    received_w = 10 ** ((received_dbm - 30) / 10)
    noise_w = 10 ** ((config.noise_power_dbm - 30) / 10)

    interference_w = 10 ** ((config.interference_dbm[node_index] - 30) / 10) # 30 is dbm transformer W instance
    snr = received_w / noise_w
    sinr = received_w / (noise_w + interference_w)
    rho = 2 * sinr * config.bandwidth_hz / config.symbol_rate_hz

    # return the data class
    return LinkBudget(config.profile_id, power_level, distance_m, offset_db,
                      cw_dbm, 10 ** ((cw_dbm - 30) / 10), received_dbm,
                      received_w, noise_w, interference_w, 0.0,
                      10 * math.log10(snr), 10 * math.log10(sinr), rho)


def fbl_reference(rho, k, n):
    if not finite_number(rho) or rho <= 0:
        raise ValueError('rho must be finite and positive')

    require_positive_int(k, 'k')
    require_positive_int(n, 'n')
    if k > n:
        raise ValueError('k must not exceed n for binary input')

    model_id = 'bi-awgn-normal-approximation-no-higher-order-v1'
    unavailable = FBLReference(model_id, rho, k, n, None, None, None, None, None,
                               'QUADRATURE_PRECISION_LIMIT')
    if rho > 64:
        return unavailable

    #
    def information(z):
        return 1 - np.logaddexp(0.0, -2 * rho - 2 * math.sqrt(rho) * z) / math.log(2)

    def normal_density(z):
        return math.exp(-z * z / 2) / math.sqrt(2 * math.pi)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always', IntegrationWarning)
        capacity, c_error = quad(lambda z: information(z) * normal_density(z),
                                 -np.inf, np.inf, epsabs=2e-12, epsrel=2e-11)
        variance, v_error = quad(lambda z: (information(z) - capacity) ** 2 * normal_density(z),
                                 -np.inf, np.inf, epsabs=2e-12, epsrel=2e-11)

    if (caught or not 0 <= capacity <= 1 or not math.isfinite(variance)
            or variance <= 1e-12 or c_error > 1e-9 or v_error > 1e-9):
        return unavailable

    try:
        x = (n * capacity - k) / math.sqrt(n * variance)
    except (OverflowError, ValueError) as error:
        raise ValueError('k/n calculation exceeds float representation') from error

    if not math.isfinite(x):
        raise ValueError('k/n calculation exceeds float representation')

    log_error = float(log_ndtr(-x))
    log_success = float(log_ndtr(x))
    if not math.isfinite(log_error) or not math.isfinite(log_success):
        return FBLReference(model_id, rho, k, n, capacity, variance, None, None, None,
                            'NORMAL_APPROXIMATION_NUMERIC_LIMIT')

    epsilon = math.exp(log_error)
    status = 'FLOAT_TAIL' if epsilon in (0.0, 1.0) else 'FINITE_REFERENCE'
    return FBLReference(model_id, rho, k, n, capacity, variance,
                        epsilon, log_error, log_success, status)


def evaluate_link(config, distance_m, power_level, offset_db, node_index, *,
                  window_id, node_id, tag_id, zone, k=64, n=128):
    require_id(node_id, 'node_id')
    require_id(tag_id, 'tag_id')
    if type(window_id) is not int or window_id < 0:
        raise ValueError('window_id must be a non-negative integer')

    if not isinstance(zone, TagZone) or classify_distance(distance_m) != zone:
        raise ValueError('zone must agree with distance')

    budget = link_budget(config, distance_m, power_level, offset_db, node_index)
    reference = fbl_reference(budget.rho, k, n)
    classes = {
        PowerLevel.LOW: ('RELIABLE', 'RANDOM', 'UNREACHABLE'),
        PowerLevel.MEDIUM: ('RELIABLE', 'RELIABLE', 'RANDOM'),
        PowerLevel.HIGH: ('RELIABLE', 'RELIABLE', 'RELIABLE'),
    }
    receive_class = classes[power_level][list(TagZone).index(zone)]
    if receive_class == 'RELIABLE':
        used, reason = 0.0, 'RESEARCH_POWER_TABLE_RELIABLE'
    elif receive_class == 'UNREACHABLE':
        used, reason = 1.0, 'RESEARCH_POWER_TABLE_UNREACHABLE'
    else:
        used = reference.epsilon
        reason = 'BINARY_INPUT_AWGN_FBL' if used is not None else 'FBL_NUMERIC_UNAVAILABLE'
    return LinkResult(window_id, config.channel_seed, node_id, tag_id, zone, budget, reference,
                      receive_class, used, reason)


def local_rng(seed, *identity):
    payload = json.dumps([seed, *identity], ensure_ascii=False, separators=(',', ':')).encode('utf-8') # dump to json sturct
    return random.Random(int.from_bytes(hashlib.sha256(payload).digest(), 'big'))



# The recive obj
def draw_reception(config, link, transmission_id):
    require_id(transmission_id, 'transmission_id')
    if link.receive_class != 'RANDOM':
        return ReceptionResult(transmission_id, link,
                               link.receive_class == 'UNREACHABLE', None,
                               'DETERMINISTIC_RESEARCH_RULE', config.phy_seed)

    if link.fbl.epsilon is None:
        raise ValueError('FBL numeric probability unavailable; packet is not sampled')

    rng = local_rng(config.phy_seed, 'packet', link.window_id, link.node_id,
                    link.tag_id, transmission_id)

    uniform = (rng.getrandbits(52) + 0.5) / 2 ** 52
    log_uniform = math.log(uniform) # bit range -> 0 ~ 51

    if link.fbl.log_error <= math.log(0.5):
        failed = log_uniform < link.fbl.log_error
    else:
        failed = not (log_uniform < link.fbl.log_success)

    # This way is calus the fbl probelity
    limited = min(link.fbl.log_error, link.fbl.log_success) < math.log(2 ** -53)
    status = 'FINITE_PRNG_RESOLUTION_LIMIT' if limited else 'CONDITIONAL_BERNOULLI_52_BIT_GRID'
    return ReceptionResult(transmission_id, link, failed, uniform, status, config.phy_seed)


class ChannelModel:
    def __init__(self, config, topology):
        validate_channel_config(config)
        if not isinstance(topology, TopologySnapshot):
            raise ValueError('topology must be TopologySnapshot')

        validate_config(topology.config)
        if type(topology.tags) is not tuple:
            raise ValueError('topology.tags must be tuple')

        if topology.config.zone_outer_radii_m != (10.0, 30.0, 50.0):
            raise ValueError('topology radii do not match accepted profile')

        self._config = config
        self._topology = topology
        self._tags = {}
        positions = {node.node_id: node.position for node in topology.config.iab_nodes}
        for tag in topology.tags:
            if not isinstance(tag, TagRecord):
                raise ValueError('topology tag must be TagRecord')

            require_id(tag.tag_id, 'tag_id')
            require_id(tag.parent_node_id, 'parent_node_id')

            if tag.tag_id in self._tags or tag.parent_node_id not in positions:
                raise ValueError('duplicate Tag or unknown parent node')

            owner = positions[tag.parent_node_id]
            if not isinstance(tag.position, Position2D):
                raise ValueError('Tag position must be Position2D')

            if not all(finite_number(v) for v in (tag.position.x_m, tag.position.y_m)):
                raise ValueError('Tag position must contain finite coordinates')

            try:
                distance = math.hypot(tag.position.x_m - owner.x_m, tag.position.y_m - owner.y_m)

            except OverflowError as error:
                raise ValueError('Tag distance cannot be represented') from error

            link_budget(config, distance, PowerLevel.LOW, 0.0, 0)

            if not isinstance(tag.zone, TagZone) or classify_distance(distance) != tag.zone:
                raise ValueError('Tag zone disagrees with distance')
            self._tags[tag.tag_id] = (tag, distance)

        if not self._tags:
            raise ValueError('topology must contain Tags')

        self._current = None
        self._packets = {}

    @property
    def config(self):
        return self._config

    @property
    def topology(self):
        return self._topology

    def window(self, window_id, power_level):
        if type(window_id) is not int or window_id < 0:
            raise ValueError('window_id must be a non-negative integer')

        if not isinstance(power_level, PowerLevel):
            raise ValueError('power_level must be PowerLevel')

        previous = self._current
        if previous is not None and window_id == previous.window_id:
            if power_level != previous.power_level:
                raise ValueError('window power is already bound')
            return previous

        if previous is not None and window_id < previous.window_id:
            raise ValueError('window_id must increase from current window')

        nodes = self.topology.config.iab_nodes
        offsets = tuple((node.node_id,
                         local_rng(self.config.channel_seed, 'channel', node.node_id, window_id).uniform(*self.config.offset_range_db))
                        for node in nodes)
        candidate = WindowSnapshot(self.config.profile_id, self.config.channel_seed,
                                   window_id, power_level, offsets)

        # if previous is instnese , we just change the link quality
        if previous is not None:
            old_offsets = dict(previous.node_offsets_db)
            for node_index, (node_id, offset) in enumerate(offsets):
                if offset == old_offsets[node_id]:
                    raise ValueError('new window offset collision; current window unchanged')

                for tag, distance in self._tags.values():
                    if tag.parent_node_id != node_id: # only handle node id == tag.parent_node_id
                        continue
                    old = link_budget(self.config, distance, previous.power_level, old_offsets[node_id], node_index)
                    new = link_budget(self.config, distance, power_level, offset, node_index)
                    if old.snr_db == new.snr_db:
                        raise ValueError('new window SNR collision; current window unchanged')

        self._current = candidate
        self._packets = {}
        return candidate

    def link(self, window_id, tag_id, k=64, n=128):
        if type(window_id) is not int or self._current is None or window_id != self._current.window_id:
            raise ValueError('only the current declared window is available')

        require_id(tag_id, 'tag_id')
        if tag_id not in self._tags:
            raise ValueError('unknown tag_id')

        tag, distance = self._tags[tag_id]
        offsets = dict(self._current.node_offsets_db)
        for node_index, node in enumerate(self.topology.config.iab_nodes):
            if node.node_id == tag.parent_node_id:
                break
        else:
            # 全部找完仍不符合時，保留原本 next() 的例外行為。
            raise StopIteration
        return evaluate_link(self.config, distance, self._current.power_level,
                             offsets[tag.parent_node_id], node_index, window_id=window_id,
                             node_id=tag.parent_node_id, tag_id=tag_id, zone=tag.zone, k=k, n=n)

    def receive(self, window_id, tag_id, transmission_id, k=64, n=128):
        require_id(transmission_id, 'transmission_id')
        link = self.link(window_id, tag_id, k, n)
        key = (tag_id, transmission_id)

        if key in self._packets:
            prior = self._packets[key]
            if prior.link != link:
                raise ValueError('transmission ID already bound to different parameters')
            return prior

        result = draw_reception(self.config, link, transmission_id)
        self._packets[key] = result
        return result
