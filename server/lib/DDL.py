from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from server.config import DATABASE_URL
from dotenv import load_dotenv
from os import environ, path
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

DATABASE_URL = environ['DATABASE_URL']

Base = declarative_base()

engine = create_engine(DATABASE_URL, connect_args={'sslmode':'require'})
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base.query = db_session.query_property()

def init_db():
    with engine.begin() as conn:
        conn.execute(text('DROP TABLE IF EXISTS users CASCADE;'))
        conn.execute(text('DROP TABLE IF EXISTS rooms CASCADE;'))
        conn.execute(text('DROP TABLE IF EXISTS rooms_users CASCADE;'))

    import server.lib.models
    Base.metadata.create_all(bind=engine)