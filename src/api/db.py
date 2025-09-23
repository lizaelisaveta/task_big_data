from sqlalchemy import create_engine, Column, Integer, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import json


Base = declarative_base()


class InferenceResult(Base):
    __tablename__ = "inference_results"
    id = Column(Integer, primary_key=True)
    input_data = Column(Text)
    prediction = Column(Float)


def get_engine():
    user = os.getenv("DB_USER")
    pwd = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST", "postgres")
    port = os.getenv("DB_PORT", "5432")
    db = os.getenv("DB_NAME", "modeldb")
    url = f"postgresql://{user}:{pwd}@{host}:{port}/{db}"
    return create_engine(url, pool_pre_ping=True)


def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    return Session()
