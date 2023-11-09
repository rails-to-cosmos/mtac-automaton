# ScrambledWordMatcher

This is a Python utility that enables permuted pattern matching of words. Given a dictionary, it can find and count instances of the words within an input string, even when the letters in the words are scrambled, provided that the first and last letters of the word remain in place.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- [devenv](https://devenv.sh) and [direnv](https://direnv.net) for container-less isolated environment
- [*Optional*] [Docker](https://www.docker.com) or analogue like [Lima](https://github.com/lima-vm/lima), [Podman](https://podman.io) or [Kaniko](https://github.com/GoogleContainerTools/kaniko) for building and running container

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/rails-to-cosmos/scrambled-word-matcher.git
cd scrambled-word-matcher
```

Install the required dependencies in isolated environment associated with the current directory:

```bash
direnv allow
```

## Running the Tests

To run the tests, execute the following command from the root directory of the project:

```bash
devenv shell ./test.sh
```

or simply (assuming you're already inside devenv shell):

```bash
./test.sh
```

## Building the Program

The program is a Python script, so there is no build step required.

## Running the Command

To use ScrambledWordMatcher, you need to provide a dictionary file and an input file. I prepared sample data for you in a `sample` directory. Run the command as follows:

```bash
devenv shell ./scrambled-strings --dictionary sample/dictionary.txt --input sample/input.txt
```

or simply (assuming you're already inside devenv shell):

```bash
./scrambled-strings --dictionary sample/dictionary.txt --input sample/input.txt
```

## Docker

The `ScrambledWordMatcher` can also be built and run using Docker. This ensures that your execution environment is consistent and isolated from the host system.

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

## Design Concepts

The matcher uses a sorting approach to identify scrambled words that match dictionary entries. Optimization efforts focus on minimizing the complexity of sorting operations and early termination of the search when possible.

## Algorithmic Complexity Analysis

The `ScrambledWordMatcher` is designed to efficiently match words from a dictionary in any scrambled form within a given text, with the constraint that the first and last letters of the word remain in place. Below is the analysis of time and memory complexities of the underlying algorithms:

### Time Complexity

The time complexity of the `add_word` method is O(N log N), where N is the length of the word being added. This is due to the sorting operation on the scrambled portion of the word.

The `scan` method has a more complex time complexity. For each position in the text, it checks possible matches for all dictionary words, resulting in a complexity of O(M * W * L log L), where:
- M is the length of the text to be scanned.
- W is the number of words in the dictionary.
- L is the average length of the words in the dictionary.

This complexity arises because for each character in the text, the algorithm generates substrings of lengths that match the word lengths in the dictionary and sorts each substring (L log L). It then checks these against the possible scrambled forms in the dictionary (W).

### Memory Complexity

The memory complexity is mainly dictated by the data structures used to store the dictionary words and their scrambled forms.

- The `index` dictionary has a key for each unique starting and ending character pair and stores another dictionary whose keys are the sorted middle characters of the words. This means the memory usage will be `O(U + S)`, where `U` is the number of unique character pairs, and `S` is the total number of all sorted middle characters from all words.
- The `word_lengths` set stores the lengths of the words, which at most can be the maximum word length permitted, hence `O(L_max)`, where L_max is the maximum word length (which equals `20` in our case).
- The `seen` set in the `scan` method can grow to be as large as the number of unique words in the dictionary in the worst case (equals `100` words), so its memory complexity is O(W).

### Parallel Execution Consideration

Parallelizing the `add_word` and `scan` methods would not change the overall time complexity but can greatly reduce the actual time taken to process large dictionaries and texts by making use of multiple CPU cores.

Memory complexity in a parallelized context could increase due to additional structures needed for synchronization and potential duplication of data across threads or processes. The specific increase would depend on the implementation details of the parallelization method used.

## Additional Information

- The current implementation is optimized for ASCII lowercase input.

- Future enhancements could include:
  - Performance improvements for larger datasets or even infinite stream of inputs, such as:
    - Using [multi-track permuted matching automaton](https://www.mdpi.com/1999-4893/12/4/73) matching algorithms applied to the current problem definition. The hard part is to implement failure links efficiently for permuted matches and add support for dictionary words of different lengths.
    - Parallel processing:
      - `add_word` method can be parallelized by dividing the dictionary into chunks and processing each chunk in a separate thread or process. Since writing to the ScrambledWordMatcher.index involves shared state, we would need to synchronize access to this shared resource to prevent race conditions.
      - `scan` method of ScrambledWordMatcher doesn't share state. So we can run `scan` method in parallel on different input lines or even partition long input lines to chunks ensuring that the division takes place at word boundaries to avoid splitting words that could be matched.

  - Reimplementation in a more efficient runtime (eg Nim, Go or Scala)

  - Support for Unicode characters and case-insensitive matching (actually can be performed with the current implementation as well)

## Authors

    Dmitry Akatov - rails-to-cosmos
