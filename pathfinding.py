import heapq
from colors import Colors
from models import Zone

def get_neighbors(self, zone) -> list[Zone]:
        neighbors = []
        for connection in self.connections:
            if connection.zone1 == zone.name and connection.zone2 in self.zones:
                neighbors.append(self.zones[connection.zone2])
            elif connection.zone2 == zone.name and connection.zone1 in self.zones:
                neighbors.append(self.zones[connection.zone1])
        return neighbors

@staticmethod
def calculate_movement_cost(from_zone: Zone, to_zone: Zone) -> int:
    if to_zone.zone_type == "blocked":
        return float("inf")
    
    dx = to_zone.x - from_zone.x
    dy = to_zone.y - from_zone.y
    distance = abs(dx) + abs(dy)
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