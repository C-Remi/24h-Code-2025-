
from utils.wsclient import WebSocketClient
from api.infos import readInfos
from api.request import reset_position, set_led_color, turtle_move_forward, turtle_rotate
from state import StateManager
from motor import Motor
import asyncio
import struct

period_ms = 500

INFOS_POSITION = b"\x01"
INFOS_LED = b"\x02"
INFOS_MOTORS = b"\x04"
INFOS_WHEELS = b"\x08"
INFOS_SPEED = b"\x10"
INFOS_RANGEFINDER = b"\x20"

class Robot:

    def __init__(
        self,
        host="192.168.84.6",
        step_angle=10,
        max_angle=360,
        path_threshold=100,
        kp=0.1
        ):
        """Initialize Robot with x, y coordinates and radial angle."""
        self._host = host
        self._uri_ws_motors = f"ws://{self._host}/motors.ws"
        self._ws_client_motors = WebSocketClient(self._uri_ws_motors)

        self.state = StateManager()

        self.step_angle = step_angle
        self.max_angle = max_angle
        self.path_threshold = path_threshold
        self.detected_paths = []  # Stores angles with open paths
        self.kp = kp

        self.left_motor = Motor("left_motor")
        self.right_motor = Motor("right_motor")

        reset_position(self._host)
        set_led_color(self._host, "#ffffff")

    async def activate(self):
        test = True

        while True:
            # Connect to information WS
            if self._ws_client_motors.is_closed():
                await self._ws_client_motors.connect()

            if test:
                test= False
                turtle_move_forward(self._host, 10)
                #turtle_rotate(self._host, 90)
                #self.rotate_and_scan()

    async def set_motor_speed(self, vl, vr):
        vl = max(-1, min(vl, 1))
        vr = max(-1, min(vr, 1))
        motor_buffer = struct.pack('ff', vl, vr)

        self.left_motor.set_speed(vl)
        self.right_motor.set_speed(vr)
        await self._ws_client_motors.send_message(motor_buffer)
        #print(f"motor_buffer: {motor_buffer}")
        await asyncio.sleep(0.1)

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

    async def rotate_and_scan(self):
        """Rotates the robot step by step, scanning for open paths."""
        self.detected_paths = []  # Reset detected paths

        while self.status_info.get("angle", 0.0) < self.max_angle:
            distance = self.status_info.get("range", 0.0)
            print(f"Angle: {self.status_info.get('angle', 0.0)}° - Distance: {distance} cm")

            if distance > self.path_threshold:
                self.detected_paths.append(self.status_info.get("angle", 0.0))
                print(f"Path detected at {self.status_info.get('angle', 0.0)}°!")

            turtle_rotate(self._host, self.step_angle)
            await asyncio.sleep(0.1)  # Simulate sensor delay

        print("Scan complete. Paths found at angles:", self.detected_paths)
