import argparse

from scrambled_word_matcher.logger import init_logger
from scrambled_word_matcher import ScrambledWordMatcher


def main(dictionary_path: str, input_path: str):
    logger = init_logger('main')

    matcher = ScrambledWordMatcher(logger)
    matcher.add_dictionary(dictionary_path)
    matcher.scan_file(input_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrambled String Matcher CLI')
    parser.add_argument('--dictionary', type=str, required=True, help='Path to the dictionary file')
    parser.add_argument('--input', type=str, required=True, help='Path to the input file')

    args = parser.parse_args()

    main(args.dictionary, args.input)
