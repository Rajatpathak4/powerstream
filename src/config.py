from functools import lru_cache
import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    PG_DB_SERVER: str = os.getenv('POSTGRES_SERVER')
    PG_DATABASE: str = os.getenv('POSTGRES_DB')
    PG_DB_USER: str = os.getenv('POSTGRES_USER')
    PG_DB_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
    PG_DB_PORT: str = os.getenv('POSTGRES_PORT')
    WEATHER_API_KEY: str = os.getenv('WEATHER_API_KEY')
    WEATHER_API_URL: str = os.getenv('WEATHER_API_URL')

@lru_cache()
def get_setting():
    return Settings()