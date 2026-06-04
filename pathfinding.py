import heapq
from collections import Counter
from models import Graph, Zone
from typing import List, Dict, Tuple


class Pathfinding():
    def __init__(self) -> None:
        self.best_path: List | None = None

    def dijkstra(self,
                 graph: Graph,
                 start: Zone,
                 end: Zone,
                 previous_paths: List[List[Zone]]) -> List[Zone] | None:

        edge_frequency: Counter = Counter()

        for path in previous_paths:
            for i in range(len(path) - 1):
                edge = frozenset((path[i], path[i + 1]))
                edge_frequency[edge] += 1

        dist = {
            z: float("inf")
            for z in graph.zones.values()
        }
        prev: Dict[Zone, Zone | None] = {z: None for z in graph.zones.values()}
        dist[start] = 0
        pq: List[Tuple[float, str, Zone]] = [(0, start.name, start)]
        while pq:
            cost, _, node = heapq.heappop(pq)

            if cost > dist[node]:
                continue

            if node == end:
                break

            for nxt in graph.adjacency[node]:

                if nxt.zone_type == "blocked":
                    continue

                dx = nxt.x - node.x
                dy = nxt.y - node.y
                move_cost = abs(dx) + abs(dy)

                if nxt.zone_type == "restricted":
                    move_cost += 2
                elif nxt.zone_type == "priority":
                    move_cost -= 1

                edge = frozenset((node, nxt))

                visited_penalty = edge_frequency[edge] * 10
                length_penalty = 0.5

                link = graph.connection_map.get(edge)
                link_penalty = 0

                if link and graph.link_usage.get(
                  edge, 0) >= link.max_link_capacity:
                    link_penalty = 100

                new_cost = (
                    cost
                    + move_cost
                    + length_penalty
                    + link_penalty
                    + visited_penalty
                    )

                if new_cost < dist[nxt]:
                    dist[nxt] = new_cost
                    prev[nxt] = node
                    heapq.heappush(pq, (new_cost, nxt.name, nxt))

        path = []
        cur: Zone | None = end
        while cur is not None:
            path.append(cur)
            cur = prev[cur]

        path.reverse()

        if path[0] != start:
            return None

        if self.best_path is None or len(path) < len(self.best_path):
            self.best_path = path

        return path
