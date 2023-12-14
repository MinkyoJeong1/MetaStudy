from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.attendance import attendance_crud, attendance_schema
from domain.user.user_router import get_current_user

from models import User

router = APIRouter(
    prefix="/api/attendance",
)

@router.get("/list", response_model=list[attendance_schema.Attendance])
def question_list(db: Session = Depends(get_db), 
                  current_user: User = Depends(get_current_user)):
    _attendance_list = attendance_crud.get_attendance_list(db)
    return _attendance_list


@router.get("/attendance", status_code=status.HTTP_204_NO_CONTENT)
def check_attendance(
                     db: Session = Depends(get_db), 
                     current_user: User = Depends(get_current_user)
                     ):
    user_exists = attendance_crud.get_existing_user(db, current_user.username)
    if not user_exists:
        raise HTTPException(status_code=400, detail="사용자가 존재하지 않습니다.")
    attendance_crud.attendance_check(db=db, check_attendance=current_user)