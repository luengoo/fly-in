from pydantic import BaseModel, model_validator, Field
import heapq

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
    model_config = {
        "arbitrary_types_allowed": True
    }
    zones: dict[str, Zone] = Field(default_factory=dict)
    connections: list[Connection] = Field(default_factory=list)
    drone_counter: int
    drones: list[Drone] = Field(default_factory=list, exclude=True)
    start_hub: Zone
    end_hub: Zone

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
            print(f"Drone: {drone.ID} starting in position: {drone.position}")

    def get_neighbors(self, zone) -> list[Zone]:
        neighbors = []
        for connection in self.connections:
            if connection.zone1 == zone.name and connection.zone2 in self.zones:
                neighbors.append(self.zones[connection.zone2])
            elif connection.zone2 == zone.name and connection.zone1 in self.zones:
                neighbors.append(self.zones[connection.zone1])
        return neighbors
    
    def simulate(self):
        self.create_drones()
        path, cost = self.dijkstra()
        print(f"Best path: {path}")
        print(f"Total cost: {cost}")

    @staticmethod
    def calculate_movement_cost(from_zone: Zone, to_zone: Zone) -> int:
        if to_zone.zone_type == "blocked":
            return float("inf")
        
        dx = to_zone.x - from_zone.x
        dy = to_zone.y - from_zone.y
        distance = (dx + dy)
        penalty = 0
        if to_zone.zone_type == "restricted":
            penalty = 2
        elif to_zone.zone_type == "priority":
            penalty = -2

        return distance + penalty
        

    def dijkstra(self):
        start = self.start_hub.name
        end = self.end_hub.name
        visited = set()

        distances = {zone: float("inf") for zone in self.zones}
        distances[start] = 0

        previous = {zone: None for zone in self.zones}

        queue = [(0, start)]

        while queue:
            current_cost, current_zone_name = heapq.heappop(queue)
            if current_zone_name == end:
                break
            if current_zone_name in visited:
                continue
            visited.add(current_zone_name)
            current_zone = self.zones[current_zone_name]
            for neighbor in self.get_neighbors(current_zone):
                cost = self.calculate_movement_cost(current_zone, neighbor)
                new_cost = current_cost + cost
                if new_cost < distances[neighbor.name]:
                    distances[neighbor.name] = new_cost
                    previous[neighbor.name] = current_zone_name
                    heapq.heappush(queue, (new_cost, neighbor.name))
        path = []
        current = end

        while current:
            path.append(current)
            current = previous[current]
        path.reverse()
        return path, distances[end]