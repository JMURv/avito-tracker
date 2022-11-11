restart:
	heroku restart -a avitotracker

logs:
	heroku logs --tail

start:
	python avito_tracker/telegram_bot.py


