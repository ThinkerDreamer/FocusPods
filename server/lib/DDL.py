import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

engine = create_engine(f'postgresql+psycopg2://{os.environ["DB_USERNAME"]}:{os.environ["DB_PASSWORD"]}@localhost/focus_pods_db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    with engine.begin() as conn:
        conn.execute(text('DROP TABLE IF EXISTS users CASCADE;'))
        conn.execute(text('DROP TABLE IF EXISTS rooms CASCADE;'))
        conn.execute(text('DROP TABLE IF EXISTS rooms_users CASCADE;'))
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import lib.models
    Base.metadata.create_all(bind=engine)