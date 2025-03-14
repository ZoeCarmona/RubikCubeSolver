import shutil
import copy
import tqdm  # For progress bar
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
    # Rotate the front face clockwise
    cube["front"] = rotate_face_clockwise(cube["front"])
    
    # Update adjacent faces
    top_row = cube["Up"][2]
    left_col = [cube["left"][i][2] for i in range(3)]
    bottom_row = cube["Down"][0]
    right_col = [cube["right"][i][0] for i in range(3)]
    
    # Move the edge pieces from Up, left, Down, and right
    for i in range(3):
        cube["Up"][2][i] = left_col[2 - i]
        cube["left"][i][2] = bottom_row[i]
        cube["Down"][0][i] = right_col[2 - i]
        cube["right"][i][0] = top_row[i]

def move_F_prime(cube):
    # Rotate the front face counterclockwise
    cube["front"] = rotate_face_counterclockwise(cube["front"])
    
    # Update adjacent faces
    top_row = cube["Up"][2]
    left_col = [cube["left"][i][2] for i in range(3)]
    bottom_row = cube["Down"][0]
    right_col = [cube["right"][i][0] for i in range(3)]
    
    # Move the edge pieces from Up, left, Down, and right
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
    
    # Update adjacent faces
    top_row = cube["Up"][0]
    right_col = [cube["right"][i][2] for i in range(3)]
    bottom_row = cube["Down"][2]
    left_col = [cube["left"][i][0] for i in range(3)]
    
    # Move the edge pieces from Up, right, Down, and left
    for i in range(3):
        cube["Up"][0][i] = left_col[i]
        cube["right"][i][2] = top_row[2 - i]
        cube["Down"][2][i] = right_col[i]
        cube["left"][i][0] = bottom_row[2 - i]

def move_B_prime(cube):
    # Rotate the back face counterclockwise
    cube["back"] = rotate_face_counterclockwise(cube["back"])
    
    # Update adjacent faces
    top_row = cube["Up"][0]
    right_col = [cube["right"][i][2] for i in range(3)]
    bottom_row = cube["Down"][2]
    left_col = [cube["left"][i][0] for i in range(3)]
    
    # Move the edge pieces from Up, right, Down, and left
    for i in range(3):
        cube["Up"][0][i] = right_col[2 - i]
        cube["right"][i][2] = bottom_row[i]
        cube["Down"][2][i] = left_col[2 - i]
        cube["left"][i][0] = top_row[i]

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
                    distance += 1
    return distance // 8  # Divide by 8 to approximate the number of moves

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
def ida_star(cube, goal_cube):
    def dfs(cube, depth, g, limit, path, visited):
        if cube_to_tuple(cube) in visited:
            return None  # Prune duplicate states
        
        visited.add(cube_to_tuple(cube))

        if cubes_equal(cube, goal_cube):
            return path

        f = g + manhattan_distance(cube, goal_cube)
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

    limit = manhattan_distance(cube, goal_cube)
    with tqdm.tqdm(total=100, desc="Solving", unit="%") as progress:
        while True:
            visited = set()
            path = []
            result = dfs(cube, 0, 0, limit, path, visited)
            progress.update(5)  # Update progress (estimated 20 iterations max)
            if isinstance(result, list):
                return result
            if result == float('inf'):
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

# Run IDA* to find the solution path
solution = ida_star(rubik_cube, goal_cube)

if solution:
    # Output the solution path in the desired format (e.g., a space-separated string of moves)
    print("Solution found:")
    print(" ".join(solution))
else:
    print("No solution found")