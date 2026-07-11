import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import re
import pygame
from .zone import Zone, DEFAULT_COLOR
from .connection import Connection
from .graph import Graph


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.nb_drones_defined = False
        self.start_hub_defined = False
        self.end_hub_defined = False
        self.zones = set()
        self.zone_objects = {}
        self.connections = []
        self.connection_keys = set()
        self.start_hub_name = None
        self.end_hub_name = None

    @staticmethod
    def strip_comment(line):
        line = line.strip()
        if line.startswith("#"):
            return ""
        line = re.split(r"\s+#", line, maxsplit=1)[0]
        return line.strip()

    def parse_file(self):
        try:
            with open(self.file_path, "r") as file:
                lines = []
                for line_number, raw_line in enumerate(file, start=1):
                    content = self.strip_comment(raw_line)
                    if not content:
                        continue
                    lines.append((line_number, content))
        except FileNotFoundError:
            raise ParserError(f"File not found: {self.file_path}")
        except PermissionError:
            raise ParserError(f"Permission denied: {self.file_path}")
        except IsADirectoryError:
            raise ParserError(f"Expected a file, got a directory: {self.file_path}")
        except OSError as e:
            raise ParserError(f"Cannot read file {self.file_path}: {e}")
        if not lines:
            raise ParserError(f"Empty file: {self.file_path}")
        first_line_number, first_content = lines[0]
        if not first_content.startswith("nb_drones:"):
            raise ParserError(
                f"Line {first_line_number}: nb_drones must be the first line of the file"
            )
        contents_only = []
        for line_number, content in lines:
            contents_only.append(content)
        self.validate_required_fields(contents_only)
        for line_number, content in lines:
            try:
                self.parse_line(content)
            except ParserError as e:
                raise ParserError(f"Line {line_number}: {e}") from e
        self.ignore_start_end_max_drones()
        self.graph = self.build_graph()

    def build_graph(self):
        graph = Graph()
        for zone in self.zone_objects.values():
            graph.add_zone(zone)
        for connection in self.connections:
            graph.add_connection(connection)
        return graph

    def ignore_start_end_max_drones(self):
        if self.start_hub_name is not None:
            self.zone_objects[self.start_hub_name].max_drones = self.nb_drones
        if self.end_hub_name is not None:
            self.zone_objects[self.end_hub_name].max_drones = self.nb_drones

    def validate_required_fields(self, lines):
        has_nb_drones = False
        has_start_hub = False
        has_end_hub = False
        for line in lines:
            if line.startswith("nb_drones:"):
                has_nb_drones = True
            if line.startswith("start_hub:"):
                has_start_hub = True
            if line.startswith("end_hub:"):
                has_end_hub = True
        if not has_nb_drones:
            raise ParserError("Missing nb_drones definition")
        if not has_start_hub:
            raise ParserError("Missing start_hub definition")
        if not has_end_hub:
            raise ParserError("Missing end_hub definition")

    def parse_line(self, line):
        if line.startswith("nb_drones:"):
            self.parse_nb_drones(line)
        elif line.startswith("start_hub:"):
            self.parse_start_hub(line)
        elif line.startswith("end_hub:"):
            self.parse_end_hub(line)
        elif line.startswith("hub:"):
            self.parse_hub(line)
        elif line.startswith("connection:"):
            self.parse_connection(line)
        else:
            raise ParserError(f"Unknown line {line}")

    def parse_nb_drones(self, line):
        if self.nb_drones_defined:
            raise ParserError("nb_drones defined multiple times")
        parts = line.split(":")
        if len(parts) != 2 or not parts[1].strip():
            raise ParserError("Invalid nb_drones format")
        try:
            nb_drones = int(parts[1].strip())
        except ValueError:
            raise ParserError("Invalid drone count")
        if nb_drones <= 0:
            raise ParserError("Drone count must be greater than 0")
        self.nb_drones = nb_drones
        self.nb_drones_defined = True

    def parse_start_hub(self, line):
        if self.start_hub_defined:
            raise ParserError("start_hub defined multiple times")
        parts = line.split(":", 1)
        if len(parts) != 2 or not parts[1].strip():
            raise ParserError("Invalid start_hub format")
        data = parts[1].strip()
        metadata = None
        if "[" in data:
            zone_data, metadata = data.split("[", 1)
            if not metadata.strip().endswith("]"):
                raise ParserError("Invalid metadata format")
            metadata = metadata.strip().rstrip("]")
        else:
            zone_data = data
        zone_data = zone_data.strip().split()
        if len(zone_data) != 3:
            raise ParserError("Invalid start_hub format")
        self.validate_zone_name(zone_data[0])
        x, y = self.validate_coordinates(zone_data[1], zone_data[2])
        zone = Zone(zone_data[0], x, y)
        self.zone_objects[zone.name] = zone
        self.start_hub_name = zone.name
        if metadata is not None:
            self.parse_zone_metadata(zone, metadata)
        self.start_hub_defined = True

    def parse_end_hub(self, line):
        if self.end_hub_defined:
            raise ParserError("end_hub defined multiple times")
        parts = line.split(":", 1)
        if len(parts) != 2 or not parts[1].strip():
            raise ParserError("Invalid end_hub format")
        data = parts[1].strip()
        metadata = None
        if "[" in data:
            zone_data, metadata = data.split("[", 1)
            if not metadata.strip().endswith("]"):
                raise ParserError("Invalid metadata format")
            metadata = metadata.strip().rstrip("]")
        else:
            zone_data = data
        zone_data = zone_data.strip().split()
        if len(zone_data) != 3:
            raise ParserError("Invalid end_hub format")
        self.validate_zone_name(zone_data[0])
        x, y = self.validate_coordinates(zone_data[1], zone_data[2])
        zone = Zone(zone_data[0], x, y)
        self.zone_objects[zone.name] = zone
        self.end_hub_name = zone.name
        if metadata is not None:
            self.parse_zone_metadata(zone, metadata)
        self.end_hub_defined = True

    def parse_hub(self, line):
        parts = line.split(":", 1)
        if len(parts) != 2 or not parts[1].strip():
            raise ParserError("Invalid hub format")
        data = parts[1].strip()
        metadata = None
        if "[" in data:
            zone_data, metadata = data.split("[", 1)
            if not metadata.strip().endswith("]"):
                raise ParserError("Invalid metadata format")
            metadata = metadata.strip().rstrip("]")
        else:
            zone_data = data
        zone_data = zone_data.strip().split()
        if len(zone_data) != 3:
            raise ParserError("Invalid hub format")
        self.validate_zone_name(zone_data[0])
        x, y = self.validate_coordinates(zone_data[1], zone_data[2])
        zone = Zone(zone_data[0], x, y)
        self.zone_objects[zone.name] = zone
        if metadata is not None:
            self.parse_zone_metadata(zone, metadata)

    def parse_connection(self, line):
        max_link_capacity = 1
        parts = line.split(":", 1)
        if len(parts) != 2:
            raise ParserError("Invalid connection format")
        data = parts[1].strip()
        parts = data.split()
        if len(parts) not in (1, 2):
            raise ParserError("Invalid connection format")
        connection = parts[0]
        zones = connection.split("-")
        if len(zones) != 2:
            raise ParserError("Invalid connection format")
        zone1 = zones[0]
        zone2 = zones[1]
        if not zone1 or not zone2:
            raise ParserError("Invalid connection format")
        if zone1 == zone2:
            raise ParserError("A zone cannot connect to itself")
        if zone1 not in self.zones:
            raise ParserError(f"Unknown zone {zone1}")
        if zone2 not in self.zones:
            raise ParserError(f"Unknown zone {zone2}")
        connection_key = frozenset((zone1, zone2))
        if connection_key in self.connection_keys:
            raise ParserError(f"Duplicate connection {zone1}-{zone2}")
        self.connection_keys.add(connection_key)
        if len(parts) == 2:
            max_link_capacity = self.parse_connection_metadata(parts[1])
        self.connections.append(Connection(zone1, zone2, max_link_capacity))

    def validate_zone_name(self, name):
        if "-" in name:
            raise ParserError("Zone name cannot contain dashes")
        if " " in name:
            raise ParserError("Zone name cannot contain spaces")
        if name in self.zones:
            raise ParserError(f"Zone name already used {name}")
        self.zones.add(name)

    def validate_coordinates(self, x, y):
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            raise ParserError("Invalid coordinate values")
        return x, y

    def parse_zone_metadata(self, zone, metadata):
        allowed_names = ["zone", "color", "max_drones"]
        seen_names = set()
        metadata = metadata.split()
        for part in metadata:
            if "=" not in part:
                raise ParserError("Invalid metadata format")
            name, value = part.split("=", 1)
            if name not in allowed_names:
                raise ParserError(f"Unknown metadata: {name}")
            if name in seen_names:
                raise ParserError(f"Duplicate metadata: {name}")
            seen_names.add(name)
            if name == "zone":
                allowed_types = ["normal", "blocked", "restricted", "priority"]
                if value not in allowed_types:
                    raise ParserError(f"Invalid zone type: {value}")
                zone.zone_type = value
            elif name == "color":
                zone.color = self.resolve_color(value)
            elif name == "max_drones":
                try:
                    value = int(value)
                except ValueError:
                    raise ParserError("Invalid max_drones value")
                if value <= 0:
                    raise ParserError("Invalid max_drones value")
                zone.max_drones = value

    def parse_connection_metadata(self, metadata):
        if not metadata.startswith("[") or not metadata.endswith("]"):
            raise ParserError(f"Invalid metadata block: {metadata}")
        content = metadata[1:-1]
        if "max_link_capacity=" not in content:
            raise ParserError("Invalid metadata format")
        parts = content.split("=")
        if len(parts) != 2:
            raise ParserError("Invalid metadata format")
        max_link_capacity = parts[1]
        try:
            max_link_capacity = int(max_link_capacity)
        except ValueError:
            raise ParserError("Invalid max_link_capacity value")
        if max_link_capacity <= 0:
            raise ParserError("Invalid max_link_capacity value")
        return max_link_capacity

    def resolve_color(self, value):
        try:
            pygame.Color(value)
        except ValueError:
            return DEFAULT_COLOR
        return value
