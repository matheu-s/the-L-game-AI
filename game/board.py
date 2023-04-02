import pygame

from config.constants import *


class Board:
    def __init__(self):
        self.squares = []
        self.selected_squares_L = []
        self.selected_square_coin = None

    def draw_board(self, screen):
        board_rect = pygame.draw.rect(screen, (240, 240, 240), (20, 40, HEIGHT - 60, HEIGHT - 60))
        square_size = 165  # 720 - 60 = 660/4 = 165
        start_x = 20
        start_y = 40
        for row in range(ROWS):
            for col in range(COLS):
                square = pygame.draw.rect(screen, GREEN, (int(start_x), int(start_y), int(square_size), int(square_size)))
                self.squares.append(square.copy())
                # Borders of the square
                for i in range(4):
                    pygame.draw.rect(screen, (0, 0, 0), (start_x - i, start_y - i, square_size-1, square_size-1), 1)
                start_y += square_size
            start_x += square_size
            start_y = 40

        print(self.squares)

        # pygame.display.update()
