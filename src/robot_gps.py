from collections import deque
from time import time

class RobotGps:
    def __init__(self):
        """Initialize Robot GPS."""
        self._position_history = deque(maxlen=100000)
        self._position_crossing  = deque(maxlen=100000)

    def add_new_position(self,posX, posY, radial):
        """Append a new position"""
        self._position_history.append((time(), posX, posY, radial))
        print(f"\t new recorded pos: {self.get_latest()}")

    def get_latest(self):
        return self._position_history[-1]

    def __repr__(self):
        return f"GPS({self._position_history})"
