import io
import sys

import pytest

from raztint.core.transient import _ERASE_LINE, TransientLine


class FakeStream(io.StringIO):
    def __init__(self, tty: bool = True) -> None:
        super().__init__()
        self._tty = tty
        self.flush_count = 0

    def isatty(self) -> bool:
        return self._tty

    def flush(self) -> None:
        self.flush_count += 1
        super().flush()


class TestInit:
    def test_writes_text_immediately_when_tty(self) -> None:
        stream = FakeStream(tty=True)
        TransientLine("hello", stream=stream)
        assert stream.getvalue() == "hello"

    def test_flushes_after_initial_write(self) -> None:
        stream = FakeStream(tty=True)
        TransientLine("hello", stream=stream)
        assert stream.flush_count == 1

    def test_writes_nothing_when_not_tty(self) -> None:
        stream = FakeStream(tty=False)
        TransientLine("hello", stream=stream)
        assert stream.getvalue() == ""

    def test_defaults_to_stdout(self, monkeypatch: pytest.MonkeyPatch) -> None:
        stream = FakeStream(tty=True)
        monkeypatch.setattr(sys, "stdout", stream)
        TransientLine("hello")
        assert stream.getvalue() == "hello"


class TestUpdate:
    def test_writes_erase_code_then_text_with_carriage_return(self) -> None:
        stream = FakeStream(tty=True)
        line = TransientLine("first", stream=stream)
        stream.truncate(0)
        stream.seek(0)

        line.update("second")

        assert stream.getvalue() == f"{_ERASE_LINE}second\r"

    def test_flushes_on_update(self) -> None:
        stream = FakeStream(tty=True)
        line = TransientLine("first", stream=stream)
        line.update("second")
        assert stream.flush_count == 2

    def test_is_noop_when_not_tty(self) -> None:
        stream = FakeStream(tty=False)
        line = TransientLine("first", stream=stream)

        line.update("second")

        assert stream.getvalue() == ""

    def test_supports_repeated_updates(self) -> None:
        stream = FakeStream(tty=True)
        line = TransientLine("first", stream=stream)
        stream.truncate(0)
        stream.seek(0)

        line.update("second")
        line.update("third")

        assert stream.getvalue() == (f"{_ERASE_LINE}second\r{_ERASE_LINE}third\r")


class TestErase:
    def test_writes_erase_code(self) -> None:
        stream = FakeStream(tty=True)
        line = TransientLine("first", stream=stream)
        stream.truncate(0)
        stream.seek(0)

        line.erase()

        assert stream.getvalue() == _ERASE_LINE

    def test_deactivates_after_erase(self) -> None:
        stream = FakeStream(tty=True)
        line = TransientLine("first", stream=stream)

        line.erase()
        stream.truncate(0)
        stream.seek(0)
        line.update("ignored")

        assert stream.getvalue() == ""

    def test_is_idempotent(self) -> None:
        stream = FakeStream(tty=True)
        line = TransientLine("first", stream=stream)

        line.erase()
        stream.truncate(0)
        stream.seek(0)
        line.erase()

        assert stream.getvalue() == ""

    def test_is_noop_when_not_tty(self) -> None:
        stream = FakeStream(tty=False)
        line = TransientLine("first", stream=stream)

        line.erase()

        assert stream.getvalue() == ""


class TestContextManager:
    def test_enter_returns_self(self) -> None:
        stream = FakeStream(tty=True)
        line = TransientLine("first", stream=stream)

        with line as ctx:
            assert ctx is line

    def test_exit_erases_line(self) -> None:
        stream = FakeStream(tty=True)

        with TransientLine("first", stream=stream) as line:
            stream.truncate(0)
            stream.seek(0)

        assert stream.getvalue() == _ERASE_LINE
        assert line._active is False

    def test_exit_erases_even_when_exception_raised(self) -> None:
        stream = FakeStream(tty=True)

        with pytest.raises(ValueError):
            with TransientLine("first", stream=stream) as line:
                stream.truncate(0)
                stream.seek(0)
                raise ValueError("boom")

        assert stream.getvalue() == _ERASE_LINE
        assert line._active is False

    def test_full_usage_as_context_manager(self) -> None:
        stream = FakeStream(tty=True)

        with TransientLine("loading", stream=stream) as line:
            line.update("50%")
            line.update("100%")

        assert stream.getvalue() == (
            f"loading{_ERASE_LINE}50%\r{_ERASE_LINE}100%\r{_ERASE_LINE}"
        )
