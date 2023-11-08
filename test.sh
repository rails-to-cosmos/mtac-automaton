#!/bin/bash

set -e

if [[ "$*" == *"-k"* ]]; then
    echo "Running specific test case (skip other checks)"
else
    pipenv run mypy .  # run type checks
    pipenv run python -m src.mtac.utils.text  # run doctests for utils
fi

pipenv run pytest . --verbose $@ # run unit tests
