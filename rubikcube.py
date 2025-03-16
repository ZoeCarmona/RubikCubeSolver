import shutil
import copy
import time
from collections import deque

# Print Rubik's Cube in the cross layout format
def print_rubik_cube(cube):
    terminal_width = shutil.get_terminal_size().columns
    print("" + " ".join(cube["Up"][0]).center(terminal_width))
    print("" + " ".join(cube["Up"][1]).center(terminal_width))
    print("" + " ".join(cube["Up"][2]).center(terminal_width))
    print()
    
    for i in range(3):
        print("    "+(" ".join(cube["left"][i]) + " | " + " ".join(cube["front"][i]) + 
            " | " + " ".join(cube["right"][i]) + " | " + " ".join(cube["back"][i])).center(terminal_width))
    
    print()
    print("" + " ".join(cube["Down"][0]).center(terminal_width))
    print("" + " ".join(cube["Down"][1]).center(terminal_width))
    print("" + " ".join(cube["Down"][2]).center(terminal_width))

# Function to get a valid face from the user
def get_face_input(face_name, center_color):
    face = []
    print(f"\nEnter the values for the {face_name} face (center color is {center_color}):")
    
    for i in range(3):
        while True:
            row = input(f"Enter row {i + 1} (3 values, separated by spaces): ").strip().split()
            
            # Check if the row has 3 values and if the center element is correct
            if len(row) != 3 or any(c not in "WYGRBO" for c in row):
                print(f"\nInvalid input! Each row should have 3 characters from 'W', 'Y', 'G', 'B', 'O'. Try again.")
            elif i == 1 and row[1] != center_color:  # Second row, second element must match the center color
                print(f"\nInvalid input! The second element in row 2 must be '{center_color}' for the {face_name} face. Try again.")
            else:
                face.append(row)
                break
    
    return face

# Set up the initial solved cube (goal state)
goal_cube = {
    "Up": [["W"] * 3 for _ in range(3)],  # Renamed from "top" to "Up"
    "front": [["G"] * 3 for _ in range(3)],  # Green is the front
    "left": [["O"] * 3 for _ in range(3)],   # Orange is the left
    "right": [["R"] * 3 for _ in range(3)],  # Red is the right
    "back": [["B"] * 3 for _ in range(3)],   # Blue is the back
    "Down": [["Y"] * 3 for _ in range(3)],   # Renamed from "bottom" to "Down"
}

# Set up the Rubik's Cube for the user to input
rubik_cube = copy.deepcopy(goal_cube)  # Start with the solved state, but will be overwritten by user input

# Centering the header text manually
def print_centered_text(text):
    terminal_width = shutil.get_terminal_size().columns
    for line in text.split("\n"):
        print(line.center(terminal_width))

# Print the initial setup and configuration instructions
print_centered_text("Rubik's Cube Solver")
print_centered_text("Please, consider that this is how we’re going to have as the final faces:")
print_rubik_cube(goal_cube)
print_centered_text("Where the configuration is:\n➥ White is the Up face                     ➥ Yellow is the Down face                   ➥ Green is the front face\n➥ Orange is the left face           ➥ Red is the right face          ➥ Blue is the back face")

# Ask the user to input the faces
rubik_cube["Up"] = get_face_input("Up", "W")
rubik_cube["front"] = get_face_input("front", "G")
rubik_cube["left"] = get_face_input("left", "O")
rubik_cube["right"] = get_face_input("right", "R")
rubik_cube["back"] = get_face_input("back", "B")
rubik_cube["Down"] = get_face_input("Down", "Y")

# Print the final Rubik's Cube state after user input
print_centered_text("Your Rubik's Cube IS:")
print_rubik_cube(rubik_cube)

# Define move functions for cube rotations
def rotate_face_clockwise(face):
    # Rotate a face 90 degrees clockwise
    return [list(row) for row in zip(*face[::-1])]

