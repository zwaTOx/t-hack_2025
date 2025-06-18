from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class TaskSchema(BaseModel):
    name: str
    category_name: str | None = Field(default='')
    start_time: Optional[str]
    deadline: int | None 
    description: Optional[str] 