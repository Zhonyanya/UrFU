import pygame
import math
from constants import PROJECTILE_POOL_SIZE, PROJECTILE_RADIUS


class Projectile:
    """Класс снаряда."""
    # есть только эти атрибуты, новые добавить не можем. Оч экономит оперативку и фепесы
    __slots__ = ('pos', 'vel', 'radius', 'damage',
                 'lifetime', 'active', 'color')

    def __init__(self):
        self.pos = pygame.math.Vector2()
        self.vel = pygame.math.Vector2()
        self.radius = PROJECTILE_RADIUS
        self.damage = 0
        self.lifetime = 0.0
        self.active = False
        self.color = (255, 255, 255)

    def spawn(self, pos, angle, speed, damage, lifetime, color):
        """Включает снаряд."""
        self.pos.update(pos)
        self.vel = pygame.math.Vector2(math.cos(angle),
                                       math.sin(angle)) * speed
        self.damage = damage
        self.lifetime = lifetime
        self.active = True
        self.color = color

    def update(self, dt):
        """Обновляет позицию и время жизни снаряда.
        Отключает снаряд."""
        if not self.active:
            return
        self.pos += self.vel * dt
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.active = False


class ProjectileManager:
    """Object pool."""
    def __init__(self, pool_size=PROJECTILE_POOL_SIZE):
        self.pool = [Projectile() for _ in range(pool_size)]
        self.active_count = 0

    def spawn(self, pos, angle, speed, damage, lifetime, color):
        """Спавнит снаряды."""
        for proj in self.pool:
            if not proj.active:
                proj.spawn(pos, angle, speed, damage, lifetime, color)
                self.active_count += 1
                return proj
        return None

    def update(self, dt):
        """Обновляет количество снарядов и сами снаряды."""
        self.active_count = 0
        for proj in self.pool:
            if proj.active:
                proj.update(dt)
                if proj.active:
                    self.active_count += 1

    def draw(self, surface):
        for proj in self.pool:
            if proj.active:
                pygame.draw.circle(surface, proj.color,
                                   (int(proj.pos.x), int(proj.pos.y)),
                                   proj.radius)
                pygame.draw.circle(surface, (255, 255, 200),
                                   (int(proj.pos.x), int(proj.pos.y)),
                                   max(1, proj.radius - 2))

    def iter_active(self):
        for proj in self.pool:
            if proj.active:
                # эффективнее чем постоянно возвращать список всех проджектайлов
                # возвращаем по одному
                yield proj
