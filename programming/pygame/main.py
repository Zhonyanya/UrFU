import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PLAYER_SIZE = 32
BACKGROUND_COLOR = (30, 30, 30)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Roguelite Top-Down - Vector Movement")
clock = pygame.time.Clock()

player_rect = pygame.Rect(
    SCREEN_WIDTH // 2 - PLAYER_SIZE // 2,
    SCREEN_HEIGHT // 2 - PLAYER_SIZE // 2,
    PLAYER_SIZE, PLAYER_SIZE
)

current_velocity = pygame.math.Vector2(0, 0)
MAX_SPEED = 600.0
ACCELERATION = 2000.0
DECELERATION = 2500.0

running = True
while running:
    # dt (delta time) - время в секундах с прошлого кадра
    # Делает движение независимым от FPS
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 1. Собираем вектор ввода
    input_vector = pygame.math.Vector2(0, 0)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        input_vector.y -= 1
    if keys[pygame.K_s]:
        input_vector.y += 1
    if keys[pygame.K_a]:
        input_vector.x -= 1
    if keys[pygame.K_d]:
        input_vector.x += 1

    # 2. Нормализация: длина вектора станет 1.0, если он не нулевой
    if input_vector.length() > 0:
        input_vector.normalize_ip()

    # 3. Целевая скорость
    target_velocity = input_vector * MAX_SPEED

    # 4. Плавное изменение скорости (разгон / торможение)
    velocity_diff = target_velocity - current_velocity
    accel_rate = ACCELERATION if input_vector.length() > 0 else DECELERATION
    max_delta = accel_rate * dt  # Максимально возможное изменение за этот кадр

    if velocity_diff.length() > 0 and velocity_diff.length() > max_delta:
        velocity_diff.normalize_ip()
        velocity_diff *= max_delta

    current_velocity += velocity_diff

    player_rect.x += current_velocity.x * dt
    player_rect.y += current_velocity.y * dt
    player_rect.clamp_ip(screen.get_rect())

    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, (255, 255, 255), player_rect)
    pygame.display.flip()

pygame.quit()
sys.exit()
