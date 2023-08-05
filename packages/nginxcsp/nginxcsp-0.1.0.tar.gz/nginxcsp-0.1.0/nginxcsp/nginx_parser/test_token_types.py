import pytest
from .token_types import Punctuation, String, Expression, is_punctuation, \
    map_character_to_punctuation, is_string_character, is_expression_character


class TestTokenTypes():

    def test_is_punctuation(self):
        for character in Punctuation.CHARACTERS.value:
            assert is_punctuation(character) is True

    def test_is_punctuation_fail(self):
        assert is_punctuation(None) is False

    def test_map_character_to_punctuation(self):
        assert map_character_to_punctuation(Punctuation.HASHTAG.value) == \
            Punctuation.HASHTAG

    def test_map_character_to_punctuation_fail(self):
        with pytest.raises(KeyError):
            map_character_to_punctuation(None)

    def test_is_string_character_quotationmark(self):
        assert is_string_character(String.QUOTATIONMARK.value) is True

    def test_is_string_character_apostrophe(self):
        assert is_string_character(String.APOSTROPHE.value) is True

    def test_is_string_fail(self):
        assert is_string_character(None) is False

    def test_is_expression_character_right_parentheses(self):
        assert is_expression_character(
            Expression.RIGHTPARENTHESES.value) is True

    def test_is_expression_character_left_parentheses(self):
        assert is_expression_character(
            Expression.LEFTPARENTHESES.value) is True

    def test_is_expression_character_fail(self):
        assert is_expression_character(None) is False
