import pygame
from utils.wsclient import WebSocketClient
from api.infos import readInfos, INFOS_POSITION, INFOS_LED, INFOS_MOTORS, INFOS_RANGEFINDER, INFOS_SPEED, INFOS_WHEELS
from api.request import reset_position, set_led_color, turtle_move_forward, turtle_rotate
from utils.tof import TimeOfFlightSensor
from robot_gps import RobotGps
from motor import Motor
import time
import struct
import asyncio

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
        self._ws_client_motors = WebSocketClient(self._uri_ws_motors)

        self._uri_ws_info = f"ws://{self._host}/infos.ws"
        self.ws_info_pos = WebSocketClient(self._uri_ws_info)
        self.ws_info_led = WebSocketClient(self._uri_ws_info)
        self.ws_info_motor = WebSocketClient(self._uri_ws_info)
        self.ws_info_wheels = WebSocketClient(self._uri_ws_info)
        self.ws_info_speed = WebSocketClient(self._uri_ws_info)
        self.ws_info_range = WebSocketClient(self._uri_ws_info)
        self.status_info = dict()


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

    async def init_infos_ws(self):
        if self.ws_info_pos.is_closed():
            await self.ws_info_pos.connect()
            await self.ws_info_pos.send_message(INFOS_POSITION)

        if self.ws_info_led.is_closed():
            await self.ws_info_led.connect()
            await self.ws_info_led.send_message(INFOS_LED)

        if self.ws_info_motor.is_closed():
            await self.ws_info_motor.connect()
            await self.ws_info_motor.send_message(INFOS_MOTORS)

        if self.ws_info_wheels.is_closed():
            await self.ws_info_wheels.connect()
            await self.ws_info_wheels.send_message(INFOS_WHEELS)

        if self.ws_info_speed.is_closed():
            await self.ws_info_speed.connect()
            await self.ws_info_speed.send_message(INFOS_SPEED)

        if self.ws_info_range.is_closed():
            await self.ws_info_range.connect()
            await self.ws_info_range.send_message(INFOS_RANGEFINDER)

    async def update_status(self):
        for ws in (
            self.ws_info_pos,
            self.ws_info_led,
            self.ws_info_motor,
            self.ws_info_wheels,
            self.ws_info_speed,
            self.ws_info_range,
        ):
            msg = await ws.receive_message()
            try:
                data = readInfos(msg)
                self.status_info.update(data)
            except Exception as e:
                print("Error while decoding", msg)

    async def activate(self):
        # Initialize Pygame
        pygame.init()

        # Initialize the joystick
        pygame.joystick.init()

        # Check if a joystick is connected
        if pygame.joystick.get_count() == 0:
            print("No joystick detected!")
            pygame.quit()
            exit()

        # Get the first joystick
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        print(f"Connected to: {joystick.get_name()}")

        try:

            while True:
                # Connect to information WS
                if self._ws_client_motors.is_closed():
                    await self._ws_client_motors.connect()

                #await self.init_infos_ws()
                #await self.update_status()

                pygame.event.pump()  # Process events
                        
                # Get joystick values
                left_stick_x = joystick.get_axis(0)  # Left stick (X-axis)
                right_stick_y = joystick.get_axis(3) # Right stick (Y-axis)
                #print(f"Left Stick: X={left_stick_x} | Right Stick: Y={right_stick_y}")

                # Print values between -1 and 1
                if round(left_stick_x,2) > 0.15 or round(left_stick_x,2) < -0.15:
                    left = round(left_stick_x,2)
                else:
                    left = 0

                if round(right_stick_y,2) > 0.15 or round(right_stick_y,2) < -0.15:
                    right = round(right_stick_y,2)
                else:
                    right = 0

                print(f"Left motor: X={left} | Right motor: Y={right}")
                await self.set_motor_speed(left, right )
                    

        except KeyboardInterrupt:
                print("\nExiting...")
                pygame.quit()

    async def set_motor_speed(self, vl, vr):
        vl = max(-1, min(vl, 1))
        vr = max(-1, min(vr, 1))
        motor_buffer = struct.pack('ff', vl, vr)

        self.left_motor.set_speed(vl)
        self.right_motor.set_speed(vr)
        await self._ws_client_motors.send_message(motor_buffer)
        #print(f"motor_buffer: {motor_buffer}")
        time.sleep(0.08)


    def __repr__(self):
        return f"Robot(x={self._x}, y={self._y}, radial={self._radial}°)"

#HOST = "192.168.84.6"
HOST="haumbot-c5cfb8.local"

async def main():
    robot = Robot(0,0,0, HOST)
    await robot.activate()

if __name__ == "__main__":
    asyncio.run(main())