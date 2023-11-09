import unittest

from scrambled_word_matcher import ScrambledWordMatcher
from scrambled_word_matcher.logger import init_logger

TEST_LOGGER = init_logger('test.matcher')

class TestScrambledWordMatcher(unittest.TestCase):
    def test_empty(self):
        "Test empty dictionary."

        matcher = ScrambledWordMatcher(TEST_LOGGER)
        self.assertEqual(matcher.scan('hello'), 0)

    def test_definition(self):
        "Test case from the task definition."

        matcher = ScrambledWordMatcher(TEST_LOGGER)
        matcher.add_word('axpaj')
        matcher.add_word('apxaj')
        matcher.add_word('dnrbt')
        matcher.add_word('pjxdn')
        matcher.add_word('abd')

        self.assertEqual(matcher.scan('aapxjdnrbtvldptfzbbdbbzxtndrvjblnzjfpvhdhhpxjdnrbt'), 4)

    def test_scramble(self):
        "Checks scrambled matching."

        matcher = ScrambledWordMatcher(TEST_LOGGER)
        matcher.add_word('abez')
        matcher.add_word('abfy')

        self.assertEqual(matcher.scan('aebz'), 1)

    def test_scramble_terminate(self):
        "Checks if matcher handles sliding windows properly."

        matcher = ScrambledWordMatcher(TEST_LOGGER)
        matcher.add_word('abeaz')
        matcher.add_word('abfy')

        self.assertEqual(matcher.scan('abeaz'), 1)

    def test_false_positive(self):
        "No false positives should arise."

        matcher = ScrambledWordMatcher(TEST_LOGGER)
        matcher.add_word('abeaz')
        matcher.add_word('abfy')

        self.assertEqual(matcher.scan('abyf'), 0)

    def test_simple(self):
        matcher = ScrambledWordMatcher(TEST_LOGGER)
        matcher.add_word('star')
        matcher.add_word('loop')
        matcher.add_word('part')

        self.assertEqual(matcher.scan('wtsartsatroplopratlopostar'), 2)

    def test_long_input(self):
        matcher = ScrambledWordMatcher(TEST_LOGGER)
        matcher.add_word('aaaaaaaa')
        matcher.add_word('ab')

        long_text = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab'

        self.assertEqual(matcher.scan(long_text), 2)

    def test_multi_scan(self):
        matcher = ScrambledWordMatcher(TEST_LOGGER)
        matcher.add_word('axpaj')
        matcher.add_word('apxaj')
        matcher.add_word('dnrbt')
        matcher.add_word('pjxdn')
        matcher.add_word('abd')

        self.assertEqual(matcher.scan('aapxjdnrbtvldptfzbbdbbzxtndrvjblnzjfpvhdhhpxjdnrbt'), 4)
        self.assertEqual(matcher.scan('aapxj'), 2)
        self.assertEqual(matcher.scan('adb'), 0)
        self.assertEqual(matcher.scan('adbtpdxjn'), 1)

if __name__ == '__main__':
    unittest.main()
