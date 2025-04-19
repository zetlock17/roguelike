import random
import os
import msvcrt
import time
import json
from colorama import Fore, Back, Style

from entities import (
    Player, Enemy, HostileEnemy, NeutralEnemy,
    Item, Weapon, Food, Key
)

from statistic import Statistics
from map_generator import MapGenerator
from introductory_screen import show_title_screen, transition_to_game
from input_handler import get_char

def display_game_over(player: Player):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + player.statistics.display())
                                                                                                          
    print("                                                                                        ")
    print("              "+Fore.RED+ Style.BRIGHT+"                Нажмите любую клавишу для выхода..."+Style.RESET_ALL+Fore.RESET+"                           ")
    print("                                                                                        ")
    print("                                                                                        ")
    get_char()

def display_dialog(title, message, options=None):
    """Отображает диалоговое окно с вариантами ответов."""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    width = max(len(title), len(message), 80)
    
    print("┌" + "─" * width + "┐")
    print(f"│{title.center(width)}│")
    print("├" + "─" * width + "┤")
    
    # Split message into lines that fit within the dialog box
    words = message.split()
    lines = []
    current_line = ""
    
    for word in words:
        if len(current_line) + len(word) + 1 <= width - 2:  # -2 for borders
            if current_line:
                current_line += " " + word
            else:
                current_line = word
        else:
            lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    for line in lines:
        print(f"│{line.ljust(width)}│")
    
    if options:
        print("├" + "─" * width + "┤")
        for i, option in enumerate(options):
            print(f"│ {i+1}. {option.ljust(width-4)}│")
    
    print("└" + "─" * width + "┘")
    
    if options:
        while True:
            key = get_char()
            try:
                choice = int(key) - 1
                if 0 <= choice < len(options):
                    return choice
            except ValueError:
                if key == '\x1b':  # Escape key
                    return -1
                
def display_victory_screen(player: Player):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + player.statistics.win_display())
                                                                                                          
    print("                                                                                        ")
    print("              "+Fore.GREEN+ Style.BRIGHT+"                Нажмите любую клавишу для выхода..."+Style.RESET_ALL+Fore.RESET+"                           ")
    print("                                                                                        ")
    print("                                                                                        ")
    get_char()

