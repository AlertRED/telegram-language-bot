# Telegram Language Bot

This app is telegram bot for collecting terms of eny languags. You can save terms in sets and folders and train it after.

Structure of menues in bot is showed bellow: 

![menues-diagram](bot-routing-map.drawio.svg)

## Deploy

### Python environment & requirements

``` shell
python -m venv venv && source /venv/bin/activate
pip install -r requirements.txt
```

### Alembic

To upgrade databse

``` shell
python -m alembic -c ./database/alembic.ini upgrade head
```

### Config file

You should to create `config.py` file based on `config.default.py` and set variables in it.

Variables:

+ API_TOKEN - api token of telegram bot
+ DATABASE_URL - url of database

## Develop

### Alembic

Making migration

``` shell
python -m alembic -c ./database/alembic.ini revision --autogenerate -m 'some message'
```
