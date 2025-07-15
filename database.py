from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import crud
import schemas
import database

DATABASE_URL = "postgresql://warehouse:drax@localhost:5432/telegram_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
