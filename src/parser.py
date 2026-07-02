class ParserError(Exception):
    pass


class Parser:
    def __init__(self, file_path):
        self.file_path = file_path

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

        elif line.startwith("start_hub:"):
            pass

        elif line.startwith("end_hub:"):
            pass

        elif line.startwith("hub:"):
            pass
        
        elif line.startwith("connection:"):
            pass

        else:
            raise ParserError(f"Unknown line: {line}")

    def parse_nb_drones(self, line):
        try:
            line = line.split(":")[1].strip()
            nb_drones = int(line)
        except ValueError:
            raise ParserError("nb_drones must be an integer")
        
        if nb_drones <= 0:
            raise ParserError("nb_drones must be greater than 0")
        
        return nb_drones

