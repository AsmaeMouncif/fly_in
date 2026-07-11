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