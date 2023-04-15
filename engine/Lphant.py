from engine.helper.data import Data


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
        for key in self.squares_data:
            piece = data.get(key)
            if piece:
                self.squares_data.update({key: piece})
            else:
                self.squares_data.update({key: 1})

    def play(self):
        tree = self.generate_game_tree()
        print('generating tree')

    def generate_game_tree(self):
        self.data_helper.set_state(self.squares_data)
        self.data_helper.generate_game_tree()
        return 'generating...'
