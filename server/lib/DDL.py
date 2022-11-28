from os import environ
import re
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

# from server.config import DATABASE_URL
# from server.config import SQLALCHEMY_DATABASE_URI


DATABASE_URL = environ["DATABASE_URL"]
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})
# engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"sslmode": "require"})

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS rooms CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS rooms_users CASCADE;"))

    import server.lib.models

    Base.metadata.create_all(bind=engine)
