from pathfinding import dijkstra
from colors import Colors


def simulate(graph):

    graph.build()
    graph.create_drones()

    for d in graph.drones:
        d.path = dijkstra(graph, d.position, graph.end_hub.name)

    turn = 0

    while not all(d.finished for d in graph.drones):

        turn += 1
        graph.link_usage.clear()

        print(f"\n======== TURN {turn} ========")

        logs = []

        for d in graph.drones:

            if d.finished:
                continue

            if d.in_transit:
                d.remaining_turns -= 1

                if d.remaining_turns == 0:
                    d.in_transit = False
                    d.position = d.target_zone
                    d.path_index += 1
                    logs.append(
                        (d, f"arrived at {d.position}", graph.zones[d.position].color)
                    )
                continue

            if d.path_index >= len(d.path) - 1:
                d.finished = True
                continue

            cur = d.position
            nxt = d.path[d.path_index + 1]

            edge = tuple(sorted((cur, nxt)))

            if graph.zone_occupancy[nxt] >= graph.zones[nxt].max_drones:
                logs.append((d, f"WAITING at {cur}", "yellow"))
                continue

            if graph.link_usage.get(edge, 0) >= graph.connection_map[edge].max_link_capacity:
                logs.append((d, f"WAITING at {cur}", "yellow"))
                continue

            graph.zone_occupancy[cur] -= 1
            graph.zone_occupancy[nxt] += 1
            graph.link_usage[edge] = graph.link_usage.get(edge, 0) + 1

            if graph.zones[nxt].zone_type == "restricted":
                d.in_transit = True
                d.remaining_turns = 1
                d.target_zone = nxt
                logs.append((d, f"entering restricted zone {nxt}", "magenta"))

            else:
                d.position = nxt
                d.path_index += 1
                logs.append((d, f"moved to {nxt} ({graph.zones[nxt].zone_type})", graph.zones[nxt].color))

        for drone, msg, color in logs:
            Colors.print(f"{drone.id} {msg}", color)