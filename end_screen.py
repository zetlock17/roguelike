import os
from colorama import Fore, Style
from entities import Player
from input_handler import get_char


"""end_screen.py - экран завершения игры:
display_game_over() - экран поражения
display_victory_screen() - экран победы"""


def display_game_over(player: Player):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + player.statistics.display())
    print("                                                                                        ")
    print("              " + Fore.RED + Style.BRIGHT + "                Нажмите любую клавишу для выхода..." +
          Style.RESET_ALL + Fore.RESET + "                           ")
    print("                                                                                        ")
    get_char()

def display_victory_screen(player: Player):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + player.statistics.win_display())
    print("                                                                                        ")
    print("              " + Fore.GREEN + Style.BRIGHT + "                Нажмите любую клавишу для выхода..." +
          Style.RESET_ALL + Fore.RESET + "                           ")
    print("                                                                                        ")
    get_char()