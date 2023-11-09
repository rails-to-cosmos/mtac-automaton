# Scrambled Word Matcher

This is a Python utility that enables permuted pattern matching of words. Given a dictionary, it can find and count instances of the words within an input string, even when the letters in the words are scrambled, provided that the first and last letters of the word remain in place.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

- [devenv](https://devenv.sh) and [direnv](https://direnv.net) for container-less isolated environment.
- *[Optional]* If you don't like the Nix approach, you can install [Python 3.11](https://www.python.org/downloads/release/python-3110/) via [pyenv](https://github.com/pyenv/pyenv), [pip](https://pypi.org/project/pip/) and [pipenv](https://pipenv.pypa.io/en/latest/).
- *[Optional]* [Docker](https://www.docker.com) or similar tool like [Lima](https://github.com/lima-vm/lima), [Podman](https://podman.io) or [Kaniko](https://github.com/GoogleContainerTools/kaniko) for the container management.

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/rails-to-cosmos/scrambled-word-matcher.git
cd scrambled-word-matcher
 ```

Install the required dependencies in isolated environment associated with the current directory:

```bash
direnv allow  # in case you have devenv and direnv installed
pipenv install --dev
```

### Running the Tests

To run the tests (I provided some unit tests, doc tests and property tests), execute the following command from the root directory of the project:

```bash
./test.sh
```

### Running the Benchmarks

To run the benchmarks, execute the following command:

```bash
./benchmark.sh
```

### Running the Matcher

To use Scrambled Word Matcher, you need to provide a dictionary file and an input file. I prepared sample data for you in a `sample` directory. Run the command as follows:

```bash
./scrambled-strings --dictionary sample/dictionary.txt --input sample/input.txt
```

## Docker

The Scrambled Word Matcher can also be built and run using Docker. This ensures that your execution environment is consistent and isolated from the host system.

### Building the Docker Image

To build the Docker image, navigate to the directory containing the Dockerfile and run the following command:

```bash
docker build -t scrambled-strings-matcher .
```

This will create a Docker image named scrambled-strings-matcher based on the instructions in your Dockerfile.

### Running the Program in Docker

Once the image is built, you can run the program inside a Docker container. To do so, you must mount the directory containing your dictionary and input files to the container. Run the following command, replacing `./sample` with the path to your host directory that contains `dictionary.txt` and `input.txt` files:

```bash
docker run -v $(pwd)/sample:/tmp/sample scrambled-strings-matcher --dictionary=/tmp/sample/dictionary.txt --input=/tmp/sample/input.txt
```

This command mounts the local `./sample` directory to `/tmp/sample` inside the container, and then runs the `scrambled-strings-matcher` using the provided dictionary and input files.

Please ensure that you have the `dictionary.txt` and `input.txt` files in the `./sample` directory on your host machine before running the Docker command.

### Notes

- You may need to use absolute paths depending on your Docker setup and operating system.
- Ensure Docker has permissions to access the directories/files you're trying to mount.

## Algorithmic Overview

The Scrambled Word Matcher utilizes a counting sort approach for the inner characters of words to identify matches in a given text, optimizing search operations and leveraging caching for efficient lookups.

## Complexity Analysis

The Scrambled Word Matcher is designed to efficiently match words from a dictionary in any scrambled form within a given text, with the constraint that the first and last letters of the word remain in place. Below is the analysis of time and memory complexities of the underlying algorithms:

### Time Complexity

- `add_word`: O(L) for a word of length L, due to the counting sort approach for character frequencies.

- `scan`: O(M * D * L) approximately, where M is the length of the text, D is the density of potential matches, and L is the maximum word length. Actual complexity may vary with early termination and the sparsity of matches.

### Memory Complexity

Memory usage is primarily due to the storage of sorted character counts:

- Dictionary Storage: O(W * L), where W is the number of words and L is the average word length.

- Sliding Window: O(L), with a single sliding window traversing the text.

### Parallel Execution Consideration

The design facilitates parallel processing, which improves the efficiency of both operations (adding words and scan), depending on the dataset size and system capabilities. In `scan_lines` I use ThreadPoolExecutor for the sake of simplicity (Matcher has some non-serializable fields). Potentially ThreadPoolExecutor could be changed to ProcessPoolExecutor to avoid Python's GIL downsides on CPU-bound processing.

### Enhancements

Future updates might include:

- Adaptation for case-insensitive and Unicode support.

- Algorithmic refinements for improved performance with large-scale data.

- Possible reimplementations in more performance-oriented languages (eg Nim, Go, Scala).

## Author

- Dmitry Akatov (rails-to-cosmos) - Initial work

Feel free to use and contribute to the development of this utility.
