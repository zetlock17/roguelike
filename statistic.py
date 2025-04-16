from colorama import Fore, Style, Back


class Statistics:
    """Класс для отслеживания статистики игрока."""
    
    def __init__(self):
        self.enemies_killed = 0
        self.items_picked = 0
        self.food_eaten = 0
        self.floors_visited = {0} 
        self.attacks_made = 0
        self.damage_taken = 0
        self.keys_found = 0
    
    def record_enemy_killed(self):
        self.enemies_killed += 1
    
    def record_item_picked(self):
        self.items_picked += 1
    
    def record_food_eaten(self):
        self.food_eaten += 1
    
    def record_floor_visited(self, floor: int):
        self.floors_visited.add(floor)
    
    def record_attack(self):
        self.attacks_made += 1
    
    def record_damage_taken(self, damage: int):
        self.damage_taken += damage
    
    def record_key_found(self):
        self.keys_found += 1
    
    def display(self):
        return (
                                                                                                               
            "                                                                                        \n"
            "                                                                                        \n"
            "     "+Fore.RED+"     ███████╗   █████╗  ██    ██╗ ███████╗      ████║   ██   ██╗ ███████╗ ██████╗               "+Fore.RESET+" \n"
            "    "+Fore.RED+"     ██╔═════╝  ██╔══██╗ ███  ███║ ██╔════╝    ██    ██╗ ██   ██║ ██╔════╝ ██   ██╗            "+Fore.RESET+" \n"
            "    "+Fore.RED+"     ██║   ██╚╗ ███████║ ██║██ ██║ █████╗      ██    ██║ ██   ██║ █████╗   ██  ██╗                "+Fore.RESET+" \n"
            "    "+Fore.RED+"     ██║    ██║ ██╔══██║ ██║   ██║ ██╔══╝      ██    ██║ ╚██ ██╔╝ ██╔══╝   █████═╗           "+Fore.RESET+" \n"
            "    "+Fore.RED+"     ╚███████╔╝ ██║  ██║ ██║   ██║ ███████╗    ╚██████╔╝  ╚██╔═╝  ███████╗ ██╔╗██║               "+Fore.RESET+" \n"
            "    "+Fore.RED+"      ╚══════╝  ╚═╝  ╚═╝ ╚═╝   ╚═╝ ╚══════╝     ╚═════╝    ╚═╝    ╚══════╝ ╚═╝╚══╝            "+Fore.RESET+"       \n"
            "                                                                                        \n"
                                                                                                       
            " \n"
            " \n"
            " \n"
            f"                    Убито врагов: {self.enemies_killed}                   Подобрано предметов: {self.items_picked}\n"
            " \n"
            f"                    Съедено еды: {self.food_eaten}                    Посещено этажей: {len(self.floors_visited)}\n"
            " \n"
            f"                    Совершено атак: {self.attacks_made}                 Получено урона: {self.damage_taken}\n"
            " \n"

        )
    
    def win_display(self):
        return (
                                                                                                               
            "                                                                                        \n"
            "                                                                                        \n"
            "     "+Fore.GREEN+"     ███████╗   █████╗  ██    ██╗ ███████╗      ████║   ██   ██╗ ███████╗ ██████╗               "+Fore.RESET+" \n"
            "    "+Fore.GREEN+"     ██╔═════╝  ██╔══██╗ ███  ███║ ██╔════╝    ██    ██╗ ██   ██║ ██╔════╝ ██   ██╗            "+Fore.RESET+" \n"
            "    "+Fore.GREEN+"     ██║   ██╚╗ ███████║ ██║██ ██║ █████╗      ██    ██║ ██   ██║ █████╗   ██  ██╗                "+Fore.RESET+" \n"
            "    "+Fore.GREEN+"     ██║    ██║ ██╔══██║ ██║   ██║ ██╔══╝      ██    ██║ ╚██ ██╔╝ ██╔══╝   █████═╗           "+Fore.RESET+" \n"
            "    "+Fore.GREEN+"     ╚███████╔╝ ██║  ██║ ██║   ██║ ███████╗    ╚██████╔╝  ╚██╔═╝  ███████╗ ██╔╗██║               "+Fore.RESET+" \n"
            "    "+Fore.GREEN+"      ╚══════╝  ╚═╝  ╚═╝ ╚═╝   ╚═╝ ╚══════╝     ╚═════╝    ╚═╝    ╚══════╝ ╚═╝╚══╝            "+Fore.RESET+"       \n"
            "                                                                                        \n"
                                                                                                       
            " \n"
            " \n"
            " \n"
            f"                   Убито врагов: {self.enemies_killed}                   Подобрано предметов: {self.items_picked}\n"
            " \n"
            f"                   Съедено еды: {self.food_eaten}                    Посещено этажей: {len(self.floors_visited)}\n"
            " \n"
            f"                   Совершено атак: {self.attacks_made}                 Получено урона: {self.damage_taken}\n"
            " \n"

        )