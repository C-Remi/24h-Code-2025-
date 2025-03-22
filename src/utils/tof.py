import random

class TimeOfFlightSensor:
    """Simulated Time-of-Flight (ToF) sensor."""
    def get_distance(self):
        """Returns a random distance in cm (simulating a real sensor)."""
        return random.randint(50, 300)  # Simulated distance values