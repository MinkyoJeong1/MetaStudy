from pydantic import BaseModel
from datetime import datetime


class Attendance(BaseModel):
    username: str
    time : datetime