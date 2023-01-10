start:
	python scripts\run.py

install:
	poetry build
	python scripts\install_db.py

uninstall:
	python scripts\uninstall_db.py

reinstall:
	python scripts\reinstall_db.py

lint:
	flake8 avito_tracker

# GIT COMMANDS
pull:
	git pull origin main

