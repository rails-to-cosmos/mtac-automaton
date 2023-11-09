from functools import cache

ALPHABET_SIZE = 26

MAX_DICTIONARY_SIZE = 100
MIN_DICTIONARY_LENGTH = 2
MAX_DICTIONARY_LENGTH = 20

MAX_INPUT_SIZE = 100
MIN_INPUT_LENGTH = 2
MAX_INPUT_LENGTH = 500


class DictionaryValidationError(ValueError):
    ...


class InputValidationError(ValueError):
    ...


@cache
def validate_char(char: str) -> None:
    """
    Validate that the given character is a lowercase letter from the English alphabet.

    The function checks if the ASCII value of the character, when subtracted from the ASCII value of 'a',
    falls within the range from 0 to ALPHABET_SIZE - 1 (inclusive). If the character is not a lowercase English letter,
    it raises a InputValidationError.

    :param char: The character to validate
    :raises InputValidationError: If char is not a lowercase English letter

    >>> validate_char('a')

    >>> validate_char('m')

    >>> validate_char('z')

    >>> validate_char('A')
    Traceback (most recent call last):
       ...
    scrambled_word_matcher.constraints.InputValidationError: Unexpected symbol: A

    >>> validate_char('!')
    Traceback (most recent call last):
       ...
    scrambled_word_matcher.constraints.InputValidationError: Unexpected symbol: !

    >>> validate_char('3')
    Traceback (most recent call last):
       ...
    scrambled_word_matcher.constraints.InputValidationError: Unexpected symbol: 3
    """

    char_lookup_index = ord(char) - ord('a')
    if not 0 <= char_lookup_index < ALPHABET_SIZE:
        raise InputValidationError('Unexpected symbol: %s' % char)


def validate_dictionary_word(word: str) -> None:
    """
    Validate a single word for dictionary constraints.

    Ensures that the word length is between the defined minimum and maximum length constants.

    :param word: The word to validate.
    :raises DictionaryValidationError: If the word does not meet the length requirements.

    >>> validate_dictionary_word("apple")  # This should pass without issue

    >>> validate_dictionary_word("a")  # This should fail
    Traceback (most recent call last):
    ...
    scrambled_word_matcher.constraints.DictionaryValidationError: Word 'a' does not meet length requirements (2-20)

    >>> validate_dictionary_word("extraordinarilylongword")  # This should fail
    Traceback (most recent call last):
    ...
    scrambled_word_matcher.constraints.DictionaryValidationError: Word 'extraordinarilylongword' does not meet length requirements (2-20)
    """

    if not (MIN_DICTIONARY_LENGTH <= len(word) <= MAX_DICTIONARY_LENGTH):
        raise DictionaryValidationError(f"Word '{word}' does not meet length requirements ({MIN_DICTIONARY_LENGTH}-{MAX_DICTIONARY_LENGTH})")


def validate_input_string(line_number: int, input_string: str) -> None:
    """
    Validate an input string based on the line number and length constraints.

    Ensures that the line number is within the allowed input size and the input string's length
    (after stripping whitespace) falls within the defined minimum and maximum input length constants.

    :param line_number: The line number in the input file.
    :param input_string: The input string to validate.
    :raises InputValidationError: If the line number exceeds the input size limit or
                                  if the input string does not meet length requirements.

    >>> validate_input_string(50, "Example input")  # This should pass without issue

    >>> validate_input_string(101, "Too many lines")  # This should fail due to line number
    Traceback (most recent call last):
    ...
    scrambled_word_matcher.constraints.InputValidationError: Input file exceeds 100 lines limit

    >>> validate_input_string(5, "")  # This should fail due to short input length
    Traceback (most recent call last):
    ...
    scrambled_word_matcher.constraints.InputValidationError: Line 5 does not meet length requirements (2-500)

    >>> validate_input_string(5, "a" * 501)  # This should fail due to long input length
    Traceback (most recent call last):
    ...
    scrambled_word_matcher.constraints.InputValidationError: Line 5 does not meet length requirements (2-500)
    """

    if not (1 <= line_number <= MAX_INPUT_SIZE):
        raise InputValidationError(f"Input file exceeds {MAX_INPUT_SIZE} lines limit")

    if not (MIN_INPUT_LENGTH <= len(input_string.strip()) <= MAX_INPUT_LENGTH):
        raise InputValidationError(f"Line {line_number} does not meet length requirements ({MIN_INPUT_LENGTH}-{MAX_INPUT_LENGTH})")


def validate_dictionary(dictionary_path: str) -> None:
    """
    Validate the contents of a dictionary file.
    """

    with open(dictionary_path, 'r', encoding='utf-8') as dictionary_file:
        dictionary_words = set()
        for line_number, line in enumerate(dictionary_file, start=1):
            word = line.strip()

            if word in dictionary_words:
                raise ValueError(f"Duplicate word found in dictionary: {word} on line {line_number}")

            validate_dictionary_word(word)
            dictionary_words.add(word)

        if len(dictionary_words) > MAX_DICTIONARY_SIZE:
            raise ValueError("Dictionary exceeds 100 words limit")


def validate_input_file(input_path: str) -> None:
    """
    Validate the contents of an input file.
    """

    with open(input_path, 'r', encoding='utf-8') as input_file:
        for line_number, input_string in enumerate(input_file, start=1):
            validate_input_string(line_number, input_string)
