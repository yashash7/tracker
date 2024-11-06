from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .schemas import Base
from .utils import get_env_var

DATABASE_URL = get_env_var("db_string")
POOL_SIZE = int(get_env_var("db_connection_pool_size", 1))
MAX_OVERFLOW = int(get_env_var("db_connection_max_overflow", 0))

engine = create_engine(DATABASE_URL, pool_size=POOL_SIZE, max_overflow=MAX_OVERFLOW)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
