# Telegram Language Bot

This is telegram bot for collecting terms for any languages you want. You can save terms in sets, create sets and folders and train it after.

Structure of menues in bot is showed bellow: 

![menues-diagram](bot-routing-map.drawio.svg)

## Deploy

### Python environment & requirements

``` shell
python -m venv venv && source /venv/bin/activate
pip install -r requirements.txt
```

### Alembic

Upgrade databse

``` shell
python -m alembic -c ./database/alembic.ini upgrade head
```

### Config file

You should create `config.py` file based on `config.default.py` and set next variables in it:

+ API_TOKEN - api token of telegram bot
+ DATABASE_URL - url of database (for sqlite: sqlite:///\<filename\>)

### Run

``` shell
source /venv/bin/activate
python main.py
```

## Development notices

### Alembic

Make migration

``` shell
python -m alembic -c ./database/alembic.ini revision --autogenerate -m 'some message'
```
