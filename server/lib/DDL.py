import os
from flask import session
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, table
from sqlalchemy.orm import registry, declarative_base, Session, sessionmaker

mapper_registry = registry()
engine = create_engine(f'postgresql+psycopg2://{os.environ["DB_USERNAME"]}:{os.environ["DB_PASSWORD"]}@localhost/focus_pods_db', echo=True, future=True)
session = sessionmaker(engine)

metadata_obj = mapper_registry.metadata
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(253), nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    owner = Column(Integer, ForeignKey("user.id"), nullable=False)
    name = Column(String(40), nullable=False)

    def __repr__(self) -> str:
        return f"Room(id={self.id!r}, owner={self.owner!r}, name={self.name!r})"

class Room_User(Base):
    __tablename__ = 'rooms_users'
    room_id = Column(Integer, ForeignKey('rooms.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    def __repr__(self) -> str:
        return f"Room_User(room_id={self.room_id!r}, user_id={self.user_id!r})"

metadata_obj.reflect(bind=engine)
metadata_obj.create_all(engine)


users_table = metadata_obj.tables['users']
rooms_table = metadata_obj.tables['rooms']
rooms_users_table = metadata_obj.tables['rooms_users']
engine.execute(users_table.delete())
engine.execute(rooms_table.delete())
engine.execute(rooms_users_table.delete())

squidward = User(name='Squidward', email='myemail@thesea.com',)
session = Session(engine)
session.add(squidward)
session.commit()


"""
cur.execute("insert into rooms (name, created_at)"
            "values (%s, %s)",
            ("First room",
             "2020-01-01 00:00:00")
            )

cur.execute("insert into users (name, email, created_at, password)"
            "values (%s, %s, %s, %s)",
            ("Angel",
            "angel@angel.com",
             "1971-09-18",
            "123456")
            )

cur.execute("insert into users (name, email, created_at, password)"
            "values (%s, %s, %s, %s)",
            ("Shae",
             "shae@scannedinavian.com",
             "1971-09-18",
             "0987")
            )

cur.execute("insert into rooms_users (room_id, user_id)"
            "values (%s, %s)",
            (1, 1)
            )

cur.execute("insert into rooms_users (room_id, user_id)"
            "values (%s, %s)",
            (1, 2)
            )
            
"""