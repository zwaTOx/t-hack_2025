from pydantic import BaseModel, Field, field_validator

class Token(BaseModel):
    access_token: str
    token_type: str