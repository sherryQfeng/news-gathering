from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///animal_crossing_news.db")
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True)
    source = Column(String(120), index=True)
    title = Column(Text, nullable=False)
    link = Column(Text, nullable=False)
    summary = Column(Text)
    published = Column(DateTime, default=datetime.utcnow)
    category = Column(String(40), index=True)  # "ai_frontier" | "economics_politics"
    emoji = Column(String(10), default="📰")  # Fun emoji for each article
    villager_comment = Column(Text)  # Whimsical comment from an Animal Crossing villager
    
    __table_args__ = (UniqueConstraint('link', name='uq_article_link'),)
    
    def __repr__(self):
        return f"<Article(title='{self.title[:50]}...', source='{self.source}')>"

def init_db():
    """Initialize the database by creating all tables"""
    Base.metadata.create_all(engine)
    print("🏠 Database initialized! Tom Nook would be proud! 🦝")

def get_db():
    """Get a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
