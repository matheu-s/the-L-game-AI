import pygame

from config.constants import SQUARE_SIZE


class L:
    def __init__(self, color):
        self.color = color

    def draw(self, screen, squares):
        for i in range(len(squares)):
            x, y, x_size, y_size = squares[i]
            print(x, y)
            square = pygame.draw.rect(screen, self.color, (x, y, x_size-2, y_size-2))
            for i in range(4):
                pygame.draw.rect(screen, (0, 0, 0), (x - i, y - i, x_size - 1, y_size - 1), 1)


