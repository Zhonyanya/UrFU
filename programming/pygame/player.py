import pygame
from constants import (PLAYER_SIZE, PLAYER_COLOR, PLAYER_START_POS,
                       PLAYER_MAX_SPEED, PLAYER_ACCELERATION,
                       PLAYER_DECELERATION)


class Player:
    def __init__(self):
        self.pos = pygame.math.Vector2(PLAYER_START_POS)
        self.vel = pygame.math.Vector2(0, 0)
        self.rect = pygame.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE)
        self.update_rect()

    def update(self, dt, input_vector, arena_rect):
        # Целевая скорость на основе нормализованного вектора
        target_vel = input_vector * PLAYER_MAX_SPEED
        vel_diff = target_vel - self.vel

        # Выбор ускорения: разгон или торможение
        if input_vector.length() > 0:
            accel_rate = PLAYER_ACCELERATION
        else:
            accel_rate = PLAYER_DECELERATION
        max_change = accel_rate * dt

        # Ограничиваем изменение скорости, чтобы разгон был плавным
        if vel_diff.length() > 0 and vel_diff.length() > max_change:
            vel_diff.normalize_ip()
            vel_diff *= max_change

        self.vel += vel_diff
        self.pos += self.vel * dt

        # Жёсткое ограничение границами арены (работает с float)
        half = PLAYER_SIZE / 2
        self.pos.x = max(arena_rect.left + half, min(arena_rect.right - half,
                                                     self.pos.x))
        self.pos.y = max(arena_rect.top + half, min(arena_rect.bottom - half,
                                                    self.pos.y))
        self.update_rect()

    def update_rect(self):
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def draw(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect)
