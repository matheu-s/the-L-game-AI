import pygame

from config.constants import YELLOW


class Coin:
    def __init__(self, pos):
        self.x, self.y, self.x_size, self.y_size = pos

    def draw(self, screen):
        radius = self.x_size // 3 - 10  # square - padding
        pygame.draw.circle(screen, (0, 0, 0), ((self.x + self.x_size / 2), (self.y + self.y_size / 2)), int(radius) + 3)
        pygame.draw.circle(screen, YELLOW, ((self.x + self.x_size / 2), (self.y + self.y_size / 2)), int(radius))

    def __repr__(self):
        return str(self.x, self.y)
