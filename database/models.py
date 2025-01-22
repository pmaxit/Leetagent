from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import enum

Base = declarative_base()

class UserContestRanking(Base):
    __tablename__ = 'user_contest_ranking'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    attended_contests_count = Column(Integer)
    rating = Column(Integer)
    global_ranking = Column(Integer)

class DifficultyRating(enum.Enum):
    HARD = 1
    MEDIUM = 2
    EASY = 3

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    title_slug = Column(String, unique=True, nullable=False)
    difficulty = Column(String, nullable=False)
    frontend_id = Column(String)
    ac_rate = Column(String)
    solutions = relationship("Solution", back_populates="question", cascade="all, delete-orphan")
    attempts = relationship("Attempt", back_populates="question", cascade="all, delete-orphan")

class Solution(Base):
    __tablename__ = 'solutions'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    summary = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    author_name = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
    question = relationship("Question", back_populates="solutions")

class Attempt(Base):
    __tablename__ = 'attempts'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    
    # SM-2 algorithm specific fields
    easiness_factor = Column(Float, default=2.5)  # Initial easiness factor
    interval = Column(Integer, default=0)  # Days between reviews
    repetition_number = Column(Integer, default=0)  # Number of successful reviews
    
    # Attempt specific fields
    difficulty_rating = Column(Enum(DifficultyRating), nullable=False)
    attempted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    next_review_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    question = relationship("Question", back_populates="attempts")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.easiness_factor = 2.5
        self.interval = 0
        self.repetition_number = 0
        self.attempted_at = datetime.utcnow()
        self.next_review_at = datetime.utcnow()

    def calculate_next_review(self, difficulty: DifficultyRating):
        """
        Implements SM-2 algorithm to calculate the next review date
        
        Args:
            difficulty: DifficultyRating enum (HARD=1, MEDIUM=2, EASY=3)
        """
        quality = difficulty.value  # Convert enum to numeric value
        
        # Calculate new easiness factor
        self.easiness_factor = max(1.3, self.easiness_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
        
        # Update repetition number and interval
        if quality < 2:  # If rating is HARD
            self.repetition_number = 0
            self.interval = 1
        else:
            self.repetition_number += 1
            if self.repetition_number == 1:
                self.interval = 1
            elif self.repetition_number == 2:
                self.interval = 6
            else:
                self.interval = round(self.interval * self.easiness_factor)
        
        # Calculate and set next review date
        self.next_review_at = datetime.utcnow() + timedelta(days=self.interval)