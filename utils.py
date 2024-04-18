def read_cube_configuration(filepath):
    """Reads the Rubik's cube configuration from a text file."""
    with open(filepath, 'r') as file:
        lines = file.readlines()
        if len(lines) != 18:
            raise ValueError("Invalid number of lines in cube configuration file.")
        return [line.strip() for line in lines]

def validate_cube_configuration(config):
    """Validates that the cube configuration has the correct number of each color."""
    color_count = {}
    for row in config:
        for color in row:
            if color in color_count:
                color_count[color] += 1
            else:
                color_count[color] = 1
    
    # Check if each color appears exactly 9 times
    for count in color_count.values():
        if count != 9:
            return False
    return True
