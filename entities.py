import random
import json
from typing import List, Tuple, Optional
from colorama import Fore, Back, Style
from statistic import Statistics
    

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
        super().__init__(x, y, Style.BRIGHT + "\033[32;47m✧\033[0m" + Fore.RESET+ Back.RESET, 
                         name, hp=100, defense=1, power=5)
        self.inventory = Inventory()
        self.equipped_weapon = Weapon("Кулаки", '*', damage=0, color='white')
        self.inventory.weapon_slot.item = self.equipped_weapon
        self.statistics = Statistics()
        self.keys_found = 0

    def take_damage(self, amount: int) -> None:
        """Применяет урон к игроку и записывает его в статистику."""
        actual_damage = max(0, amount - self.defense)
        self.hp -= actual_damage
        self.statistics.record_damage_taken(actual_damage)
    
    def attack(self, target: Character) -> int:
        """Атакует противника с использованием оружия."""
        self.statistics.record_attack()
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
            self.statistics.record_floor_visited(self.current_floor)
            next_floor = game_map[self.current_floor]
            if next_floor.stairs_down:
                self.x, self.y = next_floor.stairs_down[0]
            return True
            
        elif tile.tile_type == 5 and self.current_floor > 0:
            self.current_floor -= 1
            self.statistics.record_floor_visited(self.current_floor)
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
        self.statistics.record_food_eaten()
        return health_recovered
    
    def interact_with_character(self, game_map, enemies) -> Optional[Tuple[str, Optional['Character']]]:
        """Взаимодействует с персонажем рядом с игроком."""
        for enemy in enemies:
            if enemy.current_floor == self.current_floor and self.distance_to(enemy) <= 1.5:
                if hasattr(enemy, 'interact'):
                    return enemy.interact(self)
        return None

    def has_all_keys(self) -> bool:
        """Проверяет, собрал ли игрок все ключи."""
        return self.keys_found >= 3


class Enemy(Character):
    """Базовый класс для всех врагов."""
    
    def __init__(self, x: int, y: int, char: str, name: str, hp: int, defense: int, power: int, xp_reward: int = None):
        super().__init__(x, y, char, name, hp, defense, power)
        self.xp_reward = xp_reward if xp_reward is not None else hp
        self.weapon = None
    
    def take_turn(self, player, game_map) -> Optional[str]:
        """Выполняет ход врага. Возвращает строку сообщения, если произошло действие (например, атака)."""
        pass
    
    def on_death(self) -> Optional['Item']:
        """При смерти может выпасть предмет."""
        return None


class HostileEnemy(Enemy):
    """Класс враждебного противника, атакующего игрока."""
    
    def __init__(self, x: int, y: int, char: str, name: str, hp: int, defense: int, power: int, 
                 view_range: int = 6, weapon: 'Weapon' = None, has_key: bool = False):
        super().__init__(x, y, char, name, hp, defense, power, weapon)
        self.view_range = view_range
        self.weapon = weapon
        self.has_key = has_key
        
    
    def take_turn(self, player, game_map) -> Optional[str]:
        """Выполняет ход враждебного противника."""
        message = None
        if self.distance_to(player) <= self.view_range:
            distance = self.distance_to(player)
            
            if distance <= 1.5:
                damage = self.power
                if self.weapon:
                    damage += self.weapon.damage
                player.take_damage(damage)
                weapon_name = f" с помощью {self.weapon.name}" if self.weapon else ""
                message = Fore.RED + f"{self.name} атакует вас{weapon_name}, нанося {damage} урона!" + Fore.RESET
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
                    return message
                if dy != 0 and self.move(0, dy, game_map):
                    return message
                
                if random.random() < 0.5:
                    self.move(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]), game_map)
        else:
            if random.random() < 0.5:
                dx = random.choice([-1, 0, 1])
                dy = random.choice([-1, 0, 1])
                self.move(dx, dy, game_map)
        return message
    
    def on_death(self) -> Optional['Item']:
        """При смерти может выпасть ключ."""
        if self.has_key:
            return Key(2)
        return None


