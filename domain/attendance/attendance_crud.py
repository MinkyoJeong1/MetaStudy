from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import Attendance, User

from datetime import datetime


def get_attendance_list(db: Session):
    attendance_list = db.query(Attendance).order_by(Attendance.id).all()
    return attendance_list


def attendance_check(db: Session, check_attendance: UserCreate):
    db_attendance = Attendance(username=check_attendance.username,
                         time=datetime.now())
    db.add(db_attendance)
    db.commit()


def get_existing_user(db: Session, user_name):
    return db.query(User).filter(User.username == user_name).first()