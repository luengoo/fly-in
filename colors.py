from colorama import Fore, init, Style

init(autoreset=True)


class Colors:

    colors_dict = {
                "red": Fore.RED,
                "black": Fore.BLACK,
                "blue": Fore.BLUE,
                "cyan": Fore.CYAN,
                "green": Fore.GREEN,
                "yellow": Fore.YELLOW,
                "magenta": Fore.MAGENTA,
                "white": Fore.WHITE,
                "error": Fore.RED + Style.BRIGHT,
                "success": Fore.GREEN + Style.BRIGHT,
                "warning": Fore.YELLOW + Style.BRIGHT,
                "info": Fore.CYAN + Style.BRIGHT,
                "orange": "\033[38;5;208m",
                "purple": Fore.MAGENTA,
                "brown": "\033[33m",
                "maroon": Fore.RED + Fore.BLACK,
                "gold": Fore.YELLOW + Fore.BLACK,
                "darkred": Fore.BLACK + Style.BRIGHT,
                "crimson": Fore.RED + Style.BRIGHT,
                "violet": Fore.MAGENTA + Style.BRIGHT
        }

    @classmethod
    def get(cls, color_name: str) -> str:
        if not color_name:
            return Fore.WHITE
        return cls.colors_dict.get(color_name.lower(), Fore.WHITE)

    @classmethod
    def print(cls, text: str, color_name: str) -> None:
        rainbow_colors = [
                Fore.RED,
                Fore.YELLOW,
                Fore.GREEN,
                Fore.CYAN,
                Fore.BLUE,
                Fore.MAGENTA,
                Fore.WHITE
                ]
        if color_name != "rainbow":
            print(cls.get(color_name) + text + Style.RESET_ALL)
        else:
            for i, letter in enumerate(text):
                actual_color = rainbow_colors[i % len(rainbow_colors)]
                print(actual_color + letter, end="")
        print()