class NeutralEnemy(Enemy):
    """Класс нейтрального персонажа, который не атакует первым."""
    
    def __init__(self, x: int, y: int, char: str, name: str, hp: int, defense: int, power: int, 
                 weapon: 'Weapon' = None, has_item: bool = False, has_riddle: bool = False):
        super().__init__(x, y, char, name, hp, defense, power)
        self.aggravated = False
        self.weapon = weapon
        self.has_item = has_item
        self.has_riddle = has_riddle
        self.has_given_riddle = False
        self.has_given_key = False
        self.riddle_failed = False
        self.current_riddle = None
    
    def take_turn(self, player, game_map) -> Optional[str]:
        """Выполняет ход нейтрального противника."""
        message = None
        if self.aggravated and self.distance_to(player) <= 8:
            if self.distance_to(player) <= 1.5:
                damage = self.power
                if self.weapon:
                    damage += self.weapon.damage
                player.take_damage(damage)
                weapon_name = f" {self.weapon.name}" if self.weapon else ""
                message = Fore.RED + f"{self.name} атакует вас{weapon_name}, нанося {damage} урона!" + Fore.RESET
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
                    return message
                if dy != 0 and self.move(0, dy, game_map):
                    return message
        else:
            if random.random() < 0.3:
                dx = random.choice([-1, 0, 1])
                dy = random.choice([-1, 0, 1])
                self.move(dx, dy, game_map)
        return message
    
    def take_damage(self, amount: int) -> None:
        """При получении урона персонаж становится враждебным."""
        aggravated_before = self.aggravated
        super().take_damage(amount)
        if not aggravated_before and not self.is_dead():
            self.aggravated = True
    
    def on_death(self) -> Optional['Item']:
        """При смерти может выпасть предмет."""
        if self.has_item:
            items = [
                Food("Таракан", Style.BRIGHT + "\033[47;38;5;130m∿\033[0m" + Fore.RESET + Back.RESET + Style.RESET_ALL, 
                     nutrition=1, color='brown'),
                Food("Засохший хлеб", Style.BRIGHT + "\033[47;38;5;130m⬬\033[0m"+ Back.RESET + Style.RESET_ALL, 
                     nutrition=5, color='tan'),
                Weapon("Заточка", Style.BRIGHT + "\033[30;47m↾\033[0m" + Back.RESET + Fore.RESET + Style.RESET_ALL, 
                       damage=7, color='silver'),
                Food("Сгущенка", Style.BRIGHT + Fore.LIGHTWHITE_EX + '◎' + Fore.RESET + Back.RESET + Style.RESET_ALL, 
                     nutrition=20, color='white')
            ]
            return random.choice(items)
        return None
    
    def interact(self, player) -> Tuple[str, Optional['NeutralEnemy']]:
        """Взаимодействие с нейтральным персонажем."""
        if self.aggravated or self.riddle_failed:
            return f"{self.name} агрессивно настроен и не хочет с вами разговаривать!", self
        
        if self.has_given_key:
            return f"{self.name} говорит: 'У меня для тебя больше ничего нет, братан.'", self
        
        if not self.has_given_riddle and self.has_riddle:
            self.has_given_riddle = True
            return self.ask_riddle(player), self
        
        return f"{self.name} смотрит на вас, ожидая ответа на свою загадку.", self
    
    def ask_riddle(self, player) -> str:
        """Задает тюремную загадку."""
        try:
            with open('questions.json', 'r', encoding='utf-8') as f:
                riddles_data = json.load(f)
                
            riddles = riddles_data.get('тюремные_загадки', [])
            if not riddles:
                return f"{self.name} говорит: 'Хотел загадать тебе загадку, но что-то голова не варит...'"
            
            self.current_riddle = random.choice(riddles)
            return f"{self.name} говорит: '{self.current_riddle['вопрос']}'"
        except Exception as e:
            return f"{self.name} говорит: 'Хотел загадать тебе загадку, но не смог: {str(e)}'"
    
    def answer_riddle(self, answer_index: int, player) -> Tuple[bool, str]:
        """Проверяет ответ на загадку."""
        if not hasattr(self, 'current_riddle'):
            return False, f"{self.name} говорит: 'Я еще не задал тебе вопрос!'"
        
        correct_answer = self.current_riddle['правильный_ответ']
        
        if answer_index == correct_answer:
            self.has_given_key = True
            key = Key(1)
            player.inventory.add_item(key)
            player.keys_found += 1
            player.statistics.record_key_found()
            return True, f"{self.name} говорит: 'Правильно, браток! Вот тебе ключ от свободы.'"
        else:
            self.riddle_failed = True
            self.aggravated = True
            return False, f"{self.name} в ярости кричит: 'Неправильно! Ты нарушил воровской закон!'"


class Item:
    """Базовый класс для всех предметов."""
    
    def __init__(self, name: str, char: str, color: str = 'white'):
        self.name = name
        self.char = char
        self.color = color
    
    def use(self, user) -> bool:
        """Использует предмет. Возвращает True, если предмет должен быть удален."""
        return False


class Key(Item):
    """Класс ключа для побега."""
    
    def __init__(self, key_number: int = 1):
        super().__init__(f"Ключ #{key_number}", 
                        Style.BRIGHT + "\033[33;47m♔\033[0m" + Fore.RESET + Back.RESET, 
                        color='yellow')
        self.key_number = key_number
    
    def use(self, user: Player) -> bool:
        """Ключи нельзя использовать напрямую."""
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


class Food(Item):
    """Класс еды."""
    
    def __init__(self, name: str, char: str, nutrition: int, color: str = 'green'):
        super().__init__(name, char, color)
        self.nutrition = nutrition
    
    def use(self, user: Player) -> bool:
        """Съесть пищу, восстановив здоровье."""
        health_recovered = user.eat_food(self)
        print(Fore.GREEN + f"Вы съели {self.name} и восстановили {health_recovered} здоровья." + Fore.RESET)
        return True


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
        return isinstance(item, Key)


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