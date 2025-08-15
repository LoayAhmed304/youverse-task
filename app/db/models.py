from app.db.db import Base

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, Table
from sqlalchemy.orm import relationship

user_courses = Table("user_courses", Base.metadata,
                     Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
                     Column("course_id", Integer, ForeignKey("course.id"), primary_key=True))


class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)
    owner_id = Column(Integer, ForeignKey("user.id"))

    videos = relationship("Video", back_populates="course", cascade="all, delete-orphan")
    users = relationship("User", secondary=user_courses, back_populates="courses")


class Video(Base):
    __tablename__ = "video"

    asset_id = Column(String, primary_key=True)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    duration = Column(Float)  # in seconds
    category = Column(String)
    subcategory = Column(String)

    course = relationship("Course", back_populates="videos")


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    courses = relationship("Course", secondary=user_courses, back_populates="users")
