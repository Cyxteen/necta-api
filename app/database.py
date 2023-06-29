from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://cyxteen:fLe6e8Ak1KYKlFQR48cEzA1ZjGzage3X@dpg-cien0vtph6etu3rlkt90-a.oregon-postgres.render.com/necta")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()