from sqlalchemy import (MetaData, Table, Column, Integer, String)
from sqlalchemy import create_engine
from databases import Database
from dotenv import dotenv_values

values = dotenv_values(".env")
DATABASE_URL = values["DATABASE_URL"]

metadata = MetaData()

tasks = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("description", String, nullable=True),
    Column("status", String, nullable=True),
    Column("date", String, nullable=True),
    Column("time", String, nullable=True),
)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

database = Database(DATABASE_URL)
