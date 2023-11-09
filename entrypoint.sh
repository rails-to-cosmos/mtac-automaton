#!/bin/bash

output=$(devenv shell bash scrambled-strings $@ 2>&1 | tail -n +2)

echo -e "${output}"
