import os
import time

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import psycopg2
from psycopg2.extras import RealDictCursor

from dotenv import load_dotenv

load_dotenv()

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
HOST=os.getenv('HOST')
DATABASE_NAME=os.getenv('DATABASE_NAME')
USER=os.getenv('USER')
PASSWORD=os.getenv('PASSWORD')

# Connection sequence for sqlalchemy database url
# postgresql://<username>:<password>@<ip-address/host>/<database-name>
SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

""" 
SQLAlchemy, Connecting to PostGres DB. To be used if one needs to query db with raw SQL
"""
def ConnectDb():
    while True:
        try:
            conn = psycopg2.connect(host=HOST, database=DATABASE_NAME, user=USER, password=PASSWORD, cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            print("Database connection was successful")
            break
        except Exception as error:
            print("Connection to database failed")
            print(f"error : {error}")
            time.sleep(2)