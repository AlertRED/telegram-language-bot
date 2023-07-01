# Telegram Language Bot

## About

This app is telegram bot for collecting terms of eny languags. You can save terms in sets and folders and train it after.

## Deploy

### Alembic

``` shell
python -m alembic head
```

### Config file

You should to create `config.py` file based on `config.default.py` and set variables in it.
Variables:

+ API_TOKEN - api token of telegram bot

## Develop

### Alembic

Making migration

``` shell
python -m alembic -c ./database/alembic.ini revision --autogenerate -m 'initial'
```
