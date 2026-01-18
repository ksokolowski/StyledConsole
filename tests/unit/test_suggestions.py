"""Tests for the suggestions utility module."""

import pytest

from styledconsole.utils.suggestions import (
    find_closest_match,
    find_closest_matches,
    find_normalized_match,
    format_error_with_suggestion,
    levenshtein_distance,
    normalize_name,
    suggest_similar,
)


class TestLevenshteinDistance:
    """Tests for levenshtein_distance function."""

    def test_identical_strings(self):
        """Identical strings have distance 0."""
        assert levenshtein_distance("hello", "hello") == 0

    def test_empty_strings(self):
        """Empty string distance is length of other string."""
        assert levenshtein_distance("", "hello") == 5
        assert levenshtein_distance("hello", "") == 5
        assert levenshtein_distance("", "") == 0

    def test_single_edit(self):
        """Single character edits."""
        assert levenshtein_distance("cat", "bat") == 1  # substitution
        assert levenshtein_distance("cat", "cats") == 1  # insertion
        assert levenshtein_distance("cats", "cat") == 1  # deletion

    def test_multiple_edits(self):
        """Multiple edits."""
        assert levenshtein_distance("kitten", "sitting") == 3
        assert levenshtein_distance("rounded", "round") == 2


class TestFindClosestMatch:
    """Tests for find_closest_match function."""

    def test_exact_match(self):
        """Exact match returns candidate."""
        candidates = ["rounded", "solid", "double"]
        assert find_closest_match("rounded", candidates) == "rounded"

    def test_case_insensitive_match(self):
        """Case insensitive matching."""
        candidates = ["rounded", "solid", "double"]
        assert find_closest_match("ROUNDED", candidates) == "rounded"
        assert find_closest_match("Solid", candidates) == "solid"

    def test_typo_correction(self):
        """Typo correction finds closest match."""
        candidates = ["rounded", "solid", "double"]
        assert find_closest_match("rounde", candidates) == "rounded"
        assert find_closest_match("round", candidates) == "rounded"
        assert find_closest_match("solyd", candidates) == "solid"

    def test_no_match_beyond_threshold(self):
        """Returns None when no match within threshold."""
        candidates = ["rounded", "solid", "double"]
        assert find_closest_match("xyz", candidates, max_distance=2) is None

    def test_empty_candidates(self):
        """Returns None for empty candidates."""
        assert find_closest_match("test", []) is None

    def test_empty_query(self):
        """Returns None for empty query."""
        assert find_closest_match("", ["a", "b"]) is None


class TestFindClosestMatches:
    """Tests for find_closest_matches function."""

    def test_multiple_matches(self):
        """Returns multiple matches sorted by distance."""
        candidates = ["fire", "forest", "ocean", "sunrise"]
        matches = find_closest_matches("fore", candidates, max_results=3)
        assert "fire" in matches
        assert "forest" in matches

    def test_exact_match_first(self):
        """Exact match should be first."""
        candidates = ["fire", "forest", "ocean"]
        matches = find_closest_matches("fire", candidates)
        assert matches[0] == "fire"

    def test_max_results_limit(self):
        """Respects max_results limit."""
        candidates = ["a", "b", "c", "d", "e"]
        matches = find_closest_matches("a", candidates, max_results=2)
        assert len(matches) <= 2


class TestSuggestSimilar:
    """Tests for suggest_similar function."""

    def test_returns_suggestion_string(self):
        """Returns formatted suggestion string."""
        candidates = ["rounded", "solid", "double"]
        suggestion = suggest_similar("rounde", candidates)
        assert suggestion == "Did you mean 'rounded'?"

    def test_returns_none_when_no_match(self):
        """Returns None when no close match."""
        candidates = ["rounded", "solid", "double"]
        suggestion = suggest_similar("xyz", candidates, max_distance=1)
        assert suggestion is None


