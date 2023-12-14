from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    user_id = Column(String(255), primary_key=True)
    user_name = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(255), unique=True, nullable=False)
    use = Column(Boolean, nullable=False)
    state = Column(Boolean, nullable=False)
    attendance_type = Column(Boolean, nullable=False)


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), ForeignKey('user.user_id'), nullable=False)
    time = Column(DateTime, nullable=False)
    state = Column(String(255), nullable=False)

    # user_id를 기반으로 User 테이블과의 관계를 설정
    user = relationship("User", foreign_keys=[user_id]) 