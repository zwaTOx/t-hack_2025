from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from database import Base

class Code(Base):
    __tablename__ = 'codes'  
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(String, nullable=False, index=True)  
    code = Column(String(6), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    is_used = Column(Boolean, default=False)  