import pygame, math
from constants import (PATHFINDING_CELL_SIZE, MINION_RADIUS, MINION_COLOR,
                       MINION_MAX_SPEED, MINION_ACCELERATION)
from pathfinder import Pathfinder

def _get_closest_point_on_obb(center, half_w, half_h, angle, point):
    """Находит ближайшую точку повёрнутого прямоугольника к заданной точке."""
    diff = point - center
    # 1. Переводим точку в локальные координаты прямоугольника
    cos_a = math.cos(-angle)
    sin_a = math.sin(-angle)
    lx = diff.x * cos_a - diff.y * sin_a
    ly = diff.x * sin_a + diff.y * cos_a

    # 2. Ограничиваем (clamp) границами прямоугольника
    lx = max(-half_w, min(half_w, lx))
    ly = max(-half_h, min(half_h, ly))

    # 3. Возвращаем в мировые координаты
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    wx = center.x + lx * cos_a - ly * sin_a
    wy = center.y + lx * sin_a + ly * cos_a
    return pygame.math.Vector2(wx, wy)


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

    def resolve_collision(self, player):
        closest = _get_closest_point_on_obb(
            player.pos, player.half_size, player.half_size, player.angle, self.pos
        )
        dist_vec = self.pos - closest
        dist = dist_vec.length()

        if dist < self.radius:
            if dist > 0:
                overlap = self.radius - dist
                push_dir = dist_vec.normalize()
                # Выталкиваем игрока ВНЕ сферы врага
                player.pos -= push_dir * overlap
            else:
                # Крайний случай: центры совпали, толкаем по нормали к грани
                push_dir = pygame.math.Vector2(-math.cos(player.angle),
                                               -math.sin(player.angle))
                player.pos += push_dir * self.radius
            # Синхронизируем rect после физического сдвига
            player.rect.center = (round(player.pos.x), round(player.pos.y))

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


def resolve_enemy_collisions(enemies):
    for i in range(len(enemies)):
        for j in range(i + 1, len(enemies)):
            e1, e2 = enemies[i], enemies[j]
            diff = e1.pos - e2.pos
            dist = diff.length()
            min_dist = e1.radius + e2.radius
            if 0 < dist < min_dist:
                overlap = min_dist - dist
                push = diff.normalize() * (overlap / 2)
                e1.pos += push
                e2.pos -= push
