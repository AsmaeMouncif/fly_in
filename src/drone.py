class Drone:
    def __init__(self, path, drone_id=0):
        self.path = path
        self.path_index = 0
        self.drone_id = drone_id
        self.anim_from = path[0] if path else None
        self.anim_to = path[0] if path else None
        self.travel_step = 0
        self.travel_total_steps = 1
        self.travel_connection = None

    @property
    def current_zone(self):
        return self.path[self.path_index]

    @property
    def next_zone(self):
        if self.path_index + 1 < len(self.path):
            return self.path[self.path_index + 1]
        return None
