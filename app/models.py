import uuid
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, func, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)

class Post(Base):
    __tablename__ = "posts"

    post_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    post = Column(Text, nullable=False)
    needed = Column(Integer)
    joined = Column(Integer, default=0)

class Join(Base):
    __tablename__ = "post_joins"

    join_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.post_id"), nullable=False)