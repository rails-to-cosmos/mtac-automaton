"Generates sample files and benchmarks the system."

import timeit
import random
import string
import statistics
import tempfile
import os

from contextlib import closing
from typing import List, Tuple, Set

from scrambled_word_matcher import ScrambledWordMatcher

DICTIONARY_SIZE = 100
MIN_WORD_LENGTH = 2
MAX_WORD_LENGTH = 20
MAX_LINES = 100
MAX_LINE_LENGTH = 500

REPEAT_COUNT = 10

def calculate_percentile(data: List[float], percentile: float) -> float:
    size = len(data)
    return sorted(data)[int(size * percentile / 100)]

def generate_dictionary_file() -> str:
    words: Set[str] = set()
    while len(words) < DICTIONARY_SIZE:
        word_length = random.randint(MIN_WORD_LENGTH, MAX_WORD_LENGTH)
        word = ''.join(random.choices(string.ascii_lowercase, k=word_length))
        words.add(word)

    with closing(tempfile.NamedTemporaryFile(mode='w', delete=False)) as temp_file:
        for word in words:
            temp_file.write(word + '\n')

    return temp_file.name

def generate_input_file() -> str:
    lines = random.randint(1, MAX_LINES)

    with closing(tempfile.NamedTemporaryFile(mode='w', delete=False)) as temp_file:
        for _ in range(lines):
            line_length = random.randint(MIN_WORD_LENGTH, MAX_LINE_LENGTH)
            line = ''.join(random.choices(string.ascii_lowercase, k=line_length))
            temp_file.write(line + '\n')

    return temp_file.name

def setup_matcher(dictionary_file: str) -> ScrambledWordMatcher:
    matcher = ScrambledWordMatcher()
    with open(dictionary_file) as f:
        for word in f:
            matcher.add_word(word.strip())
    return matcher

def run_benchmark(dictionary_file: str, input_file: str) -> Tuple[float, float, float, float, float]:
    matcher = setup_matcher(dictionary_file)
    with open(input_file, 'r') as f:
        text = f.read()

    times: List[float] = timeit.repeat(lambda: matcher.scan(text), number=1, repeat=REPEAT_COUNT)
    min_time: float = min(times)
    median_time: float = statistics.median(times)
    percentile_25: float = calculate_percentile(times, 25)
    percentile_75: float = calculate_percentile(times, 75)
    percentile_90: float = calculate_percentile(times, 90)
    return min_time, median_time, percentile_25, percentile_75, percentile_90

if __name__ == '__main__':
    dictionary_file = generate_dictionary_file()
    input_file = generate_input_file()

    try:
        min_time, median_time, perc_25, perc_75, perc_90 = run_benchmark(dictionary_file, input_file)
        print(f"Minimum execution time over {REPEAT_COUNT} runs: {min_time:.4f} seconds")
        print(f"Median execution time over {REPEAT_COUNT} runs: {median_time:.4f} seconds")
        print(f"25th percentile execution time: {perc_25:.4f} seconds")
        print(f"75th percentile execution time: {perc_75:.4f} seconds")
        print(f"90th percentile execution time: {perc_90:.4f} seconds")
    finally:
        # Remove the temporary files after the benchmark
        os.remove(dictionary_file)
        os.remove(input_file)
