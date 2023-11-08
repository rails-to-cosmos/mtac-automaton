from bisect import insort, bisect_left
from collections import defaultdict
from typing import Tuple, Dict, Set, List


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
        self.index: Dict[Tuple[str, str], Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.word_lengths: List[int] = []
        self.word_count: int = 0

    def add_word(self, word: str) -> None:
        """
        Adds a word to the matcher's dictionary.

        >>> matcher = ScrambledWordMatcher()
        >>> matcher.add_word('maps')
        >>> matcher.word_count
        1
        """

        key = (word[0], word[-1])
        scramble = ''.join(sorted(word[1:-1]))
        self.index[key][scramble] += 1

        lookup = len(word)
        index = bisect_left(self.word_lengths, lookup)
        if index == len(self.word_lengths) or self.word_lengths[index] != lookup:
            insort(self.word_lengths, lookup)

        self.word_count += 1

    def scan(self, text: str) -> int:
        """
        Scans a given text and counts the number of matched words from the dictionary.

        >>> matcher = ScrambledWordMatcher()
        >>> matcher.add_word('maps')
        >>> matcher.add_word('spam')
        >>> matcher.scan('pamsapms')
        1
        """

        count = 0

        sliding_windows: Dict[int, Dict[str, int]] = {
            word_length: defaultdict(int)
            for word_length in self.word_lengths
        }

        seen = set()

        for i, char in enumerate(text):
            for word_length in self.word_lengths:

                if i + word_length > len(text):
                    break

                key = (char, text[i + word_length - 1])
                if key not in self.index:
                    continue

                window = sliding_windows[word_length]
                window[char] += 1

                candidate = ''.join(sorted(text[i + 1: i + word_length - 1]))

                if candidate in self.index[key] and (key, candidate) not in seen:
                    count += self.index[key][candidate]
                    seen.add((key, candidate))

                    if len(seen) == self.word_count:  # early exit
                        return count

        return count

if __name__ == "__main__":
    import doctest
    doctest.testmod()
