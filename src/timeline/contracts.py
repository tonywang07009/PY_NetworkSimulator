"""Immutable resource configuration and snapshot records."""
from dataclasses import dataclass
from enum import Enum

WINDOW_NS = 600_000_000

class UEDirection(str, Enum):
    UL = 'UL'
    DL = 'DL'

@dataclass(frozen=True)
class ResourceConfig:
    scenario_id: str
    seed: int
    node_ids: tuple[str, ...]
    window_starts_ns: tuple[int, ...]

@dataclass(frozen=True)
class NodeResource:
    node_id: str
    window_id: int
    start_ns: int
    ue_end_ns: int
    end_ns: int
    direction: UEDirection
    raw_duration_ms: float

@dataclass(frozen=True)
class ResourceWindow:
    window_id: int
    start_ns: int
    end_ns: int
    nodes: tuple[NodeResource, ...]
    scenario_id: str
    seed: int

@dataclass(frozen=True)
class CurrentResource:
    node_id: str
    now_ns: int
    status: str
    window_id: int | None = None
    tag_start_ns: int | None = None
    window_end_ns: int | None = None

