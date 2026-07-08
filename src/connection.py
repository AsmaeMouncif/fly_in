
class Connection:
    def __init__(self, zone1, zone2, max_link_capacity):
        self.zone1 = zone1
        self.zone2 = zone2
        self.max_link_capacity = max_link_capacity

    def find_other_end(self, zone_name):
        if zone_name == self.zone1:
            return self.zone2
        else:
            return self.zone1
