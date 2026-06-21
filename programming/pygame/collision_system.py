from typing import List


def check_projectile_enemy_collisions(projectile_manager, enemies,
                                      spatial_grid) -> int:
    """
    Проверяет коллизии между активными снарядами и врагами.
    Возвращает количество попаданий (для статистики/звуков).
    """
    hits = 0

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
                enemy.take_damage(proj.damage)
                proj.active = False
                hits += 1
                break  # Пуля попала, проверяем следующую

    return hits


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
