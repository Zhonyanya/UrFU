import pygame
import sys
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, FIXED_DT, FPS
from input_handler import InputHandler
from player import Player
from arena import Arena
from renderer import Renderer
from enemy import Minion, resolve_enemy_collisions


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Roguelite Arena")
    clock = pygame.time.Clock()

    input_handler = InputHandler()
    arena = Arena()
    player = Player()
    enemies = [Minion((SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4))]
    renderer = Renderer()

    running = True
    accumulator = 0.0

    while running:
        frame_dt = clock.tick(FPS) / 1000.0

        if frame_dt > 0.25:
            frame_dt = 0.25
        accumulator += frame_dt

        input_handler.update()
        if input_handler.quit_requested:
            break

        movement_vec = input_handler.get_movement_vector()
        mouse_pos = input_handler.mouse_pos

        while accumulator >= FIXED_DT:
            player.update(FIXED_DT, movement_vec, arena.rect, mouse_pos)

            for enemy in enemies:
                enemy.update(FIXED_DT, player.pos, enemies)

            resolve_enemy_collisions(enemies)

            for enemy in enemies:
                enemy.resolve_collision(player)

            accumulator -= FIXED_DT

        renderer.draw(screen, arena, player, enemies)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
