import unittest
from utils import read_cube_configuration, validate_cube_configuration
from cube_solver import Cube
class TestCubeConfiguration(unittest.TestCase):

    def test_configuration_validity(self):
        config = [
            'WWW', 'WWW', 'WWW', 'GGG', 'GGG', 'GGG',
            'RRR', 'RRR', 'RRR', 'BBB', 'BBB', 'BBB',
            'OOO', 'OOO', 'OOO', 'YYY', 'YYY', 'YYY'
        ]
        self.assertTrue(validate_cube_configuration(config))

    def test_invalid_configuration(self):
        config = [
            'WWW', 'WWW', 'WWW', 'GGG', 'GGG', 'GGG',
            'RRR', 'RRR', 'RRR', 'BBB', 'BBB', 'BBB',
            'OOO', 'OOO', 'OOO', 'YYZ', 'YYY', 'YYY'
        ]
        self.assertFalse(validate_cube_configuration(config))
    def test_read_and_validate_file(self):
        config = read_cube_configuration('sample_cube.txt')
        self.assertTrue(validate_cube_configuration(config))

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
