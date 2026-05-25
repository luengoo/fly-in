from pydantic import BaseModel, model_validator, Field


class Zone(BaseModel):
    name: str
    x: int
    y: int
    zone_type: str = "normal"
    color: str | None = None
    max_drones: int = 1
    hub_type: str

    @model_validator(mode="after")
    def validate(self):
        if self.zone_type not in {
          "normal", "blocked", "restricted", "priority"}:
            raise ValueError("Invalid zone_type")
        if self.name == "goal":
            self.max_drones = 42222222
        if self.max_drones < 0:
            raise ValueError("max_drones must be >= 0")
        return self


class Connection(BaseModel):
    zone1: str
    zone2: str
    max_link_capacity: int = 1

    @model_validator(mode="after")
    def validate(self):
        if self.max_link_capacity < 0:
            raise ValueError("invalid capacity")
        return self


class Drone:
    def __init__(self, drone_id: str):
        self.id = drone_id
        self.position = None
        self.path = []
        self.path_index = 0
        self.finished = False
        self.in_transit = False
        self.remaining_turns = 0
        self.target_zone = None


class Graph(BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    zones: dict[str, Zone] = Field(default_factory=dict)
    connections: list[Connection] = Field(default_factory=list)
    drone_counter: int
    start_hub: Zone
    end_hub: Zone
    drones: list[Drone] = Field(default_factory=list, exclude=True)
    adjacency: dict[str, list[str]] = Field(default_factory=dict, exclude=True)
    connection_map: dict[tuple[str, str], Connection] = Field(
        default_factory=dict, exclude=True)
    zone_occupancy: dict[str, int] = Field(default_factory=dict, exclude=True)
    link_usage: dict[tuple[str, str], int] = Field(
        default_factory=dict, exclude=True)

    @model_validator(mode="after")
    def validate(self):
        if self.drone_counter <= 0:
            raise ValueError("drone_counter must be > 0")
        return self

    def build(self):
        self.adjacency = {z: [] for z in self.zones}

        self.connection_map = {}
        for c in self.connections:
            self.adjacency[c.zone1].append(c.zone2)
            self.adjacency[c.zone2].append(c.zone1)
            self.connection_map[tuple(sorted((c.zone1, c.zone2)))] = c

        self.zone_occupancy = {z: 0 for z in self.zones}
        self.link_usage = {}

    def create_drones(self):
        self.drones = []
        for i in range(1, self.drone_counter + 1):
            d = Drone(f"D{i}")
            d.position = self.start_hub.name
            self.drones.append(d)
            self.zone_occupancy[d.position] += 1
