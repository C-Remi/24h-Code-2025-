import asyncio
from odometry_interface import *
from post_requests import *
from state import StateManager
from motor import Motors

class Robot:

    def __init__(self):
        #self.state = StateManager() # ws data collection
        #self.driving = Motors() # ws motors management
        # POST API: stateless, no object
        pass

    async def start(self):
        # TODO: implement a real autonomous algorithm
        while True:
            #set_led_color(random.randrange(256), random.randrange(256), random.randrange(256))
            #await self.driving.set_speed_left(0.5)
            #await asyncio.sleep(0.1)
            #await self.driving.set_speed_left(-0.5)
            #await asyncio.sleep(0.1)
            pass


if __name__ == "__main__":

    global running

    # Start the drawing thread
    canvas_thread = threading.Thread(target=update_canvas, daemon=True)
    canvas_thread.start()

    # Start the robot update thread
    robot_thread = threading.Thread(target=update_robot, daemon=True)
    robot_thread.start()

    # Start the robot update thread
    points_thread = threading.Thread(target=update_points, daemon=True)
    points_thread.start()

    # Start the OpenCV window thread
    window_thread = threading.Thread(target=display_window)
    window_thread.start()

    r = Robot()
    asyncio.run(r.start())

    # Wait for the OpenCV window thread to finish
    window_thread.join()
    print("Program exited.")

