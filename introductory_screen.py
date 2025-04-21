import os
import time
import random
from colorama import Fore, Back, Style, init
from input_handler import get_char



"""introductory_screen.py - вступительный экран игры
show_title_screen() - отображает заставку 
transition_to_game() - анимация перехода к игре"""



ITALIC_ON = "\033[3m"
ITALIC_OFF = "\033[23m"
subtitle = Fore.RED + Style.DIM
reset = Fore.RESET + Style.RESET_ALL
gun = Fore.YELLOW + Style.DIM


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
    print("█                                                    (҂""\033[31m`\033[0m""_""\033[31m´\033[0m"")                                                    █")
    print("█                                                   <,""\033[38;5;130m︻\033[0m""\033[30m╦╤\033[0m""\033[38;5;130m─\033[0m""💥                                                  █")
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
        "█                                                    (҂""\033[31m`\033[0m""_""\033[31m´\033[0m"")                                                    █",
        "█                                                   <,""\033[38;5;130m︻\033[0m""\033[30m╦╤\033[0m""\033[38;5;130m─\033[0m""💥                                                  █",
        "█                                                    _/ \_                                                     █",
        "█                                                                                                              █",
        "█                                         ▄█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█▄                                         █",
        "█                                       ▄█▀                          ▀█▄                                       █",
        "█                                     ▄█▀"+subtitle+"     НАЖМИТЕ ЛЮБУЮ КЛАВИШУ    "+reset+"▀█▄                                     █",
        "▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀                                  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀"
    ] 

    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    colors = [Fore.RED, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]

    for step in range(15):
        clear_screen()
        for i, line in enumerate(title_screen_lines):
           
            offset = random.randint(-1, 1) if step < 10 else 0
            glitch_line = (" " * abs(offset) + line[:len(line) - abs(offset)]) if offset >= 0 else (line[abs(offset):] + " " * abs(offset))
            
            
            if step < 12 and random.random() < 0.3:
                glitch_line = list(glitch_line)
                for _ in range(random.randint(1, 5)):
                    pos = random.randint(0, len(glitch_line) - 1)
                    glitch_line[pos] = random.choice(["#", "@", "%", "&", "█", "▒"])
                glitch_line = "".join(glitch_line)
            
            
            color = random.choice(colors) if step < 10 and random.random() < 0.4 else Fore.RESET
            
            style = Style.DIM if step > 8 and random.random() < step * 0.05 else Style.NORMAL
            
            print(color + style + glitch_line + Style.RESET_ALL)
        time.sleep(0.02)

    
    for step in range(20):
        clear_screen()
        for i, line in enumerate(title_screen_lines):
            faded_line = ""
            
            wave = abs((i + step) % 10 - 5) / 5
            threshold = step * 0.06 + wave * 0.2
            
            for char in line:
                if random.random() < threshold:
                    faded_line += " "
                else:
                    faded_line += char
            
            
            color = Fore.LIGHTBLACK_EX if step > 10 else Fore.RESET
            style = Style.DIM if step > 12 else Style.NORMAL
            print(color + style + faded_line + Style.RESET_ALL)
        # time.sleep(0.03)



    clear_screen()