import pygame
import time
import struct
import asyncio
from post_requests import *

period_ms = 500

import websockets

class WebSocketClient:
    def __init__(self, uri):
        """Initialize the WebSocket client with a server URI."""
        self.uri = uri
        self.websocket = None
        self.closed = True

    async def connect(self):
        """Establish a connection to the WebSocket server."""
        try:
            print(self.uri)
            self.websocket = await websockets.connect(self.uri)
            self.closed = False
            print(f"Connected to WebSocket server at {self.uri}")
        except Exception as e:
            print(f"Connection failed: {e}")

    async def send_message(self, message):
        """Send a message to the WebSocket server."""
        if self.websocket:
            await self.websocket.send(message)
            #print(f"Sent: {message}")

    async def receive_message(self):
        """Receive a message from the WebSocket server."""
        if self.websocket:
            try:
                message = await self.websocket.recv()
                # DEBUG
                #print(f"Received: {message}")
                return message
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed by server.")
                self.closed = True

    async def close(self):
        """Close the WebSocket connection."""
        if self.websocket:
            await self.websocket.close()
            print("WebSocket connection closed.")

    async def run(self):
        """Run the WebSocket client (send & receive messages)."""
        await self.connect()
        while True:
            message = await self.receive_message()
            if message is None:
                break  # Exit loop if connection is closed
    def is_closed(self):
        """Check if the WebSocket connection is closed."""
        return self.websocket is None or self.closed

class Robot:

    def __init__(
        self,
        host="192.168.84.6",
        ):
        """Initialize Robot with x, y coordinates and radial angle."""
        self._host = host
        self._uri_ws_motors = f"ws://{self._host}/motors.ws"
        self._ws_client_motors = WebSocketClient(self._uri_ws_motors)
        reset_position()
        

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


                pygame.event.pump()  # Process events
                        
                # Get joystick values
                left_stick_x = joystick.get_axis(0)  # Left stick (X-axis)
                right_stick_y = joystick.get_axis(3) # Right stick (Y-axis)
                #print(f"Left Stick: X={left_stick_x} | Right Stick: Y={right_stick_y}")

                lb_pressed = joystick.get_button(4)  # LB button index
                rb_pressed = joystick.get_button(5)  # RB button index
                
                a_button = joystick.get_button(0)  # Button A is index 0
                #rt = (joystick.get_axis(5) + 1) / 2  # Convert -1 to 1 → 0 to 1
                #lt = (joystick.get_axis(4) + 1) / 2  # Convert -1 to 1 → 0 to 1
                
                if a_button:
                    print("Emergency stop")
                    self.set_motor_speed(0,0)
                    set_led_color(255,155,0)
                    
                    
                # Print values between -1 and 1
                if abs(round(left_stick_x,2)) > 0.15:
                    left = round(left_stick_x,2)
                else:
                    left = 0

                if abs(round(right_stick_y,2)) > 0.15:
                    right = round(right_stick_y,2)
                else:
                    right = 0

                if lb_pressed:
                    left = 1
                if rb_pressed:
                    right = 1

                #print(f"lb_pressed: {lb_pressed}, rb_pressed: {rb_pressed} Left motor: X={left} | Right motor: Y={right}")
                if(left != 0.0 and right != 0.0):
                    print(f'Set motor speed to: {left * 0.5}{right * 0.5}')
                await self.set_motor_speed(left * 0.5, right * 0.5 )
                    

        except KeyboardInterrupt:
                print("\nExiting...")
                pygame.quit()

    async def set_motor_speed(self, vl, vr):
        vl = max(-1, min(vl, 1))
        vr = max(-1, min(vr, 1))
        motor_buffer = struct.pack('ff', vl, vr)

        await self._ws_client_motors.send_message(motor_buffer)
        #print(f"motor_buffer: {motor_buffer}")
        time.sleep(0.08)


    def __repr__(self):
        return f"Robot(x={self._x}, y={self._y}, radial={self._radial}°)"

#HOST = "192.168.84.6"
HOST="haumbot-c5cfb8.local"

async def main():
    robot = Robot(HOST)
    await robot.activate()

if __name__ == "__main__":
    asyncio.run(main())