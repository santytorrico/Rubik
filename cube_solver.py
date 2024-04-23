class RubiksCube:
    def __init__(
        self,
        n = 3,
        colors = ['w', 'o', 'g', 'r', 'b', 'y'],
        state = None
    ):
        if state is None:
            self.n = n
            self.colors = colors
            self.reset()
        else:
            self.n = int((len(state) / 6) ** (.5))
            self.colors = []
            self.cube = [[[]]]
            for i, s in enumerate(state):
                if s not in self.colours: self.colours.append(s)
                self.cube[-1][-1].append(s)
                if len(self.cube[-1][-1]) == self.n and len(self.cube[-1]) < self.n:
                    self.cube[-1].append([])
                elif len(self.cube[-1][-1]) == self.n and len(self.cube[-1]) == self.n and i < len(state) - 1:
                    self.cube.append([[]])
    def reset(self):
        """ Resets the cube to a solved state with unique colors on each face. """
        # Each face is a list of size x size filled with a single color
        self.cube = [[[c for x in range(self.n)] for y in range(self.n)] for c in self.colors]

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
        # Implementation as provided earlier
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

    def solved(self):
        """ Checks if the cube is in a solved state """
        return all(all(len(set(row)) == 1 for row in self.cube[face]) for face in self.cube)

# Example usage of the class
cube = RubiksCube()
cube.show()
print("Performing a horizontal twist on the middle row to the left:")
cube.horizontal_twist(1, 0)
cube.show()

print("Performing a vertical twist on the first column downwards:")
cube.vertical_twist(0, 0)
cube.show()
