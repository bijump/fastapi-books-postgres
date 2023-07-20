from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = 'postgresql://db_admin:adminadmin@localhost:5432/books'

engine=create_engine(DATABASE_URI)
session=sessionmaker(autoflush=False,bind=engine)

Base=declarative_base()