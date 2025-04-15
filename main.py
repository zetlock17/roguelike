import random
import os
import msvcrt
import time
from colorama import Fore, Back, Style

from entities import (
    Player, Dog, Guard, Shooter, Downcast, Authority,
    Fists, Baton, Shiv, Gun, Cockroach, StaleBread, PrisonFood, CondensedMilk,
    Item, Weapon
)

from statistic import Statistics
from map_generator import MapGenerator
from introductory_screen import show_title_screen, transition_to_game
from input_handler import get_char

def display_game_over(player: Player): # ф-ия отображения статистики
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + player.statistics.display())
                                                                                                          
    print("                                                                                        ")
    print("            "+Fore.RED+ Style.BRIGHT+"              Нажмите любую клавишу для выхода..."+Style.RESET_ALL+Fore.RESET+"                           ")
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
                        enemy = Dog(x, y)
                        enemy.current_floor = floor_idx
                        enemies.append(enemy)
                    elif enemy_type < 0.7:
                        enemy = Downcast(x, y)
                        enemy.current_floor = floor_idx
                        enemies.append(enemy)
                    else:
                        enemy = Guard(x, y)
                        enemy.current_floor = floor_idx
                        enemies.append(enemy)
                elif floor_idx == 1:
                    if enemy_type < 0.3:
                        enemy = Guard(x, y)
                        enemy.current_floor = floor_idx
                        enemies.append(enemy)
                    elif enemy_type < 0.6:
                        enemy = Downcast(x, y)
                        enemy.current_floor = floor_idx
                        enemies.append(enemy)
                    elif enemy_type < 0.8:
                        enemy = Authority(x, y)
                        enemy.current_floor = floor_idx
                        enemies.append(enemy)
                    else:
                        enemy = Shooter(x, y)
                        enemy.current_floor = floor_idx
                        enemies.append(enemy)
                else:
                    if enemy_type < 0.3:
                        enemy = Authority(x, y)
                        enemy.current_floor = floor_idx
                        enemies.append(enemy)
                    elif enemy_type < 0.6:
                        enemy = Shooter(x, y)
                        enemy.current_floor = floor_idx
                        enemies.append(enemy)
                    else:
                        enemy = Guard(x, y)
                        enemy.current_floor = floor_idx
                        enemies.append(enemy)

    items = []

    for floor_idx, floor in enumerate(dungeon):
        for room in floor.rooms:
            if random.random() < 0.5:
                x = random.randint(room.x1 + 1, room.x2 - 1)
                y = random.randint(room.y1 + 1, room.y2 - 1)
                
                if not (0 <= x < floor.width and 0 <= y < floor.height):
                    continue
                
                item_type = random.random()
                
                if item_type < 0.3:
                    items.append((Cockroach(), x, y, floor_idx))
                elif item_type < 0.6:
                    items.append((StaleBread(), x, y, floor_idx))
                elif item_type < 0.8:
                    items.append((PrisonFood(), x, y, floor_idx))
                elif item_type < 0.9:
                    items.append((Shiv(), x, y, floor_idx))
                elif item_type < 0.95:
                    items.append((Baton(), x, y, floor_idx))
                else:
                    items.append((Gun(), x, y, floor_idx))

    running = True
    message = ""
    
    dungeon[player.current_floor].update_fov(player.x, player.y)


    
    while running:
        os.system('cls' if os.name == 'nt' else 'clear')
                                                                                                            
        print("                                                                                       ")
        print(Style.BRIGHT+Fore.CYAN+f"                                 Этаж {player.current_floor + 1} "+Fore.RED + f"  HP: {player.hp}/{player.max_hp} "+Fore.MAGENTA+f"  Оружие: {player.equipped_weapon.name}     "+Fore.RESET + Style.RESET_ALL)
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

        print("\n┌─────────────────────────────────────────────────────────────────────────────────────────────┐"+Fore.RESET) 
        print("│"+Fore.GREEN+" SPACE"+Fore.RESET+" — атака |"+Fore.GREEN+" E"+Fore.RESET+" — использовать лестницу |"+Fore.GREEN+" G "+Fore.RESET+"— поднять предмет |"+Fore.GREEN+" I"+Fore.RESET+" — инвентарь |"+Fore.GREEN+" Q"+Fore.RESET+" — выход │"+Fore.RESET)
        print("└─────────────────────────────────────────────────────────────────────────────────────────────┘"+Fore.RESET)

        
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
                    items.pop(i)
                    break
            else:
                message = "Здесь нет предметов."
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