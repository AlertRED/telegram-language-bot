import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN: str = os.getenv('API_TOKEN', '')
MY_TELEGRAM_ID: int = int(os.getenv('MY_TELEGRAM_ID', 0))

REDIS_HOST: str = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT: int = os.getenv('REDIS_PORT', 6379)
REDIS_DB: int = os.getenv('REDIS_DB', 0)
REDIS_PASSWORD: str = os.getenv('REDIS_PASSWORD', '')

POSTGRES_DB: str = os.getenv('POSTGRES_DB', 'telegram_bot_db')
POSTGRES_HOST: str = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT: int = os.getenv('POSTGRES_PORT', 5432)
POSTGRES_USER: str = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', '')

DATABASE_URL: str = (
    f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
    f'@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
)

LOGGING_CONFIG_PATH: str = os.getenv('LOGGING_CONFIG_PATH', 'logging.yaml')
IS_DEVELOP: bool = os.getenv('IS_DEVELOP', False)
