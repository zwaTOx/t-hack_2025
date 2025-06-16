from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Sessionlocal, Base

from app.auth.route import get_current_user
from app.auth.route import router as auth_router
from app.routes.user import router as user_router

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Auth Failed")
    return user

if __name__ == '__main__':
    config = uvicorn.Config(app, port=8000, reload=True)
    server = uvicorn.Server(config)
    server.run()