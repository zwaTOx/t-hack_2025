from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class TaskSchema(BaseModel):
    name: str
    category_name: Optional[str] 
    start_time: Optional[str]
    deadline: Optional[str] 
    description: Optional[str] 