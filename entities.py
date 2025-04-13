import random
from typing import List, Tuple, Optional
from colorama import Fore, Back, Style




class Character:
    """Базовый класс для всех персонажей в игре."""
    
    def __init__(self, x: int, y: int, char: str, name: str, hp: int, defense: int, power: int):
        self.x = x
        self.y = y
        self.char = char 
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.defense = defense
        self.power = power
        self.current_floor = 0
    
    def move(self, dx: int, dy: int, game_map) -> bool:
        """Перемещает персонажа, если это возможно."""
        floor = game_map[self.current_floor]
        
        new_x = self.x + dx
        new_y = self.y + dy
        
        if not floor.is_blocked(new_x, new_y):
            self.x = new_x
            self.y = new_y
            return True
        return False
    
    def distance_to(self, other) -> float:
        """Вычисляет расстояние до другого персонажа."""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
    def take_damage(self, amount: int) -> None:
        """Применяет урон к персонажу."""
        self.hp -= max(0, amount - self.defense)
        
    def heal(self, amount: int) -> int:
        """Восстанавливает здоровье персонажу."""
        if self.hp == self.max_hp:
            return 0
            
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp
    
    def is_dead(self) -> bool:
        """Проверяет, мертв ли персонаж."""
        return self.hp <= 0


class Player(Character):
    """Класс игрового персонажа."""
    
    def __init__(self, x: int, y: int, name: str = "Заключенный"):
        super().__init__(x, y,Back.BLACK + '@' + Back.RESET, name, hp=100, defense=1, power=5)
        self.inventory = Inventory()
        self.equipped_weapon = Fists()

        self.inventory.weapon_slot.item = self.equipped_weapon
    
    def attack(self, target: Character) -> int:
        """Атакует противника с использованием оружия."""
        damage = self.power
        if self.equipped_weapon:
            damage += self.equipped_weapon.damage
        
        target.take_damage(damage)
        return damage
    
    def use_stairs(self, game_map) -> bool:
        """Использует лестницу для перехода между этажами."""
        floor = game_map[self.current_floor]
        tile = floor.tiles[self.x][self.y]
        
        if tile.tile_type == 4 and self.current_floor < len(game_map) - 1:
            self.current_floor += 1
            
            next_floor = game_map[self.current_floor]
            if next_floor.stairs_down:
                self.x, self.y = next_floor.stairs_down[0]
            return True
            
        elif tile.tile_type == 5 and self.current_floor > 0:
            self.current_floor -= 1
            
            prev_floor = game_map[self.current_floor]
            if prev_floor.stairs_up:
                self.x, self.y = prev_floor.stairs_up[0]
            return True
            
        return False
    
    def equip_weapon(self, weapon: 'Weapon') -> Optional['Weapon']:
        """Экипирует оружие и возвращает предыдущее."""
        old_weapon = self.equipped_weapon
        self.equipped_weapon = weapon
        return old_weapon
    
    def eat_food(self, food: 'Food') -> int:
        """Съедает пищу и получает восстановление здоровья."""
        health_recovered = self.heal(food.nutrition)
        self.inventory.remove_item(food)
        return health_recovered


class Enemy(Character):
    """Базовый класс для всех врагов."""
    
    def __init__(self, x: int, y: int, char: str, name: str, hp: int, defense: int, power: int):
        super().__init__(x, y, char, name, hp, defense, power)
        self.xp_reward = hp
    
    def take_turn(self, player, game_map) -> None:
        """Выполняет ход врага."""
        pass


