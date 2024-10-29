def set_color(color_name):
    colors = {
        "red": "\033[31m",
        "green": "\033[32m",
        "white": "\033[37m",
        "bold": "\033[1m",
        "reset_to_normal": "\033[0m"
    }
    return colors.get(color_name, "\033[0m")

red = set_color("red")
black = set_color("black")
green = set_color("green")
white = set_color("white")
bold = set_color("bold")
reset = set_color("reset_to_normal")


if __name__ == "__main__":
# Example usage:
    print(set_color("red") + "This is red text" + set_color("reset_to_normal"))
    print(set_color("green") + "This is green text" + set_color("reset_to_normal"))
    print(set_color("bold") + "This is bold text" + set_color("reset_to_normal"))