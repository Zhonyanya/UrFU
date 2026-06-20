class GameEvents:
    """Менеджер событий игры."""
    def __init__(self):
        self.shots_fired = []  # [(pos, color, radius, lifetime), ...]

    def add_shot(self, pos, color, radius, lifetime):
        """Weapon вызывает это прив ыстреле."""
        self.shots_fired.append({
            'pos': pos,
            'color': color,
            'radius': radius,
            'lifetime': lifetime
        })

    def clear(self):
        """Очищает все события."""
        self.shots_fired.clear()
