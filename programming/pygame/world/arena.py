import pygame
from config.constants import (SCREEN_WIDTH, SCREEN_HEIGHT, ARENA_MARGIN,
                              ARENA_COLOR, ARENA_BORDER_COLOR, ARENA_BORDER_WIDTH)


class Arena:
    def __init__(self):
        self.rect = pygame.Rect(
            ARENA_MARGIN, ARENA_MARGIN,
            SCREEN_WIDTH - ARENA_MARGIN * 2,
            SCREEN_HEIGHT - ARENA_MARGIN * 2
        )
        self.color = ARENA_COLOR
        self.border_color = ARENA_BORDER_COLOR
        self.border_width = ARENA_BORDER_WIDTH

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, self.border_color,
                         self.rect, self.border_width)
