# Telegram Language Bot

This is telegram bot for collecting terms for any languages you want. You can save terms in sets, create sets and folders and train it after.

Structure of menues in bot is showed bellow:

![menues-diagram](assets/bot-routing-map.drawio.svg)

## Deploy

### Dependencies

+ Python3 (used v3.11.2)
+ Redis (used v7.0.12)
+ Postgres (used v15.3) or SQLite

### .env file

You should create `.env` file based on `.env.example` and set next variables in it:

+ API_TOKEN - api token of telegram bot
+ MY_TELEGRAM_ID - telegram id of owner
+ REDIS_HOST - redis host
+ REDIS_PORT - redis port
+ REDIS_DB - redis db name
+ REDIS_PASSWORD - redis password
+ POSTGRES_DB - postgres db name
+ POSTGRES_HOST - postgres host
+ POSTGRES_PORT - postgres port
+ POSTGRES_USER - postgres username
+ POSTGRES_PASSWORD - postgres password
+ LOGGING_CONFIG_PATH - path to config of logging (by default ./logging.yaml)
+ IS_DEVELOP - run in development mode (true/false)

### Python environment & requirements

``` shell
python3 -m venv venv && source /venv/bin/activate
pip install -r requirements.txt
```

### Alembic

Upgrade databse

``` shell
python -m alembic -c ./database/alembic.ini upgrade head
```

### Run

#### Web

``` shell
gunicorn admin:app -b localhost:5000
```

#### Redis Queue

``` shell
rq worker --with-scheduler
```

#### Bot

``` shell
python run.py
```

## Development notices

### Alembic

Make migration

``` shell
python -m alembic -c ./database/alembic.ini revision --autogenerate -m 'some message'
```

### Makefile

Targets for make:

+ bot - run bot
+ web - run web admin panel
+ all - run bot and web admin panel

### Build docker image

``` shell
docker buildx build . -t telegram-language-bot -f ./docker/Dockerfile
```

### Docker-compose

``` shell
docker-compose up
```

### i18n

#### Initial

1. Initial messages.pot

    ``` shell
    pybabel extract --input-dirs=./bot -o bot/locales/messages.pot
    ```

2. Create locales

    ``` shell
    pybabel init -i bot/locales/messages.pot -d bot/locales -D messages -l ru
    pybabel init -i bot/locales/messages.pot -d bot/locales -D messages -l en
    ```

3. Write translation in files which was created

4. Compile

    ``` shell
    pybabel compile -d bot/locales -D messages
    ```

#### Update

1. Initial messages.pot

    ``` shell
    pybabel extract --input-dirs=./bot -o bot/locales/messages.pot
    ```

2. Update locales

    ``` shell
    pybabel update -d bot/locales -D messages -i bot/locales/messages.pot
    ```

3. Write translation in files which was updated

4. Compile

    ``` shell
    pybabel compile -d bot/locales -D messages
    ```
