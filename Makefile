include .env

checks:
	sh scripts/checks.sh

run-local:
	sh scripts/run.sh

test-unit:
	pytest tests/unit

test-integration:
	pytest tests/integration

test-e2e:
	pytest tests/e2e

test:
	pytest

test-cov:
	pytest --cov=src/

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt  && mypy --install-types

uninstall:
	pip freeze | xargs pip uninstall -y