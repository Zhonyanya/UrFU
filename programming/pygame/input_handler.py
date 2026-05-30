import pygame


class InputHandler:
    def __init__(self):
        self.quit_requested = False
        self.keys = None
        self.mouse_pos = (0, 0)

    def update(self):
        """Считывает сырые события и состояния кнопок за кадр."""
        self.keys = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_requested = True

    def get_movement_vector(self):
        """Возвращает нормализованный вектор движения на основе WASD."""
        vec = pygame.math.Vector2(0, 0)
        if self.keys[pygame.K_w]:
            vec.y -= 1
        if self.keys[pygame.K_s]:
            vec.y += 1
        if self.keys[pygame.K_a]:
            vec.x -= 1
        if self.keys[pygame.K_d]:
            vec.x += 1

        if vec.length() > 0:
            vec.normalize_ip()
        return vec
