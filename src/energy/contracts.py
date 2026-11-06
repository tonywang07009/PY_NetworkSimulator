"""Immutable Tag state and energy trace records; SI values and integer ns."""
from dataclasses import dataclass
from enum import Enum


class TagMode(str, Enum):
    STATIC = 'STATIC'
    WAKING = 'WAKING'
    PAGING_RX = 'PAGING_RX'
    WAIT_D2R = 'WAIT_D2R'
    BACKSCATTER = 'BACKSCATTER'
    SLEEP = 'SLEEP'
    ENERGY_RECOVERY = 'ENERGY_RECOVERY'


@dataclass(frozen=True)
class TagSnapshot:
    tag_id: str
    now_ns: int
    energy_j: float
    mode: TagMode


@dataclass(frozen=True)
class TagTraceRow:
    start_ns: int
    end_ns: int
    mode: TagMode
    phase: str
    before_j: float
    harvested_j: float
    consumed_j: float
    spilled_j: float
    after_j: float
    note: str = ''


@dataclass(frozen=True)
class TagTrace:
    snapshot: TagSnapshot
    rows: tuple
    depletion_after_s: float | None = None
    receive_success: bool | None = None


D2R_OCCUPANCY_NS = {8: 35_000_000, 16: 63_000_000, 32: 118_000_000, 64: 228_000_000}
GUARD_NS = 200_000
INACTIVE_MODES = (TagMode.STATIC, TagMode.SLEEP, TagMode.ENERGY_RECOVERY)
RESOURCE_PHASES = ('UE_UL', 'UE_DL', 'RF_SWITCH', 'PAGING', 'WAIT_D2R', 'D2R', 'GUARD', 'GAP', 'POST_TBS_CW')
