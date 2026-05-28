import heapq
from collections import Counter
from models import Graph


def dijkstra(graph: Graph,
             start: str,
             end: str,
             previous_paths: list[list[str]]) -> list[str] | None:

    edge_frequency: Counter = Counter()

    for path in previous_paths:
        for i in range(len(path) - 1):
            edge = (min(path[i], path[i + 1]),
                    max(path[i], path[i + 1]))
            edge_frequency[edge] += 1

    dist = {z: float("inf") for z in graph.zones}
    prev: dict[str, str | None] = {z: None for z in graph.zones}
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        cost, node = heapq.heappop(pq)

        if cost > dist[node]:
            continue

        if node == end:
            break

        for nxt in graph.adjacency[node]:

            if graph.zones[nxt].zone_type == "blocked":
                continue

            dx = graph.zones[nxt].x - graph.zones[node].x
            dy = graph.zones[nxt].y - graph.zones[node].y
            move_cost = abs(dx) + abs(dy)

            if graph.zones[nxt].zone_type == "restricted":
                move_cost += 2
            elif graph.zones[nxt].zone_type == "priority":
                move_cost -= 1

            occupancy_penalty = graph.zone_occupancy[nxt] ** 2

            edge = (min(node, nxt), max(node, nxt))

            visited_penalty = edge_frequency[edge] * 5

            link = graph.connection_map.get(edge)
            link_penalty = 0

            if link and graph.link_usage.get(
              edge, 0) >= link.max_link_capacity:
                link_penalty = 100

            new_cost = (
                cost
                + move_cost
                + occupancy_penalty
                + link_penalty
                + visited_penalty
                )

            if new_cost < dist[nxt]:
                dist[nxt] = new_cost
                prev[nxt] = node
                heapq.heappush(pq, (new_cost, nxt))

    path = []
    cur: str | None = end
    while cur is not None:
        path.append(cur)
        cur = prev[cur]

    path.reverse()

    if path[0] != start:
        return None

    return path
