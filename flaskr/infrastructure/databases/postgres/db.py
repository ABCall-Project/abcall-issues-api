from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from config import Config

config = Config()

engine = create_engine(
    config.DATABASE_URI,
    pool_size=10,
    max_overflow=5,
    pool_timeout=30,
    pool_recycle=1800
)

Session = scoped_session(sessionmaker(bind=engine))