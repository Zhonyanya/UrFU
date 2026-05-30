import heapq
from constants import (PATHFINDING_CELL_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH)


class Pathfinder:
    """Пасфайндер через алгоритм А*"""

    @staticmethod
    def find_path(start_pos, goal_pos):
        """Считает путь через А*"""
        # координаты в индексы сетки
        cell_size = PATHFINDING_CELL_SIZE
        grid_w = SCREEN_WIDTH // cell_size
        grid_h = SCREEN_HEIGHT // cell_size

        start = (int(start_pos.x // cell_size), int(start_pos.y // cell_size))
        goal = (int(goal_pos[0] // cell_size), int(goal_pos[1] // cell_size))

        # Ограничиваем цель границами сетки
        goal = (max(0, min(grid_w - 1, goal[0])), max(0, min(grid_h - 1, goal[1]))) 
        if start == goal:
            return [goal_pos]

        open_set = [(0, start)]  # приоритетная очередь: (f_score, ячейка)
        came_from = {}  # словарь: (ячейка -> откуда пришли) -  нужно для восстановления пути в конце
        g_score = {start: 0}  # реальная стоимость от старта до ячейки
        f_score = {start: Pathfinder._heuristic(start, goal)}  # g + h

        while open_set:
            f, current = heapq.heappop(open_set) # достаём клетку с наименьшим f
            if g_score.get(current, float('inf')) < f:
                continue
            if current == goal:
                break

            # перебор соседей
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    neighbor = (current[0] + dx, current[1] + dy)
                    if not (0 <= neighbor[0] < grid_w and 0 <= neighbor[1] < grid_h):
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
                        f_score[neighbor] = tentative_g + Pathfinder._heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        # восстановление пути
        path = []
        curr = goal
        while curr in came_from:
            path.append((curr[0] * cell_size + cell_size / 2,
                         curr[1] * cell_size + cell_size / 2))
            curr = came_from[curr]
        path.reverse()
        path.append(tuple(goal_pos))  # финишная точка - позиция игрока
        return path

    @staticmethod
    def _heuristic(a, b):
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

import heapq
from constants import (PATHFINDING_CELL_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH)


class Pathfinder:
    """Пасфайндер через алгоритм А*"""

    @staticmethod
    def find_path(start_pos, goal_pos):
        """Считает путь через А*"""
        # координаты в индексы сетки
        cell_size = PATHFINDING_CELL_SIZE
        grid_w = SCREEN_WIDTH // cell_size
        grid_h = SCREEN_HEIGHT // cell_size

        start = (int(start_pos.x // cell_size), int(start_pos.y // cell_size))
        goal = (int(goal_pos[0] // cell_size), int(goal_pos[1] // cell_size))

        # Ограничиваем цель границами сетки
        goal = (max(0, min(grid_w - 1, goal[0])), max(0, min(grid_h - 1, goal[1]))) 
        if start == goal:
            return [goal_pos]

        open_set = [(0, start)]  # приоритетная очередь: (f_score, ячейка)
        came_from = {}  # словарь: (ячейка -> откуда пришли) -  нужно для восстановления пути в конце
        g_score = {start: 0}  # реальная стоимость от старта до ячейки
        f_score = {start: Pathfinder._heuristic(start, goal)}  # g + h

        while open_set:
            f, current = heapq.heappop(open_set) # достаём клетку с наименьшим f
            if g_score.get(current, float('inf')) < f:
                continue
            if current == goal:
                break

            # перебор соседей
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    neighbor = (current[0] + dx, current[1] + dy)
                    if not (0 <= neighbor[0] < grid_w and 0 <= neighbor[1] < grid_h):
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
                        f_score[neighbor] = tentative_g + Pathfinder._heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        # восстановление пути
        path = []
        curr = goal
        while curr in came_from:
            path.append((curr[0] * cell_size + cell_size / 2,
                         curr[1] * cell_size + cell_size / 2))
            curr = came_from[curr]
        path.reverse()
        path.append(tuple(goal_pos))  # финишная точка - позиция игрока
        return path

    @staticmethod
    def _heuristic(a, b):
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