def rotate_face_counterclockwise(face):
    # Rotate a face 90 degrees counterclockwise
    return [list(row) for row in zip(*face)][::-1]

def move_F(cube):
    cube["front"] = rotate_face_clockwise(cube["front"])
    top_row = cube["Up"][2].copy()
    left_col = [cube["left"][i][2] for i in range(3)]
    bottom_row = cube["Down"][0].copy()
    right_col = [cube["right"][i][0] for i in range(3)]
    
    for i in range(3):
        cube["Up"][2][i] = left_col[2 - i]
        cube["right"][i][0] = top_row[i]
        cube["Down"][0][i] = right_col[2 - i]
        cube["left"][i][2] = bottom_row[i]

def move_F_prime(cube):
    cube["front"] = rotate_face_counterclockwise(cube["front"])
    top_row = cube["Up"][2].copy()
    left_col = [cube["left"][i][2] for i in range(3)]
    bottom_row = cube["Down"][0].copy()
    right_col = [cube["right"][i][0] for i in range(3)]
    
    for i in range(3):
        cube["Up"][2][i] = right_col[i]
        cube["left"][i][2] = top_row[2 - i]
        cube["Down"][0][i] = left_col[i]
        cube["right"][i][0] = bottom_row[2 - i]

def move_R(cube):
    # Rotate the right face clockwise
    cube["right"] = rotate_face_clockwise(cube["right"])
    
    # Update adjacent faces
    top_col = [cube["Up"][i][2] for i in range(3)]
    front_col = [cube["front"][i][2] for i in range(3)]
    bottom_col = [cube["Down"][i][2] for i in range(3)]
    back_col = [cube["back"][i][0] for i in range(3)]
    
    # Move the edge pieces from Up, front, Down, and back
    for i in range(3):
        cube["Up"][i][2] = front_col[i]
        cube["front"][i][2] = bottom_col[i]
        cube["Down"][i][2] = back_col[2 - i]
        cube["back"][i][0] = top_col[2 - i]

def move_R_prime(cube):
    # Rotate the right face counterclockwise
    cube["right"] = rotate_face_counterclockwise(cube["right"])
    
    # Update adjacent faces
    top_col = [cube["Up"][i][2] for i in range(3)]
    front_col = [cube["front"][i][2] for i in range(3)]
    bottom_col = [cube["Down"][i][2] for i in range(3)]
    back_col = [cube["back"][i][0] for i in range(3)]
    
    # Move the edge pieces from Up, front, Down, and back
    for i in range(3):
        cube["Up"][i][2] = back_col[2 - i]
        cube["front"][i][2] = top_col[i]
        cube["Down"][i][2] = front_col[i]
        cube["back"][i][0] = bottom_col[2 - i]

def move_L(cube):
    # Rotate the left face clockwise
    cube["left"] = rotate_face_clockwise(cube["left"])
    
    # Update adjacent faces
    top_col = [cube["Up"][i][0] for i in range(3)]
    front_col = [cube["front"][i][0] for i in range(3)]
    bottom_col = [cube["Down"][i][0] for i in range(3)]
    back_col = [cube["back"][i][2] for i in range(3)]
    
    # Move the edge pieces from Up, front, Down, and back
    for i in range(3):
        cube["Up"][i][0] = back_col[2 - i]
        cube["front"][i][0] = top_col[i]
        cube["Down"][i][0] = front_col[i]
        cube["back"][i][2] = bottom_col[2 - i]

def move_L_prime(cube):
    # Rotate the left face counterclockwise
    cube["left"] = rotate_face_counterclockwise(cube["left"])
    
    # Update adjacent faces
    top_col = [cube["Up"][i][0] for i in range(3)]
    front_col = [cube["front"][i][0] for i in range(3)]
    bottom_col = [cube["Down"][i][0] for i in range(3)]
    back_col = [cube["back"][i][2] for i in range(3)]
    
    # Move the edge pieces from Up, front, Down, and back
    for i in range(3):
        cube["Up"][i][0] = front_col[i]
        cube["front"][i][0] = bottom_col[i]
        cube["Down"][i][0] = back_col[2 - i]
        cube["back"][i][2] = top_col[2 - i]

