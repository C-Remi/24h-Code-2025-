import asyncio
from robot import Robot
from odometry_interface import *

HOST = "192.168.84.6"
#HOST="haumbot-c5cfb8.local"

async def main():

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

    robot = Robot(HOST)

    await robot.activate()

    # Wait for the OpenCV window thread to finish
    window_thread.join()
    print("Program exited.")

if __name__ == "__main__":
    asyncio.run(main())
