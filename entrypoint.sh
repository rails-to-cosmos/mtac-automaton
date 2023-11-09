#!/bin/bash

set -e
export PYTHONPATH="scrambled_word_matcher"

devenv shell
pipenv run pytest . --verbose $@
