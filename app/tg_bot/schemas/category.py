from pydantic import BaseModel, Field, validator
from typing import Optional

class CategorySchema(BaseModel):
    name: str
    color: str
    description: Optional[str] = None
