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
global_state = None

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
            draw_rotated_rectangle(frame, ((WIDTH//2) + robot_x, (HEIGHT//2) + robot_y), (40, 20), robot_a)

            if len(red_points) > 1024:
                red_points = red_points[-1024:]

            # Draw all red points
            i=0
            for pt in red_points:
                i+=1
                npt = ((WIDTH//2) + pt[0], (HEIGHT//2) + pt[1])
                cv2.circle(frame, npt, 3, (0, 0, int(255*(i/len(red_points)))), -1)  # Red dot

        time.sleep(0.01)

def update_robot():
    global robot_x, robot_y, robot_a, running
    global global_state

    time.sleep(3)

    while running:
        with lock:
            # Move the robot
            if global_state is not None:
                if len(global_state.records['position']) > 2:
                    robot_x = (global_state.records['position'][-1][1][0] - global_state.records['position'][0][1][0]) * 1000
                    robot_y = (global_state.records['position'][-1][1][1] - global_state.records['position'][0][1][1]) * 1000
                    robot_a = (global_state.records['position'][-1][1][2]/3.1415926)*180
                    #print('ROBOT : ', robot_x, robot_y, robot_a)

                if 'rangefinder' in global_state.records:
                    last_dist = global_state.records['rangefinder'][-1][1][0]
                    px = robot_x + last_dist * np.cos(global_state.records['position'][-1][1][2])
                    py = robot_y + last_dist * np.sin(global_state.records['position'][-1][1][2])

                    red_points.append((int(px), int(py)))
                    #print('POINT : ', px, py)


        time.sleep(0.01)


def update_points():
    global red_points

        # Main thread: Add red points dynamically
    while running:
        if np.random.rand() < 0.1:
            with lock:
                #red_points.append((np.random.randint(0, WIDTH), np.random.randint(0, HEIGHT)))
                pass

        time.sleep(0.05)


def display_window():
    global frame, running

    while running:
        with lock:
            display_frame = frame.copy()

        # Show the updated frame
        cv2.imshow("Window bleu canette de l'amour", display_frame)

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