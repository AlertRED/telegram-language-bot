import os


API_TOKEN = os.getenv('API_TOKEN', '')
MY_TELEGRAM_ID = os.getenv('MY_TELEGRAM_ID', 0)

REDIS_HOST: str = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT: int = os.getenv('REDIS_PORT', 6379)
REDIS_DB: int = os.getenv('REDIS_DB', 0)
REDIS_PASSWORD: str = os.getenv('REDIS_PASSWORD', '')

POSTGRES_DB = os.getenv('POSTGRES_DB', 'telegram_bot_db')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', 5432)
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '')

DATABASE_URL = (
    f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
    f'@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
)
