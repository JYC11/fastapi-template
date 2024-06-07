include .env

run-dev:
	fastapi dev src/main.py

init-db:
	python3 src/db.py

reset-db:
	rm data.db && python3 src/db.py

checks:
	sh scripts/checks.sh

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

uninstall:
	pip freeze | xargs pip uninstall -y
