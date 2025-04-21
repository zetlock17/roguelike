import os
from input_handler import get_char


"""dialog.py - диалоговые окна:
display_dialog() - отображает диалоги с npc и меню выбора"""


def display_dialog(title: str, message: str, options: list = None) -> int:
    os.system('cls' if os.name == 'nt' else 'clear')
    width = max(len(title), len(message), 80)

    print("┌" + "─" * width + "┐")
    print(f"│{title.center(width)}│")
    print("├" + "─" * width + "┤")

    words = message.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= width - 2:
            current_line += (" " + word) if current_line else word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    for line in lines:
        print(f"│{line.ljust(width)}│")

    if options:
        print("├" + "─" * width + "┤")
        for i, option in enumerate(options):
            print(f"│ {i+1}. {option.ljust(width-4)}│")

    print("└" + "─" * width + "┘")

    if options:
        while True:
            key = get_char()
            try:
                choice = int(key) - 1
                if 0 <= choice < len(options):
                    return choice
            except ValueError:
                if key == '\x1b':
                    return -1
    return -1