import pygame, time

from config.constants import *
from game.pieces.coin import Coin
from game.pieces.L import L


class Board:
    def __init__(self, human_player_is):
        self.human_player_is = human_player_is
        self.turn = 1
        self.squares = {'1,1': None, '1,2': None, '1,3': None, '1,4': None,
                        '2,1': None, '2,2': None, '2,3': None, '2,4': None,
                        '3,1': None, '3,2': None, '3,3': None, '3,4': None,
                        '4,1': None, '4,2': None, '4,3': None, '4,4': None,
                        }
        self.selected_squares_L1_red = []
        self.selected_squares_L2_blue = []
        self.selected_squares_coin_1 = []
        self.selected_squares_coin_2 = []
        self.temp_squares = []

    def check_input(self, pos, screen):
        if self.check_turn():
            # Painting the clicked with temporary red
            sqr = self.squares.get(self.get_clicked_square(pos))
            self.paint_square(screen, sqr, LIGHT_RED)
            self.temp_squares.append(sqr)

            # When 4 selected, form the new L
            if len(self.temp_squares) == 4:
                for rec in self.selected_squares_L1_red:
                    self.paint_square(screen, rec, GREEN)

                # Resetting temp and updating selected L position
                self.selected_squares_L1_red = self.temp_squares
                self.temp_squares = []
                l_piece = L(RED)
                l_piece.draw(screen, self.selected_squares_L1_red)

                #create an engine class and engine.update(11, 12, .. selected)

    def get_clicked_square(self, pos):
        for key in self.squares.keys():
            sqr_pos = self.squares.get(key)
            if sqr_pos.collidepoint(pos):
                print('selected square: ', key)
                return key

    def check_turn(self):
        if self.human_player_is == self.turn:
            return True
        return False

    def paint_square(self, screen, rect, color):
        a, b, c, d = rect
        pygame.draw.rect(screen, color, (int(a), int(b), int(c), int(d)))
        for i in range(4):
            pygame.draw.rect(screen, (0, 0, 0), (a - i, b - i, c - 1, d - 1), 1)

    def draw_initial_state(self, screen):
        # Drawing coins
        pos1 = self.squares.get('1,1')
        coin1 = Coin(pos1)
        coin1.draw(screen)
        self.selected_squares_coin_1 = '1,1'

        pos2 = self.squares.get('4,4')
        coin2 = Coin(pos2)
        coin2.draw(screen)
        self.selected_squares_coin_2 = '4,4'

        # Drawing L's
        L_RED = L(RED)
        initial_squares_L1 = [self.squares.get('1,2'), self.squares.get('1,3'), self.squares.get('2,3'),
                              self.squares.get('3,3')]
        L_RED.draw(screen, initial_squares_L1)
        self.selected_squares_L1_red = initial_squares_L1

        L_BLUE = L(BLUE)
        initial_squares_L2 = [self.squares.get('2,2'), self.squares.get('3,2'), self.squares.get('4,2'),
                              self.squares.get('4,3')]
        L_BLUE.draw(screen, initial_squares_L2)
        self.selected_squares_L2_blue = initial_squares_L2

    def draw_board(self, screen):
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

        print(self.squares)

        # pygame.display.update()

    def start(self):
        if (self.human_player_is == 2):
            time.sleep(2)
            print('computer moves..')
        else:
            print('wait player move')
