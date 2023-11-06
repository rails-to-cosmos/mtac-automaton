#!/bin/bash

pipenv run mypy .
pipenv run python -m doctest -v src/automaton.py
