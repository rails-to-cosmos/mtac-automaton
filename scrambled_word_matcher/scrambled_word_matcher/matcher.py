import logging

from contextlib import closing
from functools import cache
from collections import defaultdict
from typing import Tuple, Dict, Set, List

from concurrent.futures import ThreadPoolExecutor
import threading

from scrambled_word_matcher.constraints import validate_dictionary
from scrambled_word_matcher.constraints import validate_input_file
from scrambled_word_matcher.constraints import validate_char

from scrambled_word_matcher.constraints import ALPHABET_SIZE

CharCountTable = Tuple[int, ...]  # Tuple of ALPHABET_SIZE items


@cache
def counting_sort_chars(chars: str) -> CharCountTable:
    """
    Counts the occurrences of each character in a string and returns a tuple with these counts.

    Assumes that input string only contains lowercase English letters (a-z): see the constraints.py for the details.

    :param chars: The string of characters to count.
    :return: A tuple of length ALPHABET_SIZE with the count of each character.

    >>> counting_sort_chars('a')
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    >>> counting_sort_chars('abc')
    (1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    >>> counting_sort_chars('zab')
    (1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)

    >>> counting_sort_chars('mississippi')
    (0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0)

    >>> counting_sort_chars('')  # Empty string should return a tuple of zero counts
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    >>> counting_sort_chars('!')  # Non-alphabet character should raise a ValueError
    Traceback (most recent call last):
    ...
    scrambled_word_matcher.constraints.InputValidationError: Unexpected symbol: !
    """

    count = [0] * ALPHABET_SIZE  # Array of zeros for each letter in the alphabet
    a_ord = ord('a')

    for char in chars:
        validate_char(char)
        count[ord(char) - a_ord] += 1

    return tuple(count)


