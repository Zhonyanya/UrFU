import pygame
import math
from config.constants import (MINION_RADIUS, MINION_COLOR,
                       MINION_MAX_SPEED, MINION_ACCELERATION)
from systems.collision_system import _get_closest_point_on_obb

class ChaserEnemy:
    """Базовый класс для врагов с steering behaviors (Seek + Separation)."""

    def __init__(self, start_pos, radius, color,
                 max_speed, acceleration, separation_distance=50.0,
                 max_force=5000.0, max_hp=30):
        self.pos = pygame.math.Vector2(start_pos)
        self.vel = pygame.math.Vector2(0, 0)
        self.radius = radius
        self.color = color
        self.max_speed = max_speed
        self.slow_speed = self.max_speed / 2
        self.acceleration = acceleration
        self.max_force = max_force
        self.separation_distance = separation_distance
        self.max_hp = max_hp
        self.hp = max_hp
        self.alive = True

    def take_damage(self, amount):
        if not self.alive:
            return
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False

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
            nearby = spatial_grid.query(self)
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

        steering = seek_force * 1.0 + separation_force * 0.8

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


class Minion(ChaserEnemy):
    def __init__(self, start_pos):
        super().__init__(
            start_pos=start_pos,
            radius=MINION_RADIUS,
            color=MINION_COLOR,
            max_speed=MINION_MAX_SPEED,
            acceleration=MINION_ACCELERATION,
            separation_distance=50.0,
            max_force=3000.0,
            max_hp=30
        )
