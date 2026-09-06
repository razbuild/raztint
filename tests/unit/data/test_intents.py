import pytest

from raztint.data.intents import INTENTS, IntentConfig, _get_intents


class TestGetIntentsAll:
    """Test cases for _get_intents() with no name (returns every intent)."""

    def test_returns_all_intent_names(self) -> None:
        result = _get_intents()
        assert set(result) == set(INTENTS)

    def test_none_explicit_matches_default(self) -> None:
        assert _get_intents() == _get_intents(None)

    def test_each_entry_has_color_icon_styles_keys(self) -> None:
        result = _get_intents()
        for entry in result.values():
            assert set(entry) == {"color", "icon", "styles"}

    def test_string_styles_are_wrapped_in_a_list(self) -> None:
        result = _get_intents()
        assert result["success"]["styles"] == ["bold"]
        assert result["pending"]["styles"] == ["italic"]
        assert result["debug"]["styles"] == ["dim"]

    def test_none_styles_become_empty_list(self) -> None:
        result = _get_intents()
        assert result["warning"]["styles"] == []
        assert result["info"]["styles"] == []

    def test_color_and_icon_pass_through_unchanged(self) -> None:
        result = _get_intents()
        assert result["success"]["color"] == "green"
        assert result["success"]["icon"] == "ok"
        assert result["error"]["color"] == "red"
        assert result["error"]["icon"] == "err"

    @pytest.mark.parametrize("name,config", list(INTENTS.items()))
    def test_matches_source_config_for_every_intent(
        self, name: str, config: IntentConfig
    ) -> None:
        entry = _get_intents()[name]
        expected_styles = (
            [config.styles]
            if isinstance(config.styles, str)
            else list(config.styles or [])
        )
        assert entry == {
            "color": config.color,
            "icon": config.icon,
            "styles": expected_styles,
        }

    def test_does_not_mutate_source_registry(self) -> None:
        result = _get_intents()
        result["success"]["styles"].append("underline")
        assert INTENTS["success"].styles == "bold"


class TestGetIntentsSingle:
    """Test cases for _get_intents(name) with a specific intent."""

    def test_returns_flat_dict_for_known_intent(self) -> None:
        assert _get_intents("success") == {
            "color": "green",
            "icon": "ok",
            "styles": ["bold"],
        }

    def test_string_style_wrapped_in_list(self) -> None:
        assert _get_intents("pending")["styles"] == ["italic"]

    def test_none_style_becomes_empty_list(self) -> None:
        assert _get_intents("warning")["styles"] == []
        assert _get_intents("info")["styles"] == []

    def test_is_case_insensitive(self) -> None:
        assert _get_intents("SUCCESS") == _get_intents("success")
        assert _get_intents("Error") == _get_intents("error")

    def test_unknown_intent_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match=r"Unknown intent: 'bogus'"):
            _get_intents("bogus")

    def test_unknown_intent_error_lists_sorted_valid_names(self) -> None:
        with pytest.raises(ValueError) as exc_info:
            _get_intents("bogus")

        expected_list = ", ".join(sorted(INTENTS))
        assert f"Valid intents: {expected_list}" in str(exc_info.value)

    def test_unknown_intent_uses_lowercased_name_in_message(self) -> None:
        with pytest.raises(ValueError, match=r"Unknown intent: 'bogus'"):
            _get_intents("BOGUS")

    def test_empty_string_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match=r"Unknown intent: ''"):
            _get_intents("")

    @pytest.mark.parametrize("name", list(INTENTS))
    def test_single_lookup_matches_all_lookup_for_every_intent(self, name: str) -> None:
        assert _get_intents(name) == _get_intents()[name]
