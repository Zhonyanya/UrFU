import pygame
import math
from constants import (BACKGROUND_COLOR, AMBIENT_COLOR,
                       LIGHT_COLOR, LIGHT_RADIUS, SCREEN_HEIGHT,
                       SCREEN_WIDTH, LIGHT_ANGLE_RAD)


class Renderer:
    def __init__(self):
        self.light_map = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.light_map.fill(AMBIENT_COLOR)
        self.light_cone = self._create_cone_gradient(
            LIGHT_RADIUS,
            LIGHT_ANGLE_RAD,
            LIGHT_COLOR,
            AMBIENT_COLOR
        )

    @staticmethod
    def _create_cone_gradient(radius, angle_rad, center_color, edge_color):
        size = radius * 2
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        center = radius

        for x in range(size):
            for y in range(size):
                dx = x - center
                dy = y - center
                dist = math.sqrt(dx ** 2 + dy ** 2)

                if dist < radius:
                    angle = math.atan2(dy, dx)
                    if abs(angle) <= angle_rad:
                        t = dist / radius
                        r = int(center_color[0] * (1 - t) + edge_color[0] * t)
                        g = int(center_color[1] * (1 - t) + edge_color[1] * t)
                        b = int(center_color[2] * (1 - t) + edge_color[2] * t)
                        alpha = int(255 * (1 - t))
                        surface.set_at((x, y), (r, g, b, alpha))

        return surface

    def draw(self, screen, arena, player, enemies):
        screen.fill(BACKGROUND_COLOR)
        arena.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)
        player.draw(screen)

        self.light_map.fill(AMBIENT_COLOR)

        rotated_cone = pygame.transform.rotate(self.light_cone,
                                               -math.degrees(player.angle))

        cone_rect = rotated_cone.get_rect(center=(int(player.pos.x),
                                                  int(player.pos.y)))

        self.light_map.blit(rotated_cone, cone_rect.topleft,
                            special_flags=pygame.BLEND_RGB_ADD)

        screen.blit(self.light_map, (0, 0),
                    special_flags=pygame.BLEND_RGB_MULT)

        pygame.display.flip()
