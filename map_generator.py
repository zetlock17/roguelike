import random
from typing import List, Tuple, Set
from colorama import Fore, Back, Style
from entities import Item, Key


"""map_generator.py - Генерация карты
Tile, Room, Floor - классы для представления элементов карты"""


class Tile:
    EMPTY = 0
    FLOOR = 1
    WALL = 2
    CORRIDOR = 3
    STAIRS_UP = 4
    STAIRS_DOWN = 5

    def __init__(self, tile_type: int = EMPTY):
        self.tile_type = tile_type
        self.explored = False

    def __str__(self) -> str:
        if self.tile_type == Tile.EMPTY:
            return " "
        elif self.tile_type == Tile.FLOOR:
            return "\033[47m \033[0m"
        elif self.tile_type == Tile.WALL:
            return Fore.LIGHTBLACK_EX + Back.BLACK + "▒" + Style.RESET_ALL
        elif self.tile_type == Tile.CORRIDOR:
            return "\033[47m \033[0m"
        elif self.tile_type == Tile.STAIRS_UP:
            return Style.BRIGHT + "\033[32;47m⬆\033[0m" + Style.RESET_ALL
        elif self.tile_type == Tile.STAIRS_DOWN:
            return Style.BRIGHT + "\033[32;47m⬇\033[0m" + Style.RESET_ALL
        return " "

