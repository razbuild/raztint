_RESET = "\033[0m"
_BG_RESET = "\033[49m"


def apply_color(text: str, fg_code: str, *, use_color: bool) -> str:
    if not use_color:
        return text
    return f"\033[{fg_code}m{text}{_RESET}"


def apply_background(text: str, bg_code: str, *, use_color: bool) -> str:
    if not use_color:
        return text
    return f"\033[{bg_code}m{text}{_BG_RESET}"


def apply_style(text: str, on_code: str, off_code: str, *, use_color: bool) -> str:
    if not use_color:
        return text
    return f"\033[{on_code}m{text}\033[{off_code}m"


def apply_rgb(text: str, r: int, g: int, b: int, *, use_color: bool) -> str:
    if not use_color:
        return text
    return f"\033[38;2;{r};{g};{b}m{text}{_RESET}"


def apply_bg_rgb(text: str, r: int, g: int, b: int, *, use_color: bool) -> str:
    if not use_color:
        return text
    return f"\033[48;2;{r};{g};{b}m{text}{_BG_RESET}"


def apply_color256(text: str, index: int, *, use_color: bool) -> str:
    if not use_color:
        return text
    return f"\033[38;5;{index}m{text}{_RESET}"


def apply_bg_color256(text: str, index: int, *, use_color: bool) -> str:
    if not use_color:
        return text
    return f"\033[48;5;{index}m{text}{_BG_RESET}"