def move_B(cube):
    # Rotate the back face clockwise
    cube["back"] = rotate_face_clockwise(cube["back"])
    
    # Save the affected rows/columns
    top_row = cube["Up"][0].copy()  # Copy the top row of the Up face
    right_col = [cube["right"][i][2] for i in range(3)]  # Copy the right column of the Right face
    bottom_row = cube["Down"][2].copy()  # Copy the bottom row of the Down face
    left_col = [cube["left"][i][0] for i in range(3)]  # Copy the left column of the Left face
    
    # Update the Up face
    for i in range(3):
        cube["Up"][0][i] = right_col[i]  # Right column becomes the top row
    
    # Update the Left face
    for i in range(3):
        cube["left"][i][0] = top_row[2 - i]  # Top row becomes the left column (reversed)
    
    # Update the Down face
    for i in range(3):
        cube["Down"][2][i] = left_col[i]  # Left column becomes the bottom row
    
    # Update the Right face
    for i in range(3):
        cube["right"][i][2] = bottom_row[2 - i]  # Bottom row becomes the right column (reversed)

def move_B_prime(cube):
    # Rotate the back face counterclockwise
    cube["back"] = rotate_face_counterclockwise(cube["back"])
    
    # Save the affected rows/columns
    top_row = cube["Up"][0].copy()  # Copy the top row of the Up face
    right_col = [cube["right"][i][2] for i in range(3)]  # Copy the right column of the Right face
    bottom_row = cube["Down"][2].copy()  # Copy the bottom row of the Down face
    left_col = [cube["left"][i][0] for i in range(3)]  # Copy the left column of the Left face
    
    # Update the Up face
    for i in range(3):
        cube["Up"][0][i] = left_col[2 - i]  # Left column becomes the top row (reversed)
    
    # Update the Right face
    for i in range(3):
        cube["right"][i][2] = top_row[i]  # Top row becomes the right column
    
    # Update the Down face
    for i in range(3):
        cube["Down"][2][i] = right_col[2 - i]  # Right column becomes the bottom row (reversed)
    
    # Update the Left face
    for i in range(3):
        cube["left"][i][0] = bottom_row[i]  # Bottom row becomes the left column

def move_U(cube):
    # Rotate the Up face clockwise
    cube["Up"] = rotate_face_clockwise(cube["Up"])
    
    # Update adjacent faces
    front_row = cube["front"][0]
    right_row = cube["right"][0]
    back_row = cube["back"][0]
    left_row = cube["left"][0]
    
    # Move the edge pieces from front, right, back, and left
    cube["front"][0] = right_row
    cube["right"][0] = back_row
    cube["back"][0] = left_row
    cube["left"][0] = front_row

def move_U_prime(cube):
    # Rotate the Up face counterclockwise
    cube["Up"] = rotate_face_counterclockwise(cube["Up"])
    
    # Update adjacent faces
    front_row = cube["front"][0]
    right_row = cube["right"][0]
    back_row = cube["back"][0]
    left_row = cube["left"][0]
    
    # Move the edge pieces from front, right, back, and left
    cube["front"][0] = left_row
    cube["right"][0] = front_row
    cube["back"][0] = right_row
    cube["left"][0] = back_row

def move_D(cube):
    # Rotate the Down face clockwise
    cube["Down"] = rotate_face_clockwise(cube["Down"])
    
    # Update adjacent faces
    front_row = cube["front"][2]
    right_row = cube["right"][2]
    back_row = cube["back"][2]
    left_row = cube["left"][2]
    
    # Move the edge pieces from front, right, back, and left
    cube["front"][2] = left_row
    cube["right"][2] = front_row
    cube["back"][2] = right_row
    cube["left"][2] = back_row

