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
        graph.connection_map = {
               tuple(sorted([c.zone1, c.zone2])): c
              for c in graph.connections
        }

        graph.create_drones()
        for drone in graph.drones:
               path, _ = dijkstra_for_drone(graph, drone)
               drone.path = path
               graph.zone_occupancy[drone.position] += 1
        simulate_turns(graph)

def simulate_turns(graph):
       turn = 0
       active_index = 0
       while not all(drone.finished for drone in graph.drones):
              
              turn += 1
              print(f"\n======== TURN {turn} ========")
              graph.link_usage.clear()
              planned_moves = []
              if active_index < len(graph.drones):
                            graph.drones[active_index].active = True
                            active_index += 1
              for drone in graph.drones:
                     if not drone.active or drone.finished:
                            continue

                     if not drone.path or drone.path_index >= len(drone.path) - 1:
                            drone.finished = True
                            graph.zone_occupancy[drone.position] -= 1
                            continue

                     current_zone = graph.zones[drone.position]
                     next_zone_name = drone.path[drone.path_index + 1]
                     next_zone = graph.zones[next_zone_name]

                     if graph.zone_occupancy[next_zone_name] >= next_zone.max_drones:
                            drone.waiting = True
                            continue

                     edge = tuple(sorted([current_zone.name, next_zone_name]))
                     connection = graph.connection_map.get(edge)
                     max_capacity = connection.max_link_capacity if connection else 1

                     if graph.link_usage.get(edge, 0) >= max_capacity:
                            drone.waiting = True
                            continue

                     planned_moves.append((drone, current_zone, next_zone, edge))
                     drone.waiting = False

                     graph.zone_occupancy[next_zone_name] += 1
                     graph.zone_occupancy[current_zone.name] -= 1
                     graph.link_usage[edge] = graph.link_usage.get(edge, 0) + 1

              for drone, current_zone, next_zone, edge in planned_moves:
                     drone.position = next_zone.name
                     drone.path_index += 1

                     Colors.print(f"{drone.ID} moved to {next_zone.name} ({next_zone.zone_type})", next_zone.color)
                     for d in graph.drones:
                            if d.waiting and not d.finished:
                                Colors.print(f"{d.ID} WAITING at {d.position}", "yellow")   
                     
