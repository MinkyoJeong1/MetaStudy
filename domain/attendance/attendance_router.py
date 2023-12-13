from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.attendance import attendance_crud, attendance_schema

router = APIRouter(
    prefix="/api/attendance",
)

@router.get("/list", response_model=list[attendance_schema.Attendance])
def question_list(db: Session = Depends(get_db)):
    _attendance_list = attendance_crud.get_attendance_list(db)
    return _attendance_list


@router.post("/attendance", status_code=status.HTTP_204_NO_CONTENT)
def check_attendance(_check_attendance: attendance_schema.Attendance, db: Session = Depends(get_db)):
    user_exists = attendance_crud.get_existing_user(db, _check_attendance.username)
    if not user_exists:
        raise HTTPException(status_code=400, detail="사용자가 존재하지 않습니다.")
    attendance_crud.attendance_check(db=db, check_attendance=_check_attendance)