from config.constants import ROWS, COLS


class Data:
    def __init__(self):
        self.matrix_squares_availability = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

    def set_availability(self, data):
        """Update local matrix to make data handling easier"""

        index_offset = 1
        for key in data:
            row, col = key.split(',')
            row = int(row) - index_offset
            col = int(col) - index_offset
            piece = data.get(key)
            if piece:
                self.matrix_squares_availability[row][col] = piece
            else:
                self.matrix_squares_availability[row][col] = 1

    def get_L_fit(self):
        """Get places where L fits"""
        print('getting L...')
