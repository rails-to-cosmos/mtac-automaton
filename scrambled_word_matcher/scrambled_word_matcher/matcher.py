from functools import cache
from collections import defaultdict
from typing import Tuple, Dict, Set, List

ALPHABET_SIZE = 26

CharCountTable = Tuple[int, ...]  # Tuple of ALPHABET_SIZE items


@cache
def validate_char(char: str) -> None:
    char_lookup_index = ord(char) - ord('a')
    if not 0 <= char_lookup_index < ALPHABET_SIZE:
        raise ValueError('Unexpected symbol: %s', char)


@cache
def counting_sort_chars(chars: str) -> CharCountTable:
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

    >>> matcher = ScrambledWordMatcher()
    >>> matcher.add_word('maps')
    >>> matcher.add_word('spam')
    >>> matcher.scan('pamsapms')
    1
    """

    def __init__(self) -> None:
        # The inner dict now holds a tuple (counts of letters) instead of a string
        self.index: Dict[Tuple[str, str], Dict[Tuple, int]] = defaultdict(lambda: defaultdict(int))
        self.word_lengths: Set[int] = set()
        self.word_count: int = 0

    def add_word(self, word: str) -> None:
        key = (word[0], word[-1])

        # Use counting sort to create a tuple representing the character counts
        scramble = counting_sort_chars(word)
        self.index[key][scramble] += 1
        self.word_lengths.add(len(word))
        self.word_count += 1

    def scan(self, text: str) -> int:
        matches = 0
        seen: Set[Tuple[Tuple[str, str], CharCountTable]] = set()

        sliding_window_counts = self.init_sliding_windows(text)

        for left_index, char in enumerate(text):
            validate_char(char)

            for word_length in self.word_lengths:
                right_index = left_index + word_length - 1

                if left_index + word_length > len(text):
                    continue

                window_counts = sliding_window_counts[word_length]
                if left_index > 0:  # Decrement the count for the character that's sliding out of the window
                    sliding_out_char = text[left_index - 1]
                    window_counts[ord(sliding_out_char) - ord('a')] -= 1

                    # Increment the count for the character that's sliding in
                    if right_index < len(text):
                        sliding_in_char = text[right_index]
                        validate_char(sliding_in_char)
                        window_counts[ord(sliding_in_char) - ord('a')] += 1

                key = (char, text[right_index])
                if key not in self.index:
                    continue

                # Create a tuple from the window counts for comparison
                candidate = tuple(window_counts)
                if candidate in self.index[key] and (key, candidate) not in seen:
                    matches += self.index[key][candidate]
                    seen.add((key, candidate))

                    if len(seen) == self.word_count:  # Early exit
                        return matches

        return matches

    def init_sliding_windows(self, text: str) -> Dict[int, List[int]]:
        "Prepares initial state of sliding windows that we will use for scan."

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
