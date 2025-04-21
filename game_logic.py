from typing import List, Tuple, Optional
from entities import Player, Enemy, Item, NeutralEnemy, Key, Weapon
from colorama import Fore, Style, Back
from map_generator import Floor
from dialog import display_dialog
from end_screen import display_victory_screen, display_game_over
from input_handler import get_char
import os



"""game_logic.py - логика игры
handle_player_action() - обработка действий игрока (движение, атака, использование предметов)"""


def handle_player_action(action: str, player: Player, dungeon: List[Floor], enemies: List[Enemy], 
                        items: List[Tuple[Item, int, int, int]], message: str) -> Tuple[bool, str, bool]:
    player_moved = False
    running = True

    if action == 'w':
        player_moved = player.move(0, -1, dungeon)
    elif action == 's':
        player_moved = player.move(0, 1, dungeon)
    elif action == 'a':
        player_moved = player.move(-1, 0, dungeon)
    elif action == 'd':
        player_moved = player.move(1, 0, dungeon)
    elif action == ' ':
        target = None
        nearest_distance = 1.5
        for enemy in enemies:
            if enemy.current_floor == player.current_floor:
                distance = player.distance_to(enemy)
                if distance <= nearest_distance:
                    target = enemy
                    nearest_distance = distance
        if target:
            damage = player.attack(target)
            message = f"Вы атакуете {target.name} с помощью {player.equipped_weapon.name}, нанося {damage} урона!"
            if target.is_dead():
                message += f"\nВы убили {target.name}!"
                player.statistics.record_enemy_killed()
                if hasattr(target, 'on_death'):
                    dropped_item = target.on_death()
                    if dropped_item:
                        items.append((dropped_item, target.x, target.y, target.current_floor))
                        message += f"\n{target.name} уронил {dropped_item.name}!"
                enemies.remove(target)
            player_moved = True
        else:
            message = "Рядом никого нет."
    elif action == 'e':
        if player.use_stairs(dungeon):
            message = "Вы поднялись/спустились по лестнице."
            player_moved = True
        else:
            message = "Здесь нет лестницы."
    elif action == 'g':
        for i, (item, item_x, item_y, item_floor) in enumerate(items):
            if item_x == player.x and item_y == player.y and item_floor == player.current_floor:
                player.inventory.add_item(item)
                message = f"Вы подняли {item.name}."
                player.statistics.record_item_picked()
                if isinstance(item, Key):
                    player.keys_found += 1
                    player.statistics.record_key_found()
                    message = f"Вы нашли {item.name}! ({player.keys_found}/3)"
                items.pop(i)
                if player.has_all_keys():
                    display_victory_screen(player)
                    running = False
                break
        else:
            message = "Здесь нет предметов."
    elif action == 'f':
        interaction_result = player.interact_with_character(dungeon, enemies)
        if interaction_result:
            interaction_message, interacted_character = interaction_result
            if isinstance(interacted_character, NeutralEnemy) and hasattr(interacted_character, 'current_riddle'):
                riddle = interacted_character.current_riddle
                options = riddle.get('варианты', [])
                title = f"Разговор с {interacted_character.name}"
                answer_idx = display_dialog(title, interaction_message, options)
                if answer_idx >= 0:
                    success, result_message = interacted_character.answer_riddle(answer_idx, player)
                    display_dialog(title, result_message)
                    if not success:
                        message = result_message
            else:
                display_dialog(f"Разговор с {interacted_character.name}", interaction_message)
        else:
            message = "Рядом никого нет для взаимодействия."
    elif action == 'i':
        os.system('cls' if os.name == 'nt' else 'clear')
        print("                                   "+Fore.GREEN+"ИНВЕНТАРЬ"+Fore.RESET)
        print(" ")
        print(f"Экипировано:"+Fore.RED+f" {player.equipped_weapon.name}"+Fore.RESET)
        print(" ")
        
        all_items = player.inventory.get_all_items()
        if not all_items:
            print("Инвентарь пуст.")
        else:
            for i, item in enumerate(all_items):
                print(f"{i+1}. {item.name}")
                print(" ")
            
            print(Fore.LIGHTBLACK_EX+Style.DIM+"\n           Выберите предмет для использования (или Esc для выхода):"+Fore.RESET+Style.RESET_ALL)
            
            while True:
                key = get_char()
                if key == '\x1b':
                    break
                
                try:
                    index = int(key) - 1
                    if 0 <= index < len(all_items):
                        item = all_items[index]
                        if item.use(player):
                            player.inventory.remove_item(item)
                            if isinstance(item, Weapon) and item == player.equipped_weapon:
                                message = f"Вы экипировали {item.name}."
                        break
                except ValueError:
                    continue
    elif action == 'q':
        display_game_over(player)
        running = False

    return player_moved, message, running