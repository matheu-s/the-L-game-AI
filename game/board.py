import pygame, time

from config.constants import *
from game.pieces.coin import Coin
from game.pieces.L import L
from engine.Lphant import Lphant


class Board:
    def __init__(self, human_player_is):
        self.human_player_is = human_player_is
        self.engine = Lphant()
        self.turn = 1
        self.keys_L1_red = []
        self.keys_L2_blue = []
        self.key_coin_1 = ''
        self.key_coin_2 = ''
        self.temp_squares = []
        self.temp_keys = []
        self.squares = {
            '1,1': pygame.rect, '1,2': pygame.rect, '1,3': pygame.rect, '1,4': pygame.rect,
            '2,1': pygame.rect, '2,2': pygame.rect, '2,3': pygame.rect, '2,4': pygame.rect,
            '3,1': pygame.rect, '3,2': pygame.rect, '3,3': pygame.rect, '3,4': pygame.rect,
            '4,1': pygame.rect, '4,2': pygame.rect, '4,3': pygame.rect, '4,4': pygame.rect,
        }

    def check_input(self, pos, screen):
        """Called everytime there is an action on Play screen"""

        if self.check_human_turn():
            # Getting data on click
            clicked_key = self.get_key_clicked_square(pos)
            sqr = self.squares.get(clicked_key)

            # Checking if coin was the one clicked
            if clicked_key == self.key_coin_1:
                self.paint_square(screen, sqr, GREEN)
                self.key_coin_1 = None
                return
            if clicked_key == self.key_coin_2:
                self.paint_square(screen, sqr, GREEN)
                self.key_coin_2 = None
                return

            # Checking if the click is to place a new coin
            if not self.key_coin_1:
                coin = Coin(sqr)
                coin.draw(screen)
                self.key_coin_1 = clicked_key
                # Changing to bot move after coin is placed
                turn = 1 if self.human_player_is % 2 == 0 else 2
                self.turn = turn
                return
            if not self.key_coin_2:
                coin = Coin(sqr)
                coin.draw(screen)
                self.key_coin_2 = clicked_key
                # Changing to bot move after coin is placed
                turn = 1 if self.human_player_is % 2 == 0 else 2
                self.turn = turn
                return

            # Painting the clicked with temporary red
            self.paint_square(screen, sqr, LIGHT_RED)
            self.temp_squares.append(sqr)
            self.temp_keys.append(clicked_key)

            # When 4 selected, form the new L
            if len(self.temp_squares) == 4:
                # Resetting previous L
                for keys in self.keys_L1_red:
                    self.paint_square(screen, self.squares.get(keys), GREEN)

                # Resetting temp and updating selected L position
                l_piece = L(RED)
                l_piece.draw(screen, self.temp_squares)
                self.temp_squares = []
                self.keys_L1_red = self.temp_keys

        else:
            data = self.generate_data()
            self.engine.update_squares(data)
            try:
                new_board_state = self.engine.play()
            except GeneratorExit as e:
                print('bot lost')
                if e == 'LOSS':
                    print('bot lost')
                return False
            self.update_board(new_board_state, screen)
            time.sleep(1)
            self.turn = self.human_player_is

    def get_key_clicked_square(self, pos):
        """Returns the key of the clicked square according to the clicked position"""

        for key in self.squares.keys():
            sqr_pos = self.squares.get(key)
            if sqr_pos.collidepoint(pos):
                print('selected square: ', key)
                return key

    def check_human_turn(self):
        """TRUE -> Human turn, FALSE -> Lphant turn'"""

        if self.human_player_is == self.turn:
            return True
        return False

    def paint_square(self, screen, rect, color):
        """Paints 1 passed square"""

        a, b, c, d = rect
        pygame.draw.rect(screen, color, (int(a), int(b), int(c), int(d)))
        for i in range(4):
            pygame.draw.rect(screen, (0, 0, 0), (a - i, b - i, c - 1, d - 1), 1)

    def generate_data(self):
        """Gather all pieces positions and creates dict as {square_key: piece_name} -> {'1,1': 'C1'}"""

        data = {}

        for L_red in self.keys_L1_red:
            data.update({L_red: 'L1'})
        for L_blue in self.keys_L2_blue:
            data.update({L_blue: 'L2'})
        data.update({self.key_coin_1: 'C1'})
        data.update({self.key_coin_2: 'C2'})

        return data

    def update_board(self, dict_state, screen):
        """Updates all board keys and draws pieces after computer moves"""

        self.keys_L1_red = []
        self.keys_L2_blue = []
        self.key_coin_1 = ''
        self.key_coin_2 = ''
        self.temp_squares = []
        self.temp_keys = []

        # Painting all to green
        self.draw_board(screen)

        # Updating all pieces keys
        for key in dict_state:
            if dict_state[key] == 'L1':
                self.keys_L1_red.append(key)
            elif dict_state[key] == 'L2':
                self.keys_L2_blue.append(key)
            elif dict_state[key] == 'C1':
                self.key_coin_1 = key
            elif dict_state[key] == 'C2':
                self.key_coin_2 = key

        # Painting pieces on the board again
        for key in self.keys_L1_red:
            self.temp_squares.append(self.squares.get(key))
        l_piece = L(RED)
        l_piece.draw(screen, self.temp_squares)
        self.temp_squares = []

        for key in self.keys_L2_blue:
            self.temp_squares.append(self.squares.get(key))
        l_piece2 = L(BLUE)
        l_piece2.draw(screen, self.temp_squares)
        self.temp_squares = []

        coin1 = Coin(self.squares[self.key_coin_1])
        coin1.draw(screen)

        coin2 = Coin(self.squares[self.key_coin_2])
        coin2.draw(screen)

    def draw_initial_state(self, screen):
        """Draws the initial state of the game with all pieces on it"""

        # Drawing coins
        pos1 = self.squares.get('1,1')
        coin1 = Coin(pos1)
        coin1.draw(screen)
        self.key_coin_1 = '1,1'

        pos2 = self.squares.get('4,4')
        coin2 = Coin(pos2)
        coin2.draw(screen)
        self.key_coin_2 = '4,4'

        # Drawing L's
        L_RED = L(RED)
        initial_squares_L1 = [self.squares.get('1,2'), self.squares.get('1,3'), self.squares.get('2,3'),
                              self.squares.get('3,3')]
        L_RED.draw(screen, initial_squares_L1)
        self.keys_L1_red = ['1,2', '1,3', '2,3', '3,3']

        L_BLUE = L(BLUE)
        initial_squares_L2 = [self.squares.get('2,2'), self.squares.get('3,2'), self.squares.get('4,2'),
                              self.squares.get('4,3')]
        L_BLUE.draw(screen, initial_squares_L2)
        self.keys_L2_blue = ['2,2', '3,2', '4,2', '4,3']

    def draw_board(self, screen):
        """Draws initial board dimensions and squares"""

        board_rect = pygame.draw.rect(screen, (240, 240, 240), (20, 40, PLAY_SCREEN_WIDTH, PLAY_SCREEN_HEIGHT))
        square_size = 165  # 720 - 60 = 660/4 = 165
        start_x = 20
        start_y = 40
        row_x = 1
        col_y = 1
        for row in range(ROWS):
            for col in range(COLS):
                # Drawing the green squares empty
                square = pygame.draw.rect(screen, GREEN,
                                          (int(start_x), int(start_y), int(square_size), int(square_size)))
                self.squares.update({f'{col_y},{row_x}': square.copy()})
                # Borders of the square
                for i in range(4):
                    pygame.draw.rect(screen, (0, 0, 0), (start_x - i, start_y - i, square_size - 1, square_size - 1), 1)
                start_y += square_size
                col_y += 1
            start_x += square_size
            row_x += 1
            # Resetting col variables for start of new row
            start_y = 40
            col_y = 1

