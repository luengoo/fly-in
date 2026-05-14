from colorama import Fore, init, Style

init(autoreset=True)

class Colors:
        colors_dict = {
            "red":Fore.RED,
            "black":Fore.BLACK,
            "blue":Fore.BLUE,
            "cyan":Fore.CYAN,
            "green":Fore.GREEN,
            "yellow":Fore.YELLOW,
            "magenta":Fore.MAGENTA,
            "white":Fore.WHITE,
            "error":Fore.RED + Style.BRIGHT,
            "success":Fore.GREEN + Style.BRIGHT,
            "warning":Fore.YELLOW + Style.BRIGHT,
            "info":Fore.CYAN + Style.BRIGHT,
            "orange":"\033[38;5;208m"
        }

        @classmethod
        def get(cls, color_name: str):
                if not color_name:
                        return Fore.WHITE
                return cls.colors_dict.get(color_name.lower(), Fore.WHITE)
        
        @classmethod
        def print(cls, text: str, color_name: str):
                print(cls.get(color_name) + text + Style.RESET_ALL)