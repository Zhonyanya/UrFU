import pygame
import sys
from constants import (SCREEN_HEIGHT, SCREEN_WIDTH, FIXED_DT,
                       MINIGUN_FIRE_RATE, MINIGUN_PROJECTILE_SPEED,
                       MINIGUN_SPREAD, MINIGUN_PROJECTILES_PER_SHOT,
                       MINIGUN_IS_AUTOMATIC, MINIGUN_COLOR,
                       MINIGUN_MUZZLE_LIFETIME, MINIGUN_MUZZLE_RADIUS,
                       SHOTGUN_FIRE_RATE, SHOTGUN_PROJECTILE_SPEED,
                       SHOTGUN_SPREAD, SHOTGUN_PROJECTILES_PER_SHOT,
                       SHOTGUN_IS_AUTOMATIC, SHOTGUN_COLOR,
                       SHOTGUN_MUZZLE_LIFETIME, SG_CELL_SIZE, SHOTGUN_DAMAGE,
                       SHOTGUN_MUZZLE_RADIUS, SHOTGUN_LIFETIME,
                       MINIGUN_DAMAGE, MINIGUN_LIFETIME)
from input_handler import InputHandler
from player import Player
from arena import Arena
from renderer import Renderer
from enemy import Minion
from spatial_grid import SpatialGrid
from weapon import Weapon
from projectile import ProjectileManager
from events import GameEvents
from collision_system import (check_projectile_enemy_collisions,
                              resolve_enemy_player_collisions,
                              resolve_enemy_enemy_collisions)
from fps_counter import FPSCounter


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
    spatial_grid = SpatialGrid(SG_CELL_SIZE)
    projectile_manager = ProjectileManager()
    events = GameEvents()
    fps_counter = FPSCounter()

    minigun = Weapon(
        fire_rate=MINIGUN_FIRE_RATE,
        projectile_speed=MINIGUN_PROJECTILE_SPEED,
        damage=MINIGUN_DAMAGE,
        spread=MINIGUN_SPREAD,
        projectiles_per_shot=MINIGUN_PROJECTILES_PER_SHOT,
        lifetime=MINIGUN_LIFETIME,
        is_automatic=MINIGUN_IS_AUTOMATIC,
        color=MINIGUN_COLOR,
        muzzle_flash_radius=MINIGUN_MUZZLE_RADIUS,
        muzzle_flash_lifetime=MINIGUN_MUZZLE_LIFETIME
    )
    shotgun = Weapon(
        fire_rate=SHOTGUN_FIRE_RATE,
        projectile_speed=SHOTGUN_PROJECTILE_SPEED,
        damage=SHOTGUN_DAMAGE,
        spread=SHOTGUN_SPREAD,
        projectiles_per_shot=SHOTGUN_PROJECTILES_PER_SHOT,
        lifetime=SHOTGUN_LIFETIME,
        is_automatic=SHOTGUN_IS_AUTOMATIC,
        color=SHOTGUN_COLOR,
        muzzle_flash_radius=SHOTGUN_MUZZLE_RADIUS,
        muzzle_flash_lifetime=SHOTGUN_MUZZLE_LIFETIME
    )
    weapons_by_button = {0: minigun, 2: shotgun}

    running = True
    accumulator = 0.0

    while running:
        frame_dt = clock.tick() / 1000.0
        if frame_dt > 0.25:
            frame_dt = 0.25
        accumulator += frame_dt

        fps_counter.update(frame_dt)

        input_handler.update()
        if input_handler.quit_requested:
            break

        if input_handler.spawn_enemy_requested:
            enemies.append(Minion(input_handler.mouse_pos))

        movement_vec = input_handler.get_movement_vector()
        mouse_pos = input_handler.mouse_pos

        for btn_idx, weapon in weapons_by_button.items():
            weapon.update(frame_dt)
            is_held = input_handler.is_mouse_held(btn_idx)
            just_pressed = input_handler.is_mouse_just_pressed(btn_idx)
            weapon.try_fire(is_held, just_pressed, player.pos, player.angle,
                            projectile_manager, events)

        while accumulator >= FIXED_DT:

            player.update(FIXED_DT, movement_vec, arena.rect, mouse_pos)

            spatial_grid.clear()
            for enemy in enemies:
                if enemy.alive:
                    spatial_grid.insert(enemy)

            for enemy in enemies:
                if enemy.alive:
                    enemy.update(FIXED_DT, player.pos, enemies, spatial_grid)

            projectile_manager.update(FIXED_DT)

            check_projectile_enemy_collisions(projectile_manager, enemies, spatial_grid)
            resolve_enemy_enemy_collisions(enemies, spatial_grid)
            resolve_enemy_player_collisions(enemies, player)

            enemies[:] = [e for e in enemies if e.alive]

            accumulator -= FIXED_DT

        renderer.draw(screen, arena, player, enemies, projectile_manager)

        # graph_width = 160
        # graph_height = 60
        # graph_x = SCREEN_WIDTH - graph_width - 10
        # graph_y = 50
        # fps_counter.draw_graph(screen, graph_x, graph_y, graph_width, graph_height)
        # pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()