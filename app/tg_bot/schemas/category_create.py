from pydantic import BaseModel, Field, validator
from typing import Optional

class CategoryCreate(BaseModel):
    category_name: str