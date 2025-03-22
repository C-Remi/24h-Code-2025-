import asyncio
import random

import pygame

from post_requests import *
from state import StateManager
from motor import Motors

class Robot:

    def __init__(self):
        self.state = StateManager() # ws data collection
        self.driving = Motors() # ws motors management
        # POST API: stateless, no object

        pygame.init()
        pygame.joystick.init()

    async def start(self):
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print(f"Connected to: {joystick.get_name()}")

        while True:
            pygame.event.pump()  # Process events

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("\nExiting...")
                    pygame.quit()
                    break

            # Get joystick values
            left_stick_x = joystick.get_axis(0)  # Left stick (X-axis)
            right_stick_y = joystick.get_axis(3) # Right stick (Y-axis)
            lb_pressed = joystick.get_button(4)  # LB button index
            rb_pressed = joystick.get_button(5)  # RB button index

            if abs(left_stick_x) >= 0.15:
                await self.driving.set_speed_left(round(left_stick_x,2))
            elif lb_pressed:
                await self.driving.set_speed_left(1.0)

            if abs(right_stick_y) >= 0.15:
                await self.driving.set_speed_right(round(right_stick_y,2))
            elif rb_pressed:
                await self.driving.set_speed_right(1.0)



if __name__ == "__main__":
    async def main():
        r = Robot()
        await r.start()

    asyncio.run(main())
