from pydantic import BaseModel, model_validator, ValidationError, Field
from heapq import heapq

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

    class Graph(BaseModel):
        zones: dict[str, Zone] = Field(default_factory=dict)
        connections: list[Connections] = Field(default_factory=list)
        drone_counter: int = Field(default_factory=int)
        drones: list = Field(default_factory=list, exclude=True)
        start_hub: Zone
        end_hub: Zone

        @model_validator(mode="after")
        def validate_graph(self):
            if self.drone_counter <= 0:
                raise ValueError("Drone count must be greater than 0")
            return self
        
        def create_drones(self) -> None:
            for i in range(1, self.drone_counter + 1):
                self.drones.append(Drone(f"D{i}"))
            starting_hub = self.start_hub
            for drone in self.drones:
                drone.position = starting_hub.name
                print(f"Drone: {drone.ID} starting in position: {drone.position}")

        def get_neighbors(self, zone) -> list[Zone]:
            neighbors = []
            for connection in self.connections:
                if connection.zone1 == zone.name:
                    neighbors.append(self.zones[connection.zone2])
                if connection.zone2 == zone.name:
                    neighbors.append(self.zones[connection.zone1])
            return neighbors
        
        def simulate(self):
            self.create_drones()

        @staticmethod
        def calculate_movement_costs():
            pass

        def dijkstra(self):
            pass