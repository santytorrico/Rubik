from queue import Queue

class Cube:
    def __init__(self, configuration):
        self.config = configuration

    def rotate_face(self, face_index, clockwise=True):
        """Rotate a single face 90 degrees clockwise or counterclockwise."""
        face = self.config[face_index]
        if clockwise:
            # Rotate the face clockwise
            new_face = face[6] + face[3] + face[0] + face[7] + face[4] + face[1] + face[8] + face[5] + face[2]
        else:
            # Rotate the face counterclockwise
            new_face = face[2] + face[5] + face[8] + face[1] + face[4] + face[7] + face[0] + face[3] + face[6]
        self.config[face_index] = new_face

    def U_move(self):
        """Perform the U move (rotate the top face clockwise)."""
        self.rotate_face(0, clockwise=True)
        front_top_row = self.config[1][:3]
        self.config[1] = self.config[4][:3] + self.config[1][3:]  # Left to Front
        self.config[4] = self.config[3][:3] + self.config[4][3:]  # Back to Left
        self.config[3] = self.config[2][:3] + self.config[3][3:]  # Right to Back
        self.config[2] = front_top_row + self.config[2][3:]       # Front to Right

    def U_prime_move(self):
        """Perform the U' move (rotate the top face counterclockwise)."""
        self.rotate_face(0, clockwise=False)
        front_top_row = self.config[1][:3]
        self.config[1] = self.config[2][:3] + self.config[1][3:]
        self.config[2] = self.config[3][:3] + self.config[2][3:]
        self.config[3] = self.config[4][:3] + self.config[3][3:]
        self.config[4] = front_top_row + self.config[4][3:]

    def is_solved(self):
        """Check if the cube is solved."""
        return all(face == face[0]*9 for face in self.config)
    

def bfs_solve(start_cube):
    queue = Queue()
    visited = set()
    queue.put((start_cube, []))  # (current_cube, moves_list)

    while not queue.empty():
        current_cube, moves = queue.get()

        if current_cube.is_solved():
            return moves  # Return the list of moves that solved the cube

        for move in current_cube.possible_moves():
            new_cube = current_cube.perform_move(move)
            if str(new_cube.config) not in visited:  
                visited.add(str(new_cube.config))
                queue.put((new_cube, moves + [move]))

    return []  # Return an empty list if no solution found

def display_cube(cube):
    
    labels = ['Top', 'Front', 'Right', 'Back', 'Left', 'Bottom']
    for i, face in enumerate(cube.config):
        print(f"{labels[i]} Face:")
        print(f"{face[0:3]}\n{face[3:6]}\n{face[6:9]}\n")


if __name__ == '__main__':
    
    initial_config = ['WWWWWWWWW', 'GGGGGGGGG', 'RRRRRRRRR', 'BBBBBBBBB', 'OOOOOOOOO', 'YYYYYYYYY']
    cube = Cube(initial_config)
    display_cube(cube)
    solution_moves = bfs_solve(cube)
    print("Solution moves:", solution_moves)
