import pygame
from constants import (BACKGROUND_COLOR, AMBIENT_COLOR,
                       LIGHT_COLOR, LIGHT_RADIUS, SCREEN_HEIGHT, SCREEN_WIDTH)


class Renderer:
    def __init__(self):
        self.light_map = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.light_map.fill(AMBIENT_COLOR)

    def draw(self, screen, arena, player, enemies):
        screen.fill(BACKGROUND_COLOR)
        arena.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)
        player.draw(screen)

        self.light_map.fill(AMBIENT_COLOR)

        pygame.draw.circle(
            self.light_map,
            LIGHT_COLOR,
            (int(player.pos.x), int(player.pos.y)),
            LIGHT_RADIUS
        )

        screen.blit(self.light_map, (0, 0),
                    special_flags=pygame.BLEND_RGB_MULT)

        pygame.display.flip()
