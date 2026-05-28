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
        if path in different_paths or path is None:
            break
        different_paths.append(path)

    paths_cycle = cycle(different_paths)
    for d in graph.drones:
        d.path = next(paths_cycle)

    turn = 0
    while not all(d.finished for d in graph.drones):
        turn += 1
        logs = []

        for d in graph.drones:
            if d.finished:
                continue
            if not d.in_transit:
                continue
            d.remaining_turns -= 1
            if d.remaining_turns <= 0:
                edge = d.buffer_edge
                if edge in graph.link_usage:
                    graph.link_usage[edge] -= 1
                    if graph.link_usage[edge] <= 0:
                        del graph.link_usage[edge]

                d.zone = d.target_zone
                graph.zone_occupancy[d.zone] += 1

                d.in_transit = False
                d.buffer_zone = None
                d.buffer_edge = None
                d.path_index += 1
                d.just_arrived = True
                logs.append(
                    (d, f"arrived to restricted zone {d.zone.name}",
                     d.zone.color)
                )
            continue

        for d in graph.drones:
            if d.finished or d.in_transit or getattr(d, "just_arrived", False):
                continue

            if d.path_index >= len(d.path) - 1:
                d.finished = True
                continue

            cur = d.zone
            nxt = d.path[d.path_index + 1]
            edge = frozenset((cur, nxt))
            conn = graph.connection_map.get(edge)

            if nxt.zone_type in {
              "normal", "priority"} or nxt.hub_type == "end_hub":
                if nxt.hub_type == "end_hub" or graph.zone_occupancy.get(
                  nxt, 0) < nxt.max_drones:
                    graph.zone_occupancy[cur] -= 1
                    if nxt.hub_type != "end_hub":
                        graph.zone_occupancy[nxt] += 1
                    d.zone = nxt
                    d.path_index += 1
                    logs.append((d, f"moved to {nxt.name}", nxt.color))
                    if nxt.hub_type == "end_hub":
                        d.finished = True
                else:
                    logs.append((d, f"waiting at {cur.name}", "warning"))

            elif nxt.zone_type == "restricted":
                if conn is None:
                    logs.append((d, f"No connection to {nxt.name}", "red"))
                    continue

                if graph.link_usage.get(edge, 0) >= conn.max_link_capacity:
                    logs.append((d, f"waiting at {cur.name} (connection full)",
                                 "warning"))
                    continue

                graph.link_usage[edge] = graph.link_usage.get(edge, 0) + 1
                graph.zone_occupancy[cur] -= 1

                d.in_transit = True
                d.remaining_turns = 1
                d.target_zone = nxt
                d.buffer_zone = cur
                d.buffer_edge = edge

                logs.append((d,
                             f"entering buffer to restricted zone {nxt.name}",
                             "magenta"))
        for d in graph.drones:
            d.just_arrived = False
        if logs:
            print(f"\n======== TURN {turn} ========")
        for drone, msg, color in logs:
            Colors.print(f"{drone.id} {msg}", color)