def move_D_prime(cube):
    # Rotate the Down face counterclockwise
    cube["Down"] = rotate_face_counterclockwise(cube["Down"])
    
    # Update adjacent faces
    front_row = cube["front"][2]
    right_row = cube["right"][2]
    back_row = cube["back"][2]
    left_row = cube["left"][2]
    
    # Move the edge pieces from front, right, back, and left
    cube["front"][2] = right_row
    cube["right"][2] = back_row
    cube["back"][2] = left_row
    cube["left"][2] = front_row

# Function to return possible moves (cube rotations)
def possible_moves():
    return ["F", "F'", "R", "R'", "L", "L'", "B", "B'", "U", "U'", "D", "D'"]

# Manhattan distance heuristic: calculate the Manhattan distance for each cubie
def manhattan_distance(cube, goal_cube):
    distance = 0
    for face in cube:
        for row in range(3):
            for col in range(3):
                if cube[face][row][col] != goal_cube[face][row][col]:
                    # Calculate the distance based on the position of the mismatched tile
                    # For simplicity, we'll use a basic count, but you can implement a more accurate heuristic
                    distance += 1
    return distance

# Function to compare two cube states
def cubes_equal(cube1, cube2):
    for face in cube1:
        for row in range(3):
            for col in range(3):
                if cube1[face][row][col] != cube2[face][row][col]:
                    return False
    return True

# Convert cube state to a hashable tuple
def cube_to_tuple(cube):
    return tuple(tuple(row) for face in cube.values() for row in face)

# IDA* Search with Iterative DFS and Progress Bar
def ida_star(cube, goal_cube, heuristic, max_depth=20):
    start_time = time.time()
    def dfs(cube, depth, g, limit, path, visited):
        if depth > max_depth:
            return float('inf')  # Stop if depth exceeds max_depth
        
        if cube_to_tuple(cube) in visited:
            return None  # Prune duplicate states
        
        visited.add(cube_to_tuple(cube))

        if cubes_equal(cube, goal_cube):
            return path

        f = g + heuristic(cube)
        if f > limit:
            return f

        min_next_limit = float('inf')
        for move in possible_moves():
            new_cube = make_move(copy.deepcopy(cube), move)
            path.append(move)
            result = dfs(new_cube, depth + 1, g + 1, limit, path, visited)
            if isinstance(result, list):
                return result
            if isinstance(result, int):
                min_next_limit = min(min_next_limit, result)
            path.pop()

        return min_next_limit

    limit = heuristic(cube)
    print(f"\nSolving, please wait ...")
    while True:
        visited = set()
        path = []
        result = dfs(cube, 0, 0, limit, path, visited)
        elapsed_time = time.time() - start_time
        if isinstance(result, list):
            print(f"\nResult found in {int(elapsed_time)} seconds!")
            return result
        if result == float('inf'):
            print("No solution found within depth limit.")
            return None
        limit = result

# Utility function for cube moves and configurations
def make_move(cube, move):
    new_cube = copy.deepcopy(cube)
    if move == "F":
        move_F(new_cube)
    elif move == "F'":
        move_F_prime(new_cube)
    elif move == "R":
        move_R(new_cube)
    elif move == "R'":
        move_R_prime(new_cube)
    elif move == "L":
        move_L(new_cube)
    elif move == "L'":
        move_L_prime(new_cube)
    elif move == "B":
        move_B(new_cube)
    elif move == "B'":
        move_B_prime(new_cube)
    elif move == "U":
        move_U(new_cube)
    elif move == "U'":
        move_U_prime(new_cube)
    elif move == "D":
        move_D(new_cube)
    elif move == "D'":
        move_D_prime(new_cube)
    return new_cube

