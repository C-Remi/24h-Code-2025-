class Motor:
    """Simulated Motor Controller."""
    def __init__(self, name):
        self.name = name
        self.speed = 0.0

    def set_speed(self, speed):
        """Set motor speed (float between 0 and 1)."""
        self.speed = max(0.0, min(1.0, speed))  # Ensure valid range
        #print(f"{self.name} motor speed: {self.speed:.2f}")