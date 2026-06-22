import pygame
from config.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class GameOverScreen:
    """Экран окончания игры со статистикой и кнопкой рестарта."""

    def __init__(self) -> None:
        self.font_big = pygame.font.Font(None, 80)
        self.font = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 28)

        btn_w, btn_h = 280, 64
        self.restart_button_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - btn_w // 2,
            SCREEN_HEIGHT // 2 + 110,
            btn_w, btn_h
        )
        self._button_color = (70, 70, 90)
        self._button_hover_color = (100, 100, 130)
        self._border_color = (160, 160, 190)

        self._title_text = self.font_big.render("GAME OVER", True, (220, 60, 70))
        self._restart_label = self.font.render("НАЧАТЬ ЗАНОВО", True, (255, 255, 255))
        self._hint_text = self.font_small.render(
            "или нажмите R", True, (170, 170, 190)
        )

    def draw(self, surface: pygame.Surface, stats: dict,
             mouse_pos: tuple[int, int]) -> None:
        # Полупрозрачное затемнение
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # Заголовок
        title_rect = self._title_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120)
        )
        surface.blit(self._title_text, title_rect)

        # Статистика
        kills_text = self.font.render(
            f"Убито врагов: {stats.get('kills', 0)}", True, (240, 240, 240)
        )
        waves_text = self.font.render(
            f"Пройдено волн: {stats.get('waves', 0)}", True, (240, 240, 240)
        )
        surface.blit(kills_text, kills_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)))
        surface.blit(waves_text, waves_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)))

        # Кнопка (с ховером)
        btn_color = (self._button_hover_color
                     if self.restart_button_rect.collidepoint(mouse_pos)
                     else self._button_color)
        pygame.draw.rect(surface, btn_color, self.restart_button_rect,
                         border_radius=10)
        pygame.draw.rect(surface, self._border_color, self.restart_button_rect,
                         2, border_radius=10)
        label_rect = self._restart_label.get_rect(
            center=self.restart_button_rect.center)
        surface.blit(self._restart_label, label_rect)

        # Подсказка
        hint_rect = self._hint_text.get_rect(
            center=(SCREEN_WIDTH // 2, self.restart_button_rect.bottom + 25))
        surface.blit(self._hint_text, hint_rect)

    def is_restart_clicked(self, mouse_pos: tuple[int, int],
                           left_just_pressed: bool) -> bool:
        return (left_just_pressed and
                self.restart_button_rect.collidepoint(mouse_pos))
