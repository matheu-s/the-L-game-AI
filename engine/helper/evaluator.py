from config.constants import ROWS, COLS
from copy import deepcopy


class Evaluator:
    def __init__(self):
        self.state = None

    def get_score(self, move):
        """Calculates and returns score using center occupancy and border touches factor"""

        self.state = move
        score = 0
        score += self.calculate_center_occupancy()
        score += self.calculate_border_touches()
        return score

    def calculate_center_occupancy(self):
        """Evaluates how many squares own L occupies on center, if 3 squares, +2'"""

        pieces_on_center = 0
        for i in range(1, 3):
            for j in range(1, 3):
                if self.state[i][j] == 'L2':
                    pieces_on_center += 1

        if pieces_on_center == 3:
            return 2
        else:
            return 0

    def calculate_border_touches(self):
        """Evaluates if all own L piece is touching the border, if yes, -1'"""

        pieces_on_border = 0

        # Checking rows 0 and 3
        for i in range(0, 4, 3):
            for j in range(4):
                if self.state[i][j] == 'L2':
                    pieces_on_border += 1
        # Checking mid of cols 0 and 3
        for i in range(0, 4, 3):
            for j in range(1, 3):
                if self.state[j][i] == 'L2':
                    pieces_on_border += 1
        if pieces_on_border == 4:
            return -1
        else:
            return 0
