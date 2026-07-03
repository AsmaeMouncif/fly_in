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
        # elif line.startswith("end_hub:"):
        #     self.parse_end_hub(line)
        # elif line.startswith("hub:"):
        #     self.parse_hub(line)
        # elif line.startswith("connection:"):
        #     self.parse_connection(line)
        # else:
        #     raise ParserError(f"Unknown line: {line}")

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

    # def parse_end_hub(self, line):
    #     if self.end_hub_defined:
    #         raise ParserError("end_hub defined multiple times")
    #     parts = line.split(":")
    #     if len(parts) != 2:
    #         raise ParserError("Invalid end_hub format")

    # def parse_hub(self, line):
    #     pass
    
    # def parse_connection(self, line):
    #     pass

    def validate_coordinates(self, x, y):
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            raise ParserError("Invalid coordinate values")
        return x, y

    def validate_zone_name(self, name):
        if "-" in name:
            raise ParserError("Zone name cannot contain dashes")
