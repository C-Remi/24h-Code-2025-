from collections import deque

class RobotGps:
    def __init__(self):
        """Initialize Robot GPS."""
        self._position_history = deque(maxlen=100000)
        self._position_crossing  = deque(maxlen=100000)

    @property
    def add_new_position(self,posX, posY, radial):
        """Append a new position"""
        self._position_history.append((posX, posY, radial))

    def get_latest(self):
        return self._position_history[-1]
    
    def __repr__(self):
        return f"GPS({self._position_history})"