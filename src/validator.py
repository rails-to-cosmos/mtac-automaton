def validate_dictionary(dictionary_path: str) -> None:
    with open(dictionary_path, 'r') as dictionary_file:
        dictionary_words = set()
        for line_number, line in enumerate(dictionary_file, start=1):
            word = line.strip()
            if word in dictionary_words:
                raise ValueError(f"Duplicate word found in dictionary: {word} on line {line_number}")
            if not (2 <= len(word) <= 20):
                raise ValueError(f"Word '{word}' does not meet length requirements (2-20) on line {line_number}")
            dictionary_words.add(word)
        if len(dictionary_words) > 100:
            raise ValueError("Dictionary exceeds 100 words limit")


def validate_input_file(input_path: str) -> None:
    with open(input_path, 'r') as input_file:
        for line_number, line in enumerate(input_file, start=1):
            if not (1 <= line_number <= 100):
                raise ValueError("Input file exceeds 100 lines limit")
            if not (2 <= len(line.strip()) <= 500):
                raise ValueError(f"Line {line_number} does not meet length requirements (2-500)")
