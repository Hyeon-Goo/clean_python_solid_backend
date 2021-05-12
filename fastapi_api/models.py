import datetime
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    TIMESTAMP,
    )
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users_fast"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    profile = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now())
    updated_at = Column(TIMESTAMP, onupdate=True)


class UserFollowList(Base):
    __tablename__ = "users_follow_list_fast"
    user_id = relationship("User", back_populates="id", primary_key=True)
    follow_user = relationship("User", back_populates="id", primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now())


class Tweets(Base):
    __tablename__ = "tweets_fast"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = relationship("User", back_populates="id")
