class Parser:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse_file(self):
        with open(self.file_path, "r") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue
                
                self.parse_line(line)

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
            print(f"Unknown line: {line}")

    # def parse_nb_drones(self, line):
    #     value = int(line.split(":")[1].strip())
    #     print(f"Number of drones: {value}")
