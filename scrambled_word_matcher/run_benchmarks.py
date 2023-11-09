"Generates sample files and benchmarks the system."

import os
import random
import statistics
import string
import tempfile
import timeit
from contextlib import closing

from typing import List, Tuple, Set

from scrambled_word_matcher import ScrambledWordMatcher
from scrambled_word_matcher.logger import init_logger
from scrambled_word_matcher.constraints import MAX_DICTIONARY_SIZE
from scrambled_word_matcher.constraints import MIN_INPUT_LENGTH
from scrambled_word_matcher.constraints import MAX_INPUT_LENGTH
from scrambled_word_matcher.constraints import MAX_INPUT_SIZE

BENCHMARK_REPEAT_COUNT = 100
BENCHMARK_LOGGER = init_logger('benchmark')


def calculate_percentile(data: List[float], percentile: float) -> float:
    """
    Calculate the given percentile of a list of numbers.

    :param data: A list of floating-point numbers.
    :param percentile: The percentile to calculate (a float between 0 and 100).
    :return: The percentile value from the data.

    Examples:
    >>> calculate_percentile([10, 20, 30, 40, 50], 25)
    20.0
    >>> calculate_percentile([1, 2, 3, 4, 5], 50)
    3.0
    >>> calculate_percentile([1, 3, 5, 7, 9], 80)
    7.2
    >>> calculate_percentile([1.5, 3.5, 4.5, 6.5], 75)
    5.25
    """

    if not data:
        raise ValueError("Data list cannot be empty.")

    if not 0 <= percentile <= 100:
        raise ValueError("Percentile must be between 0 and 100.")

    size = len(data)
    if size == 1:
        return data[0]

    # When the percentile does not fall exactly on an index, interpolate between the two surrounding data points.
    index = (size * percentile / 100)
    prev_index = int(index)
    next_index = min(prev_index + 1, size - 1)
    interpolation = index - prev_index

    sorted_data = sorted(data)
    return sorted_data[prev_index] * (1 - interpolation) + sorted_data[next_index] * interpolation


def generate_dictionary_file() -> str:
    words: Set[str] = set()

    while len(words) < MAX_DICTIONARY_SIZE:
        word_length = random.randint(MIN_INPUT_LENGTH, MAX_INPUT_LENGTH)
        word = ''.join(random.choices(string.ascii_lowercase, k=word_length))
        words.add(word)

    with closing(tempfile.NamedTemporaryFile(mode='w', delete=False)) as temp_file:
        for word in words:
            temp_file.write(word)

    return temp_file.name


def generate_input_file() -> str:
    lines = random.randint(1, MAX_INPUT_SIZE)

    with closing(tempfile.NamedTemporaryFile(mode='w', delete=False)) as temp_file:
        for _ in range(lines):
            line_length = random.randint(MIN_INPUT_LENGTH, MAX_INPUT_LENGTH)
            line = ''.join(random.choices(string.ascii_lowercase, k=line_length))
            temp_file.write(line)

    return temp_file.name


def setup_matcher(dictionary_file: str) -> ScrambledWordMatcher:
    matcher = ScrambledWordMatcher(BENCHMARK_LOGGER)
    with open(dictionary_file) as f:
        for word in f:
            matcher.add_word(word.strip())
    return matcher


def run_benchmark(dictionary_file: str, input_file: str) -> Tuple[float, float, float, float, float]:
    matcher = setup_matcher(dictionary_file)
    with open(input_file, 'r') as f:
        text = f.read()

    times: List[float] = timeit.repeat(lambda: matcher.scan(text), number=1, repeat=BENCHMARK_REPEAT_COUNT)
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
        print(f"Minimum execution time over {BENCHMARK_REPEAT_COUNT} runs: {min_time:.4f} seconds")
        print(f"Median execution time over {BENCHMARK_REPEAT_COUNT} runs: {median_time:.4f} seconds")
        print(f"25th percentile execution time: {perc_25:.4f} seconds")
        print(f"75th percentile execution time: {perc_75:.4f} seconds")
        print(f"90th percentile execution time: {perc_90:.4f} seconds")
    finally:
        # Remove the temporary files after the benchmark
        os.remove(dictionary_file)
        os.remove(input_file)
