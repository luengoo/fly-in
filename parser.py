from models import Zone, Connection, Graph


class Parser:
    def __init__(self, filename: str):
        self.filename = filename

    def parse(self) -> Graph:
        pending_connections = []
        zones = {}
        drone_counter = 0
        start_hub = None
        end_hub = None

        with open(self.filename, "r") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                result = self.parse_line(line)

                if isinstance(result, int):
                    drone_counter = result

                elif isinstance(result, Zone):
                    zones[result.name] = result

                    if result.hub_type == "start_hub":
                        start_hub = result
                    elif result.hub_type == "end_hub":
                        end_hub = result

                else:
                    pending_connections.append(result)

        if start_hub is None or end_hub is None:
            raise ValueError("Missing start_hub or end_hub")

        connections = []

        for zone1_name, zone2_name, capacity in pending_connections:
            zone1 = zones.get(zone1_name)
            zone2 = zones.get(zone2_name)
            if not zone1 or not zone2:
                raise ValueError("Invalid connection")
            connections.append(
                Connection(
                    zone1=zone1,
                    zone2=zone2,
                    max_link_capacity=capacity
                )
            )

        graph = Graph(
            zones=zones,
            connections=connections,
            drone_counter=drone_counter,
            start_hub=start_hub,
            end_hub=end_hub
        )

        graph.build()

        return graph

    @staticmethod
    def parse_line(line: str) -> Connection | int | Zone | None:
        ZONE_COLORS = {
            "normal": "white",
            "restricted": "red",
            "priority": "green",
            "blocked": "gray"
        }

        meta_dict = {}

        if line.startswith("nb_drones"):
            return int(line.split(":")[1].strip())

        if line.startswith(("start_hub", "end_hub", "hub")):
            prefix, rest = line.split(":", 1)

            meta = ""
            if "[" in rest:
                main, meta = rest.split("[", 1)
                meta = meta.strip("]")
            else:
                main = rest

            parts = main.split()
            name = parts[0]
            x = int(parts[1])
            y = int(parts[2])

            if meta:
                for item in meta.split():
                    key, value = item.split("=")
                    meta_dict[key] = value

            zone_type = meta_dict.get("zone", "normal")

            return Zone(
                hub_type=prefix,
                name=name,
                x=x,
                y=y,
                zone_type=zone_type,
                color=meta_dict.get(
                    "color", ZONE_COLORS.get(zone_type, "white")),
                max_drones=int(meta_dict.get("max_drones", 1))
            )

        if line.startswith("connection"):
            _, rest = line.split(":", 1)
            rest = rest.strip()

            capacity = 1

            if "[" in rest:
                main, meta = rest.split("[", 1)
                meta = meta.strip("]")
                capacity = int(meta.split("=")[1])
            else:
                main = rest

            try:
                zone1, zone2 = main.strip().split("-", 1)
            except ValueError:
                raise ValueError(
                    "connection name cannot contain '-' characters")

            return (zone1, zone2, capacity)
        return None
