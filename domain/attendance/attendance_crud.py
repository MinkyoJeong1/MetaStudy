from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import func

from datetime import date, datetime, timedelta
import calendar

from domain.user.user_schema import UserCreate
from models import Attendance, User

import lib.const as const


def get_all_attendance_list(db: Session):
    attendance_list = db.query(Attendance).order_by(Attendance.id).all()
    return attendance_list


def get_user_attendance_list(db: Session, username: str):
    return db.query(Attendance).filter(Attendance.username == username).order_by(Attendance.id).all()


def attendance_check(db: Session, check_attendance: UserCreate, state: str):
    db_attendance = Attendance(username=check_attendance.username,
                         time=datetime.now(),
                         state=state)
    db.add(db_attendance)
    db.commit()


def get_existing_user(db: Session, user_name):
    return db.query(User).filter(User.username == user_name).first()


def get_attendance_count(db: Session, user_name: str, target_date: date):
    day_start = datetime.combine(target_date, datetime.min.time())
    day_end = datetime.combine(target_date, datetime.max.time())

    attendance_count = db.query(Attendance).filter(
        Attendance.username == user_name,
        Attendance.time >= day_start,
        Attendance.time <= day_end
    ).count()
    
    return attendance_count


def caculate_attendance_time(start, end):
    now = datetime.now()
    start_time = datetime.strptime(start, "%H:%M").time()
    end_time = datetime.strptime(end, "%H:%M").time()
    start_datetime = datetime.combine(now.date(), start_time)
    end_datetime = datetime.combine(now.date(), end_time)

    return start_datetime <= now <= end_datetime


def calculate_attendance_stats(db: Session, username: str):
    current_year = datetime.now().year
    current_month = datetime.now().month

    last_day = calendar.monthrange(current_year, current_month)[1]

    if const.START_DAY == 0:
        start_date = date(current_year, current_month, 1)
    else:
        start_date = date(current_year, current_month, const.START_DAY)

    if const.END_DAY == 0:
        end_date = datetime.now().date()
    elif const.END_DAY > last_day:
        end_date = date(current_year, current_month, last_day)
    else:
        end_date = date(current_year, current_month, const.END_DAY)

    end_date = end_date + timedelta(days=1)

    attendance_count = db.query(func.count()).filter(
        Attendance.username == username,
        Attendance.time.between(start_date, end_date),
        Attendance.state == 'present'
    ).scalar()

    late_count = db.query(func.count()).filter(
        Attendance.username == username,
        Attendance.time.between(start_date, end_date),
        Attendance.state == 'late'
    ).scalar()

    total_days = (end_date - start_date).days
    absent_count = total_days - (attendance_count + late_count)

    total_fine = late_count*const.LATE_FINE + absent_count*const.ABSENT_FINE

    return {
        "attendance_count": attendance_count,
        "late_count": late_count,
        "absent_count": absent_count,
        "total_fine": total_fine
    }