#!/usr/bin/env bash
source $HOME/.poetry/env
poetry add -vv $(grep -v ";" ./.venv/build_dependency.txt | grep -v "*" )
# poetry add -vv $(grep -v ";" ./.venv/build_dependency.txt | grep -v "*" | sed 's/==/@^/' )
# poetry export -f ./.venv/build_dependency.txt --dev | poetry run -- pip install -r /dev/stdin
