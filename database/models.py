from sqlalchemy import Column, Integer, String, Text, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class UserContestRanking(Base):
    __tablename__ = 'user_contest_ranking'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    attended_contests_count = Column(Integer)
    rating = Column(Integer)
    global_ranking = Column(Integer)

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    title_slug = Column(String, unique=True, nullable=False)
    difficulty = Column(String, nullable=False)
    frontend_id = Column(String)
    ac_rate = Column(String)
    solutions = relationship("Solution", back_populates="question", cascade="all, delete-orphan")

class Solution(Base):
    __tablename__ = 'solutions'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    summary = Column(Text, nullable=False)
    author_name = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
    question = relationship("Question", back_populates="solutions")