from engine.helper.data import Data
from engine.helper.minimax import Minimax
from config.constants import ROWS, COLS


class Lphant:
    def __init__(self):
        self.squares_data = {
            '1,1': 0, '1,2': 0, '1,3': 0, '1,4': 1,
            '2,1': 1, '2,2': 0, '2,3': 0, '2,4': 1,
            '3,1': 1, '3,2': 0, '3,3': 0, '3,4': 1,
            '4,1': 1, '4,2': 0, '4,3': 0, '4,4': 0,
        }
        self.data_helper = Data()

    def update_squares(self, data):
        """Updates engine data after a move"""

        for key in self.squares_data:
            piece = data.get(key)
            if piece:
                self.squares_data.update({key: piece})
            else:
                self.squares_data.update({key: 1})

    def play(self):
        """Start the process of finding the best move and return new board state"""

        move, score = self.get_the_best_move()
        if not move:
            return
        board_dict = self.transform_matrix_to_board(move)
        return [board_dict, score]

    def get_the_best_move(self):
        # Generating game tree, depth 2-3
        self.data_helper.set_state(self.squares_data)
        self.data_helper.generate_game_tree()

        # Finding the best move of the generated tree
        minimax = Minimax(self.data_helper.root)
        move_data = minimax.get_the_best_move()

        return move_data

    def transform_matrix_to_board(self, matrix):
        dict_board = {}
        for i in range(ROWS):
            for j in range(COLS):
                key = f'{i + 1},{j + 1}'
                val = matrix[i][j]
                dict_board.update({key: val})
        return dict_board
