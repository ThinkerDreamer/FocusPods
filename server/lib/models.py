from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from flask_sqlalchemy import SQLAlchemy

from .DDL import Base

db = SQLAlchemy()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(253), nullable=False)
    password = Column(String(100), nullable=False)
    rooms_in = relationship("Room", secondary="rooms_users", back_populates="users")

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, email={self.email})"


class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True)
    owner = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(40), nullable=False)
    users = relationship("User", secondary="rooms_users", back_populates="rooms_in")

    def __repr__(self) -> str:
        return f"Room(id={self.id}, owner={self.owner}, name={self.name})"


room_user = Table(
    "rooms_users",
    Base.metadata,
    Column("room_id", ForeignKey("rooms.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)

class Invite(Base):
    __tablename__ = "invites"
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    link_id = Column(String(100), nullable=False)

    def __repr__(self) -> str:
        return f"""Invite(id={self.id},
        room_id={self.room_id},
        user_id={self.user_id},
        link_id={self.link_id}
        )"""