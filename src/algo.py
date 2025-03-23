import math

def solve_maze(maze):
    rows, cols = len(maze), len(maze[0])

    # Find start and goal positions
    start, goal = None, None
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == "S":
                start = (r, c)
            elif maze[r][c] == "G":
                goal = (r, c)

    # Directions: Right, Left, Down, Up
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # DFS search stack
    stack = [(start[0], start[1], [])]  # (row, col, path taken)

    while stack:
        r, c, path = stack.pop()

        # If we reached the goal, return the path
        if (r, c) == goal:
            return path + [(r, c)]

        # Mark as visited
        if maze[r][c] not in ("S", "G"):  
            maze[r][c] = "V"

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] in (".",",", "G"):
                stack.append((nr, nc, path + [(r, c)]))

    return None  # No path found

def display_maze(maze, path):
    # Copy the maze to modify
    maze_display = [row[:] for row in maze]

    # Mark the path
    for r, c in path:
        if maze_display[r][c] not in ("S", "G"):
            maze_display[r][c] = "*"

    # Print the maze
    for row in maze_display:
        print("".join(row))

def filter_array(arr):
    return [x for i, x in enumerate(arr) if (i // 2) % 2 == 0]

def compute_commands(positions):
    if len(positions) < 2:
        return []

    commands = []
    current_direction = 0  # Initial direction (degrees)

    for i in range(len(positions) - 1):
        x1, y1 = positions[i]
        x2, y2 = positions[i + 1]

        # Compute distance
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        # Compute absolute angle
        absolute_angle = math.degrees(math.atan2(y2 - y1, x2 - x1))

        # Compute relative turn angle
        turn_angle = absolute_angle - current_direction

        # Normalize turn angle (-180, 180)
        turn_angle = (turn_angle + 180) % 360 - 180

        # Store command
        commands.append(("TURN",round(turn_angle)))
        commands.append(("MOVE",190 * distance))

        # Update direction
        current_direction = absolute_angle

    return commands