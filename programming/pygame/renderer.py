import pygame
from constants import BACKGROUND_COLOR


class Renderer:
    @staticmethod
    def draw(screen, arena, player, enemies):
        screen.fill(BACKGROUND_COLOR)
        arena.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)
        player.draw(screen)

        pygame.display.flip()
