import argparse

from matcher import ScrambledWordMatcher
from validator import validate_dictionary
from validator import validate_input_file


def main(dictionary_path: str, input_path: str):
    validate_dictionary(dictionary_path)
    validate_input_file(input_path)

    matcher = ScrambledWordMatcher()

    with open(dictionary_path, 'r') as dictionary_file:  # Read and add words from the dictionary
        for line in dictionary_file:
            word = line.strip()
            matcher.add_word(word)

    with open(input_path, 'r') as input_file:  # Read the input file and scan for matches
        for case_number, line in enumerate(input_file, start=1):
            matches = matcher.scan(line)
            print(f'Case #{case_number}: {matches}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrambled String Matcher CLI')
    parser.add_argument('--dictionary', type=str, required=True, help='Path to the dictionary file')
    parser.add_argument('--input', type=str, required=True, help='Path to the input file')

    args = parser.parse_args()

    main(args.dictionary, args.input)
