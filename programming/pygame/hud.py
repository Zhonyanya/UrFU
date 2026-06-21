import pygame
from constants import (HUD_COLOR, HUD_HEART_COLOR, HUD_HEART_SIZE,
                       HUD_FONT_SIZE, HUD_PADDING)


class HUD:
    """Минималистичный HUD: сердечко + HP в формате 'текущее/макс'."""

    def __init__(self) -> None:
        self.font = pygame.font.Font(None, HUD_FONT_SIZE)
        self.heart_size = HUD_HEART_SIZE
        self.padding = HUD_PADDING
        # Пре-рендерим сердечко на отдельную поверхность (с альфой)
        self.heart_surface = self._render_heart(self.heart_size,
                                                HUD_HEART_COLOR)

    @staticmethod
    def _render_heart(size: int, color: tuple[int, int, int]) -> pygame.Surface:
        """Рисует сердечко: два круга сверху + треугольник снизу."""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        r = size // 4
        cy = r  # центр кругов по Y
        # Два круга сверху
        pygame.draw.circle(surface, color, (r, cy), r)
        pygame.draw.circle(surface, color, (3 * r, cy), r)
        # Заполнение между кругами
        pygame.draw.rect(surface, color, (r, 0, 2 * r, r))
        # Треугольник снизу
        pygame.draw.polygon(surface, color, [
            (0, cy),
            (4 * r, cy),
            (2 * r, 3 * r)
        ])
        return surface

    def draw(self, surface: pygame.Surface, hp: int, max_hp: int) -> None:
        x = self.padding
        y = self.padding
        surface.blit(self.heart_surface, (x, y))

        # Цвет текста зависит от процента HP
        ratio = hp / max_hp if max_hp > 0 else 0
        if ratio > 0.5:
            text_color = HUD_COLOR
        elif ratio > 0.25:
            text_color = (255, 200, 80)
        else:
            text_color = (255, 90, 90)

        text = self.font.render(f"{hp}/{max_hp}", True, text_color)
        text_x = x + self.heart_size + 10
        text_y = y + (self.heart_size - text.get_height()) // 2
        surface.blit(text, (text_x, text_y))
