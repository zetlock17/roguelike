class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Person:
    def __init__(self, health, position):
        self.health = health
        self.max_health = health
        self.position = position        
        self.inventory = Inventory(5)

    def atack_person(self, person):
        total_damage = 0
        for i in self.inventory.items:
            if isinstance(i, Sword):
                total_damage += i.damage
        
        person.health -= total_damage

    def get_state(self):
        return f"Здоровье: {self.health}/{self.max_health}"

class Hero(Person):
    def __init__(self, health, position, symbol):
        super().__init__(health, position)
        self.symbol = symbol

class Enemy(Person):
    def __init__(self, health, position, symbol):
        super().__init__(health, position)
        self.symbol = symbol

class Item:
    def __init__(self, title, type):
        self.title = title
        self.type = type

class Sword(Item):
    def __init__(self, title, type, damage):
        super().__init__(title, type)
        self.damage = damage

class Inventory:
    def __init__(self, size, items=[]):
        self.items = items
        self.size = size
    
    def add_item(self, item):
        if len(self.items) < self.size:
            self.items.append(item)

player = Hero(20, Position(0, 0), "%")
enemy = Enemy(10, Position(1, 1), "!")

sword = Sword("Меч", "sword", 5)
player.inventory.add_item(sword)

player.atack_person(enemy)

print(player.get_state())
print(enemy.get_state())
