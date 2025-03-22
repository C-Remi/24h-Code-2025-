
from utils.wsclient import WebSocketClient
from api.infos import readInfos, INFOS_POSITION, INFOS_LED, INFOS_MOTORS, INFOS_RANGEFINDER, INFOS_SPEED, INFOS_WHEELS
from api.request import reset_position, set_led_color
from utils.tof import TimeOfFlightSensor
from robot_gps import RobotGps
from motor import Motor
import time
import struct

period_ms = 500

class Robot:
    def __init__(
        self,
        x=0,
        y=0,
        radial=0,
        host="192.168.84.6",
        step_angle=10,
        max_angle=360,
        path_threshold=100,
        kp=0.1
        ):
        """Initialize Robot with x, y coordinates and radial angle."""
        self._x = x
        self._y = y
        self._radial = radial  # Angle in degrees
        self._host = host
        self._uri_ws_info = f"ws://{self._host}/infos.ws"
        self._uri_ws_motors = f"ws://{self._host}/motors.ws"
        self._ws_client_info = WebSocketClient(self._uri_ws_info)
        self._ws_client_motors = WebSocketClient(self._uri_ws_motors)

        self.step_angle = step_angle
        self.max_angle = max_angle
        self.path_threshold = path_threshold
        self.sensor = TimeOfFlightSensor()  # Simulated ToF sensor
        self.detected_paths = []  # Stores angles with open paths
        self.kp = kp

        self.left_motor = Motor("left_motor")
        self.right_motor = Motor("right_motor")

        self.gps = RobotGps()
        reset_position(self._host)
        set_led_color(self._host, "#ffffff")


    @property
    def x(self):
        """Get the x-coordinate."""
        return self._x

    @x.setter
    def x(self, value):
        """Set the x-coordinate."""
        if isinstance(value, (int, float)):
            self._x = value
        else:
            raise ValueError("X must be a number.")

    @property
    def y(self):
        """Get the y-coordinate."""
        return self._y

    @y.setter
    def y(self, value):
        """Set the y-coordinate."""
        if isinstance(value, (int, float)):
            self._y = value
        else:
            raise ValueError("Y must be a number.")

    @property
    def radial(self):
        """Get the radial angle (0 to 360 degrees)."""
        return self._radial

    @radial.setter
    def radial(self, value):
        """Set the radial angle and keep it within 0-360 degrees."""
        if isinstance(value, (int, float)):
            self._radial = value % 360  # Ensure it's always within 0-360
        else:
            raise ValueError("Radial must be a number.")

    async def activate(self):
        while True:
            # Connect to information WS
            if self._ws_client_motors.is_closed():
                await self._ws_client_motors.connect()

            if self._ws_client_info.is_closed():
                await self._ws_client_info.connect()
                print(b'2' + bytes([INFOS_POSITION | INFOS_LED | INFOS_MOTORS | INFOS_RANGEFINDER | INFOS_SPEED | INFOS_WHEELS]))
                await self._ws_client_info.send_message(b'2' + bytes([INFOS_POSITION | INFOS_LED | INFOS_MOTORS | INFOS_RANGEFINDER | INFOS_SPEED | INFOS_WHEELS]))
                

            # Read INFO WS
            msg = await self._ws_client_info.receive_message()
            try:
                readInfos(msg)
            except:
                pass

    async def set_motor_speed(self, vl, vr):
        vl = max(-1, min(vl, 1))
        vr = max(-1, min(vr, 1))
        motor_buffer = struct.pack('ff', vl, vr)

        self.left_motor.set_speed(vl)
        self.right_motor.set_speed(vr)
        await self._ws_client_motors.send_message(motor_buffer)
        #print(f"motor_buffer: {motor_buffer}")
        time.sleep(0.1)

    async def move_straight(self, initial_radial,  radial, base_speed=1.0):
        """
        Moves the robot straight based on position and radial angle.
        :param x: Current X position
        :param y: Current Y position
        :param radial: Current orientation (degrees)
        :param base_speed: Base motor speed (float)
        """
        # Normalize radial to range [-180, 180] for better error correction
        #heading_error = (radial + 180) % 360 - 180

        # Adjust motor speed to compensate for error
        #correction = self.kp * heading_error

        # Calculate deviation from initial radial
        heading_error = radial - initial_radial

        # Compute correction based on heading error
        correction = self.kp * heading_error

        left_speed = base_speed - correction
        right_speed = base_speed + correction

        # Ensure speeds remain within a valid range (0.0 to 1.0)
        left_speed = max(0.0, min(1.0, left_speed))
        right_speed = max(0.0, min(1.0, right_speed))

        # Apply speeds to motors
        await self.set_motor_speed(left_speed, right_speed)

        #self.motor_left.set_speed(left_speed)
        #self.motor_right.set_speed(right_speed)

        print(f"Radial: {radial}° | Left Motor: {left_speed:.2f}, Right Motor: {right_speed:.2f}")

    def rotate_and_scan(self):
        """Rotates the robot step by step, scanning for open paths."""
        self.detected_paths = []  # Reset detected paths

        while self.angle < self.max_angle:
            distance = self.sensor.get_distance()
            print(f"Angle: {self.angle}° - Distance: {distance} cm")

            if distance > self.path_threshold:
                self.detected_paths.append(self.angle)
                print(f"Path detected at {self.angle}°!")

            self.angle += self.step_angle
            time.sleep(0.1)  # Simulate sensor delay

        self.angle = 0  # Reset rotation
        print("Scan complete. Paths found at angles:", self.detected_paths)

    def __repr__(self):
        return f"Robot(x={self._x}, y={self._y}, radial={self._radial}°)"