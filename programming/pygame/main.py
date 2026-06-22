import pygame
import sys
from config.constants import (SCREEN_HEIGHT, SCREEN_WIDTH, FIXED_DT, MAX_FRAME_DT,
                              MINIGUN_FIRE_RATE, MINIGUN_PROJECTILE_SPEED,
                              MINIGUN_SPREAD, MINIGUN_PROJECTILES_PER_SHOT,
                              MINIGUN_IS_AUTOMATIC, MINIGUN_COLOR,
                              MINIGUN_MUZZLE_LIFETIME, MINIGUN_MUZZLE_RADIUS,
                              SHOTGUN_FIRE_RATE, SHOTGUN_PROJECTILE_SPEED,
                              SHOTGUN_SPREAD, SHOTGUN_PROJECTILES_PER_SHOT,
                              SHOTGUN_IS_AUTOMATIC, SHOTGUN_COLOR,
                              SHOTGUN_MUZZLE_LIFETIME, SG_CELL_SIZE, SHOTGUN_DAMAGE,
                              SHOTGUN_MUZZLE_RADIUS, SHOTGUN_LIFETIME,
                              MINIGUN_DAMAGE, MINIGUN_LIFETIME,
                              WAVE_SPAWNER_INITIAL_INTERVAL, WAVE_SPAWNER_MIN_INTERVAL,
                              WAVE_SPAWNER_INTERVAL_DECAY, WAVE_SPAWNER_BASE_COUNT,
                              WAVE_SPAWNER_COUNT_GROWTH, WAVE_SPAWNER_MAX_COUNT,
                              WAVE_SPAWNER_SPAWN_MARGIN)
from systems.input_handler import InputHandler
from entities.player import Player
from world.arena import Arena
from rendering.renderer import Renderer
from entities.enemy import Minion
from systems.spatial_grid import SpatialGrid
from entities.weapon import Weapon
from entities.projectile import ProjectileManager
from systems.events import GameEvents
from systems.collision_system import (check_projectile_enemy_collisions,
                              resolve_enemy_player_collisions,
                              resolve_enemy_enemy_collisions,
                              check_player_damage)
from rendering.fps_counter import FPSCounter
from world.spawner import WaveSpawner
from rendering.hud import HUD
from rendering.game_over_screen import GameOverScreen


def _create_weapons() -> dict[int, 'Weapon']:
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
        muzzle_flash_lifetime=MINIGUN_MUZZLE_LIFETIME,
        is_global_light=False
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
        muzzle_flash_lifetime=SHOTGUN_MUZZLE_LIFETIME,
        is_global_light=True
    )
    return {0: minigun, 2: shotgun}


def _create_game(arena_rect_holder: list) -> dict:
    """Создаёт/пересоздаёт игровые объекты. Возвращает словарь состояния."""
    arena = Arena()
    arena_rect_holder.clear()
    arena_rect_holder.append(arena.rect)
    return {
        'arena': arena,
        'player': Player(),
        'enemies': [],
        'projectile_manager': ProjectileManager(),
        'events': GameEvents(),
        'wave_spawner': WaveSpawner(
            arena_rect=arena.rect,
            spawn_factory=Minion,
            initial_interval=WAVE_SPAWNER_INITIAL_INTERVAL,
            min_interval=WAVE_SPAWNER_MIN_INTERVAL,
            interval_decay=WAVE_SPAWNER_INTERVAL_DECAY,
            base_count=WAVE_SPAWNER_BASE_COUNT,
            count_growth=WAVE_SPAWNER_COUNT_GROWTH,
            max_count=WAVE_SPAWNER_MAX_COUNT,
            spawn_margin=WAVE_SPAWNER_SPAWN_MARGIN
        ),
        'weapons': _create_weapons(),
        'kills': 0,
    }


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Roguelite Arena")
    clock = pygame.time.Clock()
    input_handler = InputHandler()
    renderer = Renderer()
    spatial_grid = SpatialGrid(SG_CELL_SIZE)
    fps_counter = FPSCounter()
    hud = HUD()
    game_over_screen = GameOverScreen()

    arena_rect_holder = []
    state = _create_game(arena_rect_holder)

    game_state = 'playing'  # 'playing' | 'game_over'
    stats = {'kills': 0, 'waves': 0}

    running = True
    accumulator = 0.0

    while running:
        frame_dt = clock.tick() / 1000.0
        if frame_dt > MAX_FRAME_DT:
            frame_dt = MAX_FRAME_DT
        accumulator += frame_dt

        fps_counter.update(frame_dt)
        input_handler.update()

        if input_handler.quit_requested:
            break

        mouse_pos = input_handler.mouse_pos
        left_pressed = input_handler.is_mouse_just_pressed(0)

        if game_state == 'game_over':
            restart = (game_over_screen.is_restart_clicked(mouse_pos, left_pressed)
                       or input_handler.is_key_just_pressed(pygame.K_r))
            if restart:
                state = _create_game(arena_rect_holder)
                game_state = 'playing'
                accumulator = 0.0
                renderer.draw(screen, state['arena'], state['player'],
                              state['enemies'], state['projectile_manager'],
                              state['events'])
                hud.draw(screen, state['player'].hp, state['player'].max_hp)
                pygame.display.flip()
                continue

        if game_state == 'playing':
            movement_vec = input_handler.get_movement_vector()
            player = state['player']
            enemies = state['enemies']
            events = state['events']
            projectile_manager = state['projectile_manager']
            wave_spawner = state['wave_spawner']

            if input_handler.spawn_enemy_requested:
                enemies.append(Minion(input_handler.mouse_pos))

            for btn_idx, weapon in state['weapons'].items():
                weapon.update(frame_dt)
                is_held = input_handler.is_mouse_held(btn_idx)
                just_pressed = input_handler.is_mouse_just_pressed(btn_idx)
                weapon.try_fire(is_held, just_pressed, player.pos,
                                player.angle, projectile_manager, events)

            events.update(frame_dt)

            while accumulator >= FIXED_DT:

                wave_spawner.update(FIXED_DT, enemies)

                player.update(FIXED_DT, movement_vec,
                              state['arena'].rect, mouse_pos)

                spatial_grid.clear()
                for enemy in enemies:
                    if enemy.alive:
                        spatial_grid.insert(enemy)

                for enemy in enemies:
                    if enemy.alive:
                        enemy.update(FIXED_DT, player.pos, enemies,
                                     spatial_grid)

                projectile_manager.update(FIXED_DT)

                _, kills_this_step = check_projectile_enemy_collisions(
                    projectile_manager, enemies, spatial_grid
                )
                state['kills'] += kills_this_step

                check_player_damage(enemies, player, events)
                resolve_enemy_enemy_collisions(enemies, spatial_grid)
                resolve_enemy_player_collisions(enemies, player)

                enemies[:] = [e for e in enemies if e.alive]

                accumulator -= FIXED_DT

        if player.is_dead:
            game_state = 'game_over'
            stats['kills'] = state['kills']
            stats['waves'] = wave_spawner.get_wave_number()

        renderer.draw(screen, state['arena'], state['player'],
                      state['enemies'], state['projectile_manager'],
                      state['events'])
        hud.draw(screen, state['player'].hp, state['player'].max_hp)

        if game_state == 'game_over':
            game_over_screen.draw(screen, stats, mouse_pos)

        pygame.display.flip()

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