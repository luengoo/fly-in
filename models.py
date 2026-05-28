from pydantic import BaseModel, model_validator, Field
from typing import TypeVar, Literal


Z = TypeVar("Z", bound="Zone")
C = TypeVar("C", bound="Connection")
G = TypeVar("G", bound="Graph")


class Zone(BaseModel):
    model_config = {"frozen": True}

    name: str
    x: int
    y: int
    zone_type: str = "normal"
    color: str
    max_drones: int = 1
    hub_type: Literal[
        "hub",
        "start_hub",
        "end_hub"
    ]

    @model_validator(mode="after")
    def validation(self: Z) -> Z:
        if self.zone_type not in {
          "normal", "blocked", "restricted", "priority"}:
            raise ValueError("Invalid zone_type")
        if self.max_drones < 0:
            raise ValueError("max_drones must be >= 0")
        return self


class Connection(BaseModel):
    zone1: Zone
    zone2: Zone
    max_link_capacity: int = 1

    @model_validator(mode="after")
    def validation(self: C) -> C:
        if self.max_link_capacity < 0:
            raise ValueError("invalid capacity")
        return self

    def key(self) -> frozenset:
        return frozenset((self.zone1, self.zone2))


class Drone:
    def __init__(self, drone_id: str):
        self.id = drone_id
        self.zone: Zone
        self.connection: Connection | None = None
        self.path: list[Zone] = []
        self.path_index = 0
        self.finished = False
        self.in_transit: bool = False
        self.remaining_turns: int = 0
        self.target_zone: Zone
        self.buffer_zone: Zone | None = None
        self.buffer_edge: frozenset | None = None
        self.just_arrived: bool = False


class Graph(BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    zones: dict[str, Zone] = Field(default_factory=dict)
    connections: list[Connection] = Field(default_factory=list)
    drone_counter: int
    start_hub: Zone
    end_hub: Zone
    drones: list[Drone] = Field(default_factory=list, exclude=True)
    adjacency: dict[Zone, list[Zone]] = Field(
        default_factory=dict, exclude=True)
    connection_map: dict[frozenset[Zone], Connection] = Field(
        default_factory=dict, exclude=True)
    zone_occupancy: dict[Zone, int] = Field(default_factory=dict, exclude=True)
    link_usage: dict[frozenset[Zone], int] = Field(
        default_factory=dict, exclude=True)
    restricted_buffer: dict[frozenset[Zone], int] = Field(
        default_factory=dict, exclude=True)

    @model_validator(mode="after")
    def validation(self: G) -> G:
        if self.drone_counter <= 0:
            raise ValueError("drone_counter must be > 0")
        return self

    def build(self) -> None:
        self.adjacency = {z: [] for z in self.zones.values()}
        self.connection_map = {}
        for c in self.connections:
            self.adjacency[c.zone1].append(c.zone2)
            self.adjacency[c.zone2].append(c.zone1)
            self.connection_map[c.key()] = c
        self.zone_occupancy = {
            z: 0 for z in self.zones.values()
        }
        self.link_usage = {}

    def create_connections(
            self, name1: str, name2: str, capacity: int) -> Connection:
        return Connection(
            zone1=self.zones[name1],
            zone2=self.zones[name2],
            max_link_capacity=capacity
        )

    def create_drones(self) -> None:
        self.drones = []
        for i in range(1, self.drone_counter + 1):
            d = Drone(f"D{i}")
            d.zone = self.start_hub
            self.zone_occupancy[d.zone] += 1
            self.drones.append(d)
