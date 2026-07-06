DEFAULT_COLOR = "white"


class Zone:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = "normal"
        self.color = DEFAULT_COLOR
        self.max_drones = 1
