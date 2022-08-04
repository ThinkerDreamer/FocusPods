from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .DDL import Base

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
    users = relationship("User", secondary="rooms_users")

    def __repr__(self) -> str:
        return f"Room(id={self.id!r}, owner={self.owner!r}, name={self.name!r})"

room_user = Table(
    'rooms_users',
    Base.metadata,
    Column("room_id", ForeignKey('rooms.id'), primary_key=True),
    Column("user_id", ForeignKey('users.id'), primary_key=True),
)

# How we understand
# 1 [Fish, Dolphin]
# 2 [Cat, Dog]

# USERS
# 1 Fish
# 2 Dolphin
# 3 Cat
# 4 Dog

# ROOMS
# 1
# 2

# ROOM to USER 
# 1,  1
# 1,  2
# 2,  3
# 2,  4

