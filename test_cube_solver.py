import unittest
from utils import read_cube_configuration, validate_cube_configuration

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

if __name__ == '__main__':
    unittest.main()