class Room:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.openings = []

    @property
    def center(self) -> Tuple[int, int]:
        return (self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2

    def intersects(self, other: 'Room') -> bool:
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

class Floor:
    # Класс Floor представляет собой отдельный этаж (уровень) подземелья.
    # Он хранит информацию о размере этажа, всех плитках (tiles), комнатах и лестницах.
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.tiles = [[Tile() for _ in range(height)] for _ in range(width)]
        self.rooms: List[Room] = []
        self.stairs_up: List[Tuple[int, int]] = []
        self.stairs_down: List[Tuple[int, int]] = []

    def update_fov(self, x: int, y: int, radius: int = 5) -> None:
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx**2 + dy**2 <= radius**2:
                    tx, ty = x + dx, y + dy
                    if 0 <= tx < self.width and 0 <= ty < self.height:
                        self.tiles[tx][ty].explored = True

    def is_blocked(self, x: int, y: int) -> bool:
        # Проверяет, заблокирована ли позиция (x, y) для перемещения.
        # Возвращает True, если:
        # - позиция за пределами карты
        # - в позиции находится стена (WALL) или пустота (EMPTY)
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[x][y].tile_type in (Tile.WALL, Tile.EMPTY)
        return True

    def is_valid_position(self, x: int, y: int) -> bool:
        # Проверяет, находится ли позиция (x, y) в пределах карты.
        # Используется для предотвращения выхода за границы карты.
        return 0 <= x < self.width and 0 <= y < self.height

class MapGenerator:
    # Класс MapGenerator отвечает за процедурную генерацию многоуровневого подземелья.
    # Он создает этажи с комнатами, коридорами и лестницами между уровнями.
    
    def __init__(self, width: int = 80, height: int = 40, num_floors: int = 3,
                 max_rooms: int = 15, min_room_size: int = 5, max_room_size: int = 10):
        # Инициализация генератора карты с параметрами:
        # - width, height: размеры каждого этажа
        # - num_floors: количество уровней подземелья
        # - max_rooms: максимальное число комнат на этаж
        # - min/max_room_size: минимальный/максимальный размер комнат
        self.width = width
        self.height = height
        self.num_floors = num_floors
        self.max_rooms = max_rooms
        self.min_room_size = min_room_size
        self.max_room_size = max_room_size
        self.floors: List[Floor] = []

    def generate_map(self) -> List[Floor]:
        # Основной метод генерации карты, создающий все этажи подземелья
        # Для каждого этажа вызывает _generate_floor(), затем добавляет лестницы между этажами
        self.floors = []
        for floor_num in range(self.num_floors):
            floor = self._generate_floor()
            if floor.rooms:
                start_room = floor.rooms[0]
                start_x, start_y = start_room.center
                floor.update_fov(start_x, start_y)
            self.floors.append(floor)

        for floor_num in range(self.num_floors - 1):
            self._add_stairs(floor_num, floor_num + 1)
        return self.floors

    def _generate_floor(self) -> Floor:
        # Генерирует один этаж подземелья:
        # 1. Создает объект Floor
        # 2. Пытается разместить случайные комнаты (до max_rooms)
        # 3. При размещении проверяет, не пересекается ли новая комната с существующими
        # 4. Соединяет каждую новую комнату с ближайшей из уже соединенных
        # 5. В конце проверяет связность всех комнат
        floor = Floor(self.width, self.height)
        safe_margin = 3
        connected_rooms = []

        for _ in range(self.max_rooms):
            w = random.randint(self.min_room_size, self.max_room_size)
            h = random.randint(self.min_room_size, self.max_room_size)
            x = random.randint(safe_margin, self.width - w - safe_margin)
            y = random.randint(safe_margin, self.height - h - safe_margin)

            new_room = Room(x, y, w, h)
            if any(new_room.intersects(other_room) for other_room in floor.rooms):
                continue

            self._create_room(floor, new_room)
            floor.rooms.append(new_room)

            if connected_rooms:
                closest_room = min(connected_rooms, key=lambda r: self._calculate_distance(new_room, r))
                self._connect_rooms(floor, new_room, closest_room)
            else:
                connected_rooms.append(new_room)

        self._ensure_connectivity(floor)
        return floor

    def _create_room(self, floor: Floor, room: Room) -> None:
        # Создает комнату на карте, устанавливая соответствующие типы плиток:
        # - Внутренность комнаты: плитки типа FLOOR
        # - Периметр комнаты: плитки типа WALL
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                floor.tiles[x][y].tile_type = Tile.FLOOR
        for x in range(room.x1, room.x2 + 1):
            floor.tiles[x][room.y1].tile_type = Tile.WALL
            floor.tiles[x][room.y2].tile_type = Tile.WALL
        for y in range(room.y1, room.y2 + 1):
            floor.tiles[room.x1][y].tile_type = Tile.WALL
            floor.tiles[room.x2][y].tile_type = Tile.WALL

    def _connect_rooms(self, floor: Floor, room1: Room, room2: Room) -> None:
        # Соединяет две комнаты коридором:
        # 1. Находит подходящие точки выхода из каждой комнаты
        # 2. Создает L-образный коридор между этими точками
        # 3. Добавляет выходы в список отверстий каждой комнаты
        x1, y1 = room1.center
        x2, y2 = room2.center

        # Choose closest valid opening points
        opening1 = self._find_valid_opening(floor, room1, x2, y2)
        opening2 = self._find_valid_opening(floor, room2, x1, y1)

        if not (opening1 and opening2):
            return

        ox1, oy1 = opening1
        ox2, oy2 = opening2

        floor.tiles[ox1][oy1].tile_type = Tile.CORRIDOR
        floor.tiles[ox2][oy2].tile_type = Tile.CORRIDOR
        room1.openings.append((ox1, oy1))
        room2.openings.append((ox2, oy2))

        # Create L-shaped corridor
        if random.random() < 0.5:
            self._create_horizontal_tunnel(floor, ox1, ox2, oy1)
            self._create_vertical_tunnel(floor, oy1, oy2, ox2)
        else:
            self._create_vertical_tunnel(floor, oy1, oy2, ox1)
            self._create_horizontal_tunnel(floor, ox1, ox2, oy2)

    def _find_valid_opening(self, floor: Floor, room: Room, target_x: int, target_y: int) -> Tuple[int, int]:
        # Ищет лучшую точку для прокладки коридора из комнаты:
        # 1. Перебирает все стены комнаты
        # 2. Находит точку, ближайшую к целевым координатам
        best_opening = None
        min_dist = float('inf')
        center_x, center_y = room.center

        # Check all walls for valid openings
        for x in range(room.x1 + 1, room.x2):
            for y in (room.y1, room.y2):
                if floor.is_valid_position(x, y) and floor.tiles[x][y].tile_type == Tile.WALL:
                    dist = ((x - target_x) ** 2 + (y - target_y) ** 2) ** 0.5
                    if dist < min_dist:
                        min_dist = dist
                        best_opening = (x, y)
        for y in range(room.y1 + 1, room.y2):
            for x in (room.x1, room.x2):
                if floor.is_valid_position(x, y) and floor.tiles[x][y].tile_type == Tile.WALL:
                    dist = ((x - target_x) ** 2 + (y - target_y) ** 2) ** 0.5
                    if dist < min_dist:
                        min_dist = dist
                        best_opening = (x, y)

        return best_opening or room.center

    def _create_horizontal_tunnel(self, floor: Floor, x1: int, x2: int, y: int) -> None:
        # Создает горизонтальный коридор от x1 до x2 на высоте y
        if not (0 <= y < floor.height):
            return
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if floor.is_valid_position(x, y) and floor.tiles[x][y].tile_type != Tile.FLOOR:
                floor.tiles[x][y].tile_type = Tile.CORRIDOR
            self._add_tunnel_walls(floor, x, y)

    def _create_vertical_tunnel(self, floor: Floor, y1: int, y2: int, x: int) -> None:
        # Создает вертикальный коридор от y1 до y2 на позиции x
        if not (0 <= x < floor.width):
            return
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if floor.is_valid_position(x, y) and floor.tiles[x][y].tile_type != Tile.FLOOR:
                floor.tiles[x][y].tile_type = Tile.CORRIDOR
            self._add_tunnel_walls(floor, x, y)

    def _add_tunnel_walls(self, floor: Floor, x: int, y: int) -> None:
        # Добавляет стены вокруг коридора, чтобы коридор был окружен стенами
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            tx, ty = x + dx, y + dy
            if (floor.is_valid_position(tx, ty) and
                floor.tiles[tx][ty].tile_type == Tile.EMPTY):
                floor.tiles[tx][ty].tile_type = Tile.WALL

    def _ensure_connectivity(self, floor: Floor) -> None:
        # Проверяет и обеспечивает, чтобы все комнаты на этаже были соединены:
        # 1. Находит все уже соединенные комнаты
        # 2. Для каждой несоединенной комнаты находит ближайшую соединенную
        # 3. Создает коридор между ними
        if not floor.rooms:
            return

        connected = self._find_connected_rooms(floor, 0)
        for i, room in enumerate(floor.rooms):
            if i not in connected:
                closest_idx = min(connected, key=lambda j: self._calculate_distance(room, floor.rooms[j]))
                self._connect_rooms(floor, room, floor.rooms[closest_idx])
                connected.update(self._find_connected_rooms(floor, i))

    def _find_connected_rooms(self, floor: Floor, start_idx: int) -> Set[int]:
        # Находит все комнаты, соединенные с комнатой start_idx:
        # Использует поиск в глубину по графу комнат и коридоров
        if not floor.rooms:
            return set()

        visited = set()
        stack = [(start_idx, opening) for opening in floor.rooms[start_idx].openings]
        while stack:
            room_idx, (x, y) = stack.pop()
            if room_idx in visited:
                continue
            visited.add(room_idx)

            # Check adjacent tiles for connected corridors
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (floor.is_valid_position(nx, ny) and
                    floor.tiles[nx][ny].tile_type == Tile.CORRIDOR):
                    for i, other_room in enumerate(floor.rooms):
                        if i != room_idx and (nx, ny) in other_room.openings:
                            stack.append((i, (nx, ny)))
        return visited

    def _calculate_distance(self, room1: Room, room2: Room) -> float:
        # Вычисляет евклидово расстояние между центрами двух комнат
        x1, y1 = room1.center
        x2, y2 = room2.center
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def _add_stairs(self, floor_num: int, next_floor_num: int) -> None:
        # Добавляет лестницы между этажами:
        # 1. Случайно выбирает комнаты на обоих этажах
        # 2. Размещает лестницу вверх в центре комнаты на нижнем этаже
        # 3. Размещает лестницу вниз в центре комнаты на верхнем этаже
        current_floor = self.floors[floor_num]
        next_floor = self.floors[next_floor_num]

        room_up = random.choice(current_floor.rooms)
        x_up, y_up = room_up.center
        x_up = max(1, min(current_floor.width - 2, x_up))
        y_up = max(1, min(current_floor.height - 2, y_up))
        current_floor.tiles[x_up][y_up].tile_type = Tile.STAIRS_UP
        current_floor.stairs_up.append((x_up, y_up))

        room_down = random.choice(next_floor.rooms)
        x_down, y_down = room_down.center
        x_down = max(1, min(next_floor.width - 2, x_down))
        y_down = max(1, min(next_floor.height - 2, y_down))
        next_floor.tiles[x_down][y_down].tile_type = Tile.STAIRS_DOWN
        next_floor.stairs_down.append((x_down, y_down))

    def print_map(self, floor_num: int, player=None) -> None:
        # Отображает карту этажа в консоли:
        # - Показывает только исследованные плитки
        # - Если передан игрок, отображает его символом @
        if floor_num < 0 or floor_num >= len(self.floors):
            print(f"Этаж {floor_num} не существует!")
            return
        floor = self.floors[floor_num]
        for y in range(floor.height):
            row = ""
            for x in range(floor.width):
                tile = floor.tiles[x][y]
                if player and player.current_floor == floor_num and player.x == x and player.y == y:
                    row += "@"
                else:
                    row += str(tile) if tile.explored else " "
            print(row)
    
    def generate_random_key(self, dungeon: List[Floor]) -> Tuple[Item, int, int, int]:
        random_key_floor = random.randint(0, len(dungeon) - 1)
        room = random.choice(dungeon[random_key_floor].rooms)
        key_x = random.randint(room.x1 + 1, room.x2 - 1)
        key_y = random.randint(room.y1 + 1, room.y2 - 1)
        if 0 <= key_x < dungeon[random_key_floor].width and 0 <= key_y < dungeon[random_key_floor].height:
            return Key(3), key_x, key_y, random_key_floor
        return None