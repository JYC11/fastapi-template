#!/bin/sh -e
set -x

ruff check --fix .
black . --line-length=120
mypy --check-untyped-defs -p src
