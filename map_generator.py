import random
from typing import List, Tuple, Dict, Optional, Set
from colorama import Fore, Back, Style


class Tile:
    """Представляет один тайл на карте."""
    
    EMPTY = 0     # Пустое пространство
    FLOOR = 1     # Пол комнаты
    WALL = 2      # Стена комнаты
    CORRIDOR = 3  # Коридор
    STAIRS_UP = 4 # Лестница вверх
    STAIRS_DOWN = 5 # Лестница вниз
    
    def __init__(self, tile_type: int = EMPTY):
        self.tile_type = tile_type
        self.explored = False
        
    def __str__(self) -> str:
        """Возвращает символьное отображение тайла."""
        if self.tile_type == Tile.EMPTY:
            return " "
        elif self.tile_type == Tile.FLOOR:
            return Back.BLACK+" "+Back.RESET
        elif self.tile_type == Tile.WALL:
            return Fore.LIGHTBLACK_EX + Back.BLACK+ "░" + Fore.RESET + Back.RESET
        elif self.tile_type == Tile.CORRIDOR:
            return Back.BLACK+" "+Back.RESET
        elif self.tile_type == Tile.STAIRS_UP:
            return Back.BLACK + "\033[38;5;130m▤\033[0m" + Back.RESET
        elif self.tile_type == Tile.STAIRS_DOWN:
            return Back.BLACK + "\033[38;5;130m▤\033[0m" + Back.RESET
        return " "

