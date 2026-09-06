import sys
from typing import TextIO

_ERASE_LINE = "\033[2K\r"


class TransientLine:
    def __init__(self, text: str, stream: TextIO | None = None) -> None:
        self._stream = stream or sys.stdout
        self._active = self._stream.isatty()

        if self._active:
            self._write(text)

    def _write(self, text: str) -> None:
        self._stream.write(text)
        self._stream.flush()

    def update(self, text: str) -> None:
        if not self._active:
            return

        self._write(f"{_ERASE_LINE}{text}\r")

    def erase(self) -> None:
        if not self._active:
            return

        self._write(_ERASE_LINE)
        self._active = False

    def __enter__(self) -> "TransientLine":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.erase()
