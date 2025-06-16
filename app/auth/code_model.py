from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class Code(Base):
    __tablename__ = 'codes'  
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(6), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    is_used = Column(Boolean, default=False)  
    
    user = relationship('User', back_populates='codes')
