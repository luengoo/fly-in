from models import Zone, Connection, Graph
from typing import cast, Literal, List, Dict


class Parser:
    def __init__(self, filename: str):
        self.filename = filename

    def parse(self) -> Graph:
        pending_connections: List[tuple[str, str, int]] = []
        zones: Dict = {}
        drone_counter = 0
        start_hub = None
        end_hub = None
        seen_start = False
        seen_end = False
        seen_connections: set[frozenset] = set()

        with open(self.filename, "r") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                result = self.parse_line(line)

                if isinstance(result, int):
                    if len(zones) > 0 or len(pending_connections) > 0:
                        raise ValueError(
                            f"Line {line_number}: nb_drones must"
                            " be the first definition")
                    drone_counter = result

                elif isinstance(result, Zone):
                    if result.name in zones:
                        raise ValueError(
                            f"Line {line_number}: Duplicate zone name:"
                            f"'{result.name}'")
                    zones[result.name] = result

                    if result.hub_type == "start_hub":
                        start_hub = result
                        if seen_start:
                            raise ValueError(
                                f"Line {line_number}:"
                                f"Can't have two start_hubs")
                        else:
                            seen_start = True

                    elif result.hub_type == "end_hub":
                        end_hub = result
                        if seen_end:
                            raise ValueError(
                                f"Line {line_number}:"
                                "Can't have two end_hubs")
                        else:
                            seen_end = True

                elif isinstance(result, tuple):
                    zone1_name, zone2_name, capacity = result

                    if zone1_name not in zones:
                        raise ValueError(
                            f"Line {line_number}:"
                            "Connection references undefined zone:"
                            f"'{zone1_name}'")
                    if zone2_name not in zones:
                        raise ValueError(
                            f"Line {line_number}:"
                            "Connection references undefined zone:"
                            f" '{zone2_name}'")

                    pair = frozenset({zone1_name, zone2_name})
                    if pair in seen_connections:
                        raise ValueError(
                            f"Line {line_number}: "
                            "Duplicated connection between"
                            f"'{zone1_name} and {zone2_name}'"
                        )
                    seen_connections.add(pair)
                    pending_connections.append(
                        cast(tuple[str, str, int], result))

        if start_hub is None or end_hub is None:
            raise ValueError("Missing start_hub or end_hub")

        connections = []

        for zone1_name, zone2_name, capacity in pending_connections:
            connections.append(
                Connection(
                    zone1=zones[zone1_name],
                    zone2=zones[zone2_name],
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
    def parse_line(line: str) -> tuple[str, str, int] | int | Zone | None:
        ZONE_COLORS = {
            "normal": "white",
            "restricted": "red",
            "priority": "green",
            "blocked": "gray"
        }
        VALID_ZONE_KEYS = {"zone", "color", "max_drones"}
        VALID_CONNECTION_KEYS = {"max_link_capacity"}

        meta_dict = {}

        if line.startswith("nb_drones"):
            try:
                result = int(line.split(":")[1].strip())
            except Exception:
                raise ValueError(
                    "nb_drones must be: 'nb_drones: x'. Check the .txt file")
            return result

        if line.startswith(("start_hub", "end_hub", "hub")):
            prefix, rest = line.split(":", 1)

            main: str
            meta: str = ""
            if "[" in rest:
                parts: List[str] = rest.split("[", 1)
                main = parts[0]
                meta = parts[1].strip("]")
            else:
                main = rest
                meta = ""
            try:
                if meta:
                    for item in meta.split():
                        if "=" not in item:
                            raise ValueError(
                                f"Invalid metadata format '{item}'"
                                ", expected key=value")
                        key, value = item.split("=", 1)
                        if key not in VALID_ZONE_KEYS:
                            raise ValueError(f"Unknown metadata key '{key}'")
                        meta_dict[key] = value
                parts = main.split()
                if len(parts) != 3:
                    raise ValueError(
                        f"Invalid zone name (got: '{main.strip()}')")
                name = parts[0]
                x = int(parts[1])
                y = int(parts[2])
                if '-' in name or ' ' in name:
                    raise ValueError(
                        f"Zone name '{name}' can't have dashes")
            except Exception as e:
                raise ValueError(f"Invalid value: {e}.")

            zone_type = meta_dict.get("zone", "normal")
            hub_type = cast(Literal["hub", "start_hub", "end_hub"], prefix)
            return Zone(
                hub_type=hub_type,
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
                for item in meta.split():
                    if "=" not in item:
                        raise ValueError(f"Invalid metadata format '{item}'")
                    key, value = item.split("=", 1)
                    if key not in VALID_CONNECTION_KEYS:
                        raise ValueError(
                            f"Unknown connection metadata key '{key}'")
                try:
                    capacity = int(meta.split("=")[1])
                except ValueError:
                    raise ValueError("max_link_capacity must be an integer")
            else:
                main = rest

            try:
                zone1, zone2 = main.strip().split("-", 1)
            except ValueError:
                raise ValueError("Connection must have format 'zone1-zone2'")

            return (zone1, zone2, capacity)
        return None
