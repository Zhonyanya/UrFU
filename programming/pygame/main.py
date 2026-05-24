import pygame
import sys
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, FPS
from input_handler import InputHandler
from player import Player
from arena import Arena
from renderer import Renderer


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Roguelite Arena")
    clock = pygame.time.Clock()

    input_handler = InputHandler()
    arena = Arena()
    player = Player()
    enemies = []
    renderer = Renderer()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        input_handler.update()
        if input_handler.quit_requested:
            break

        movement_vec = input_handler.get_movement_vector()

        player.update(dt, movement_vec, arena.rect)
        for enemy in enemies:
            enemy.update(dt, player.pos)

        renderer.draw(screen, arena, player, enemies)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
