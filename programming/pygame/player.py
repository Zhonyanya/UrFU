# player.py
import pygame
import math
from constants import (PLAYER_SIZE, PLAYER_COLOR, PLAYER_START_POS,
                       PLAYER_MAX_SPEED, PLAYER_ACCELERATION, PLAYER_DECELERATION)

class Player:
    def __init__(self):
        self.pos = pygame.math.Vector2(PLAYER_START_POS)
        self.vel = pygame.math.Vector2(0, 0)
        self.size = PLAYER_SIZE
        self.half_size = self.size / 2
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.rect.center = self.pos
        self.angle = 0.0  # Угол в радианах

        # Пре-рендерим базовый спрайт
        self.base_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        # Тело игрока
        pygame.draw.rect(self.base_surface, PLAYER_COLOR, (0, 0, self.size, self.size))
        # "Лицо" (для наглядности направления)
        half = self.half_size
        pygame.draw.rect(self.base_surface, (0, 255, 0), (half + 2, half - 5, 8, 4))
        pygame.draw.rect(self.base_surface, (0, 255, 0), (half + 2, half + 2, 8, 4))

    def update(self, dt, input_vector, arena_rect, mouse_pos):
        # Движение
        target_vel = input_vector * PLAYER_MAX_SPEED
        vel_diff = target_vel - self.vel
        accel_rate = PLAYER_ACCELERATION if input_vector.length() > 0 else PLAYER_DECELERATION
        max_change = accel_rate * dt
        if vel_diff.length() > 0 and vel_diff.length() > max_change:
            vel_diff.normalize_ip()
            vel_diff *= max_change
        self.vel += vel_diff
        self.pos += self.vel * dt

        # Ограничение границами арены (по центру)
        self.pos.x = max(arena_rect.left + self.half_size, min(arena_rect.right - self.half_size, self.pos.x))
        self.pos.y = max(arena_rect.top + self.half_size, min(arena_rect.bottom - self.half_size, self.pos.y))
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        # Вращение за мышью
        dx = mouse_pos[0] - self.pos.x
        dy = mouse_pos[1] - self.pos.y
        self.angle = math.atan2(dy, dx)

    def draw(self, surface):
        # Поворачиваем ВЕСЬ квадрат
        # -math.degrees учитывает разницу между математическими углами и Y-down в Pygame
        rotated = pygame.transform.rotate(self.base_surface, -math.degrees(self.angle))
        rect = rotated.get_rect(center=(self.pos.x, self.pos.y))
        surface.blit(rotated, rect.topleft)