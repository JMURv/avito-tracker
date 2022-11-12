restart:
	heroku restart -a avitotracker

logs:
	heroku logs --tail

localstart:
	python avito_tracker/telegram_bot.py

lint:
	flake8 avito_tracker

# GIT COMMANDS
update:
	git pull origin main

