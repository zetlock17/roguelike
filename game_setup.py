import random
from typing import List, Tuple
from colorama import Fore, Style, Back
from entities import (
    Player, Enemy, HostileEnemy, NeutralEnemy,
    Item, Weapon, Food, Key
)
from map_generator import Floor



"""Генерация врагов и предметов на карте
generate_enemies() - создает врагов разных типов на каждом этаже
generate_items() - размещает случайные предметы (еда, оружие) по карте
generate_random_key() - создает случайный ключ на одном из этажей"""



def generate_enemies(dungeon: List[Floor]) -> List[Enemy]:
    enemies = []
    key_holder_added = False

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


        # Добавляем носителя ключа на последний этаж
        if floor_idx == len(dungeon) - 1 and not key_holder_added:
            room = random.choice(floor.rooms)
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)
            if 0 <= x < floor.width and 0 <= y < floor.height:
                key_holder = HostileEnemy(x, y, 
                    "\033[91;47m➹\033[0m", "Стрелок", hp=25, defense=1, power=1, 
                    weapon=Weapon("Пистолет", "\033[47;30m⌐\033[0m", damage=10, color='darkgrey'), has_key=True)
                key_holder.current_floor = floor_idx
                enemies.append(key_holder)
                key_holder_added = True

    return enemies

def generate_items(dungeon: List[Floor]) -> List[Tuple[Item, int, int, int]]:
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
    return items

def generate_random_key(dungeon: List[Floor]) -> Tuple[Item, int, int, int]:
    random_key_floor = random.randint(0, len(dungeon) - 1)
    room = random.choice(dungeon[random_key_floor].rooms)
    key_x = random.randint(room.x1 + 1, room.x2 - 1)
    key_y = random.randint(room.y1 + 1, room.y2 - 1)
    if 0 <= key_x < dungeon[random_key_floor].width and 0 <= key_y < dungeon[random_key_floor].height:
        return Key(3), key_x, key_y, random_key_floor
    return None