class ScrambledWordMatcher:
    """
    A class that matches words from a dictionary in any scrambled form within a given text.
    The scrambled form must maintain the first and last letter of the word.

    >>> logger = logging.getLogger('doctest')
    >>> matcher = ScrambledWordMatcher(logger)
    >>> matcher.add_word('maps')
    >>> matcher.add_word('spam')
    >>> matcher.scan('pamsapms')
    1
    """

    def __init__(self, logger: logging.Logger) -> None:
        """
        Initialize the ScrambledWordMatcher with a logger.

        The matcher maintains an index for fast lookups, a set of word lengths to optimize scanning,
        and a count of words added to the dictionary. The logger is used for debugging and information output.

        :param logger: A logging.Logger instance for logging messages.

        Properties:
        - index: A default dictionary to store the occurrence count of words with the same first and last letter.
                 The keys are tuples of the form (first_letter, last_letter), and the values are dictionaries
                 where keys are tuples representing the sorted character counts of the word,
                 and values are the counts of how many times these character counts occur.
        - word_lengths: A set that stores the lengths of all unique words added to the matcher.
                        This is used to optimize the scanning process.
        - word_count: An integer count of the total number of unique words added to the matcher.
                      This is used for early exit.
        - logger: The logging.Logger instance passed during initialization for logging.

        Usage:
        >>> import logging
        >>> logger = logging.getLogger('test_logger')
        >>> matcher = ScrambledWordMatcher(logger)
        """

        self.index: Dict[Tuple[str, str], Dict[Tuple, int]] = defaultdict(lambda: defaultdict(int))
        self.word_lengths: Set[int] = set()
        self.word_count: int = 0
        self.logger = logger
        self.lock = threading.Lock()

    def import_dictionary(self, dictionary_path: str) -> None:
        validate_dictionary(dictionary_path)

        with open(dictionary_path, 'r', encoding='utf-8') as dictionary_file:
            for line in dictionary_file:
                self.add_word(line.strip())

    def add_words(self, words: List[str]) -> None:
        with ThreadPoolExecutor() as executor:
            executor.map(self.add_word, words)

    def add_word(self, word: str) -> None:
        """
        Adds a word to the matcher's dictionary for later matching.

        This method updates the matcher's index with the character count signature
        of the word's middle characters (excluding the first and last character).
        It also updates the set of word lengths and the total word count.

        The word is expected to only contain lowercase English letters (a-z),
        and it must be at least 2 characters long.

        :param word: The word to be added to the dictionary. It is assumed
                     that 'word' has already been validated for length and character set.

        Usage:
        >>> matcher = ScrambledWordMatcher(logging.getLogger('test'))
        >>> matcher.add_word('apple')
        >>> matcher.word_count
        1
        >>> matcher.index[('a', 'e')][tuple(counting_sort_chars('apple'))]
        1
        >>> matcher.add_word('apply')
        >>> matcher.word_count
        2
        >>> matcher.index[('a', 'y')][tuple(counting_sort_chars('apply'))]
        1
        >>> 'apple' in matcher.index[('a', 'e')]
        False
        """

        key = (word[0], word[-1])
        scramble = counting_sort_chars(word)

        with self.lock:
            self.index[key][scramble] += 1
            self.word_lengths.add(len(word))
            self.word_count += 1

    def scan_file(self, input_path: str) -> List[int]:
        """
        Reads the input file line by line, scans each line for matches against the
        dictionary, and returns a list of match counts for each line.

        Before scanning, the input file is validated to ensure it meets the required
        criteria (e.g., line count, line length).

        :param input_path: The file system path to the input file to be scanned.
        :return: A list of integers where each integer is the number of matches
                 found in the corresponding line of the input file.
        """

        validate_input_file(input_path)

        input_lines = []

        with closing(open(input_path, 'r', encoding='utf-8')) as input_file:
            for input_line in input_file:
                input_lines.append(input_line)

        result = []

        for line in input_lines:
            matches = self.scan(line.strip())
            result.append(matches)

        return result

    def scan(self, text: str) -> int:
        """
        Scan the given text and count the number of dictionary word occurrences.

        The method implements a sliding window to count occurrences of each character in the window,
        compares the count against the stored dictionary counts, and returns count of matches.

        It also ensures that each dictionary word is only counted once per text scan.

        :param text: The string of text to be scanned for dictionary word occurrences.
        :return: The total count of dictionary word matches found in the text.

        Usage:
        >>> matcher = ScrambledWordMatcher(logging.getLogger('test'))
        >>> matcher.add_word('hello')
        >>> matcher.add_word('world')
        >>> matcher.scan('ehllodlrowhelloworld')
        2
        """

        matches = 0
        seen: Set[Tuple[Tuple[str, str], CharCountTable]] = set()

        sliding_window_counts = self.init_sliding_windows(text)

        for left_index, left_char in enumerate(text):
            validate_char(left_char)

            for word_length in self.word_lengths:
                right_index = left_index + word_length - 1
                if right_index >= len(text):
                    continue  # Potential optimization: we could break if self.word_lengths is sorted.
                right_char = text[right_index]
                validate_char(right_char)

                window_counts = sliding_window_counts[word_length]
                if left_index > 0:  # Decrement the count for the character that's sliding out of the window
                    sliding_out_char = text[left_index - 1]
                    window_counts[ord(sliding_out_char) - ord('a')] -= 1

                    # Increment the count for the character that's sliding in
                    if right_index < len(text):
                        sliding_in_char = text[right_index]
                        validate_char(sliding_in_char)
                        window_counts[ord(sliding_in_char) - ord('a')] += 1

                key = (left_char, right_char)
                if key not in self.index:
                    continue

                # Create a tuple from the window counts for efficient comparison
                candidate = tuple(window_counts)
                if candidate in self.index[key] and (key, candidate) not in seen:
                    matches += self.index[key][candidate]
                    seen.add((key, candidate))

                    if len(seen) == self.word_count:  # Early exit
                        return matches

        return matches

    def init_sliding_windows(self, text: str) -> Dict[int, List[int]]:
        """
        Initializes sliding windows for distinct character counts in the given text.

        This method prepares a dictionary with keys as word lengths and values as lists.
        Each list represents the count of each letter in the alphabet within the sliding
        window at the beginning of the text.

        :param text: The text for which the sliding windows are to be initialized.
        :return: A dictionary mapping word lengths to character count lists.

        Usage:
        >>> matcher = ScrambledWordMatcher(logging.getLogger('test'))
        >>> matcher.word_lengths = {3, 4, 5}  # Assume these lengths are in the dictionary
        >>> sliding_windows = matcher.init_sliding_windows('hello')
        >>> sliding_windows[3]
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        >>> sliding_windows[4]
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        >>> sliding_windows[5]
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        """

        sliding_window_counts: Dict[int, List[int]] = {word_length: [0] * ALPHABET_SIZE for word_length in self.word_lengths}

        for word_length in self.word_lengths:
            window_counts = sliding_window_counts[word_length]

            i = 0
            while i < min(word_length, len(text)):
                char = text[i]
                validate_char(char)
                window_counts[ord(char) - ord('a')] += 1
                i += 1

        return sliding_window_counts
