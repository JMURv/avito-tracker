[![Maintainability](https://api.codeclimate.com/v1/badges/bef7550670ac9773e886/maintainability)](https://codeclimate.com/github/JMURv/avito-tracker/maintainability)
___
## How to install:
 1. Clone the repo ```git clone https://github.com/JMURv/avito-tracker.git```
 2. Examine `.env.example` file inside `./docker/env/` directory and fill it with your data.
    - If you are using linux system to start the container, please, fill "DSN" env with text, not with variables
 3. Use `docker-compose up --build` command to start the bot.
    - Probably, it requires 2 starts: one for image build and db to create all tables and the second for actual start

## About:
This is an asyncio telegram bot built with aiogram library.
He is tracking links you've sent to him and keep you notified when new product is showing.
You can find working example by click this [link](https://t.me/AvitoTrackBot)
## Payment:
Every user has a chance to test it for free with only one active worker, but subscription can break the limit. 
I've used Crystal PAY system to integrate payments to make it all possible. Sub is very cheap and flexible.

## TODO:
- Sent images of the advertisement in the response

## Image Examples
### Message from bot example.

![example-of-message.png](https://wampi.ru/image/YxzMAUghttps://wampi.ru/image/YxzMqSt)

 There is update about "RTX 3080" task.
___
### Interface example

![example-of-interface.png](https://wampi.ru/image/YxzMAUg)