class TestFormatErrorWithSuggestion:
    """Tests for format_error_with_suggestion function."""

    def test_includes_suggestion(self):
        """Includes suggestion when match found."""
        result = format_error_with_suggestion(
            "Unknown border style: 'rounde'",
            "rounde",
            ["rounded", "solid", "double"],
        )
        assert "Did you mean 'rounded'?" in result
        assert "Unknown border style: 'rounde'" in result

    def test_includes_available_options(self):
        """Includes available options list."""
        result = format_error_with_suggestion(
            "Unknown style",
            "xyz",
            ["rounded", "solid", "double"],
        )
        assert "Available:" in result
        assert "rounded" in result

    def test_limits_available_options(self):
        """Limits number of available options shown."""
        candidates = [f"style{i}" for i in range(20)]
        result = format_error_with_suggestion(
            "Unknown style",
            "xyz",
            candidates,
            max_available=5,
        )
        assert "... (20 total)" in result


class TestNormalizeName:
    """Tests for normalize_name function."""

    def test_lowercase(self):
        """Converts to lowercase."""
        assert normalize_name("RED") == "red"
        assert normalize_name("LightBlue") == "lightblue"

    def test_removes_hyphens(self):
        """Removes hyphens."""
        assert normalize_name("light-blue") == "lightblue"

    def test_removes_underscores(self):
        """Removes underscores."""
        assert normalize_name("dark_green") == "darkgreen"

    def test_combined(self):
        """Handles combined normalization."""
        assert normalize_name("Light-Blue_Color") == "lightbluecolor"


class TestFindNormalizedMatch:
    """Tests for find_normalized_match function."""

    def test_case_match(self):
        """Finds match with different case."""
        candidates = ["fire", "ocean", "sunset"]
        assert find_normalized_match("FIRE", candidates) == "fire"

    def test_separator_match(self):
        """Finds match with different separators."""
        candidates = ["lightblue", "darkgreen", "red"]
        assert find_normalized_match("light-blue", candidates) == "lightblue"
        assert find_normalized_match("light_blue", candidates) == "lightblue"

    def test_no_match(self):
        """Returns None when no match."""
        candidates = ["fire", "ocean"]
        assert find_normalized_match("xyz", candidates) is None


class TestIntegration:
    """Integration tests with actual StyledConsole components."""

    def test_border_style_suggestion(self):
        """Border style errors include suggestions."""
        from styledconsole.core.box_mapping import get_box_style

        with pytest.raises(ValueError) as exc_info:
            get_box_style("rounde")

        error_msg = str(exc_info.value)
        assert "Did you mean 'rounded'?" in error_msg

    def test_effect_preset_suggestion(self):
        """Effect preset errors include suggestions."""
        from styledconsole.effects.registry import EFFECTS

        with pytest.raises(KeyError) as exc_info:
            EFFECTS.get("rainbo")

        error_msg = str(exc_info.value)
        assert "Did you mean 'rainbow'?" in error_msg

    def test_alignment_suggestion(self):
        """Alignment errors include suggestions."""
        from styledconsole.utils.validation import validate_align

        with pytest.raises(ValueError) as exc_info:
            validate_align("middle")

        error_msg = str(exc_info.value)
        assert "Did you mean 'center'?" in error_msg

    def test_alignment_centre_british_spelling(self):
        """British spelling 'centre' suggests 'center'."""
        from styledconsole.utils.validation import validate_align

        with pytest.raises(ValueError) as exc_info:
            validate_align("centre")

        error_msg = str(exc_info.value)
        assert "Did you mean 'center'?" in error_msg

    def test_object_type_suggestion(self):
        """Object type errors include suggestions."""
        from styledconsole.model.registry import create_object

        with pytest.raises(ValueError) as exc_info:
            create_object({"type": "fram", "content": "test"})

        error_msg = str(exc_info.value)
        assert "Did you mean 'frame'?" in error_msg
