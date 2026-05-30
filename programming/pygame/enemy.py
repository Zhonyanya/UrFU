import pygame
import math
from constants import (MINION_RADIUS, MINION_COLOR,
                       MINION_MAX_SPEED, MINION_ACCELERATION)

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
    """Базовый класс для врагов с steering behaviors (Seek + Separation)."""
    
    def __init__(self, start_pos, radius, color,
                 max_speed, acceleration, separation_distance=60.0,
                 max_force=5000.0):
        self.pos = pygame.math.Vector2(start_pos)
        self.vel = pygame.math.Vector2(0, 0)
        self.radius = radius
        self.color = color
        self.max_speed = max_speed
        self.slow_speed = self.max_speed / 2
        self.acceleration = acceleration
        self.max_force = max_force
        self.separation_distance = separation_distance

    def seek(self, target):
        """Steering behavior: движение к цели."""
        desired = target - self.pos
        if desired.length() > 0:
            desired = desired.normalize() * self.max_speed
        steer = desired - self.vel
        steer = self._clamp_magnitude(steer, self.max_force)
        return steer

    def separation(self, enemies, spatial_grid=None):
        """Steering behavior: отталкивание от других врагов."""
        steer = pygame.math.Vector2(0, 0)
        total = 0

        if spatial_grid:
            nearby = spatial_grid.get_nearby(self)
            for other in nearby:
                if other is self:
                    continue
                diff = self.pos - other.pos
                dist = diff.length()
                if 0 < dist < self.separation_distance:
                    diff = diff.normalize() / dist
                    steer += diff
                    total += 1
        else:
            # Fallback: полная проверка O(N)
            for other in enemies:
                if other is self:
                    continue
                diff = self.pos - other.pos
                dist = diff.length()
                if 0 < dist < self.separation_distance:
                    diff = diff.normalize() / dist
                    steer += diff
                    total += 1

        if total > 0:
            steer = steer / total
            if steer.length() > 0:
                steer = steer.normalize() * self.max_speed
            steer -= self.vel
            steer = self._clamp_magnitude(steer, self.max_force)

        return steer

    def _clamp_magnitude(self, vector, max_mag):
        """Ограничивает длину вектора."""
        if vector.length() > max_mag:
            vector = vector.normalize() * max_mag
        return vector

    def update(self, dt, player_pos, enemies=None, spatial_grid=None):
        """Обновление позиции с применением steering behaviors."""
        seek_force = self.seek(player_pos)

        separation_force = pygame.math.Vector2(0, 0)
        if enemies is not None:
            separation_force = self.separation(enemies, spatial_grid)

        steering = seek_force * 1.0 + separation_force * 1.5

        steering = self._clamp_magnitude(steering, self.max_force)
        self.vel += steering * dt

        if self.vel.length() > self.max_speed:
            self.vel = self.vel.normalize() * self.max_speed

        self.pos += self.vel * dt

    def resolve_collision(self, player):
        """Разрешение коллизии с игроком (OBB + Circle)."""
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
            player.rect.center = (round(player.pos.x), round(player.pos.y))

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.pos.x),
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
            separation_distance=70.0,
            max_force=3000.0
        )


def resolve_enemy_collisions(enemies):
    """
    Упрощённая функция для финальной коррекции позиций.
    Теперь основная работа делается через separation steering,
    эта функция только предотвращает полное перекрытие.
    """
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
