import pygame


class InputHandler:
    def __init__(self):
        self.quit_requested = False
        self.keys = None
        self.mouse_pos = (0, 0)
        self.mouse_buttons = (False, False, False)  # лкм скм пкм
        self._prev_mouse_buttons = (False, False, False)
        self.spawn_enemy_requested = False

    def update(self):
        """Считывает сырые события и состояния кнопок за кадр."""
        self.keys = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self._prev_mouse_buttons = self.mouse_buttons
        self.mouse_buttons = pygame.mouse.get_pressed()
        self.spawn_enemy_requested = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_requested = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                self.spawn_enemy_requested = True

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

    def is_mouse_held(self, button):
        """Зажата ли кнопка мыши сейчас."""
        return self.mouse_buttons[button]

    def is_mouse_just_pressed(self, button):
        """Кнопка была нажата в этом кадре?"""
        return (self.mouse_buttons[button] and
                not self._prev_mouse_buttons[button])
