from collections import defaultdict
from typing import Tuple, Dict, Set

Index = Dict[Tuple[str, str], Dict[str, int]]


class ScrambledWordMatcher:
    def __init__(self) -> None:
        self.index: Index = defaultdict(lambda: defaultdict(int))
        self.word_lengths: Set[int] = set()

    def add_word(self, word: str) -> None:
        scramble = ''.join(sorted(word[1:-1]))
        self.index[(word[0], word[-1])][scramble] += 1
        self.word_lengths.add(len(word))

    def scan(self, text: str) -> int:
        count = 0
        word_lengths = sorted(self.word_lengths)

        for i, char in enumerate(text):
            for word_length in word_lengths:

                if i + word_length > len(text):
                    continue

                key = (char, text[i + word_length - 1])
                if key in self.index:
                    candidate = ''.join(sorted(text[i + 1: i + word_length - 1]))

                    if candidate in self.index[key]:
                        count += self.index[key][candidate]
                        self.index[key][candidate] = 0

        return count