# Helper functions for Phase 1 heuristic
def get_edges(cube):
    edges = []
    edges.append((cube["Up"][1][0], cube["left"][0][1]))  # Up-Left edge
    edges.append((cube["Up"][0][1], cube["back"][0][1]))  # Up-Back edge
    edges.append((cube["Up"][1][2], cube["right"][0][1])) # Up-Right edge
    edges.append((cube["Up"][2][1], cube["front"][0][1])) # Up-Front edge
    
    edges.append((cube["Down"][1][0], cube["left"][2][1])) # Down-Left edge
    edges.append((cube["Down"][0][1], cube["back"][2][1])) # Down-Back edge
    edges.append((cube["Down"][1][2], cube["right"][2][1])) # Down-Right edge
    edges.append((cube["Down"][2][1], cube["front"][2][1])) # Down-Front edge
    
    edges.append((cube["front"][1][0], cube["left"][1][2])) # Front-Left edge
    edges.append((cube["front"][1][2], cube["right"][1][0])) # Front-Right edge
    edges.append((cube["back"][1][0], cube["right"][1][2]))  # Back-Right edge
    edges.append((cube["back"][1][2], cube["left"][1][0]))  # Back-Left edge
    
    return edges

def is_edge_oriented_correctly(edge):
    solved_edges = [
        ("W", "O"), ("W", "B"), ("W", "R"), ("W", "G"),  # Up edges
        ("Y", "O"), ("Y", "B"), ("Y", "R"), ("Y", "G"),  # Down edges
        ("G", "O"), ("G", "R"), ("B", "R"), ("B", "O")   # Middle edges
    ]
    return edge in solved_edges or edge[::-1] in solved_edges

def get_corners(cube):
    corners = []
    corners.append((cube["Up"][0][0], cube["left"][0][0], cube["back"][0][2]))  # Up-Left-Back corner
    corners.append((cube["Up"][0][2], cube["right"][0][2], cube["back"][0][0])) # Up-Right-Back corner
    corners.append((cube["Up"][2][0], cube["left"][0][2], cube["front"][0][0])) # Up-Left-Front corner
    corners.append((cube["Up"][2][2], cube["right"][0][0], cube["front"][0][2])) # Up-Right-Front corner
    
    corners.append((cube["Down"][0][0], cube["left"][2][2], cube["back"][2][2])) # Down-Left-Back corner
    corners.append((cube["Down"][0][2], cube["right"][2][2], cube["back"][2][0])) # Down-Right-Back corner
    corners.append((cube["Down"][2][0], cube["left"][2][0], cube["front"][2][0])) # Down-Left-Front corner
    corners.append((cube["Down"][2][2], cube["right"][2][0], cube["front"][2][2])) # Down-Right-Front corner
    
    return corners

def is_corner_in_correct_slice(corner):
    solved_corners = [
        ("W", "O", "B"), ("W", "B", "R"), ("W", "R", "G"), ("W", "G", "O"),  # Up corners
        ("Y", "O", "G"), ("Y", "G", "R"), ("Y", "R", "B"), ("Y", "B", "O")   # Down corners
    ]
    # Check all rotations of the corner
    return (corner in solved_corners or
            (corner[1], corner[2], corner[0]) in solved_corners or
            (corner[2], corner[0], corner[1]) in solved_corners)

# Helper function to check if an edge is solved
def is_edge_solved(edge):
    solved_edges = [
        ("W", "O"), ("W", "B"), ("W", "R"), ("W", "G"),  # Up edges
        ("Y", "O"), ("Y", "B"), ("Y", "R"), ("Y", "G"),  # Down edges
        ("G", "O"), ("G", "R"), ("B", "R"), ("B", "O")   # Middle edges
    ]
    return edge in solved_edges or edge[::-1] in solved_edges

