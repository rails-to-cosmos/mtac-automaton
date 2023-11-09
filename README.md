# ScrambledWordMatcher

`ScrambledWordMatcher` is a Python utility that enables permuted pattern matching of words. Given a dictionary, it can find and count instances of the words within an input string, even when the letters in the words are scrambled, provided that the first and last letters of the word remain in place.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- [devenv](https://devenv.sh) and [direnv](https://direnv.net) for container-less isolated environment
- [Optional] Docker

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

## Additional Information

- The current implementation is optimized for ASCII lowercase input.
- Future enhancements could include:
  - Performance improvements for larger datasets or even infinite stream of inputs, such as:
    - Using [multi-track permuted matching automaton](https://www.mdpi.com/1999-4893/12/4/73) matching algorithms applied to the current problem definition;
    - Parallel processing;

  - Support for Unicode characters
  - Case-insensitive matching


## Authors

    Dmitry Akatov - rails-to-cosmos
