from urllib.parse import quote_plus
from config import Settings as settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData



PG_DB_URL = f"postgresql://{settings.PG_DB_USER}:{quote_plus(settings.PG_DB_PASSWORD)}@{settings.PG_DB_SERVER}:{settings.PG_DB_PORT}/{settings.PG_DATABASE}"

print(PG_DB_URL,'PG_DB_URL')

engine = create_engine(PG_DB_URL,connect_args={"options": "-c timezone=Asia/Kolkata -c search_path=public"},echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base(metadata=MetaData(schema='public'))


def get_transaction_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()