if __name__ == "__main__":
    show_title_screen()
    transition_to_game()
    map_generator = MapGenerator(width=80, height=24, num_floors=3)
    dungeon = map_generator.generate_map()

    start_x, start_y = dungeon[0].rooms[0].center
    player = Player(start_x, start_y, "Заключенный Жужун")

    enemies = []
    items = []
    key_holder_added = False
    
    # Создание врагов
    for floor_idx, floor in enumerate(dungeon):
        for room in floor.rooms[1:]:
            if random.random() < 0.7:
                x = random.randint(room.x1 + 1, room.x2 - 1)
                y = random.randint(room.y1 + 1, room.y2 - 1)
                
                if not (0 <= x < floor.width and 0 <= y < floor.height):
                    continue

                enemy_type = random.random()
                
                if floor_idx == 0:
                    if enemy_type < 0.4:
                        enemy = HostileEnemy(x, y, 
                                           Style.BRIGHT + "\033[91;47m✺\033[0m" + Back.RESET + Fore.RESET + Style.RESET_ALL, 
                                           "Злая собака", hp=20, defense=0, power=3, view_range=8)
                    elif enemy_type < 0.7:
                        enemy = NeutralEnemy(x, y, 
                                           Style.BRIGHT + "\033[33;47m☻\033[0m" + Fore.RESET + Back.BLACK + Style.RESET_ALL, 
                                           "Опущенный", hp=15, defense=0, power=2, has_item=True)
                    else:
                        enemy = HostileEnemy(x, y, 
                                           Fore.LIGHTRED_EX + Style.BRIGHT + "\033[91;47m⚔︎\033[0m" + Fore.RESET + Style.RESET_ALL, 
                                           "Охранник", hp=30, defense=2, power=5, 
                                           weapon=Weapon("Полицейская дубинка", 
                                                       Style.BRIGHT + "\033[47;38;5;130m┤\033[0m" + Back.RESET + Style.RESET_ALL, 
                                                       damage=5, color='blue'))
                elif floor_idx == 1:
                    if enemy_type < 0.3:
                        enemy = HostileEnemy(x, y, 
                                           Fore.LIGHTRED_EX + Style.BRIGHT + "\033[91;47m⚔︎\033[0m" + Fore.RESET + Style.RESET_ALL, 
                                           "Охранник", hp=30, defense=2, power=5, 
                                           weapon=Weapon("Полицейская дубинка", 
                                                       Style.BRIGHT + "\033[47;38;5;130m┤\033[0m" + Back.RESET + Style.RESET_ALL, 
                                                       damage=5, color='blue'))
                    elif enemy_type < 0.6:
                        enemy = NeutralEnemy(x, y, 
                                           Style.BRIGHT + "\033[33;47m☻\033[0m" + Fore.RESET + Back.BLACK + Style.RESET_ALL, 
                                           "Опущенный", hp=15, defense=0, power=2, has_item=True)
                    elif enemy_type < 0.8:
                        enemy = HostileEnemy(x, y, 
                                           Style.BRIGHT + "\033[91;47m✺\033[0m" + Back.RESET + Fore.RESET + Style.RESET_ALL, 
                                           "Злая собака", hp=20, defense=0, power=3, view_range=8)
                    else:
                        enemy = HostileEnemy(x, y, 
                                           Fore.RED + Style.BRIGHT + "\033[91;47m➹\033[0m" + Fore.RESET + Back.RESET + Style.RESET_ALL, 
                                           "Стрелок", hp=25, defense=1, power=1, 
                                           weapon=Weapon("Пистолет", 
                                                       Style.BRIGHT + "\033[47;30m⌐\033[0m" + Fore.RESET + Back.RESET + Style.RESET_ALL, 
                                                       damage=10, color='darkgrey'))
                else:
                    if enemy_type < 0.3:
                        enemy = HostileEnemy(x, y, 
                                           Style.BRIGHT + "\033[91;47m✺\033[0m" + Back.RESET + Fore.RESET + Style.RESET_ALL, 
                                           "Злая собака", hp=20, defense=0, power=3, view_range=8)
                    elif enemy_type < 0.6:
                        enemy = HostileEnemy(x, y, 
                                           Fore.RED + Style.BRIGHT + "\033[91;47m➹\033[0m" + Fore.RESET + Back.RESET + Style.RESET_ALL, 
                                           "Стрелок", hp=25, defense=1, power=1, 
                                           weapon=Weapon("Пистолет", 
                                                       Style.BRIGHT + "\033[47;30m⌐\033[0m" + Fore.RESET + Back.RESET + Style.RESET_ALL, 
                                                       damage=10, color='darkgrey'))
                    else:
                        enemy = HostileEnemy(x, y, 
                                           Fore.LIGHTRED_EX + Style.BRIGHT + "\033[91;47m⚔︎\033[0m" + Fore.RESET + Style.RESET_ALL, 
                                           "Охранник", hp=30, defense=2, power=5, 
                                           weapon=Weapon("Полицейская дубинка", 
                                                       Style.BRIGHT + "\033[47;38;5;130m┤\033[0m" + Back.RESET + Style.RESET_ALL, 
                                                       damage=5, color='blue'))
                    
                    # Добавляем авторитета на последний этаж
                    enemy = NeutralEnemy(x, y, 
                                       Fore.MAGENTA + Style.BRIGHT + "\033[95;47m⛛\033[0m" + Fore.RESET + Back.RESET, 
                                       "Авторитет", hp=40, defense=3, power=6, 
                                       weapon=Weapon("Заточка", 
                                                   Style.BRIGHT + "\033[30;47m↾\033[0m" + Back.RESET + Fore.RESET + Style.RESET_ALL, 
                                                   damage=7, color='silver'), 
                                       has_item=True, has_riddle=True)
                
                enemy.current_floor = floor_idx
                enemies.append(enemy)

        # Добавляем ключ-носителя на последний этаж (гарантированно)
        if floor_idx == len(dungeon) - 1 and not key_holder_added:
            room = random.choice(floor.rooms)
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)
            
            if 0 <= x < floor.width and 0 <= y < floor.height:
                key_holder = HostileEnemy(x, y, 
                                       Fore.RED + Style.BRIGHT + "\033[91;47m➹\033[0m" + Fore.RESET + Back.RESET + Style.RESET_ALL, 
                                       "Стрелок", hp=25, defense=1, power=1, 
                                       weapon=Weapon("Пистолет", 
                                                   Style.BRIGHT + "\033[47;30m⌐\033[0m" + Fore.RESET + Back.RESET + Style.RESET_ALL, 
                                                   damage=10, color='darkgrey'),
                                       has_key=True)
                key_holder.current_floor = floor_idx
                enemies.append(key_holder)
                key_holder_added = True

    # Создание предметов
    for floor_idx, floor in enumerate(dungeon):
        for room in floor.rooms:
            if random.random() < 0.5:
                x = random.randint(room.x1 + 1, room.x2 - 1)
                y = random.randint(room.y1 + 1, room.y2 - 1)
                
                if not (0 <= x < floor.width and 0 <= y < floor.height):
                    continue
                
                item_type = random.random()
                
                if item_type < 0.3:
                    items.append((Food("Таракан", 
                                     Style.BRIGHT + "\033[47;38;5;130m∿\033[0m" + Fore.RESET + Back.RESET + Style.RESET_ALL, 
                                     nutrition=1, color='brown'), x, y, floor_idx))
                elif item_type < 0.6:
                    items.append((Food("Засохший хлеб", 
                                     Style.BRIGHT + "\033[47;38;5;130m⬬\033[0m"+ Back.RESET + Style.RESET_ALL, 
                                     nutrition=5, color='tan'), x, y, floor_idx))
                elif item_type < 0.8:
                    items.append((Food("Тюремное хрючево", 
                                     Style.BRIGHT + Fore.LIGHTWHITE_EX + "\033[47;38;5;130m✱\033[0m"+ Fore.RESET + Back.RESET + Style.RESET_ALL, 
                                     nutrition=10, color='yellow'), x, y, floor_idx))
                elif item_type < 0.9:
                    items.append((Weapon("Заточка", 
                                       Style.BRIGHT + "\033[30;47m↾\033[0m" + Back.RESET + Fore.RESET + Style.RESET_ALL, 
                                       damage=7, color='silver'), x, y, floor_idx))
                elif item_type < 0.95:
                    items.append((Weapon("Полицейская дубинка", 
                                       Style.BRIGHT + "\033[47;38;5;130m┤\033[0m" + Back.RESET + Style.RESET_ALL, 
                                       damage=5, color='blue'), x, y, floor_idx))
                else:
                    items.append((Weapon("Пистолет", 
                                       Style.BRIGHT + "\033[47;30m⌐\033[0m" + Fore.RESET + Back.RESET + Style.RESET_ALL, 
                                       damage=10, color='darkgrey'), x, y, floor_idx))
    
    # Добавляем случайный ключ на одном из этажей
    random_key_floor = random.randint(0, len(dungeon) - 1)
    room = random.choice(dungeon[random_key_floor].rooms)
    key_x = random.randint(room.x1 + 1, room.x2 - 1)
    key_y = random.randint(room.y1 + 1, room.y2 - 1)
    
    if 0 <= key_x < dungeon[random_key_floor].width and 0 <= key_y < dungeon[random_key_floor].height:
        items.append((Key(3), key_x, key_y, random_key_floor))

    running = True
    message = ""
    
    dungeon[player.current_floor].update_fov(player.x, player.y)

    while running:
        os.system('cls' if os.name == 'nt' else 'clear')
                                                                                                            
        print("                                                                                       ")
        print(Style.BRIGHT+Fore.CYAN+f"                           Этаж {player.current_floor + 1} "+Fore.RED + f"  HP: {player.hp}/{player.max_hp} "+Fore.MAGENTA+f"  Оружие: {player.equipped_weapon.name}     "+Fore.RESET + Style.RESET_ALL)
        print("                                                                                       ")
        current_floor = player.current_floor
        floor = dungeon[current_floor]
        
        for y in range(floor.height):
            row = ""
            for x in range(floor.width):
                tile = floor.tiles[x][y]
                if not tile.explored:
                    row += " "
                    continue

                if player.x == x and player.y == y and player.current_floor == current_floor:
                    row += player.char
                else:
                    enemy_here = False
                    for enemy in enemies:
                        if enemy.x == x and enemy.y == y and enemy.current_floor == current_floor:
                            row += enemy.char
                            enemy_here = True
                            break

                    if not enemy_here:
                        item_here = False
                        for item, item_x, item_y, item_floor in items:
                            if item_x == x and item_y == y and item_floor == current_floor:
                                row += item.char
                                item_here = True
                                break
                        
                        if not item_here:
                            row += str(tile)
            print(row)
        
        if message:
            print(message)
            message = ""

        print("\n "+Fore.RESET) 
        print(Fore.GREEN+"                   SPACE"+Fore.RESET+" — атака  "+Fore.GREEN+" E"+Fore.RESET+" — использовать лестницу  "+Fore.GREEN+" G "+Fore.RESET+"— поднять предмет  ")
        print(Fore.GREEN+"                           F"+Fore.RESET+" — взаимодействие  "+Fore.GREEN+" I"+Fore.RESET+" — инвентарь  "+Fore.GREEN+" Q"+Fore.RESET+" — выход  "+Fore.RESET)

        
        action = get_char()
        
        player_moved = False
        
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
                    
                    # If it's a key, update the key count
                    if isinstance(item, Key):
                        player.keys_found += 1
                        player.statistics.record_key_found()
                        message = f"Вы нашли {item.name}! ({player.keys_found}/3)"
                        
                    items.pop(i)
                    
                    # Check for victory
                    if player.has_all_keys():
                        display_victory_screen(player)
                        running = False
                        break
                    
                    break
            else:
                message = "Здесь нет предметов."
        elif action == 'f':  # New interaction key
            interaction_result = player.interact_with_character(dungeon, enemies)
            if interaction_result:
                interaction_message, interacted_character = interaction_result
                
                if isinstance(interacted_character, NeutralEnemy) and hasattr(interacted_character, 'current_riddle'):
                    riddle = interacted_character.current_riddle
                    options = riddle.get('варианты', [])
                    
                    title = f"Разговор с {interacted_character.name}"
                    answer_idx = display_dialog(title, interaction_message, options)
                    
                    if answer_idx >= 0:  # If not ESC
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
        
        # Check for victory after getting a key from Authority (or other source)
        if player.has_all_keys() and running:
            display_victory_screen(player)
            running = False
        
        if player_moved:
            dungeon[player.current_floor].update_fov(player.x, player.y)

            # Process enemy turns
            enemies_on_floor = [e for e in enemies if e.current_floor == player.current_floor]
            for enemy in enemies_on_floor:
                # Check if enemy is within explored area (optional, but good for performance/realism)
                if dungeon[player.current_floor].tiles[enemy.x][enemy.y].explored:
                    # Let the enemy decide its action (move or attack) based on its internal logic
                    action_message = enemy.take_turn(player, dungeon) 
                    if action_message: # Append enemy action message if take_turn returns one
                         message += f"\n{action_message}"

            # Check if player died after enemy turns
            if player.is_dead():
                os.system('cls' if os.name == 'nt' else 'clear')
                display_game_over(player)
                get_char()
                running = False 