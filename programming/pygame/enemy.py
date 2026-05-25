# enemy.py
import pygame
import heapq
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_SIZE, ENEMY_COLOR,
                       ENEMY_MAX_SPEED, ENEMY_ACCELERATION, PATHFINDING_CELL_SIZE)

class Enemy:
    def __init__(self, start_pos):
        self.pos = pygame.math.Vector2(start_pos)
        self.vel = pygame.math.Vector2(0, 0)
        self.radius = ENEMY_SIZE / 2
        
        self.path = []
        self.path_timer = 0
        self.path_update_interval = 0.2  # Пересчитываем путь каждые 0.2 сек для баланса производительности

        self.grid_w = SCREEN_WIDTH // PATHFINDING_CELL_SIZE
        self.grid_h = SCREEN_HEIGHT // PATHFINDING_CELL_SIZE

    def update(self, dt, player_pos):
        # 1. Обновление пути
        self.path_timer += dt
        if self.path_timer >= self.path_update_interval or not self.path:
            self.path = self._calculate_astar(player_pos)
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

        target_vel = target_dir * ENEMY_MAX_SPEED
        vel_diff = target_vel - self.vel
        max_change = ENEMY_ACCELERATION * dt

        if vel_diff.length() > 0:
            if vel_diff.length() > max_change:
                vel_diff.normalize_ip()
                vel_diff *= max_change
            self.vel += vel_diff

        self.pos += self.vel * dt

    def _calculate_astar(self, goal_pos):
        # координаты в индексы сетки
        start_node = (int(self.pos.x // PATHFINDING_CELL_SIZE),
                      int(self.pos.y // PATHFINDING_CELL_SIZE))
        goal_node = (int(goal_pos[0] // PATHFINDING_CELL_SIZE),
                     int(goal_pos[1] // PATHFINDING_CELL_SIZE))

        # Ограничиваем цель границами сетки
        goal_node = (max(0, min(self.grid_w - 1, goal_node[0])),
                     max(0, min(self.grid_h - 1, goal_node[1])))

        if start_node == goal_node:
            return [goal_pos]

        open_set = [(0, start_node)]  # приоритетная очередь: (f_score, ячейка)
        came_from = {}  # словарь: (ячейка -> откуда пришли) -  нужно для восстановления пути в конце
        g_score = {start_node: 0}  # реальная стоимость от старта до ячейки
        f_score = {start_node: self._heuristic(start_node, goal_node)}  # g + h

        while open_set:
            _, current = heapq.heappop(open_set) # достаём клетку с наименьшим f
            if current == goal_node:
                break  # путь найден

            # перебор соседей
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    neighbor = (current[0] + dx, current[1] + dy)
                    if not (0 <= neighbor[0] < self.grid_w and 0 <= neighbor[1] < self.grid_h):
                        continue

                    # расчёт стоимости перехода
                    if (dx != 0 and dy != 0):
                        move_cost = 1.414  # корень из двух
                    else:
                        move_cost = 1.0
                    tentative_g = g_score[current] + move_cost  # предполагаемая стоимость
                    # нашли ли путь лучше??
                    if tentative_g < g_score.get(neighbor, float('inf')):
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g
                        f_score[neighbor] = tentative_g + self._heuristic(neighbor, goal_node)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        # восстановление пути
        path = []
        curr = goal_node
        while curr in came_from:
            path.append((curr[0] * PATHFINDING_CELL_SIZE + PATHFINDING_CELL_SIZE / 2,
                         curr[1] * PATHFINDING_CELL_SIZE + PATHFINDING_CELL_SIZE / 2))
            curr = came_from[curr]
        path.reverse()
        path.append(tuple(goal_pos))  # финишная точка - позиция игрока
        return path

    def _heuristic(self, a, b):
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

    def draw(self, surface):
        pygame.draw.circle(surface, ENEMY_COLOR, (int(self.pos.x),
                           int(self.pos.y)), self.radius)
