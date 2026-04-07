import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Database connection
DATABASE_URL = os.getenv("POSTGRES_URL")
engine = create_engine(DATABASE_URL)

# Session Factory
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
)


# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)
