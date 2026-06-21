import random
from typing import List, Callable, Tuple, TypeVar
import pygame

# Тип для врага (любой объект с атрибутом pos)
EnemyType = TypeVar('EnemyType')


class WaveSpawner:
    """
    Система волн: периодически спавнит врагов по периметру арены.
    С течением времени количество врагов в волне растёт.
    """

    def __init__(
        self,
        arena_rect: pygame.Rect,
        spawn_factory: Callable[[Tuple[float, float]], EnemyType],
        initial_interval: float = 4.0,
        min_interval: float = 2.0,
        interval_decay: float = 0.15,
        base_count: int = 3,
        count_growth: int = 2,
        max_count: int = 40,
        spawn_margin: float = 20.0,
    ) -> None:
        """
        :param arena_rect: прямоугольник арены (используется как граница спавна).
        :param spawn_factory: фабрика, создающая врага по позиции (x, y).
                              Это может быть класс (например, Minion) или функция.
        :param initial_interval: интервал между волнами в начале игры (сек).
        :param min_interval: минимальный интервал между волнами.
        :param interval_decay: насколько быстрее становятся волны с каждой новой.
        :param base_count: базовое количество врагов в первой волне.
        :param count_growth: прирост врагов с каждой волной.
        :param max_count: потолок по количеству врагов в волне.
        :param spawn_margin: отступ наружу от границы арены.
        """
        self.arena_rect = arena_rect
        self.spawn_factory = spawn_factory

        self.current_interval = initial_interval
        self.min_interval = min_interval
        self.interval_decay = interval_decay

        self.base_count = base_count
        self.count_growth = count_growth
        self.max_count = max_count
        self.spawn_margin = spawn_margin

        self.time_to_next_wave = initial_interval
        self.wave_number = 0
        self.total_spawned = 0

    def update(self, dt: float, enemies: List[EnemyType]) -> List[EnemyType]:
        """
        Обновляет таймер и, при необходимости, спавнит новую волну.
        Возвращает список только что созданных врагов (для удобства отладки/UI).
        """
        self.time_to_next_wave -= dt
        if self.time_to_next_wave > 0:
            return []

        spawned = self._spawn_wave(enemies)

        # Готовим следующую волну
        self.wave_number += 1
        self.current_interval = max(
            self.min_interval,
            self.current_interval - self.interval_decay,
        )
        self.time_to_next_wave = self.current_interval

        return spawned

    def get_time_to_next_wave(self) -> float:
        """Сколько секунд осталось до следующей волны."""
        return max(0.0, self.time_to_next_wave)

    def get_wave_number(self) -> int:
        """Номер последней завершённой волны (сколько волн уже прошло)."""
        return self.wave_number

    def _spawn_wave(self, enemies: List[EnemyType]) -> List[EnemyType]:
        """Спавнит врагов для текущей волны."""
        count = min(self.max_count, self.base_count + self.wave_number * self.count_growth)
        spawned: List[EnemyType] = []

        for _ in range(count):
            pos = self._random_edge_position()
            # Вызываем фабрику (класс или функцию) с позицией
            enemy = self.spawn_factory(pos)
            enemies.append(enemy)
            spawned.append(enemy)
            self.total_spawned += 1

        return spawned

    def _random_edge_position(self) -> Tuple[float, float]:
        """
        Случайная точка по периметру арены, с небольшим отступом наружу,
        чтобы враги не появлялись прямо на игроке.
        """
        r = self.arena_rect
        margin = self.spawn_margin

        # Выбираем одну из 4 сторон
        side = random.randint(0, 3)

        if side == 0:  # верх
            x = random.uniform(r.left, r.right)
            y = r.top - margin
        elif side == 1:  # низ
            x = random.uniform(r.left, r.right)
            y = r.bottom + margin
        elif side == 2:  # лево
            x = r.left - margin
            y = random.uniform(r.top, r.bottom)
        else:  # право
            x = r.right + margin
            y = random.uniform(r.top, r.bottom)

        return x, y
