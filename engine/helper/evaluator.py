class Evaluator:
    def __init__(self):
        self.player = None
        self.state = None

    def get_score(self, move):
        """Calculates and returns score using center occupancy and border touches factor"""

        self.state = move
        maximizer_score = 0
        minimizer_score = 0

        # Getting points for Lphant
        maximizer_score += self.calculate_center_occupancy('L2')
        if maximizer_score != 1:
            maximizer_score += self.calculate_border_touches('L2')

        # Getting points for human player
        minimizer_score += self.calculate_center_occupancy('L1')
        if minimizer_score != 1:
            minimizer_score += self.calculate_border_touches('L1')

        # Returning score according to which player has more points
        if maximizer_score > minimizer_score:
            return maximizer_score - minimizer_score
        elif minimizer_score > maximizer_score:
            return -(minimizer_score - maximizer_score)
        else:
            return 0

    def calculate_center_occupancy(self, piece):
        """Evaluates how many squares own L occupies on center, if 3 squares, +1'"""

        pieces_on_center = 0
        for i in range(1, 3):
            for j in range(1, 3):
                if self.state[i][j] == piece:
                    pieces_on_center += 1

        if pieces_on_center == 3:
            return 1
        else:
            return 0

    def calculate_border_touches(self, piece):
        """Evaluates if whole own L piece is touching the border, if yes, -1'"""

        pieces_on_border = 0

        # Checking rows 0 and 3
        for i in range(0, 4, 3):
            for j in range(4):
                if self.state[i][j] == piece:
                    pieces_on_border += 1
        # Checking mid of cols 0 and 3
        for i in range(0, 4, 3):
            for j in range(1, 3):
                if self.state[j][i] == piece:
                    pieces_on_border += 1

        if pieces_on_border == 4:
            return -1
        else:
            return 0
