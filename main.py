from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import get_db

from domain.user import user_router
from domain.attendance import attendance_router

app = FastAPI()

app.include_router(user_router.router)
app.include_router(attendance_router.router)
