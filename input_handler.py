import os
import msvcrt


"""input_handler.py - обработка ввода с клавиатуры:
get_char() - получает символ с клавиатуры"""


# def get_char():
#     return msvcrt.getch().decode('utf-8').lower()

def get_char():
    try:
        if os.name == 'nt':  
            ch = msvcrt.getch()
            if ch == b'\xe0': 
                ch = msvcrt.getch()
                return None
            return ch.decode('latin-1').lower()
        else:  
            import tty, termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch.lower()
    except:
        return None