import unittest
from cube_solver import Cube

class TestCubeMoves(unittest.TestCase):
    def test_U_move(self):
        cube = Cube(['YYYYYYYYY', 'BBBBBBBBB', 'RRRRRRRRR', 'GGGGGGGGG', 'OOOOOOOOO', 'WWWWWWWWW'])
        cube.U_move()
        self.assertEqual(cube.config[1][:3], 'OOO')  # Front face top row should now be orange from left face

    def test_U_prime_move(self):
        cube = Cube(['YYYYYYYYY', 'BBBBBBBBB', 'RRRRRRRRR', 'GGGGGGGGG', 'OOOOOOOOO', 'WWWWWWWWW'])
        cube.U_prime_move()
        self.assertEqual(cube.config[1][:3], 'RRR')  # Front face top row should now be red from right face

if __name__ == '__main__':
    unittest.main()
