import cv2
import numpy as np
import threading
import time

# Constants
HEIGHT, WIDTH = 800, 800

# Shared global resources
frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
robot_a, robot_x, robot_y = 0, 0, 0
red_points = []
lock = threading.Lock()
running = True  # Control variable to stop threads

def draw_rotated_rectangle(frame, position, size, angle):
    """
    Draw a rotated rectangle on a frame/image.
    """
    center_x, center_y = position
    width, height = size
    rotated_rect = ((center_x, center_y), (width, height), angle)
    box_points = cv2.boxPoints(rotated_rect)
    box_points = box_points.astype(int)
    cv2.drawContours(frame, [box_points], contourIdx=0, color=(0, 255, 0), thickness=-1)
    return frame

def update_canvas():
    global frame, robot_x, robot_y, robot_a, red_points, running
    while running:
        with lock:
            # Create blank canvas
            frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

            # Draw the robot
            draw_rotated_rectangle(frame, (robot_x, robot_y), (40, 20), robot_a)

            # Draw all red points
            for pt in red_points:
                cv2.circle(frame, pt, 3, (0, 0, 255), -1)  # Red dot

        time.sleep(0.01)

def update_robot():
    global robot_x, robot_y, robot_a, running
    while running:
        with lock:
            # Move the robot
            robot_x += 5
            robot_y += 5
            robot_x %= 500
            robot_y %= 500
            robot_a += 1

        time.sleep(0.01)


def update_points():
    global red_points

        # Main thread: Add red points dynamically
    while running:
        if np.random.rand() < 0.1:
            with lock:
                red_points.append((np.random.randint(0, WIDTH), np.random.randint(0, HEIGHT)))

        time.sleep(0.05)


def display_window():
    global frame, running

    while running:
        with lock:
            display_frame = frame.copy()

        # Show the updated frame
        cv2.imshow("Robot Canvas (Double Threads)", display_frame)

        # Check for ESC key to stop
        if cv2.waitKey(30) == 27:  # ESC key
            running = False
            break

    cv2.destroyAllWindows()

def main():
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

    # Wait for the OpenCV window thread to finish
    window_thread.join()
    print("Program exited.")

if __name__ == "__main__":
    main()