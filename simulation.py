from colors import Colors
from pathfinding import dijkstra_for_drone

def initialize_occupancy(graph):
        graph.zone_occupancy = {
            zone: 0
            for zone in graph.zones
        }
        graph.link_usage = {}

def simulate(graph):
        initialize_occupancy(graph)
        graph.create_drones()
        for drone in graph.drones:
               path, _ = dijkstra_for_drone(graph, drone)
               drone.path = path
               graph.zone_occupancy[drone.position] += 1
        simulate_turns(graph)

def simulate_turns(graph):
       turn = 0
       while not all(drone.finished for drone in graph.drones):
              turn += 1
              print(f"\n======== TURN {turn} ========")
              graph.link_usage.clear()
              planned_moves = []
              for drone in sorted(graph.drones, key=lambda d: d.ID):
                     if drone.finished:
                            continue
                     if drone.path_index + 1 >= len(drone.path):
                            drone.finished = True
                            continue
                     
                     current_zone = graph.zones[drone.position]
                     next_zone_name = drone.path[drone.path_index + 1]
                     next_zone = graph.zones[next_zone_name]

                     if graph.zone_occupancy[next_zone_name] >= next_zone.max_drones:
                            drone.waiting = True
                            continue
                     
                     edge = tuple(sorted([current_zone.name, next_zone_name]))
                     connection = next((c for c in graph.connections
                                        if {c.zone1, c.zone2} == set(edge)), None)
                     max_capacity = connection.max_link_capacity if connection else 1

                     if graph.link_usage.get(edge, 0) >= max_capacity:
                            drone.waiting = True
                            continue
                     
                     planned_moves.append((drone, current_zone, next_zone, edge))
                     drone.waiting = False

              for drone, current_zone, next_zone, edge in planned_moves:
                     graph.zone_occupancy[current_zone.name] -= 1
                     graph.zone_occupancy[next_zone.name] += 1
                     graph.link_usage[edge] = graph.link_usage.get(edge, 0) + 1
                     drone.position = next_zone.name
                     drone.path_index += 1

                     Colors.print(f"{drone.ID} moved to {next_zone.name} ({next_zone.zone_type})", next_zone.color)
                     for drone in graph.drones:
                            if drone.waiting and not drone.finished:
                                Colors.print(f"{drone.ID} WAITING at {drone.position}", "yellow")   
                     
