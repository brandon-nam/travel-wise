from sqlalchemy import Column, Integer, String, Float, Enum, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()


class ClassificationType(enum.Enum):
    travel_tip = "travel_tip"
    travel_suggestion = "travel_suggestion"
    other = "other"


class Post(Base):
    __tablename__ = "posts"
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    score = Column(Integer, nullable=False)


class Comment(Base):
    __tablename__ = "comments"
    id = Column(String, primary_key=True)
    post_id = Column(String, ForeignKey("posts.id"), nullable=False)
    body = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    classification = Column(Enum(ClassificationType), nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    locations = relationship(
        "Location", backref="comment", cascade="all, delete-orphan"
    )


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    comment_id = Column(String, ForeignKey("comments.id", ondelete="CASCADE"))
    lat = Column(Float)
    lng = Column(Float)
