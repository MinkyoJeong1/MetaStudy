from pydantic import BaseModel
from datetime import datetime


class Attendance(BaseModel):
    user_id: str
    time : datetime
    state : str