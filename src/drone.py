from typing import List


class Drone:
    def __init__(self, path: List[str], drone_id: int = 0) -> None:
        self.path: List[str] = path
        self.path_index: int = 0
        self.drone_id: int = drone_id

    @property
    def current_zone(self) -> str:
        return self.path[self.path_index]

    @property
    def next_zone(self) -> str | None:
        if self.path_index + 1 < len(self.path):
            return self.path[self.path_index + 1]
        return None
