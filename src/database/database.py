from urllib.parse import quote_plus
from config import Settings as settings


PG_DB_URL = f"postgresql://{settings.PG_DB_USER}:{quote_plus(settings.PG_DB_PASSWORD)}@{settings.PG_DB_SERVER}:{settings.PG_DB_PORT}/{settings.PG_DATABASE}"

print(PG_DB_URL,'PG_DB_URL')