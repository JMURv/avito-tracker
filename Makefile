start:
	python run.py

install:
	poetry build
	python avito_tracker\install_db.py

lint:
	flake8 avito_tracker

# GIT COMMANDS
pull:
	git pull origin main

