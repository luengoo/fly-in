from models import Zone, Connection, Graph

class Parser():
    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        with open(self.filename, "r") as file:
            connections = []
            zones = {}
            drone_counter = 0
            start_hub = None
            end_hub = None

            for line in file:
                line = line.strip()
                if line.startswith("#") or not line:
                    continue
                result = self.parse_line(line)
                if isinstance(result, int):
                    drone_counter = result
                if isinstance(result, Zone):
                    zones[result.name] = result
                    if result.hub_type == "start_hub":
                        start_hub = result
                    if result.hub_type == "end_hub":
                        end_hub = result
                elif isinstance(result, Connection):
                    connections.append(result)
            if not start_hub or not end_hub:
                raise ValueError("Missing start_hub or end_hub")
            graph = Graph(zones=zones, connections=connections, drone_counter=drone_counter, start_hub=start_hub, end_hub=end_hub)
            return graph

    @staticmethod
    def parse_line(line):
        meta_dict = {}
        if line.startswith("nb_drones"):
            return int(line.split(":")[1].strip())
        if line.startswith("start_hub") or line.startswith("end_hub") or line.startswith("hub"):
            prefix, rest = line.split(":")
            meta = ""
            if "[" in rest:
                main, meta = rest.split("[")
                meta = meta.strip("]")
            else:
                main = rest
            parts = main.split()
            name = parts[0]
            x = int(parts[1])
            y = int(parts[2])

            for item in meta.split():
                key, value = item.split("=")
                meta_dict[key] = value
            
            return Zone(hub_type=prefix, name=name, x=x, y=y, color=meta_dict.get("color", None), max_drones=int(meta_dict.get("max_drones", 1)))
        
        if line.startswith("connection"):
            _, rest = line.split(":", 1)
            rest = rest.strip()

            if "[" in rest:
                main, meta_str = rest.split("[")
                meta_str = meta_str.strip("]")
                capacity = int(meta_str.split("=")[1])

            else:
                main = rest
                capacity = 1

            try:
                zone1, zone2 = main.strip().split("-")
            except Exception:
                raise ValueError("connection name cannot contain '-' characters")
            
            return Connection(zone1=zone1, zone2=zone2, max_link_capacity=capacity)