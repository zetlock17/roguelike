import random
import os
import msvcrt

from entities import (
    Player, Dog, Guard, Shooter, Downcast, Authority,
    Fists, Baton, Shiv, Gun, Cockroach, StaleBread, PrisonFood, CondensedMilk,
    Item
)

from map_generator import MapGenerator

def get_char():
    return msvcrt.getch().decode('utf-8').lower()
    
if __name__ == "__main__":
    map_generator = MapGenerator(width=80, height=24, num_floors=3)
    dungeon = map_generator.generate_map()

    start_x, start_y = dungeon[0].rooms[0].center
    player = Player(start_x, start_y, "Заключенный #42")

    enemies = []
    
    for floor_idx, floor in enumerate(dungeon):
        for room in floor.rooms[1:]:
            if random.random() < 0.7:
                x, y = room.center

                enemy_type = random.random()
                
                if floor_idx == 0:
                    if enemy_type < 0.4:
                        enemies.append(Dog(x, y))
                    elif enemy_type < 0.7:
                        enemies.append(Downcast(x, y))
                    else:
                        enemies.append(Guard(x, y))
                elif floor_idx == 1:
                    if enemy_type < 0.3:
                        enemies.append(Guard(x, y))
                    elif enemy_type < 0.6:
                        enemies.append(Downcast(x, y))
                    elif enemy_type < 0.8:
                        enemies.append(Authority(x, y))
                    else:
                        enemies.append(Shooter(x, y))
                else:
                    if enemy_type < 0.3:
                        enemies.append(Authority(x, y))
                    elif enemy_type < 0.6:
                        enemies.append(Shooter(x, y))
                    else:
                        enemies.append(Guard(x, y))

    items = []

    for floor_idx, floor in enumerate(dungeon):
        for room in floor.rooms:
            if random.random() < 0.5:
                x, y = random.randint(room.x1 + 1, room.x2 - 1), random.randint(room.y1 + 1, room.y2 - 1)

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
    
    while running:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"Этаж {player.current_floor + 1} | HP: {player.hp}/{player.max_hp} | Оружие: {player.equipped_weapon.name}")
        
        current_floor = player.current_floor
        floor = dungeon[current_floor]
        
        for y in range(floor.height):
            row = ""
            for x in range(floor.width):
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
                            row += str(floor.tiles[x][y])
            print(row)
        
        if message:
            print(message)
            message = ""
            
        print("\nУправление: W=вверх, A=влево, S=вниз, D=вправо, SPACE=атака, E=использовать лестницу, G=поднять предмет, I=инвентарь, Q=выход")
        
        action = get_char()
        
        # Обработка действий игрока
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
                    items.pop(i)
                    break
            else:
                message = "Здесь нет предметов."
        elif action == 'i':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("=== ИНВЕНТАРЬ ===")
            print(f"Экипировано: {player.equipped_weapon.name}")
            
            all_items = player.inventory.get_all_items()
            if not all_items:
                print("Инвентарь пуст.")
            else:
                for i, item in enumerate(all_items):
                    print(f"{i+1}. {item.name}")
                
                print("\nВыберите предмет для использования (или Esc для выхода):")
                
                while True:
                    key = get_char()
                    if key == '\x1b':
                        break
                    
                    try:
                        index = int(key) - 1
                        if 0 <= index < len(all_items):
                            item = all_items[index]
                            if item.use(player):
                                if isinstance(item, Weapon) and item != player.equipped_weapon:
                                    player.inventory.general_items.remove(item)
                                    message = f"Вы экипировали {item.name}."
                                elif item in player.inventory.general_items:
                                    player.inventory.general_items.remove(item)
                            break
                    except ValueError:
                        continue
        elif action == 'q':
            running = False
        
        if player_moved:
            for enemy in enemies:
                if enemy.current_floor == player.current_floor:
                    if enemy.distance_to(player) <= 1.5:
                        if isinstance(enemy, Guard):
                            damage = enemy.power + enemy.weapon.damage
                        elif isinstance(enemy, Shooter) and enemy.distance_to(player) <= 1.5:
                            damage = enemy.power + enemy.weapon.damage
                        elif isinstance(enemy, Authority) and enemy.aggravated:
                            damage = enemy.power + enemy.weapon.damage
                        else:
                            damage = enemy.power
                        
                        player.take_damage(damage)
                        message += f"\n{enemy.name} атакует вас, нанося {damage} урона!"
                    else:
                        enemy.take_turn(player, dungeon)

            if player.is_dead():
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Вы погибли!")
                print("\nНажмите любую клавишу для выхода...")
                get_char()
                running = False