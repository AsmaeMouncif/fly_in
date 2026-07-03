class ParserError(Exception):
    pass


class Parser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.nb_drones_defined = False

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
            self.parse_nb_drones(line)
        elif line.startswith("end_hub:"):
            self.parse_nb_drones(line)
        elif line.startswith("hub:"):
            self.parse_nb_drones(line)
        elif line.startswith("connection:"):
            self.parse_nb_drones(line)
        else:
            raise ParserError(f"Unknown line: {line}")

    def parse_nb_drones(self, line):
        if self.nb_drones_defined == True:
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