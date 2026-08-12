from typing import Protocol


class IconHost(Protocol):
    icons: dict[str, dict[str, str]]
    colors: dict[str, str]

    icon_mode: str
    use_color: bool

    def color(self, text: str, fg_code: str) -> str: ...


class FormatTarget(IconHost, Protocol):
    backgrounds: dict[str, str]
    styles: dict[str, tuple[str, str]]

    def background(self, text: str, bg_code: str) -> str: ...

    def style(self, text: str, on_code: str, off_code: str) -> str: ...

    @staticmethod
    def _has_nerd_fonts() -> bool: ...
