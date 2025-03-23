import asyncio
import random
from algo import *

from post_requests import *
from state import StateManager
from motor import Motors

class Robot:

    def __init__(self):
        #self.state = StateManager() # ws data collection
        self.driving = Motors() # ws motors management
        # POST API: stateless, no object
        # Example Maze (2D list)
        self.maze = [
            ['.', ',', '.', ',', '.', ',', '.'],
            [',', 'G', ',', '#', '#', '#', '#'],
            ['.', ',', '.', '#', '.', ',', '.'],
            ['#', '#', ',', '#', ',', '#', ','],
            ['.', ',', '.', ',', '.', '#', '.'],
            [',', '#', '#', '#', '#', '#', ','],
            ['.', '#', 'S', ',', '.', ',', '.']
        ]
        
        self.path = solve_maze(self.maze)
        self.commands = compute_commands(self.path)
        self.commands = filter_array(self.commands)
        
        
        
    async def start(self):
        print(self.commands)
        set_led_color(255,0,0)

        for (cmd, val) in self.commands:

            if(cmd == "TURN"):
                if(val != 0):
                    print(f"{cmd} : {val}")
                    if val == 90:
                        val = 80
                    if val == -90:
                        val = 270
                    turtle_rotate(val)
            if(cmd == "MOVE"):
                if(val != 0):
                    print(f"{cmd} : {val}")
                    turtle_move_forward(val)

            await asyncio.sleep(5) 
        set_led_color(0,256,0)
            
                        

if __name__ == "__main__":
    async def main():
        r = Robot()
        await r.start()

    asyncio.run(main())
