from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    tg_id = Column(String, unique=True, nullable=False)
    chat_id = Column(Integer, unique=True, nullable=False)

    codes = relationship('Code', back_populates='user', cascade="all, delete-orphan")