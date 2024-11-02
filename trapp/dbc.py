from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://u1iztmftoulf57th:t9g4GtD5iEtSM8JGOVcb@bm4f9lg4nenej6tsgm8t-mysql.services.clever-cloud.com:3306/bm4f9lg4nenej6tsgm8t"

engine = create_engine(DATABASE_URL, pool_size=4, max_overflow=0)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)
