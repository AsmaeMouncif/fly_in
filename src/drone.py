class Drone:
    def __init__(self, path):
        self.path = path
        self.path_index = 0

    @property
    def current_zone(self):
        return self.path[self.path_index]

    @property
    def next_zone(self):
        if self.path_index + 1 < len(self.path):
            return self.path[self.path_index + 1]
        return None
