import os
from colorama import Fore, Style
from entities import Player, Enemy, Item
from map_generator import Floor
from typing import List, Tuple, Optional


"""renderer.py - отрисовка игры:
render_game() - выводит текущее состояние игры (карту, персонажей, интерфейс)"""

def render_game(player: Player, dungeon: List[Floor], enemies: List[Enemy], items: List[Tuple[Item, int, int, int]], message: str):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("                                                                                       ")
    print(Style.BRIGHT + Fore.CYAN + f"                           Этаж {player.current_floor + 1} " +
          Fore.RED + f"  HP: {player.hp}/{player.max_hp} " +
          Fore.MAGENTA + f"  Оружие: {player.equipped_weapon.name}     " + Fore.RESET + Style.RESET_ALL)
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

    print("\n " + Fore.RESET)
    print(Fore.GREEN + "                   SPACE" + Fore.RESET + " — атака  " +
          Fore.GREEN + " E" + Fore.RESET + " — использовать лестницу  " +
          Fore.GREEN + " G " + Fore.RESET + "— поднять предмет  ")
    print(Fore.GREEN + "                           F" + Fore.RESET + " — взаимодействие  " +
          Fore.GREEN + " I" + Fore.RESET + " — инвентарь  " +
          Fore.GREEN + " Q" + Fore.RESET + " — выход  " + Fore.RESET)