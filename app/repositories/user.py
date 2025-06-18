from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.user import User

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_tg(self, tg_id: str):
        existing_user = self.db.query(User).filter(User.tg_id == tg_id).first()
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не существует, нужно пообщаться с ботом"
            )
        return existing_user
    
    def get_user(self, user_id):
        existing_user = self.db.query(User).filter(User.id == user_id).first()
        if existing_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не существует, нужно пообщаться с ботом"
            )
        return existing_user
    
    def create_user(self, tg_id: str, chat_id: int):
        existing_user = self.db.query(User).filter(User.tg_id == tg_id).first()
        if existing_user:
            return existing_user
            
        new_user = User(tg_id=tg_id, chat_id=chat_id)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    # def delete_user_codes(self, user_id):
    #     self.db.query(ви).filter(
    #         db_ResetCode.user_id == user_id
    #     ).delete()
    #     self.db.commit()