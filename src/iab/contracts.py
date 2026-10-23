"""拓撲共用Config、DTO與Enum；集合設定只接受tuple。"""
from dataclasses import dataclass
from enum import Enum

# Tag sigal level zone
class TagZone(str, Enum):
    NEAR = 'NEAR'
    MID = 'MID'
    FAR = 'FAR'

# coordiate x,y 
@dataclass(frozen=True)
class Position2D:
    x_m: float 
    y_m: float


 # The Node postion sturct
 # lile (node_id = "node=1,
 #       Position2D (x_m=0 , y_m=0)")
@dataclass(frozen=True)
class FixedNodeConfig:
    node_id: str
    position: Position2D


@dataclass(frozen=True)
class TopologyConfig:
    donor: FixedNodeConfig
    iab_nodes: tuple[FixedNodeConfig, ...]
    zone_outer_radii_m: tuple[float, float, float] = (10.0, 30.0, 50.0) # The cycle zone
    zone_tag_counts: tuple[int, int, int] = (10, 13, 7) # The cycle zone for tag {good, midle, bad}
    min_tags_per_node: int = 2 # every node need until 2 tag.
    seed: int = 42

@dataclass(frozen=True)
class UERecord:
    ue_id: str
    parent_node_id: str 


@dataclass(frozen=True)
class TagRecord:
    tag_id: str
    parent_node_id: str
    zone: TagZone
    position: Position2D

# Store The topolgy status
@dataclass(frozen=True)
class TopologySnapshot:
    config: TopologyConfig
    ues: tuple[UERecord, ...]
    tags: tuple[TagRecord, ...]
