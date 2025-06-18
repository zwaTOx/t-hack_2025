from pydantic import BaseModel, Field, validator
from typing import Optional

class TaskCreate(BaseModel):
    task_name: str