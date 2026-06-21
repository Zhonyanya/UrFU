class GameEvents:
    """Менеджер событий игры."""
    def __init__(self):
        self.shots_fired = []

    def add_shot(self, pos, color, radius, lifetime, is_global=False):
        """Weapon вызывает это при выстреле."""
        self.shots_fired.append({
            'pos': pos,
            'color': color,
            'radius': radius,
            'lifetime': lifetime,
            'max_lifetime': lifetime,
            'is_global': is_global
        })

    def update(self, dt):
        """Обновляет время жизни вспышек."""
        for shot in self.shots_fired:
            shot['lifetime'] -= dt

        # Удаляем потухшие вспышки
        self.shots_fired = [s for s in self.shots_fired if s['lifetime'] > 0]

    def clear(self):
        """Очищает все события."""
        self.shots_fired.clear()
