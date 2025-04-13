import os
import time
import random
from colorama import Fore, Back, Style


from input_handler import get_char



ITALIC_ON = "\033[3m"
ITALIC_OFF = "\033[23m"
subtitle = Fore.RED + Style.DIM
reset = Fore.RESET + Style.RESET_ALL


def show_title_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
        
    print("█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█")
    print("█                                                                                                              █")
    print("█                                ███████╗███████╗ ██████╗ █████╗ ██████╗ ███████╗                              █")
    print("█                                ██╔════╝██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝                              █")
    print("█                                █████╗  ███████╗██║     ███████║██████╔╝█████╗                                █")
    print("█                                ██╔══╝  ╚════██║██║     ██╔══██║██╔═══╝ ██╔══╝                                █")
    print("█                                ███████╗███████║╚██████╗██║  ██║██║     ███████╗                              █")
    print("█                                ╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚══════╝                              █")
    print("█                                                                                                              █")
    print("█                                                                                                              █")
    print("█                                                                                                              █")
    print("█                                                                                                              █")
    print("█"+ITALIC_ON+"                                Вы - серийный убийца на пожизненном заключении"+ITALIC_OFF+"                                █")
    print("█"+ITALIC_ON+"                          В тюрьме произошел сбой, открывший все двери, кроме одной..."+ITALIC_OFF+"                        █")
    print("█"+ITALIC_ON+"                           Найди три ключа и соверши побег. Но будет ли это так легко?"+ITALIC_OFF+"                        █")
    print("█                                                                                                              █")
    print("█                                                                                                              █")
    print("█                                                                                                              █")
    print("█                                                     .-.                                                      █")
    print("█                                                    (҂`_´)                                                    █")
    print("█                                                   <,︻╦╤─💥                                                  █")
    print("█                                                    _/ \_                                                     █")
    print("█                                                                                                              █")
    print("█                                         ▄█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█▄                                         █")
    print("█                                       ▄█▀                          ▀█▄                                       █")
    print("█                                     ▄█▀"+subtitle+"     НАЖМИТЕ ЛЮБУЮ КЛАВИШУ    "+reset+"▀█▄                                     █")
    print("▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀                                  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀")

    
    get_char()




def transition_to_game():
    title_screen_lines = [
        "█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█",
        "█                                                                                                              █",
        "█                                ███████╗███████╗ ██████╗ █████╗ ██████╗ ███████╗                              █",
        "█                                ██╔════╝██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝                              █",
        "█                                █████╗  ███████╗██║     ███████║██████╔╝█████╗                                █",
        "█                                ██╔══╝  ╚════██║██║     ██╔══██║██╔═══╝ ██╔══╝                                █",
        "█                                ███████╗███████║╚██████╗██║  ██║██║     ███████╗                              █",
        "█                                ╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚══════╝                              █",
        "█                                                                                                              █",
        "█                                                                                                              █",
        "█                                                                                                              █",
        "█                                                                                                              █",
        "█"+ITALIC_ON+"                                Вы - серийный убийца на пожизненном заключении"+ITALIC_OFF+"                                █",
        "█"+ITALIC_ON+"                          В тюрьме произошел сбой, открывший все двери, кроме одной..."+ITALIC_OFF+"                        █",
        "█"+ITALIC_ON+"                           Найди три ключа и соверши побег. Но будет ли это так легко?"+ITALIC_OFF+"                        █",
        "█                                                                                                              █",
        "█                                                                                                              █",
        "█                                                                                                              █",
        "█                                                     .-.                                                      █",
        "█                                                    (҂`_´)                                                    █",
        "█                                                   <,︻╦╤─💥                                                  █",
        "█                                                    _/ \_                                                     █",
        "█                                                                                                              █",
        "█                                         ▄█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█▄                                         █",
        "█                                       ▄█▀                          ▀█▄                                       █",
        "█                                     ▄█▀"+subtitle+"     НАЖМИТЕ ЛЮБУЮ КЛАВИШУ    "+reset+"▀█▄                                     █",
        "▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀                                  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀"
    ] 

    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    for _ in range(3):
        clear_screen()
        time.sleep(0.15)
        for line in title_screen_lines:
            print(line)
        time.sleep(0.15)

    remaining_lines = title_screen_lines.copy()
    line_indices = list(range(len(remaining_lines)))

    while line_indices:
        index = random.choice(line_indices)
        line_indices.remove(index)
        
        clear_screen()
        for i in range(len(title_screen_lines)):
            if i in line_indices:
                print(title_screen_lines[i])
            else:
                print(" " * len(title_screen_lines[i]))  
        time.sleep(0.01)  

    clear_screen()