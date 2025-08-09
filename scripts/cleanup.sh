#!/bin/bash

GITIGNORE_FILE=".gitignore"

cat $GITIGNORE_FILE | xargs rm -rf

find "${1:-.}" -type d -name "__pycache__" -exec rm -rf {} +
