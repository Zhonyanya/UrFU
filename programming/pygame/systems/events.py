class GameEvents:
    """Менеджер событий игры."""
    def __init__(self):
        self.shots_fired = []
        self.damage_flash_lifetime = 0.0
        self.damage_flash_max_lifetime = 0.0

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

    def trigger_damage_flash(self, duration):
        """Активирует красную вспышку на всю карту."""
        self.damage_flash_lifetime = duration
        self.damage_flash_max_lifetime = duration

    def update(self, dt):
        """Обновляет время жизни вспышек."""
        for shot in self.shots_fired:
            shot['lifetime'] -= dt
        self.shots_fired = [s for s in self.shots_fired if s['lifetime'] > 0]
        if self.damage_flash_lifetime > 0.0:
            self.damage_flash_lifetime = max(0.0,
                                             self.damage_flash_lifetime - dt)

    def clear(self):
        """Очищает все события."""
        self.shots_fired.clear()
        self.damage_flash_lifetime = 0.0
        self.damage_flash_max_lifetime = 0.0
