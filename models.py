from pydantic import BaseModel, model_validator, Field
from colors import Colors

class Zone(BaseModel):
    name: str
    x: int
    y: int
    zone_type : str = "normal"
    color: str | None = None
    max_drones: int = 1
    hub_type: str

    @model_validator(mode="after")
    def validate_zone(self):
        allowed = {"normal", "blocked", "restricted", "priority"}
        if self.zone_type not in allowed:
            raise ValueError(f"Invalid zone type: {self.zone_type}.")
        if self.max_drones < 0:
            raise ValueError(f"Invalid max_drones count: {self.max_drones}.")
        return self
    
class Connection(BaseModel):
    zone1: str
    zone2: str
    max_link_capacity: int = 1

    @model_validator(mode="after")
    def validate_connection(self):
        if self.max_link_capacity < 0:
            raise ValueError("max_link_capacity cannot be negative")
        return self
    
class Drone():
    def __init__(self, drone_id: str):
        self.ID = drone_id
        self.position = None
        self.path = []
        self.path_index = 0
        self.finished = False
        self.waiting = False
        self.active = False

class Graph(BaseModel):
    model_config = {
        "arbitrary_types_allowed": True
    }
    zones: dict[str, Zone] = Field(default_factory=dict)
    connections: list[Connection] = Field(default_factory=list)
    drone_counter: int
    drones: list[Drone] = Field(default_factory=list, exclude=True)
    start_hub: Zone
    end_hub: Zone
    zone_occupancy: dict = Field(default_factory=dict, exclude=True)
    link_usage: dict = Field(default_factory=dict, exclude=True)
    connection_map: dict = Field(default_factory=dict, exclude=True)

    @model_validator(mode="after")
    def validate_graph(self):
        if self.drone_counter <= 0:
            raise ValueError("Drone count must be greater than 0")
        for conn in self.connections:
            if conn.zone1 not in self.zones or conn.zone2 not in self.zones:
                raise ValueError(f"Invalid connection: {conn}")
        return self
    
    def create_drones(self) -> None:
        for i in range(1, self.drone_counter + 1):
            self.drones.append(Drone(f"D{i}"))
        starting_hub = self.start_hub
        for drone in self.drones:
            drone.position = starting_hub.name
            zone = self.zones[drone.position]

            Colors.print(
                f"Drone: {drone.ID} starting in position: {drone.position}",
                zone.color
            )