# Helper function to check if a corner is solved
def is_corner_solved(corner):
    solved_corners = [
        # Up corners (all rotations)
        ("W", "O", "B"), ("W", "B", "O"), ("O", "W", "B"), ("O", "B", "W"), ("B", "W", "O"), ("B", "O", "W"),
        ("W", "B", "R"), ("W", "R", "B"), ("B", "W", "R"), ("B", "R", "W"), ("R", "W", "B"), ("R", "B", "W"),
        ("W", "R", "G"), ("W", "G", "R"), ("R", "W", "G"), ("R", "G", "W"), ("G", "W", "R"), ("G", "R", "W"),
        ("W", "G", "O"), ("W", "O", "G"), ("G", "W", "O"), ("G", "O", "W"), ("O", "W", "G"), ("O", "G", "W"),
        
        # Down corners (all rotations)
        ("Y", "O", "G"), ("Y", "G", "O"), ("O", "Y", "G"), ("O", "G", "Y"), ("G", "Y", "O"), ("G", "O", "Y"),
        ("Y", "G", "R"), ("Y", "R", "G"), ("G", "Y", "R"), ("G", "R", "Y"), ("R", "Y", "G"), ("R", "G", "Y"),
        ("Y", "R", "B"), ("Y", "B", "R"), ("R", "Y", "B"), ("R", "B", "Y"), ("B", "Y", "R"), ("B", "R", "Y"),
        ("Y", "B", "O"), ("Y", "O", "B"), ("B", "Y", "O"), ("B", "O", "Y"), ("O", "Y", "B"), ("O", "B", "Y")
    ]
    return corner in solved_corners

def phase1_heuristic(cube):
    edge_orientation_cost = 0
    print("Checking edges:")
    for edge in get_edges(cube):
        print("Edge:", edge, "Solved:", is_edge_oriented_correctly(edge))
        if not is_edge_oriented_correctly(edge):
            edge_orientation_cost += 1
    
    corner_grouping_cost = 0
    print("Checking corners:")
    for corner in get_corners(cube):
        print("Corner:", corner, "Solved:", is_corner_in_correct_slice(corner))
        if not is_corner_in_correct_slice(corner):
            corner_grouping_cost += 1
    
    print("Phase 1 Heuristic Value:", edge_orientation_cost + corner_grouping_cost)
    return edge_orientation_cost + corner_grouping_cost

def phase2_heuristic(cube):
    unsolved_edges = 0
    unsolved_corners = 0
    
    # Check edges
    print("Checking edges:")
    for edge in get_edges(cube):
        print("Edge:", edge, "Solved:", is_edge_solved(edge))
        if not is_edge_solved(edge):
            unsolved_edges += 1
    
    # Check corners
    print("Checking corners:")
    for corner in get_corners(cube):
        print("Corner:", corner, "Solved:", is_corner_solved(corner))
        if not is_corner_solved(corner):
            unsolved_corners += 1
    
    print("Phase 2 Heuristic Value:", unsolved_edges + unsolved_corners)
    return unsolved_edges + unsolved_corners

def two_phase_ida_star(cube, goal_cube):
    # Phase 1: Reduce the cube to a reduced state
    print("Starting Phase 1...")
    phase1_solution = ida_star(cube, goal_cube, phase1_heuristic)
    if not phase1_solution:
        print("No solution found in Phase 1.")
        return None
    
    # Apply Phase 1 solution to the cube
    for move in phase1_solution:
        cube = make_move(cube, move)
    
    # Print the reduced state
    print("Reduced State after Phase 1:")
    print_rubik_cube(cube)
    
    # Check if the cube is already solved after Phase 1
    if cubes_equal(cube, goal_cube):
        print("Cube is already solved after Phase 1! Returning solution.")
        return phase1_solution
    
    # Phase 2: Solve the cube from the reduced state
    print("Starting Phase 2...")
    print("Is the cube already solved?", cubes_equal(cube, goal_cube))
    phase2_solution = ida_star(cube, goal_cube, phase2_heuristic)
    if not phase2_solution:
        print("No solution found in Phase 2.")
        return None
    
    # Combine both solutions
    return phase1_solution + phase2_solution

# Run the Two-Phase IDA* algorithm
solution = two_phase_ida_star(rubik_cube, goal_cube)

if solution:
    print("Solution:", " ".join(solution))
else:
    print("No solution found.")