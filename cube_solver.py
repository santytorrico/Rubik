import heapq
from collections import deque

class RubiksCube:
    def __init__(self, n=3, colors=['w', 'o', 'g', 'r', 'b', 'y'], file_path=None):
        self.n = n
        self.colors = colors
        self.last_move = None
        if file_path:
            self.load_from_file(file_path)
        else:
            self.reset()
            
    def reset(self):
        """ Resets the cube to a solved state with unique colors on each face. """
        # Each face is a list of size x size filled with a single color
        self.cube = [[[color for x in range(self.n)] for y in range(self.n)] for color in self.colors]

    def load_from_file(self, file_path):
        """ Load the cube's state from a file. """
        try:
            with open(file_path, 'r') as file:
                lines = [line.strip() for line in file if line.strip()]
            if not self.validate_configuration(lines):
                print("Invalid configuration. Loading default solved state instead.")
                self.reset()
            else:
                self.cube = []
                for i in range(0, len(lines), self.n):
                    face = [list(lines[j]) for j in range(i, i + self.n)]
                    self.cube.append(face)
        except FileNotFoundError:
            print("File not found. Loading default solved state instead.")
            self.reset()
    def validate_configuration(self, lines):
        """ Validate the cube's configuration. """
        # Check the total number of lines
        if len(lines) != 6 * self.n:
            raise ValueError("Invalid number of lines in the configuration.")
        
        # Create a dictionary to count occurrences of each color
        color_count = {color: 0 for color in self.colors}
        
        # Check each line for correct number of characters
        for line in lines:
            if len(line) != self.n:
                raise ValueError("Invalid line length in the configuration.")
            
            # Count each color occurrence
            for char in line:
                if char in color_count:
                    color_count[char] += 1
                else:
                    raise ValueError(f"Unknown color {char} in the configuration.")
        
        # Check for correct number of each color
        expected_count = self.n * self.n
        if any(count != expected_count for count in color_count.values()):
            raise ValueError("Incorrect number of pieces for one or more colors.")
        
        # Specific check for centers for 3x3 or any odd n cubes (even n don't have a single center)
        if self.n % 2 != 0:
            center_indices = [self.n // 2]  # Get the index of the center row and column
            centers = [lines[self.n * i + center_indices[0]][center_indices[0]] for i in range(6)]
            if len(set(centers)) != 6:
                raise ValueError("There are duplicate centers or incorrect center configuration.")
        
        return True

    def show(self):
        """
        Input: None
        Description: Show the rubiks cube
        Output: None
        """
        spacing = f'{" " * (len(str(self.cube[0][0])) + 2)}'
        l1 = '\n'.join(spacing + str(c) for c in self.cube[0])
        l2 = '\n'.join('  '.join(str(self.cube[i][j]) for i in range(1,5)) for j in range(len(self.cube[0])))
        l3 = '\n'.join(spacing + str(c) for c in self.cube[5])
        print(f'{l1}\n\n{l2}\n\n{l3}')

    def horizontal_twist(self, row, direction):
        """ Horizontal twist of a row in the specified direction """
        self.last_move = ('h', row, direction)
        if row < len(self.cube[0]):
            if direction == 0: #Twist left
                self.cube[1][row], self.cube[2][row], self.cube[3][row], self.cube[4][row] = (self.cube[2][row],
                                                                                              self.cube[3][row],
                                                                                              self.cube[4][row],
                                                                                              self.cube[1][row])

            elif direction == 1: #Twist right
                self.cube[1][row], self.cube[2][row], self.cube[3][row], self.cube[4][row] = (self.cube[4][row],
                                                                                              self.cube[1][row],
                                                                                              self.cube[2][row],
                                                                                              self.cube[3][row])
            else:
                print(f'ERROR - direction must be 0 (left) or 1 (right)')
                return
            #Rotating connected face
            if direction == 0: #Twist left
                if row == 0:
                    self.cube[0] = [list(x) for x in zip(*reversed(self.cube[0]))] #Transpose top
                elif row == len(self.cube[0]) - 1:
                    self.cube[5] = [list(x) for x in zip(*reversed(self.cube[5]))] #Transpose bottom
            elif direction == 1: #Twist right
                if row == 0:
                    self.cube[0] = [list(x) for x in zip(*self.cube[0])][::-1] #Transpose top
                elif row == len(self.cube[0]) - 1:
                    self.cube[5] = [list(x) for x in zip(*self.cube[5])][::-1] #Transpose bottom
        else:
            print(f'ERROR - desired row outside of rubiks cube range. Please select a row between 0-{len(self.cube[0])-1}')
            return

    def vertical_twist(self, column, direction):
        """ Vertical twist of a column in the specified direction """
        self.last_move = ('v', column, direction)
        if column < len(self.cube[0]):
            for i in range(len(self.cube[0])):
                if direction == 0: #Twist down
                    self.cube[0][i][column], self.cube[2][i][column], self.cube[4][-i-1][-column-1], self.cube[5][i][column] = (self.cube[4][-i-1][-column-1],
                                                                                                                                self.cube[0][i][column],
                                                                                                                                self.cube[5][i][column],
                                                                                                                                self.cube[2][i][column])
                elif direction == 1: #Twist up
                    self.cube[0][i][column], self.cube[2][i][column], self.cube[4][-i-1][-column-1], self.cube[5][i][column] = (self.cube[2][i][column],
                                                                                                                                self.cube[5][i][column],
                                                                                                                                self.cube[0][i][column],
                                                                                                                                self.cube[4][-i-1][-column-1])
                else:
                    print(f'ERROR - direction must be 0 (down) or 1 (up)')
                    return
            #Rotating connected face
            if direction == 0: #Twist down
                if column == 0:
                    self.cube[1] = [list(x) for x in zip(*self.cube[1])][::-1] #Transpose left
                elif column == len(self.cube[0]) - 1:
                    self.cube[3] = [list(x) for x in zip(*self.cube[3])][::-1] #Transpose right
            elif direction == 1: #Twist up
                if column == 0:
                    self.cube[1] = [list(x) for x in zip(*reversed(self.cube[1]))] #Transpose left
                elif column == len(self.cube[0]) - 1:
                    self.cube[3] = [list(x) for x in zip(*reversed(self.cube[3]))] #Transpose right

        else:
            print(f'ERROR - desired column outside of rubiks cube range. Please select a column between 0-{len(self.cube[0])-1}')
            return

    def side_twist(self, column, direction):
        """ Side twist affecting edges and corresponding rotations of the side faces """
        self.last_move = ('s', column, direction)
        if column < len(self.cube[0]):
            for i in range(len(self.cube[0])):
                if direction == 0: #Twist down
                    self.cube[0][column][i], self.cube[1][-i-1][column], self.cube[3][i][-column-1], self.cube[5][-column-1][-1-i] = (self.cube[3][i][-column-1],
                                                                                                                                      self.cube[0][column][i],
                                                                                                                                      self.cube[5][-column-1][-1-i],
                                                                                                                                      self.cube[1][-i-1][column])
                elif direction == 1: #Twist up
                    self.cube[0][column][i], self.cube[1][-i-1][column], self.cube[3][i][-column-1], self.cube[5][-column-1][-1-i] = (self.cube[1][-i-1][column],
                                                                                                                                      self.cube[5][-column-1][-1-i],
                                                                                                                                      self.cube[0][column][i],
                                                                                                                                      self.cube[3][i][-column-1])
                else:
                    print(f'ERROR - direction must be 0 (down) or 1 (up)')
                    return
            #Rotating connected face
            if direction == 0: #Twist down
                if column == 0:
                    self.cube[4] = [list(x) for x in zip(*reversed(self.cube[4]))] #Transpose back
                elif column == len(self.cube[0]) - 1:
                    self.cube[2] = [list(x) for x in zip(*reversed(self.cube[2]))] #Transpose top
            elif direction == 1: #Twist up
                if column == 0:
                    self.cube[4] = [list(x) for x in zip(*self.cube[4])][::-1] #Transpose back
                elif column == len(self.cube[0]) - 1:
                    self.cube[2] = [list(x) for x in zip(*self.cube[2])][::-1] #Transpose top
        else:
            print(f'ERROR - desired column outside of rubiks cube range. Please select a column between 0-{len(self.cube[0])-1}')
            return
    def __lt__(self, other):
        """
        Define the less than operator to compare two RubiksCube instances based on their cube state.
        """
        return str(self.cube) < str(other.cube)
    
    def get_successors(self):
        """
        Generate all possible successor states from the current state.
        """
        successors = []
        for row in range(self.n):
            for direction in [0, 1]:
                new_state = RubiksCube(self.n, self.colors)
                new_state.cube = [face[:] for face in self.cube]
                new_state.horizontal_twist(row, direction)
                successors.append(new_state)

        for col in range(self.n):
            for direction in [0, 1]:
                new_state = RubiksCube(self.n, self.colors)
                new_state.cube = [face[:] for face in self.cube]
                new_state.vertical_twist(col, direction)
                successors.append(new_state)

        for col in range(self.n):
            for direction in [0, 1]:
                new_state = RubiksCube(self.n, self.colors)
                new_state.cube = [face[:] for face in self.cube]
                new_state.side_twist(col, direction)
                successors.append(new_state)

        return successors
    
    # def heuristic(self):
    #     """
    #     Implement a heuristic function to estimate the distance or cost from the current state to the goal state.
    #     """
    #     cost = 0
    #     for face in self.cube:
    #         unique_colors = set(color for row in face for color in row)
    #         cost += len(unique_colors) - 1  # Subtract 1 for the correct color
    #     return cost
    # def heuristic(self):
    #     """
    #     Implement a heuristic function based on the Manhattan distance to estimate the distance to the goal state.
    #     """
    #     goal_state = [[[color for _ in range(self.n)] for _ in range(self.n)] for color in self.colors]
    #     distance = 0

    #     for face in range(6):
    #         for row in range(self.n):
    #             for col in range(self.n):
    #                 if self.cube[face][row][col] != goal_state[face][row][col]:
    #                     # Find the correct position of the cube piece
    #                     correct_face, correct_row, correct_col = self.find_correct_position(face, row, col)
                        
    #                     # Calculate the Manhattan distance
    #                     distance += abs(face - correct_face) + abs(row - correct_row) + abs(col - correct_col)

    #     return distance

    # def find_correct_position(self, face, row, col):
    #     """
    #     Find the correct position of a cube piece given its current position.
    #     """
    #     color = self.cube[face][row][col]
    #     for f in range(6):
    #         if color == self.colors[f]:
    #             return f, row, col

    #     # If no correct position is found, return the current position
    #     return face, row, col

    def heuristic(self):
        """
        Implement the 'Sum of Permutation Inversions' heuristic for the Rubik's cube problem.
        """
        goal_state = [[[color for _ in range(self.n)] for _ in range(self.n)] for color in self.colors]
        inversions = 0

        # Count inversions for each face
        for face in range(6):
            face_inversions = 0
            for row in range(self.n):
                for col in range(self.n):
                    if self.cube[face][row][col] != goal_state[face][row][col]:
                        piece_value = self.cube[face][row][col]
                        for f in range(face, 6):
                            for r in range(self.n):
                                for c in range(self.n):
                                    if goal_state[f][r][c] == piece_value:
                                        for f2 in range(face, f):
                                            for r2 in range(self.n):
                                                for c2 in range(self.n):
                                                    if self.cube[f2][r2][c2] != goal_state[f2][r2][c2]:
                                                        face_inversions += 1
                                        break
                    else:
                        continue
                    break
            inversions += face_inversions

        return inversions


    def is_goal_state(self):
        """
        Check if the current state is the goal state (solved cube).
        """
        return self.heuristic() == 0

    def solved(self):
        """
        Checks if the cube is in a solved state
        """
        for i, face in enumerate(self.cube):
            if any(len(set(row)) != 1 for row in face):
                return False
        return True
    
def solve_rubik_cube(initial_state):
    frontier = []
    heapq.heappush(frontier, (initial_state.heuristic(), initial_state, []))  # Initialize with an empty move list
    came_from = {str(initial_state.cube): (None, None)}  # Store (parent_state, moves_to_parent)
    cost_so_far = {str(initial_state.cube): 0}

    while frontier:
        _, current_state, current_moves = heapq.heappop(frontier)

        if current_state.is_goal_state():
            path = []
            state, moves = current_state, current_moves
            while state is not None:
                if str(state.cube) in came_from:
                    path.append((state, moves))
                    parent_state, parent_moves = came_from[str(state.cube)]
                    state = parent_state
                    moves = parent_moves
                else:
                    break
            solution_path = list(reversed(path))
            print("Solution found in", len(solution_path), "steps:")
            for state, moves in solution_path:
                state.show()
                print("Moves:", " -> ".join(map(str, moves)))
                print()
            return solution_path

        for neighbor in current_state.get_successors():
            neighbor_cube = str(neighbor.cube)
            new_cost = cost_so_far[str(current_state.cube)] + 1
            if neighbor_cube not in cost_so_far or new_cost < cost_so_far[neighbor_cube]:
                cost_so_far[neighbor_cube] = new_cost
                priority = new_cost + neighbor.heuristic()
                neighbor_moves = current_moves + [neighbor.last_move]  # Append the move that led to this neighbor
                heapq.heappush(frontier, (priority, neighbor, neighbor_moves))
                came_from[neighbor_cube] = (current_state, current_moves)

    print("No solution found.")
    return None

initial_cube = RubiksCube(file_path='sample_cube.txt')
# initial_cube= RubiksCube()
initial_cube.horizontal_twist(0,1)
# initial_cube.vertical_twist(1,0)

solution = solve_rubik_cube(initial_cube)

print("Is the cube solvable?", initial_cube.solved())

if solution:
    print("Solution found:")
    for state, moves in solution:
        state.show()
        print("Moves:", " -> ".join(map(str, moves)))
        print()
else:
    print("No solution found.")