from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
import re


class UserCreate(BaseModel):
    username: str
    password1: str
    password2: str
    email: EmailStr
    phone_number: str

    @field_validator('username', 'password1', 'password2', 'email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @field_validator('password2')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password1' in info.data and v != info.data['password1']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v
    
    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        pattern = re.compile(r'^01[016789][1-9]\d{6,7}$')
        if not pattern.match(v):
            raise ValueError('유효하지 않은 핸드폰 번호 형식입니다.')
        return v
    

class UserState(BaseModel):
    id: int
    username: str
    state: bool


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str