import pygame


class FPSCounter:
    """
    Счётчик FPS с circular buffer и визуализацией графика.
    Используется для отладки производительности.
    """
    def __init__(self, size: int = 120):
        self.size = size
        self.frame_times: list[float] = [0.0] * size  # circular buffer
        self.index: int = 0

    def update(self, delta_time: float) -> None:
        """Записывает время кадра в буфер."""
        self.frame_times[self.index] = delta_time
        self.index = (self.index + 1) % self.size

    def get_fps(self) -> float:
        """Средний FPS за последние `size` кадров."""
        avg = sum(self.frame_times) / self.size
        return 1.0 / avg if avg > 0 else 0.0

    def get_avg_ms(self) -> float:
        """Среднее время кадра в миллисекундах."""
        return sum(self.frame_times) / self.size * 1000

    def draw_graph(self, screen: pygame.Surface, x: int, y: int,
                   width: int, height: int) -> None:
        """Рисует график времени кадра и текст с FPS/MS."""
        bar_width = width / self.size
        target_ms = 16.67  # 60 FPS target

        # Рисуем бары
        for i in range(self.size):
            idx = (self.index + i) % self.size
            ms = self.frame_times[idx] * 1000
            bar_height = min(ms / target_ms * (height / 2), height)
            color = (0, 255, 0) if ms < target_ms else (255, 0, 0)
            bx = int(x + i * bar_width)
            pygame.draw.rect(
                screen, color,
                (bx, int(y + height - bar_height),
                 max(int(bar_width), 1), int(bar_height))
            )

        # Линия цели 60 FPS (16.67 ms)
        line_y = int(y + height / 2)
        pygame.draw.line(screen, (255, 255, 0), (x, line_y), (x + width, line_y), 1)

        # Текст с текущими значениями
        font = pygame.font.SysFont("consolas", 14)
        fps_text = font.render(f"FPS: {self.get_fps():.1f}", True, (255, 255, 255))
        ms_text = font.render(f"MS:  {self.get_avg_ms():.2f}", True, (255, 255, 255))
        screen.blit(fps_text, (x, y - 32))
        screen.blit(ms_text, (x, y - 16))
