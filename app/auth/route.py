import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from datetime import datetime, timedelta, timezone
import random
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from app.auth.code_model import Code
from schemas import Token
from database import Sessionlocal

from app.tg_bot.telegram_bot import telegram_bot

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

router = APIRouter(
    tags=['Auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='login')

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
    
@router.post('/code/send', status_code=status.HTTP_201_CREATED)
async def create_password_restore_code(tg_id: str, db: Session = Depends(get_db)):
    existing_code = db.query(Code).filter(
        Code.tg_id == tg_id,
        Code.is_used == False,
        # Code.created_at >= datetime.now(timezone.utc) - timedelta(minutes=5)
    ).first()
    
    # if existing_code:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Код уже был отправлен. Попробуйте позже."
    #     )
    code = str(random.randint(100000, 999999))
    
    db_code = Code(
        tg_id=tg_id,
        code=code,
    )
    
    try:
        db.add(db_code)
        db.commit()
        db.refresh(db_code)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при сохранении кода: {str(e)}"
        )
    try:
        success = await telegram_bot.send_code(code, tg_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Не удалось отправить код в Telegram"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при отправке кода: {str(e)}"
        )
    
    return {
        "message": "Код отправлен",
        "status": "success"
    }

@router.post('/code/verify/{code}', status_code=status.HTTP_201_CREATED)
async def auth_with_code(code: str, db: db_dependency):
    db_code = db.query(Code).filter(
        Code.code == code,
        Code.is_used == False,
        Code.created_at >= datetime.now(timezone.utc) - timedelta(minutes=5)
    ).first()
    
    if not db_code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Неверный или просроченный код"
        )
    
    db_code.is_used = True
    db.commit()
    token_data = {
        "tg_id": db_code.tg_id,
        "id": db_code.id,
        "exp": datetime.now(timezone.utc) + timedelta(days=1)
    }
    
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        'access_token': token,
        'token_type': 'bearer'
    }
    
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        tg_id: str = payload.get('tg_id')
        user_id: int = payload.get('id')
        if tg_id is None or user_id is None:
            raise HTTPException(status_code=401, detail='Could not validate user.')
        return {'tg_id': tg_id, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail='Could not validate user.')