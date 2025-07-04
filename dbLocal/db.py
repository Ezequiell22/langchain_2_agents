from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbLocal.models import Base

engine = create_engine("sqlite:///dbLocal/dicionario.db", echo=False)

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
