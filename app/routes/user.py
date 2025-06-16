from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.database import Sessionlocal
from sqlalchemy.orm import Session

from app.repositories.user import UserRepository

router = APIRouter(
    tags=['Profile']
)

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(tg_id: str, chat_id: int, db: db_dependency):
    UserRepository(db).create_user(tg_id, chat_id)
    