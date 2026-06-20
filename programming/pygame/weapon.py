import pygame
import math
import random


class Weapon:
    """
    Универсальное оружие.
    is_automatic=True  -> стреляет пока зажата кнопка (миниган).
    is_automatic=False -> один клик = один выстрел (дробовик).
    """
    def __init__(self, fire_rate, projectile_speed, damage, spread,
                 projectiles_per_shot, lifetime, is_automatic, color,
                 muzzle_flash_radius, muzzle_flash_lifetime):
        self.fire_rate = fire_rate
        self.cooldown = 0.0
        self.projectile_speed = projectile_speed
        self.damage = damage
        self.spread = spread
        self.projectiles_per_shot = projectiles_per_shot
        self.lifetime = lifetime
        self.is_automatic = is_automatic
        self.color = color
        self.muzzle_flash_radius = muzzle_flash_radius
        self.muzzle_flash_lifetime = muzzle_flash_lifetime

    def update(self, dt):
        if self.cooldown > 0:
            self.cooldown -= dt

    def try_fire(self, is_held, was_just_pressed, player_pos, player_angle,
                 projectile_manager, events):
        """
        Пытается выстрелить. При успехе генерирует событие в events.
        """
        should_fire = is_held if self.is_automatic else was_just_pressed

        if not should_fire or self.cooldown > 0:
            return False

        self.cooldown = 1.0 / self.fire_rate

        muzzle_offset = 22.0
        muzzle_pos = player_pos + pygame.math.Vector2(
            math.cos(player_angle) * muzzle_offset,
            math.sin(player_angle) * muzzle_offset
        )

        for _ in range(self.projectiles_per_shot):
            angle_offset = random.uniform(-self.spread, self.spread)
            projectile_manager.spawn(
                muzzle_pos,
                player_angle + angle_offset,
                self.projectile_speed,
                self.damage,
                self.lifetime,
                self.color
            )

        events.add_shot(
            pos=muzzle_pos,
            color=self.color,
            radius=self.muzzle_flash_radius,
            lifetime=self.muzzle_flash_lifetime
        )
        return True
