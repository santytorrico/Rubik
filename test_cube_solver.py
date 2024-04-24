import unittest
from cube_solver import RubiksCube, solve_rubik_cube

class TestRubiksCubeSolver(unittest.TestCase):


    def test_initialization_solved(self):
        cube = RubiksCube()
        self.assertTrue(cube.solved(), "The cube should be solved upon initialization.")

    def test_file_loading(self):
        # Assuming 'solved_cube.txt' is a file that represents a solved cube state.
        cube = RubiksCube(file_path='sample_cube.txt')
        self.assertTrue(cube.solved(), "The cube should be solved when loaded from a solved state file.")

    def test_horizontal_twist(self):
        cube = RubiksCube()
        cube.horizontal_twist(0, 1)  # Twist the top row to the right
        cube.horizontal_twist(0, 0)  # Reverse the twist
        self.assertTrue(cube.solved(), "The cube should be solved after reversing the twist.")

    def test_vertical_twist(self):
        cube = RubiksCube()
        cube.vertical_twist(0, 1)  # Twist the first column upwards
        self.assertFalse(cube.solved(), "The cube should not be solved after a vertical twist.")
        cube.vertical_twist(0, 0)  # Reverse the twist
        self.assertTrue(cube.solved(), "The cube should be solved after reversing the twist.")


if __name__ == "__main__":
    unittest.main()
