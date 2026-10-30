"""通道Config、DTO與Enum；集合設定只接受tuple。"""
from dataclasses import dataclass
from enum import Enum

from iab.contracts import TagZone


class PowerLevel(str, Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'


@dataclass(frozen=True)
class ChannelConfig:
    profile_id: str = 'channel-entry-synthetic-v0.1'
    frequency_hz: float = 915e6
    reference_distance_m: float = 1.0
    reference_gain_linear: float = 0.0006797973850689421
    path_loss_exponent: float = 2.0
    reflection_power_coefficient: float = 0.1
    min_distance_m: float = 1.0
    max_distance_m: float = 50.0
    bandwidth_hz: float = 10000.0
    symbol_rate_hz: float = 10000.0
    noise_power_dbm: float = -128.0
    interference_dbm: tuple = (-128.0, -128.0, -128.0, -128.0, -128.0)
    cw_power_dbm: tuple = (-2.0, 10.0, 22.0)
    offset_range_db: tuple = (-3.0, 3.0)
    channel_seed: int = 20261029
    phy_seed: int = 20261030


@dataclass(frozen=True)
class LinkBudget:
    profile_id: str
    power_level: PowerLevel
    distance_m: float
    offset_db: float
    cw_power_dbm: float
    cw_power_w: float
    received_dbm: float
    received_w: float
    noise_w: float
    interference_w: float
    residual_self_interference_w: float
    snr_db: float
    sinr_db: float
    rho: float


@dataclass(frozen=True)
class FBLReference:
    model_id: str
    rho: float
    k: int
    n: int
    capacity_bits: float | None
    dispersion_bits2: float | None
    epsilon: float | None
    log_error: float | None
    log_success: float | None
    status: str


@dataclass(frozen=True)
class LinkResult:
    window_id: int
    channel_seed: int
    node_id: str
    tag_id: str
    zone: TagZone
    budget: LinkBudget
    fbl: FBLReference
    receive_class: str
    used_error_probability: float | None
    rule_reason: str


@dataclass(frozen=True)
class ReceptionResult:
    transmission_id: str
    link: LinkResult
    failed: bool
    uniform_draw: float | None
    sampling_status: str
    phy_seed: int


@dataclass(frozen=True)
class WindowSnapshot:
    profile_id: str
    channel_seed: int
    window_id: int
    power_level: PowerLevel
    node_offsets_db: tuple
