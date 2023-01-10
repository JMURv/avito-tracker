start:
	python avito_tracker\telegram_bot.py

install:
	poetry build
	python avito_tracker\create_db.py

lint:
	flake8 avito_tracker

# GIT COMMANDS
pull:
	git pull origin main

