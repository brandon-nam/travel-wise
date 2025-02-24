import uuid

from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
    Enum,
    Float,
    Date,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class ClassificationType(enum.Enum):
    travel_tip = "travel_tip"
    travel_suggestion = "travel_suggestion"
    other = "other"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Text, primary_key=True)
    title = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    score = Column(Integer, nullable=False)
    num_comments = Column(Integer, nullable=False)


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Text, primary_key=True)
    post_id = Column(Text, ForeignKey("posts.id"), nullable=False)
    body = Column(Text, nullable=False)
    score = Column(Integer, nullable=False)
    classification = Column(Enum(ClassificationType), nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    locations = relationship(
        "Location", backref="comment", cascade="all, delete-orphan"
    )


class Location(Base):
    __tablename__ = "locations"

    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    comment_id = Column(Text, ForeignKey("comments.id", ondelete="CASCADE"))
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    location_name = Column(Text, nullable=False)
    characteristic = Column(Text, nullable=False)
