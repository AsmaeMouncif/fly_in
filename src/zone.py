DEFAULT_COLOR = "white"
# MOVEMENT_COSTS = {
#     "normal": 1,
#     "priority": 1,
#     "restricted": 2,
# }


class Zone:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = "normal"
        self.color = DEFAULT_COLOR
        self.max_drones = 1

    # def is_blocked(self):
    #     return self.zone_type == "blocked"
    
    # def movement_cost(self):
    #     return MOVEMENT_COSTS[self.zone_type]