class HostileEnemy(Enemy):
    """Класс враждебного противника, атакующего игрока."""
    
    def __init__(self, x: int, y: int, char: str, name: str, hp: int, defense: int, power: int, view_range: int = 6):
        super().__init__(x, y, char, name, hp, defense, power)
        self.view_range = view_range
    
    def take_turn(self, player, game_map) -> None:
        """Выполняет ход враждебного противника."""
        if self.distance_to(player) <= self.view_range:
            distance = self.distance_to(player)
            
            if distance <= 1.5:
                damage = self.power
                player.take_damage(damage)
                print(f"{self.name} атакует вас, нанося {damage} урона!")
            else:
                dx = 0
                dy = 0
                
                if self.x < player.x:
                    dx = 1
                elif self.x > player.x:
                    dx = -1
                    
                if self.y < player.y:
                    dy = 1
                elif self.y > player.y:
                    dy = -1

                if dx != 0 and self.move(dx, 0, game_map):
                    return
                if dy != 0 and self.move(0, dy, game_map):
                    return
                
                if random.random() < 0.5:
                    self.move(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]), game_map)
        else:
            if random.random() < 0.5:
                dx = random.choice([-1, 0, 1])
                dy = random.choice([-1, 0, 1])
                self.move(dx, dy, game_map)


class NeutralEnemy(Enemy):
    """Класс нейтрального персонажа, который не атакует первым."""
    
    def __init__(self, x: int, y: int, char: str, name: str, hp: int, defense: int, power: int):
        super().__init__(x, y, char, name, hp, defense, power)
        self.aggravated = False
    
    def take_turn(self, player, game_map) -> None:
        """Выполняет ход нейтрального противника."""
        if self.aggravated and self.distance_to(player) <= 8:
            if self.distance_to(player) <= 1.5:
                damage = self.power
                player.take_damage(damage)
                print(f"{self.name} атакует вас, нанося {damage} урона!")
            else:
                dx = 0
                dy = 0
                
                if self.x < player.x:
                    dx = 1
                elif self.x > player.x:
                    dx = -1
                    
                if self.y < player.y:
                    dy = 1
                elif self.y > player.y:
                    dy = -1

                if dx != 0 and self.move(dx, 0, game_map):
                    return
                if dy != 0 and self.move(0, dy, game_map):
                    return
        else:
            if random.random() < 0.3:
                dx = random.choice([-1, 0, 1])
                dy = random.choice([-1, 0, 1])
                self.move(dx, dy, game_map)
    
    def take_damage(self, amount: int) -> None:
        """При получении урона персонаж становится враждебным."""
        super().take_damage(amount)
        self.aggravated = True


class Dog(HostileEnemy):
    """Класс враждебной собаки."""
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 'D', "Злая собака", hp=20, defense=0, power=3, view_range=8)


class Police(HostileEnemy):
    """Базовый класс для полицейских."""
    
    def __init__(self, x: int, y: int, char: str, name: str, hp: int, defense: int, power: int):
        super().__init__(x, y, char, name, hp, defense, power)


class Guard(Police):
    """Класс охранника - полицейский с дубинкой."""
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 'G', "Охранник", hp=30, defense=2, power=5)
        self.weapon = Baton()
    
    def take_turn(self, player, game_map) -> None:
        """Охранник агрессивнее и наносит больше урона благодаря дубинке."""
        if self.distance_to(player) <= 8:
            if self.distance_to(player) <= 1.5:
                damage = self.power + self.weapon.damage
                player.take_damage(damage)
                print(f"{self.name} бьет вас дубинкой, нанося {damage} урона!")
            else:
                dx = 0
                dy = 0
                
                if self.x < player.x:
                    dx = 1
                elif self.x > player.x:
                    dx = -1
                    
                if self.y < player.y:
                    dy = 1
                elif self.y > player.y:
                    dy = -1
                
                if dx != 0 and dy != 0 and self.move(dx, dy, game_map):
                    return
                if dx != 0 and self.move(dx, 0, game_map):
                    return
                if dy != 0 and self.move(0, dy, game_map):
                    return
        else:
            if random.random() < 0.7:
                dx = random.choice([-1, 0, 1])
                dy = random.choice([-1, 0, 1])
                self.move(dx, dy, game_map)


