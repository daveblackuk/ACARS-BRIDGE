import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init()

def set_color(color_name):
    colors = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "white": Fore.WHITE,
        "bold": Style.BRIGHT,
        "reset_to_normal": Style.RESET_ALL
    }
    return colors.get(color_name, Style.RESET_ALL)

red = set_color("red")
black = Fore.BLACK  # Manually set black color
green = set_color("green")
white = set_color("white")
bold = set_color("bold")
reset = set_color("reset_to_normal")

def clear_screen():
    print(Fore.RESET + Style.RESET_ALL + '\033[2J\033[H')

if __name__ == "__main__":
# Example usage:
    print(set_color("red") + "This is red text" + set_color("reset_to_normal"))
    print(set_color("green") + "This is green text" + set_color("reset_to_normal"))
    print(set_color("bold") + "This is bold text" + set_color("reset_to_normal"))

