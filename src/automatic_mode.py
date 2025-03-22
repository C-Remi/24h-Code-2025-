import asyncio
import random

from post_requests import *
from state import StateManager
from motor import Motors

class Robot:

    def __init__(self):
        self.state = StateManager() # ws data collection
        self.driving = Motors() # ws motors management
        # POST API: stateless, no object

    async def start(self):
        # TODO: implement a real autonomous algorithm
        while True:
            set_led_color(random.randrange(256), random.randrange(256), random.randrange(256))
            await self.driving.set_speed_left(0.5)
            await asyncio.sleep(0.1)
            await self.driving.set_speed_left(-0.5)
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    r = Robot()
    asyncio.run(r.start())
