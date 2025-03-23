import asyncio
import odometry_interface
from post_requests import *
from state import StateManager
from motor import Motors

import cv2
import numpy as np
import threading
import time

class Robot:

    def __init__(self):
        global odometry_interface

        self.state = StateManager() # ws data collection
        self.driving = Motors() # ws motors management
        # POST API: stateless, no object

        odometry_interface.global_state = self.state


    async def start(self):
        # TODO: implement a real autonomous algorithm
        while True:
            #await self.driving.set_speed_left(0.5)
            #await asyncio.sleep(0.1)
            #await self.driving.set_speed_left(-0.5)
            #await asyncio.sleep(0.1)
            await asyncio.sleep(1)
            pass


if __name__ == "__main__":

    global running

    # Start the drawing thread
    canvas_thread = threading.Thread(target=odometry_interface.update_canvas, daemon=True)
    canvas_thread.start()

    # Start the robot update thread
    robot_thread = threading.Thread(target=odometry_interface.update_robot, daemon=True)
    robot_thread.start()

    # Start the robot update thread
    points_thread = threading.Thread(target=odometry_interface.update_points, daemon=True)
    points_thread.start()

    # Start the OpenCV window thread
    window_thread = threading.Thread(target=odometry_interface.display_window)
    window_thread.start()

    async def main():
        r = Robot()
        await r.start()

    asyncio.run(main())

    # Wait for the OpenCV window thread to finish
    window_thread.join()
    print("Program exited.")

