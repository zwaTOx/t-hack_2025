import logging
import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
import httpx
from jose import jwt
from app.auth.route import ALGORITHM, SECRET_KEY, get_current_user
from app.database import Sessionlocal
from sqlalchemy.orm import Session

from app.repositories.user import UserRepository
from app.tg_bot.telegram_bot_model import TelegramBot

load_dotenv()
n8n_url = os.getenv('N8N_URL')
logger = logging.getLogger(__name__)
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
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(tg_id: str, chat_id: int, db: db_dependency):
    UserRepository(db).create_user(tg_id, chat_id)


def decode_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    if not payload or "id" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format"
        )
    logger.info(f'{payload["id"]}')
    return payload["id"]

@router.post('/message')
async def send_message(msg: str, token: str, db: db_dependency):
    user_id = decode_token(token)
    founded_user = UserRepository(db).get_user(user_id)
    data = {
        "userId": founded_user.chat_id,
        "action": "sendMessage",
        "chatInput": msg
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            n8n_url,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=30.0
        )
        response_data = response.json() if response.content else None
    return response_data

@router.post('/notyfication')
async def send_notification(user_id: int, ):
    pass