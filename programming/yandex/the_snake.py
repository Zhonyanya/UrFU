from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Общий класс, от которого будут наследоваться другие."""

    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        """
        Общий класс, от которого будут наследоваться другие.

        Args:
            position (tuple): Кортеж-координаты в формате (x, y)
        """
        self.position = position

    def draw(self):
        """Абстрактная функция рисования"""
        pass


class Apple(GameObject):
    """Класс яблока, которое должна съесть змейка."""

    def __init__(self, body_color=APPLE_COLOR):
        """
        Класс яблока, которое должна съесть змейка.

        Args:
            body_color (tuple, optional): Кортеж с тремя значениями 0-255,
                                         означающими RGB запись
        """
        self.body_color = body_color
        self.randomize_position()

    def randomize_position(self):
        """Рандомизирует положение яблока."""
        posx = randint(0, 620) // GRID_SIZE * GRID_SIZE
        posy = randint(0, 460) // GRID_SIZE * GRID_SIZE
        self.position = (posx, posy)

    def draw(self):
        """Рисует яблоко."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self, position=(0, 0), body_color=SNAKE_COLOR):
        """
        Класс змейки.

        Args:
            body_color (tuple, optional): Кортеж с тремя значениями 0-255,
                                         означающими RGB запись
        """
        self.length = 1
        self.direction = RIGHT
        self.body_color = body_color
        self.next_direction = None
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                          for _ in range(self.length)]
        self.last = []

    def update_direction(self):
        """Обновляет направление движения после нажатия на стрелочки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает координаты головы."""
        return self.positions[0]

    def move(self):
        if self.last != self.get_head_position():
            self.last = self.positions[-1]
        """Двигает змейку согласно направлению движения."""
        if self.positions[0][0] >= SCREEN_WIDTH:
            self.positions[0] = (0, self.positions[0][1])
        elif self.positions[0][0] < 0:
            self.positions[0] = (SCREEN_WIDTH, self.positions[0][1])
        elif self.positions[0][1] >= SCREEN_HEIGHT:
            self.positions[0] = (self.positions[0][0], 0)
        elif self.positions[0][1] < 0:
            self.positions[0] = (self.positions[0][0], SCREEN_HEIGHT)
        if self.direction == RIGHT:
            self.positions.insert(0, (self.positions[0][0] + GRID_SIZE,
                                      self.positions[0][1]))
        elif self.direction == LEFT:
            self.positions.insert(0, (self.positions[0][0] - GRID_SIZE,
                                      self.positions[0][1]))
        elif self.direction == DOWN:
            self.positions.insert(0, (self.positions[0][0],
                                      self.positions[0][1] + GRID_SIZE))
        else:
            self.positions.insert(0, (self.positions[0][0],
                                      self.positions[0][1] - GRID_SIZE))
        self.last = self.positions.pop()

    def draw(self):
        """Рисует змейку."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def check_loop(self):
        """Проверяет, закольцевалась ли змейка."""
        for segment in self.positions[1:]:
            if self.positions[0] == segment:
                return True
        return False

    def reset(self):
        """Возвращает змейку в начальное положение."""
        for _ in range(len(self.positions) - 1):
            self.positions.pop()
        self.length = 1
        self.positions[0] = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.direction = choice([RIGHT, LEFT, UP, DOWN])


def handle_keys(game_object):
    """
    Обрабатывает действия пользователя.

    Args:
        game_object (GameObject): объект змейки
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple(APPLE_COLOR)
    snake = Snake((0, 0), SNAKE_COLOR)

    while True:
        clock.tick(SPEED)
        apple.draw()
        snake.draw()
        snake.update_direction()
        snake.move()
        handle_keys(snake)

        head_x, head_y = snake.get_head_position()
        apple_x, apple_y = apple.position
        if (head_x // GRID_SIZE == apple_x // GRID_SIZE
                and head_y // GRID_SIZE == apple_y // GRID_SIZE):
            snake.length += 1
            if snake.direction == RIGHT:
                snake.positions.insert(0, (snake.positions[0][0] + GRID_SIZE,
                                           snake.positions[0][1]))
            elif snake.direction == LEFT:
                snake.positions.insert(0, (snake.positions[0][0] - GRID_SIZE,
                                           snake.positions[0][1]))
            elif snake.direction == DOWN:
                snake.positions.insert(0, (snake.positions[0][0],
                                           snake.positions[0][1] + GRID_SIZE))
            else:
                snake.positions.insert(0, (snake.positions[0][0],
                                           snake.positions[0][1] - GRID_SIZE))
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()
            apple.draw()

        if snake.check_loop():
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position()
            apple.draw()
            snake.reset()

        # Тут опишите основную логику игры.
        pygame.display.update()


if __name__ == '__main__':
    main()
