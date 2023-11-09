import unittest
import string
from typing import Tuple, List
from hypothesis import given, strategies as st
from matcher import ScrambledWordMatcher


@st.composite
def arbitrary_scramblings(draw) -> Tuple[str, str]:
    base_word = draw(st.text(min_size=3, max_size=20, alphabet=string.ascii_lowercase))
    first, middle, last = base_word[0], list(base_word[1:-1]), base_word[-1]
    scrambled_middle = draw(st.permutations(middle))
    return base_word, first + ''.join(scrambled_middle) + last

@st.composite
def random_words(draw, alphabet=string.ascii_lowercase, min_size=2, max_size=20) -> str:
    return draw(st.text(alphabet=alphabet, min_size=min_size, max_size=max_size))

@st.composite
def unique_words_list(draw, min_size=2, max_size=20, list_max_size=100) -> List[str]:
    return draw(st.lists(random_words(min_size=min_size, max_size=max_size),
                         unique=True, max_size=list_max_size))

class TestScrambledWordMatcher(unittest.TestCase):

    @given(unique_words_list(), random_words())
    def test_no_false_positives(self, dictionary: List[str], non_dict_word: str) -> None:
        matcher = ScrambledWordMatcher()
        for word in dictionary:
            if sorted(word) != sorted(non_dict_word):
                matcher.add_word(word)
        self.assertEqual(matcher.scan(non_dict_word), 0)

    @given(unique_words_list())
    def test_detection_of_dictionary_words(self, dictionary: List[str]) -> None:
        matcher = ScrambledWordMatcher()
        for word in dictionary:
            matcher.add_word(word)
        self.assertEqual(matcher.scan(' '.join(dictionary)), len(dictionary))

    @given(random_words())
    def test_no_duplicates_counted(self, word: str) -> None:
        matcher = ScrambledWordMatcher()
        matcher.add_word(word)
        repeated = ' '.join([word] * 5)
        self.assertEqual(matcher.scan(repeated), 1)

    @given(unique_words_list(), st.text(min_size=100, max_size=100))
    def test_dictionary_words_in_a_long_text(self, dictionary: List[str], long_text: str) -> None:
        matcher = ScrambledWordMatcher()
        for word in dictionary:
            matcher.add_word(word)
        self.assertGreaterEqual(matcher.scan(long_text + ' ' + ' '.join(dictionary)), len(dictionary))

    @given(arbitrary_scramblings())
    def test_arbitrary_scrambled_word_matching(self, word_and_scrambling: Tuple[str, str]) -> None:
        word, scrambling = word_and_scrambling
        matcher = ScrambledWordMatcher()
        matcher.add_word(word)
        self.assertEqual(matcher.scan(scrambling), 1)

    @given(st.sets(random_words(), max_size=100))
    def test_unique_word_matches(self, words: set) -> None:
        text = ' '.join(words)
        matcher = ScrambledWordMatcher()
        for word in words:
            matcher.add_word(word)
        matches = matcher.scan(text)
        self.assertLessEqual(matches, len(words))

if __name__ == '__main__':
    unittest.main()
