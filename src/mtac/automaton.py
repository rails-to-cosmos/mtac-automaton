from bisect import insort, bisect_left
from collections import defaultdict
from typing import Tuple, Dict, Set, List


class ScrambledWordMatcher:
    def __init__(self) -> None:
        self.index: Dict[Tuple[str, str], Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.word_lengths: List[int] = list()

    def add_word(self, word: str) -> None:
        scramble = ''.join(sorted(word[1:-1]))
        self.index[(word[0], word[-1])][scramble] += 1

        lookup = len(word)
        index = bisect_left(self.word_lengths, lookup)
        if index == len(self.word_lengths) or self.word_lengths[index] != lookup:
            insort(self.word_lengths, lookup)

    def scan(self, text: str) -> int:
        count = 0
        word_lengths = sorted(self.word_lengths)
        sliding_windows: Dict[int, Dict[str, int]] = {word_length: defaultdict(int) for word_length in word_lengths}

        for i, char in enumerate(text):
            for word_length in word_lengths:

                if i + word_length > len(text):
                    break

                key = (char, text[i + word_length - 1])
                if key not in self.index:
                    continue

                window = sliding_windows[word_length]
                window[char] += 1

                candidate = ''.join(sorted(text[i + 1: i + word_length - 1]))

                if candidate in self.index[key]:
                    count += self.index[key][candidate]
                    self.index[key][candidate] = 0

        return count
