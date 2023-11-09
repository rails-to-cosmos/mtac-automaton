import unittest
from unittest.mock import patch, mock_open

from scrambled_word_matcher import validate_dictionary, validate_input_file


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

    # def test_integration_valid_files(self) -> None:
    #     mock_dictionary_content = "apple\nbanana\norange\n"
    #     mock_input_content = "aplep\nbannaa\noenrag\n"

    #     dictionary_mock = mock_open(read_data=mock_dictionary_content)
    #     input_mock = mock_open(read_data=mock_input_content)

    #     with patch('builtins.open', dictionary_mock), \
    #          patch('builtins.open', input_mock), \
    #          patch('entrypoint.print') as mock_print:
    #             main('fake_dictionary_path', 'fake_input_path')
    #             mock_print.assert_called_with('Case #3: 1')


if __name__ == '__main__':
    unittest.main()
