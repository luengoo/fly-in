from pathfinding import dijkstra
from colors import Colors
from itertools import cycle
from models import Graph


def simulate(graph: Graph) -> None:

    graph.build()
    graph.create_drones()
    different_paths: list = []

    while True:
        path = dijkstra(graph, graph.start_hub,
                        graph.end_hub,
                        previous_paths=different_paths)
        if path in different_paths:
            break
        different_paths.append(path)

    paths_cycle = cycle(different_paths)
    for d in graph.drones:
        d.path = next(paths_cycle)

    turn = 0

    while not all(d.finished for d in graph.drones):

        turn += 1
        graph.link_usage.clear()

        logs = []

        for d in graph.drones:

            if d.finished:
                continue

            if d.in_transit:
                d.remaining_turns -= 1
                if d.remaining_turns <= 0:
                    edge = d.buffer_edge
                    d.zone = d.target_zone
                    graph.zone_occupancy[d.zone] += 1
                    d.in_transit = False
                    d.target_zone = None
                    d.buffer_zone = None
                    d.path_index += 1

                    logs.append((d, f"arrived to {d.zone.name}", d.zone.color))
                    continue

            if d.path_index >= len(d.path) - 1:
                d.finished = True
                continue

            cur = d.zone
            nxt = d.path[d.path_index + 1]
            edge = frozenset((cur, nxt))
            d.buffer_edge = edge
            conn = graph.connection_map.get(edge)

            if nxt.zone_type in {"normal", "priority"}:
                if graph.zone_occupancy[nxt] < nxt.max_drones:
                    graph.zone_occupancy[cur] -= 1
                    graph.zone_occupancy[nxt] += 1
                    d.zone = nxt
                    d.path_index += 1
                    logs.append((d, f"moved to {nxt.name}", nxt.color))
                else:
                    logs.append((d, f"waiting at {cur.name}", "yellow"))

            elif nxt.zone_type == "restricted":
                if graph.link_usage.get(edge, 0) < conn.max_link_capacity:
                    graph.link_usage[edge] = graph.link_usage.get(edge, 0) + 1
                    graph.zone_occupancy[cur] -= 1

                    d.in_transit = True
                    d.remaining_turns = 1
                    d.target_zone = nxt
                    d.buffer_zone = cur

                    logs.append((d, f"entering to restricted zone {nxt.name}", "magenta"))
                else:
                    logs.append((d, f"waiting at {cur.name}", "yellow"))

        if logs:
            print(f"\n======== TURN {turn} ========")
        for drone, msg, color in logs:
            Colors.print(f"{drone.id} {msg}", color)
