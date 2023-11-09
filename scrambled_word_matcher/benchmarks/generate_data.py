import itertools
import random
import string

# Constants for the file generation
DICTIONARY_FILE = 'resources/dictionary.txt'
INPUT_FILE = 'resources/input.txt'
MAX_DICT_WORDS = 100
MAX_WORD_LENGTH = 20
MAX_INPUT_LINES = 100
MAX_LINE_LENGTH = 500

base_word = ''.join(random.choices(string.ascii_lowercase, k=MAX_WORD_LENGTH))

def create_permutation_word():
    return ''.join(random.sample(base_word, len(base_word)))

def create_dictionary_file():
    words = (''.join(p) for p in itertools.permutations(base_word, MAX_WORD_LENGTH))
    unique = set()

    for i, word in enumerate(words):
        if len(unique) >= MAX_DICT_WORDS:
            break
        unique.add(word)

    with open(DICTIONARY_FILE, 'w') as f:
        for i in range(2, 21):
            word = unique.pop()
            f.write(f"{word[:i]}\n")

def create_input_file():
    with open(INPUT_FILE, 'w') as f:
        for _ in range(MAX_INPUT_LINES):
            line = ''.join(create_permutation_word() for _ in range(MAX_LINE_LENGTH // MAX_WORD_LENGTH))
            f.write(f"{line}\n")

create_dictionary_file()
create_input_file()

print(f"Dictionary and input files created: {DICTIONARY_FILE}, {INPUT_FILE}")
