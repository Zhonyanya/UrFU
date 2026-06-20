class SpatialGrid:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.grid = {}  # словарь {(col, row): [entity1, entity2, ...]}

    def clear(self):
        """Очищает сетку."""
        self.grid.clear()

    def get_cell_coords(self, pos):
        """Возвращает координаты клетки."""
        col = int(pos.x // self.cell_size)
        row = int(pos.y // self.cell_size)
        return (col, row)

    def insert(self, entity):
        """Добавляет сущность в клетку."""
        cell = self.get_cell_coords(entity.pos)
        if cell not in self.grid:
            self.grid[cell] = []
        self.grid[cell].append(entity)

    def query(self, entity):
        return self.query_pos(entity.pos)

    def query_pos(self, pos):
        """Возвращает все сущности в 9 клетках от точки pos."""
        col, row = self.get_cell_coords(pos)
        nearby = []
        for dx in range(col - 1, col + 2):
            for dy in range(row - 1, row + 2):
                cell = (dx, dy)
                if cell in self.grid:
                    nearby.extend(self.grid[cell])
        return nearby
