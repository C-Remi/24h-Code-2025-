import tkinter as tk

# Constants
GRID_SIZE = 50  # Size of each grid square
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
ROBOT_SIZE = 40  # Robot's square size
POINT_RADIUS = 5  # Size of target points

# Initial robot position (centered)
robot_x, robot_y = CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2

# Store clicked points
points = []

def draw_grid():
    """Draws the background grid."""
    for x in range(0, CANVAS_WIDTH, GRID_SIZE):
        canvas.create_line(x, 0, x, CANVAS_HEIGHT, fill="lightgray")
    for y in range(0, CANVAS_HEIGHT, GRID_SIZE):
        canvas.create_line(0, y, CANVAS_WIDTH, y, fill="lightgray")

def draw_robot():
    """Draws the robot as a square."""
    x0 = robot_x - ROBOT_SIZE // 2
    y0 = robot_y - ROBOT_SIZE // 2
    x1 = robot_x + ROBOT_SIZE // 2
    y1 = robot_y + ROBOT_SIZE // 2
    canvas.create_rectangle(x0, y0, x1, y1, fill="blue", outline="black", width=2)

def draw_points():
    """Draws all added points."""
    for px, py in points:
        canvas.create_oval(px - POINT_RADIUS, py - POINT_RADIUS,
                           px + POINT_RADIUS, py + POINT_RADIUS,
                           fill="red")

def refresh():
    """Redraws the entire canvas."""
    canvas.delete("all")
    draw_grid()
    draw_robot()
    draw_points()

def add_point(event):
    """Adds a point where the user clicks."""
    grid_x = (event.x // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
    grid_y = (event.y // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
    points.append((grid_x, grid_y))
    refresh()

def launch_graphical_interface():

    # Tkinter setup
    root = tk.Tk()
    root.title("Robot Grid Simulation")
    canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
    canvas.pack()

    canvas.bind("<Button-1>", add_point)

    refresh()
    root.mainloop()
