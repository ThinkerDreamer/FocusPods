from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from server.config import DATABASE_URL

engine = create_engine({DATABASE_URL}, echo=True)
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

    import server.lib.models
    Base.metadata.create_all(bind=engine)