import unittest
from unittest.mock import patch, mock_open

from scrambled_word_matcher.validations import validate_dictionary, validate_input_file


class TestScrambledWordMatcher(unittest.TestCase):
    def test_valid_dictionary(self) -> None:
        mock_dictionary_content = "word\nanother\nyetanotherword\n"
        with patch('builtins.open', mock_open(read_data=mock_dictionary_content)):
            # Should not raise an exception
            validate_dictionary('fake_dictionary_path')

    def test_duplicate_words_in_dictionary(self) -> None:
        mock_dictionary_content = "word\nanother\nword\n"
        with patch('builtins.open', mock_open(read_data=mock_dictionary_content)):
            self.assertRaises(ValueError, validate_dictionary, 'fake_dictionary_path')

    def test_valid_input_file(self) -> None:
        mock_input_content = "this is a test\nthis is another test\n"
        with patch('builtins.open', mock_open(read_data=mock_input_content)):
            # Should not raise an exception
            validate_input_file('fake_input_path')

    def test_input_file_too_many_lines(self) -> None:
        mock_input_content = "test\n" * 101
        with patch('builtins.open', mock_open(read_data=mock_input_content)):
            self.assertRaises(ValueError, validate_input_file, 'fake_input_path')


if __name__ == '__main__':
    unittest.main()