class Room:
    """Представляет комнату в подземелье."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.openings = []
        
    @property
    def center(self) -> Tuple[int, int]:
        """Возвращает координаты центра комнаты."""
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return center_x, center_y
    
    def intersects(self, other: 'Room') -> bool:
        """Проверяет, пересекается ли эта комната с другой."""
        return (
            self.x1 <= other.x2 and self.x2 >= other.x1 and
            self.y1 <= other.y2 and self.y2 >= other.y1
        )

class Floor:
    """Представляет один этаж подземелья."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.tiles = [[Tile() for _ in range(height)] for _ in range(width)]
        self.rooms: List[Room] = []
        self.stairs_up: List[Tuple[int, int]] = []
        self.stairs_down: List[Tuple[int, int]] = []

    def update_fov(self, x: int, y: int, radius: int = 5) -> None:
        """Обновляет исследованные тайлы вокруг позиции (x, y)."""
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx**2 + dy**2 <= radius**2:
                    tx = x + dx
                    ty = y + dy
                    if 0 <= tx < self.width and 0 <= ty < self.height:
                        self.tiles[tx][ty].explored = True
        
    def is_blocked(self, x: int, y: int) -> bool:
        """Проверяет, заблокирована ли клетка для прохождения."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[x][y].tile_type in (Tile.WALL, Tile.EMPTY)
        return True
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """Проверяет, является ли позиция допустимой."""
        return 0 <= x < self.width and 0 <= y < self.height

class MapGenerator:
    """Генерирует карту подземелья с несколькими этажами."""
    
    def __init__(self, width: int, height: int, num_floors: int = 3, 
                max_rooms: int = 15, min_room_size: int = 5, max_room_size: int = 10):
        self.width = width
        self.height = height
        self.num_floors = num_floors
        self.max_rooms = max_rooms
        self.min_room_size = min_room_size
        self.max_room_size = max_room_size
        self.floors: List[Floor] = []
        
    def generate_map(self) -> List[Floor]:
        """Генерирует полную карту подземелья с несколькими этажами."""
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
        """Генерирует один этаж с комнатами и коридорами."""
        floor = Floor(self.width, self.height)
        
        safe_margin = 3 
        
        for _ in range(self.max_rooms):
            w = random.randint(self.min_room_size, self.max_room_size)
            h = random.randint(self.min_room_size, self.max_room_size)
            
            x = random.randint(safe_margin, self.width - w - safe_margin)
            y = random.randint(safe_margin, self.height - h - safe_margin)
            
            new_room = Room(x, y, w, h)
            
            if any(new_room.intersects(other_room) for other_room in floor.rooms):
                continue

            self._create_room(floor, new_room)

            if floor.rooms:
                prev_room = floor.rooms[-1]
                self._connect_rooms(floor, prev_room, new_room)
            
            floor.rooms.append(new_room)
            
            if len(floor.rooms) > 2 and random.random() < 0.3:
                other_room = random.choice(floor.rooms[:-1])
                self._connect_rooms(floor, new_room, other_room)
        
        self._ensure_room_accessibility(floor)
        
        self._clean_dead_ends(floor)
                
        return floor
    
    def _connect_rooms(self, floor: Floor, room1: Room, room2: Room) -> None:
        """Соединяет две комнаты коридором."""
        center1_x, center1_y = room1.center
        center2_x, center2_y = room2.center

        if center2_x < center1_x:
            wall1 = 'left'
            wall2 = 'right'
        elif center2_x > center1_x:
            wall1 = 'right'
            wall2 = 'left'
        else:
            wall1 = random.choice(['left', 'right'])
            wall2 = 'left' if wall1 == 'right' else 'right'
        
        if center2_y < center1_y:
            wall1_alt = 'top'
            wall2_alt = 'bottom'
        elif center2_y > center1_y:
            wall1_alt = 'bottom'
            wall2_alt = 'top'
        else:
            wall1_alt = random.choice(['top', 'bottom'])
            wall2_alt = 'top' if wall1_alt == 'bottom' else 'bottom'

        if random.random() < 0.5 and center1_x != center2_x and center1_y != center2_y:
            wall1, wall2 = wall1_alt, wall2_alt

        opening1_x, opening1_y = None, None
        
        # Try to find a valid opening point on the chosen wall for room1
        if wall1 == 'top' and room1.y1 > 0:
            potential_x = [x for x in range(room1.x1 + 1, room1.x2) if floor.is_valid_position(x, room1.y1 - 1)]
            if potential_x: opening1_x = random.choice(potential_x)
            opening1_y = room1.y1
        elif wall1 == 'bottom' and room1.y2 < floor.height - 1:
            potential_x = [x for x in range(room1.x1 + 1, room1.x2) if floor.is_valid_position(x, room1.y2 + 1)]
            if potential_x: opening1_x = random.choice(potential_x)
            opening1_y = room1.y2
        elif wall1 == 'left' and room1.x1 > 0:
            opening1_x = room1.x1
            potential_y = [y for y in range(room1.y1 + 1, room1.y2) if floor.is_valid_position(room1.x1 - 1, y)]
            if potential_y: opening1_y = random.choice(potential_y)
        elif wall1 == 'right' and room1.x2 < floor.width - 1:
            opening1_x = room1.x2
            potential_y = [y for y in range(room1.y1 + 1, room1.y2) if floor.is_valid_position(room1.x2 + 1, y)]
            if potential_y: opening1_y = random.choice(potential_y)

        # Fallback if the chosen wall didn't yield a valid opening
        if opening1_x is None or opening1_y is None:
            opening1_x, opening1_y = room1.center
            opening1_x = max(room1.x1, min(room1.x2, opening1_x))
            opening1_y = max(room1.y1, min(room1.y2, opening1_y))

        opening2_x, opening2_y = None, None

        # Try to find a valid opening point on the chosen wall for room2
        if wall2 == 'top' and room2.y1 > 0:
            potential_x = [x for x in range(room2.x1 + 1, room2.x2) if floor.is_valid_position(x, room2.y1 - 1)]
            if potential_x: opening2_x = random.choice(potential_x)
            opening2_y = room2.y1
        elif wall2 == 'bottom' and room2.y2 < floor.height - 1:
            potential_x = [x for x in range(room2.x1 + 1, room2.x2) if floor.is_valid_position(x, room2.y2 + 1)]
            if potential_x: opening2_x = random.choice(potential_x)
            opening2_y = room2.y2
        elif wall2 == 'left' and room2.x1 > 0:
            opening2_x = room2.x1
            potential_y = [y for y in range(room2.y1 + 1, room2.y2) if floor.is_valid_position(room2.x1 - 1, y)]
            if potential_y: opening2_y = random.choice(potential_y)
        elif wall2 == 'right' and room2.x2 < floor.width - 1:
            opening2_x = room2.x2
            potential_y = [y for y in range(room2.y1 + 1, room2.y2) if floor.is_valid_position(room2.x2 + 1, y)]
            if potential_y: opening2_y = random.choice(potential_y)

        # Fallback for room2
        if opening2_x is None or opening2_y is None:
            opening2_x, opening2_y = room2.center
            opening2_x = max(room2.x1, min(room2.x2, opening2_x))
            opening2_y = max(room2.y1, min(room2.y2, opening2_y))

        # Crucial check: Ensure calculated points are valid before proceeding
        if (opening1_x is None or opening1_y is None or
            opening2_x is None or opening2_y is None or
            not floor.is_valid_position(opening1_x, opening1_y) or
            not floor.is_valid_position(opening2_x, opening2_y)):
            return

        # Make the openings in the walls
        floor.tiles[opening1_x][opening1_y].tile_type = Tile.CORRIDOR
        floor.tiles[opening2_x][opening2_y].tile_type = Tile.CORRIDOR

        # Add openings to room data
        if (opening1_x, opening1_y) not in room1.openings:
            room1.openings.append((opening1_x, opening1_y))
        if (opening2_x, opening2_y) not in room2.openings:
            room2.openings.append((opening2_x, opening2_y))

        # Create the tunnels connecting the openings
        if random.random() < 0.5:
            self._create_horizontal_tunnel(floor, opening1_x, opening2_x, opening1_y)
            self._create_vertical_tunnel(floor, opening1_y, opening2_y, opening2_x)
        else:
            self._create_vertical_tunnel(floor, opening1_y, opening2_y, opening1_x)
            self._create_horizontal_tunnel(floor, opening1_x, opening2_x, opening2_y)

    def _create_horizontal_tunnel(self, floor: Floor, x1: int, x2: int, y: int) -> None:
        """Создает горизонтальный коридор."""
        if not (0 <= y < floor.height):
            return

        for x in range(min(x1, x2), max(x1, x2) + 1):
            if not floor.is_valid_position(x, y):
                continue

            if floor.tiles[x][y].tile_type != Tile.FLOOR:
                floor.tiles[x][y].tile_type = Tile.CORRIDOR

            if floor.is_valid_position(x, y - 1) and floor.tiles[x][y - 1].tile_type == Tile.EMPTY:
                floor.tiles[x][y - 1].tile_type = Tile.WALL
            if floor.is_valid_position(x, y + 1) and floor.tiles[x][y + 1].tile_type == Tile.EMPTY:
                floor.tiles[x][y + 1].tile_type = Tile.WALL

    def _create_vertical_tunnel(self, floor: Floor, y1: int, y2: int, x: int) -> None:
        """Создает вертикальный коридор."""
        if not (0 <= x < floor.width):
            return

        for y in range(min(y1, y2), max(y1, y2) + 1):
            if not floor.is_valid_position(x, y):
                continue

            if floor.tiles[x][y].tile_type != Tile.FLOOR:
                floor.tiles[x][y].tile_type = Tile.CORRIDOR

            if floor.is_valid_position(x - 1, y) and floor.tiles[x - 1][y].tile_type == Tile.EMPTY:
                floor.tiles[x - 1][y].tile_type = Tile.WALL
            if floor.is_valid_position(x + 1, y) and floor.tiles[x + 1][y].tile_type == Tile.EMPTY:
                floor.tiles[x + 1][y].tile_type = Tile.WALL

    def _connect_room_to_corridor(self, floor: Floor, room: Room, corridor: Tuple[int, int]) -> None:
        """Соединяет комнату с существующим коридором."""
        corridor_x, corridor_y = corridor
        center_x, center_y = room.center
        
        wall = None
        opening_x, opening_y = None, None
        
        if corridor_x < center_x:
            wall = 'left'
            opening_x = room.x1
            opening_y = center_y
        elif corridor_x > center_x:
            wall = 'right'
            opening_x = room.x2
            opening_y = center_y
        elif corridor_y < center_y:
            wall = 'top'
            opening_x = center_x
            opening_y = room.y1
        else:
            wall = 'bottom'
            opening_x = center_x
            opening_y = room.y2
        
        if wall == 'left' or wall == 'right':
            potential_openings = []
            for y in range(room.y1 + 1, room.y2):
                if floor.is_valid_position(opening_x, y):
                    potential_openings.append((opening_x, y))
                    
            if potential_openings:
                min_dist = float('inf')
                for ox, oy in potential_openings:
                    dist = ((ox - corridor_x) ** 2 + (oy - corridor_y) ** 2) ** 0.5
                    if dist < min_dist:
                        min_dist = dist
                        opening_y = oy
        
        elif wall == 'top' or wall == 'bottom':
            potential_openings = []
            for x in range(room.x1 + 1, room.x2):
                if floor.is_valid_position(x, opening_y):
                    potential_openings.append((x, opening_y))
                    
            if potential_openings:
                min_dist = float('inf')
                for ox, oy in potential_openings:
                    dist = ((ox - corridor_x) ** 2 + (oy - corridor_y) ** 2) ** 0.5
                    if dist < min_dist:
                        min_dist = dist
                        opening_x = ox
        
        if not floor.is_valid_position(opening_x, opening_y):
            return
            
        floor.tiles[opening_x][opening_y].tile_type = Tile.CORRIDOR
        room.openings.append((opening_x, opening_y))
        
        if random.random() < 0.5:
            self._create_horizontal_tunnel(floor, opening_x, corridor_x, opening_y)
            self._create_vertical_tunnel(floor, opening_y, corridor_y, corridor_x)
        else:
            self._create_vertical_tunnel(floor, opening_y, corridor_y, opening_x)
            self._create_horizontal_tunnel(floor, opening_x, corridor_x, corridor_y)
        
    def _ensure_room_accessibility(self, floor: Floor) -> None:
        """Проверяет и обеспечивает, что все комнаты имеют как минимум один выход и все доступны."""
        if not floor.rooms:
            return

        for room in floor.rooms:
            if not room.openings:
                closest_room = self._find_closest_room(room, floor.rooms)
                if closest_room:
                    self._connect_rooms(floor, room, closest_room)
        
        accessible_rooms = self._find_accessible_rooms(floor, 0)
        
        if len(accessible_rooms) < len(floor.rooms):
            corridor_tiles = []
            for x in range(floor.width):
                for y in range(floor.height):
                    if floor.tiles[x][y].tile_type == Tile.CORRIDOR:
                        corridor_tiles.append((x, y))
            
            if not corridor_tiles:
                for i, room in enumerate(floor.rooms):
                    if i not in accessible_rooms:
                        closest_accessible = None
                        min_distance = float('inf')
                        
                        for accessible_idx in accessible_rooms:
                            accessible_room = floor.rooms[accessible_idx]
                            distance = self._calculate_distance(room, accessible_room)
                            
                            if distance < min_distance:
                                min_distance = distance
                                closest_accessible = accessible_room
                        
                        if closest_accessible:
                            self._connect_rooms(floor, room, closest_accessible)
            else:
                for i, room in enumerate(floor.rooms):
                    if i not in accessible_rooms:
                        center_x, center_y = room.center
                        closest_corridor = None
                        min_distance = float('inf')
                        
                        for corridor_x, corridor_y in corridor_tiles:
                            distance = ((center_x - corridor_x) ** 2 + (center_y - corridor_y) ** 2) ** 0.5
                            if distance < min_distance:
                                min_distance = distance
                                closest_corridor = (corridor_x, corridor_y)
                        
                        if closest_corridor:
                            self._connect_room_to_corridor(floor, room, closest_corridor)
    
    def _clean_dead_ends(self, floor: Floor) -> None:
        """Удаляет тупиковые проходы, которые не ведут никуда."""
        for room in floor.rooms:
            valid_openings = []
            for opening_x, opening_y in room.openings:
                has_connection = False
                for other_room in floor.rooms:
                    if room == other_room:
                        continue
                    
                    for other_x, other_y in other_room.openings:
                        if self._are_openings_connected(floor, (opening_x, opening_y), (other_x, other_y)):
                            has_connection = True
                            break
                    
                    if has_connection:
                        break
                
                if has_connection:
                    valid_openings.append((opening_x, opening_y))
                else:
                    floor.tiles[opening_x][opening_y].tile_type = Tile.WALL
            
            room.openings = valid_openings
    
    def _find_accessible_rooms(self, floor: Floor, start_room_idx: int) -> Set[int]:
        """Находит все комнаты, доступные из данной комнаты."""
        if not floor.rooms:
            return set()

        room_graph = {}
        for i, room in enumerate(floor.rooms):
            room_graph[i] = []
            for opening_x, opening_y in room.openings:
                for j, other_room in enumerate(floor.rooms):
                    if i == j:
                        continue
                    for other_x, other_y in other_room.openings:
                        if self._are_openings_connected(floor, (opening_x, opening_y), (other_x, other_y)):
                            room_graph[i].append(j)
                            break

        visited = set()
        queue = [start_room_idx]
        
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
                
            visited.add(current)
            
            for neighbor in room_graph[current]:
                if neighbor not in visited:
                    queue.append(neighbor)
        
        return visited
    
    def _are_openings_connected(self, floor: Floor, opening1: Tuple[int, int], opening2: Tuple[int, int]) -> bool:
        """Проверяет, соединены ли два прохода коридором."""
        x1, y1 = opening1
        x2, y2 = opening2
        
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if floor.tiles[x1][y].tile_type != Tile.CORRIDOR and (x1, y) != opening1 and (x1, y) != opening2:
                    return False
            return True
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if floor.tiles[x][y1].tile_type != Tile.CORRIDOR and (x, y1) != opening1 and (x, y1) != opening2:
                    return False
            return True
        
        bend1 = (x1, y2)
        bend2 = (x2, y1)
        
        path1_valid = True
        for x in range(min(x1, bend1[0]), max(x1, bend1[0]) + 1):
            if floor.tiles[x][y1].tile_type != Tile.CORRIDOR and (x, y1) != opening1:
                path1_valid = False
                break
        
        if path1_valid:
            for y in range(min(bend1[1], y2), max(bend1[1], y2) + 1):
                if floor.tiles[bend1[0]][y].tile_type != Tile.CORRIDOR and (bend1[0], y) != opening2:
                    path1_valid = False
                    break
        
        if path1_valid:
            return True

        path2_valid = True
        for y in range(min(y1, bend2[1]), max(y1, bend2[1]) + 1):
            if floor.tiles[x1][y].tile_type != Tile.CORRIDOR and (x1, y) != opening1:
                path2_valid = False
                break
        
        if path2_valid:
            for x in range(min(bend2[0], x2), max(bend2[0], x2) + 1):
                if floor.tiles[x][bend2[1]].tile_type != Tile.CORRIDOR and (x, bend2[1]) != opening2:
                    path2_valid = False
                    break
        
        return path2_valid
    
    def _find_closest_room(self, target: Room, rooms: List[Room]) -> Optional[Room]:
        """Находит комнату, ближайшую к целевой."""
        closest = None
        min_distance = float('inf')
        
        for room in rooms:
            if room == target:
                continue
                
            distance = self._calculate_distance(target, room)
            if distance < min_distance:
                min_distance = distance
                closest = room
                
        return closest
    
    def _calculate_distance(self, room1: Room, room2: Room) -> float:
        """Вычисляет евклидово расстояние между центрами комнат."""
        x1, y1 = room1.center
        x2, y2 = room2.center
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    
    def _create_room(self, floor: Floor, room: Room) -> None:
        """Создает комнату на этаже с полом внутри и стенами по периметру."""
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                floor.tiles[x][y].tile_type = Tile.FLOOR
        
        for x in range(room.x1, room.x2 + 1):
            if floor.is_valid_position(x, room.y1):
                floor.tiles[x][room.y1].tile_type = Tile.WALL

            if floor.is_valid_position(x, room.y2):
                floor.tiles[x][room.y2].tile_type = Tile.WALL
        
        for y in range(room.y1, room.y2 + 1):
            if floor.is_valid_position(room.x1, y):
                floor.tiles[room.x1][y].tile_type = Tile.WALL
            if floor.is_valid_position(room.x2, y):
                floor.tiles[room.x2][y].tile_type = Tile.WALL
    
    def _add_stairs(self, floor_num: int, next_floor_num: int) -> None:
        """Добавляет лестницы, соединяющие два соседних этажа."""
        current_floor = self.floors[floor_num]
        next_floor = self.floors[next_floor_num]
        
        suitable_rooms_up = [room for room in current_floor.rooms 
                          if room.x1 > 1 and room.x2 < current_floor.width - 2 
                          and room.y1 > 1 and room.y2 < current_floor.height - 2]
        
        if not suitable_rooms_up:
            suitable_rooms_up = current_floor.rooms
            
        room_up = random.choice(suitable_rooms_up)
        x_up, y_up = room_up.center
        
        x_up = max(1, min(current_floor.width - 2, x_up))
        y_up = max(1, min(current_floor.height - 2, y_up))
        
        current_floor.tiles[x_up][y_up].tile_type = Tile.STAIRS_UP
        current_floor.stairs_up.append((x_up, y_up))

        suitable_rooms_down = [room for room in next_floor.rooms 
                            if room.x1 > 1 and room.x2 < next_floor.width - 2 
                            and room.y1 > 1 and room.y2 < next_floor.height - 2]
        
        if not suitable_rooms_down:
            suitable_rooms_down = next_floor.rooms
            
        room_down = random.choice(suitable_rooms_down)
        x_down, y_down = room_down.center
        
        x_down = max(1, min(next_floor.width - 2, x_down))
        y_down = max(1, min(next_floor.height - 2, y_down))
        
        next_floor.tiles[x_down][y_down].tile_type = Tile.STAIRS_DOWN
        next_floor.stairs_down.append((x_down, y_down))
    
    def print_map(self, floor_num: int, player=None) -> None:
        """Отображает карту этажа с позицией игрока (если указан)."""
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
                    if tile.explored:
                        row += str(tile)
                    else:
                        row += " "
            print(row)