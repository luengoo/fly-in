import heapq
from models import Zone

def get_neighbors(graph, zone) -> list[Zone]:
        neighbors = []
        for connection in graph.connections:
            if connection.zone1 == zone.name and connection.zone2 in graph.zones:
                neighbors.append(graph.zones[connection.zone2])
            elif connection.zone2 == zone.name and connection.zone1 in graph.zones:
                neighbors.append(graph.zones[connection.zone1])
        return neighbors

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


def dijkstra_for_drone(graph, drone):

    start = drone.position
    end = graph.end_hub.name

    visited = set()

    distances = {
        zone: float("inf")
        for zone in graph.zones
    }

    distances[start] = 0

    previous = {
        zone: None
        for zone in graph.zones
    }

    queue = [(0, start)]

    while queue:

        current_cost, current_zone_name = heapq.heappop(queue)

        if current_zone_name in visited:
            continue

        if current_zone_name == end:
            break

        visited.add(current_zone_name)

        current_zone = graph.zones[current_zone_name]

        for neighbor in get_neighbors(graph, current_zone):

            if neighbor.zone_type == "blocked":
                continue

            congestion_penalty = graph.zone_occupancy.get(
                neighbor.name,
                0
            )

            movement_cost = calculate_movement_cost(
                current_zone,
                neighbor
            )

            total_cost = (
                current_cost
                + movement_cost
                + congestion_penalty
            )

            if total_cost < distances[neighbor.name]:

                distances[neighbor.name] = total_cost

                previous[neighbor.name] = current_zone_name

                heapq.heappush(
                    queue,
                    (total_cost, neighbor.name)
                )

    path = []

    current = end

    while current:

        path.append(current)

        current = previous[current]

    path.reverse()

    return path, distances[end]