from sqlalchemy import Column, ForeignKey, Integer, String
from lib.DDL import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(253), nullable=False)
    password = Column(String(100), nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    owner = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(40), nullable=False)

    def __repr__(self) -> str:
        return f"Room(id={self.id!r}, owner={self.owner!r}, name={self.name!r})"

class Room_User(Base):
    __tablename__ = 'rooms_users'
    room_id = Column(Integer, ForeignKey('rooms.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    def __repr__(self) -> str:
        return f"Room_User(room_id={self.room_id!r}, user_id={self.user_id!r})"