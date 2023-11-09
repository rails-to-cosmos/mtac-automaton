#!/bin/bash

set -e
export PYTHONPATH="scrambled_word_matcher"
pipenv run python scrambled_word_matcher/run_benchmarks.py
