from introductory_screen import show_title_screen, transition_to_game
from map_generator import MapGenerator
from entities import Player
from game_setup import generate_enemies, generate_items
from renderer import render_game
from game_logic import handle_player_action
from input_handler import get_char
from end_screen import display_game_over, display_victory_screen

if __name__ == "__main__":
    
    show_title_screen()
    transition_to_game()

    # Инициализация карты и игрока
    map_generator = MapGenerator(width=80, height=24, num_floors=3)
    dungeon = map_generator.generate_map()
    start_x, start_y = dungeon[0].rooms[0].center
    player = Player(start_x, start_y, "Заключенный Жужун")

    # Инициализация врагов и предметов
    enemies = generate_enemies(dungeon)
    items = generate_items(dungeon)
    random_key = map_generator.generate_random_key(dungeon)
    if random_key:
        items.append(random_key)

    running = True
    message = ""
    dungeon[player.current_floor].update_fov(player.x, player.y)

    while running:
        current_message = ""
        render_game(player, dungeon, enemies, items, message)
        action = get_char()
        player_moved, action_message, running = handle_player_action(action, player, dungeon, enemies, items, current_message)
        if action_message:
            current_message = action_message  

        if player_moved:
            dungeon[player.current_floor].update_fov(player.x, player.y)
            enemies_on_floor = [e for e in enemies if e.current_floor == player.current_floor]
            for enemy in enemies_on_floor:
                if dungeon[player.current_floor].tiles[enemy.x][enemy.y].explored:
                    enemy_message = enemy.take_turn(player, dungeon)
                    if enemy_message:
                        current_message = enemy_message  

            if player.is_dead():
                display_game_over(player)
                running = False

        message = current_message