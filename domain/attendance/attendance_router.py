from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from starlette import status
from datetime import date, datetime

from database import get_db
from domain.attendance import attendance_crud, attendance_schema
from domain.user.user_router import get_current_user

from models import User

import lib.const as const

router = APIRouter(
    prefix="/api/attendance",
)

@router.get("/all_list", response_model=list[attendance_schema.Attendance])
def question_list(db: Session = Depends(get_db), 
                  current_user: User = Depends(get_current_user)):
    _attendance_list = attendance_crud.get_all_attendance_list(db)
    return _attendance_list


@router.get("/user_attendance/{username}", response_model=list[attendance_schema.Attendance])
def get_user_attendance(db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    user_attendance_list = attendance_crud.get_user_attendance_list(db, current_user.user_id)
    return user_attendance_list


@router.get("/attendance", status_code=status.HTTP_200_OK)
def check_attendance(db: Session = Depends(get_db), 
                     current_user: User = Depends(get_current_user)):
    
    check_present_time = attendance_crud.caculate_attendance_time(const.PRESENT_START, const.PRESENT_END)
    check_late_time = attendance_crud.caculate_attendance_time(const.PRESENT_END, const.LATE_END)
    if not check_present_time and not check_late_time:
        raise HTTPException(status_code=400, detail="현재 시간에는 출석을 할 수 없습니다.")
    
    user_exists = attendance_crud.get_existing_user(db, current_user.user_id)
    if not user_exists:
        raise HTTPException(status_code=400, detail="사용자가 존재하지 않습니다.")
    
    count = attendance_crud.get_attendance_count(db, current_user.user_id, date.today())
    if count != 0:
        raise HTTPException(status_code=400, detail="출석은 하루에 한번만 할 수 있습니다.")
    
    if check_present_time:
        attendance_crud.attendance_check(db=db, check_attendance=current_user, state="present")
        return {"message" : "출석"}
    elif check_late_time:
        attendance_crud.attendance_check(db=db, check_attendance=current_user, state="late")
        return {"message" : "지각"}
    

@router.get("/attendance_stats/{username}")
def get_attendance_stats(db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    stats = attendance_crud.calculate_attendance_stats(db, current_user.username)
    return stats