class Shooter(Police):
    """Класс стрелка - полицейский с пистолетом."""
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 'S', "Стрелок", hp=25, defense=1, power=3)
        self.weapon = Gun()
        self.shoot_range = 5
    
    def take_turn(self, player, game_map) -> None:
        """Стрелок может атаковать на расстоянии."""
        distance = self.distance_to(player)
        
        if distance <= self.shoot_range:
            damage = self.power + self.weapon.damage
            player.take_damage(damage)
            print(f"{self.name} стреляет в вас, нанося {damage} урона!")
        elif distance <= 8:
            dx = 0
            dy = 0
            
            if self.x < player.x:
                dx = -1
            elif self.x > player.x:
                dx = 1
                
            if self.y < player.y:
                dy = -1
            elif self.y > player.y:
                dy = 1

            if dx != 0 and self.move(dx, 0, game_map):
                return
            if dy != 0 and self.move(0, dy, game_map):
                return
            
            if distance <= self.shoot_range:
                damage = self.power + self.weapon.damage
                player.take_damage(damage)
                print(f"{self.name} стреляет в вас, нанося {damage} урона!")
        else:
            if random.random() < 0.5:
                dx = random.choice([-1, 0, 1])
                dy = random.choice([-1, 0, 1])
                self.move(dx, dy, game_map)


class Downcast(NeutralEnemy):
    """Класс опущенного заключенного."""
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 'p', "Опущенный", hp=15, defense=0, power=2)
        self.has_item = random.random() < 0.3
    
    def on_death(self) -> Optional['Item']:
        """При смерти может выпасть предмет."""
        if self.has_item:
            items = [StaleBread(), Cockroach()]
            return random.choice(items)
        return None


class Authority(NeutralEnemy):
    """Класс авторитета - сильного заключенного."""
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 'A', "Авторитет", hp=40, defense=3, power=6)
        self.weapon = Shiv()
        self.has_good_item = random.random() < 0.5
    
    def take_turn(self, player, game_map) -> None:
        """Авторитет опаснее когда разозлен."""
        super().take_turn(player, game_map)
        
        if self.aggravated and self.distance_to(player) <= 1.5:
            damage = self.power + self.weapon.damage
            player.take_damage(damage)
            print(f"{self.name} атакует вас заточкой, нанося {damage} урона!")
    
    def on_death(self) -> Optional['Item']:
        """При смерти может выпасть хороший предмет."""
        if self.has_good_item:
            items = [Shiv(), CondensedMilk()]
            return random.choice(items)
        return None

class Item:
    """Базовый класс для всех предметов."""
    
    def __init__(self, name: str, char: str, color: str = 'white'):
        self.name = name
        self.char = char
        self.color = color
    
    def use(self, user) -> bool:
        """Использует предмет. Возвращает True, если предмет должен быть удален."""
        return False


class Weapon(Item):
    """Класс оружия."""
    
    def __init__(self, name: str, char: str, damage: int, color: str = 'red'):
        super().__init__(name, char, color)
        self.damage = damage
    
    def use(self, user: Player) -> bool:
        """Экипировать оружие."""
        old_weapon = user.equip_weapon(self)
        if old_weapon and old_weapon.name != "Кулаки":
            user.inventory.add_item(old_weapon)
        return True


class Fists(Weapon):
    """Класс кулаков - базовое оружие."""
    
    def __init__(self):
        super().__init__("Кулаки", '*', damage=0, color='white')
    
    def use(self, user: Player) -> bool:
        """Кулаки нельзя использовать как предмет."""
        return False


class Baton(Weapon):
    """Класс полицейской дубинки."""
    
    def __init__(self):
        super().__init__("Полицейская дубинка", '🏏', damage=5, color='blue')


class Shiv(Weapon):
    """Класс заточки."""
    
    def __init__(self):
        super().__init__("Заточка",Back.BLACK + '🔪' + Back.RESET, damage=7, color='silver')


class Gun(Weapon):
    """Класс пистолета."""
    
    def __init__(self):
        super().__init__("Пистолет",Back.BLACK + '🔫' + Back.RESET, damage=10, color='darkgrey')


class Food(Item):
    """Класс еды."""
    
    def __init__(self, name: str, char: str, nutrition: int, color: str = 'green'):
        super().__init__(name, char, color)
        self.nutrition = nutrition
    
    def use(self, user: Player) -> bool:
        """Съесть пищу, восстановив здоровье."""
        health_recovered = user.eat_food(self)
        print(f"Вы съели {self.name} и восстановили {health_recovered} здоровья.")
        return True


