import pygame
from constants import (PATHFINDING_CELL_SIZE, MINION_RADIUS, MINION_COLOR,
                       MINION_MAX_SPEED, MINION_ACCELERATION)
from pathfinder import Pathfinder

class ChaserEnemy:
    """Базовый класс для врагов с A* пасфайндингом."""
    def __init__(self, start_pos, radius, color,
                 max_speed, acceleration, path_update_interval=0.2):
        self.pos = pygame.math.Vector2(start_pos)
        self.vel = pygame.math.Vector2(0, 0)

        self.radius = radius
        self.color = color
        self.max_speed = max_speed
        self.slow_speed = self.max_speed / 2
        self.acceleration = acceleration
        self.path_update_interval = path_update_interval  # Пересчитываем путь каждые 0.2 сек для баланса производительности

        self.path = []
        self.path_timer = 0

    def update(self, dt, player_pos):
        # 1. Обновление пути
        self.path_timer += dt
        if self.path_timer >= self.path_update_interval or not self.path:
            self.path = Pathfinder.find_path(self.pos, player_pos)
            self.path_timer = 0

        # 2. Определение целевого направления
        target_dir = pygame.math.Vector2(0, 0)
        if self.path:
            target = pygame.math.Vector2(self.path[0])
            to_target = target - self.pos

            # Если до текущей вейпоинта осталось меньше половины клетки, переходим к следующей
            if to_target.length() < PATHFINDING_CELL_SIZE * 0.5:
                self.path.pop(0)
                target = pygame.math.Vector2(self.path[0] if self.path else player_pos)
                to_target = target - self.pos

            if to_target.length() > 0:
                target_dir = to_target.normalize()

        target_vel = target_dir * self.max_speed
        vel_diff = target_vel - self.vel
        max_change = self.acceleration * dt

        if vel_diff.length() > 0:
            if vel_diff.length() > max_change:
                vel_diff.normalize_ip()
                vel_diff *= max_change
            self.vel += vel_diff

        self.pos += self.vel * dt

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.pos.x),
                           int(self.pos.y)), self.radius)


class Minion(ChaserEnemy):
    def __init__(self, start_pos):
        super().__init__(
            start_pos=start_pos,
            radius=MINION_RADIUS,
            color=MINION_COLOR,
            max_speed=MINION_MAX_SPEED,
            acceleration=MINION_ACCELERATION,
            path_update_interval=0.2
        )
