from typing import List
import pygame
import math
from config.constants import PLAYER_DAMAGE_PER_HIT, DAMAGE_FLASH_DURATION


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


def check_projectile_enemy_collisions(projectile_manager, enemies,
                                      spatial_grid) -> int:
    """
    Проверяет коллизии между активными снарядами и врагами.
    Возвращает количество попаданий (для статистики/звуков).
    """
    hits = 0
    kills = 0
    for proj in projectile_manager.iter_active():
        nearby = spatial_grid.query_pos(proj.pos)

        for enemy in nearby:
            if not enemy.alive:
                continue

            # Circle vs Circle collision
            dx = proj.pos.x - enemy.pos.x
            dy = proj.pos.y - enemy.pos.y
            min_dist = proj.radius + enemy.radius

            if dx * dx + dy * dy < min_dist * min_dist:
                was_alive = enemy.alive
                enemy.take_damage(proj.damage)
                proj.active = False
                hits += 1
                if was_alive and not enemy.alive:
                    kills += 1
                break  # Пуля попала, проверяем следующую
    return hits, kills


def check_player_damage(enemies, player, events):
    """Проверяет, получил ли игрок урон.
    При попадании снимает хп и запускает красную вспышку"""
    if player.is_invulnerable or player.is_dead:
        return 0
    for enemy in enemies:
        if not enemy.alive:
            continue
        closest = _get_closest_point_on_obb(
            player.pos, player.half_size, player.half_size,
            player.angle, enemy.pos
        )
        dist_vec = enemy.pos - closest
        dist = dist_vec.length()
        if dist < enemy.radius:
            if player.take_damage(PLAYER_DAMAGE_PER_HIT):
                events.trigger_damage_flash(DAMAGE_FLASH_DURATION)
                return 1
    return 0


def resolve_enemy_player_collisions(enemies: List, player) -> None:
    """Разрешает коллизии всех врагов с игроком."""
    for enemy in enemies:
        if enemy.alive:
            enemy.resolve_collision(player)


def resolve_enemy_enemy_collisions(enemies: List, spatial_grid) -> None:
    """Разрешает коллизии между врагами."""
    checked_pairs = set()

    for enemy in enemies:
        if not enemy.alive:
            continue

        nearby = spatial_grid.query(enemy)

        for other in nearby:
            if other is enemy or not other.alive:
                continue

            # Уникальный ID пары, чтобы не проверять e1-e2 и e2-e1 дважды
            pair_id = tuple(sorted((id(enemy), id(other))))

            if pair_id in checked_pairs:
                continue

            checked_pairs.add(pair_id)
            _resolve_collision_pair(enemy, other)


def _resolve_collision_pair(e1, e2) -> None:
    """Внутренняя функция: разрешает коллизию двух кругов."""
    diff = e1.pos - e2.pos
    dist = diff.length()
    min_dist = e1.radius + e2.radius

    if 0 < dist < min_dist:
        overlap = min_dist - dist
        push = diff.normalize() * (overlap / 2)
        e1.pos += push
        e2.pos -= push