class Cockroach(Food):
    """Класс таракана - минимальная еда."""
    
    def __init__(self):
        super().__init__("Таракан",Back.BLACK + '🪳' + Back.RESET, nutrition=1, color='brown')


class StaleBread(Food):
    """Класс засохшего хлеба - обычная еда."""
    
    def __init__(self):
        super().__init__("Засохший хлеб",Back.BLACK + '🥖' + Back.RESET, nutrition=5, color='tan')


class PrisonFood(Food):
    """Класс тюремного хрючева - средняя еда."""
    
    def __init__(self):
        super().__init__("Тюремное хрючево",Back.BLACK + '🍲' + Back.RESET, nutrition=10, color='yellow')


class CondensedMilk(Food):
    """Класс сгущенки - лучшая еда."""
    
    def __init__(self):
        super().__init__("Сгущенка",Back.BLACK + '🍯' + Back.RESET, nutrition=20, color='white')

class Slot:
    """Базовый класс слота инвентаря."""
    
    def __init__(self, name: str):
        self.name = name
        self.item = None
    
    def is_empty(self) -> bool:
        """Проверяет, пуст ли слот."""
        return self.item is None
    
    def can_contain(self, item: Item) -> bool:
        """Проверяет, может ли слот содержать данный предмет."""
        return True
    
    def put(self, item: Item) -> Optional[Item]:
        """Помещает предмет в слот. Возвращает вытесненный предмет, если такой есть."""
        if not self.can_contain(item):
            return item
            
        old_item = self.item
        self.item = item
        return old_item
    
    def take(self) -> Optional[Item]:
        """Забирает предмет из слота."""
        item = self.item
        self.item = None
        return item


class WeaponSlot(Slot):
    """Слот для оружия."""
    
    def __init__(self):
        super().__init__("Оружие")
    
    def can_contain(self, item: Item) -> bool:
        """Проверяет, может ли слот содержать данное оружие."""
        return isinstance(item, Weapon)


class KeySlot(Slot):
    """Слот для ключей."""
    
    def __init__(self):
        super().__init__("Ключ")
    
    def can_contain(self, item: Item) -> bool:
        """Проверяет, может ли слот содержать данный ключ."""
        return False


class FoodSlot(Slot):
    """Слот для еды."""
    
    def __init__(self):
        super().__init__("Еда")
    
    def can_contain(self, item: Item) -> bool:
        """Проверяет, может ли слот содержать данную еду."""
        return isinstance(item, Food)


class Inventory:
    """Класс инвентаря."""
    
    def __init__(self):
        self.weapon_slot = WeaponSlot()
        self.key_slots = [KeySlot() for _ in range(3)]
        self.food_slots = [FoodSlot() for _ in range(5)]
        self.general_items = []
    
    def add_item(self, item: Item) -> bool:
        """Добавляет предмет в инвентарь."""
        if isinstance(item, Weapon):
            if self.weapon_slot.is_empty():
                self.weapon_slot.put(item)
                return True
        elif isinstance(item, Food):
            for slot in self.food_slots:
                if slot.is_empty():
                    slot.put(item)
                    return True
        
        self.general_items.append(item)
        return True
    
    def get_all_items(self) -> List[Item]:
        """Возвращает список всех предметов в инвентаре."""
        items = []
        
        if not self.weapon_slot.is_empty():
            items.append(self.weapon_slot.item)
            
        for slot in self.key_slots:
            if not slot.is_empty():
                items.append(slot.item)
                
        for slot in self.food_slots:
            if not slot.is_empty():
                items.append(slot.item)
                
        items.extend(self.general_items)
        return items
        
    def remove_item(self, item: Item) -> bool:
        """Удаляет предмет из инвентаря независимо от типа слота."""
        if isinstance(item, Food):
            for slot in self.food_slots:
                if not slot.is_empty() and slot.item == item:
                    slot.take()
                    return True
        
        if not self.weapon_slot.is_empty() and self.weapon_slot.item == item and item.name != "Кулаки":
            self.weapon_slot.take()
            return True
        
        if item in self.general_items:
            self.general_items.remove(item)
            return True
        
        return False