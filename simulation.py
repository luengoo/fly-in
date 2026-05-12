from colors import Colors

def initialize_occupancy(self):
        self.zone_occupancy = {
            zone: 0
            for zone in self.zones
        }
        self.link_usage = {}

def simulate(self):
        self.create_drones()
        path, cost = self.dijkstra()
        print("\nBest path:\n")

        for zone_name in path:
            zone = self.zones[zone_name]

            Colors.print(
                f"{zone.name} ({zone.zone_type})",
                zone.color
            )

        print(f"\nTotal cost: {cost}")

def turns

def collisions

def waiting

def schedule