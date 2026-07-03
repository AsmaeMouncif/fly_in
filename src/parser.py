class ParserError(Exception):
    pass


class Parser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.nb_drones_defined = False
        self.start_hub_defined = False
        self.end_hub_defined = False

    def parse_file(self):
        try:
            with open(self.file_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    self.parse_line(line)
        except FileNotFoundError:
            raise ParserError(f"File not found: {self.file_path}")

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
            raise ParserError(f"Unknown line: {line}")

    def parse_nb_drones(self, line):
        if self.nb_drones_defined:
            raise ParserError("nb_drones defined multiple times")
        parts = line.split(":")
        if len(parts) != 2:
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
        if len(parts) != 2:
            raise ParserError("Invalid start_hub format")
        data = parts[1].strip()
        parts = data.split()
        if len(parts) not in (3, 4):
            raise ParserError("Invalid start_hub format")
        if len(parts) == 3:
            self.validate_zone_name(parts[0])
            x, y = self.validate_coordinates(parts[1], parts[2])
        if len(parts) == 4:
            self.validate_zone_name(parts[0])
            x, y = self.validate_coordinates(parts[1], parts[2])
            self.parse_metadata(parts[3])
        self.start_hub_defined = True

    def parse_end_hub(self, line):
        if self.end_hub_defined:
            raise ParserError("end_hub defined multiple times")
        parts = line.split(":", 1)
        if len(parts) != 2:
            raise ParserError("Invalid end_hub format")
        data = parts[1].strip()
        parts = data.split()
        if len(parts) not in (3, 4):
            raise ParserError("Invalid end_hub format")
        if len(parts) == 3:
            self.validate_zone_name(parts[0])
            x, y = self.validate_coordinates(parts[1], parts[2])
        if len(parts) == 4:
            self.validate_zone_name(parts[0])
            x, y = self.validate_coordinates(parts[1], parts[2])
            self.parse_metadata(parts[3])
        self.end_hub_defined = True

    def parse_hub(self, line):
        parts = line.split(":", 1)
        if len(parts) != 2:
            raise ParserError("Invalid hub format")
        data = parts[1].strip()
        parts = data.split()
        if len(parts) not in (3, 4):
            raise ParserError("Invalid hub format")
        if len(parts) == 3:
            self.validate_zone_name(parts[0])
            x, y = self.validate_coordinates(parts[1], parts[2])
        if len(parts) == 4:
            self.validate_zone_name(parts[0])
            x, y = self.validate_coordinates(parts[1], parts[2])
            self.parse_metadata(parts[3])

    def parse_connection(self, line):
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
        if len(parts) == 2:
            self.parse_metadata(parts[1])

    def validate_zone_name(self, name):
        if "-" in name:
            raise ParserError("Zone name cannot contain dashes")

    def validate_coordinates(self, x, y):
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            raise ParserError("Invalid coordinate values")
        return x, y

    def parse_metadata(self, metadata):
        pass
