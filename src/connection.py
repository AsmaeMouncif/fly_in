class Connection:
    def __init__(self, zone1: str, zone2: str, max_link_capacity: int) -> None:
        self.zone1: str = zone1
        self.zone2: str = zone2
        self.max_link_capacity: int = max_link_capacity

    def find_other_end(self, zone_name: str) -> str:
        if zone_name == self.zone1:
            return self.zone2
        else:
            return self.zone1
