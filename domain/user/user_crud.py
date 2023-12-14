from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_create: UserCreate):
    db_user = User(user_id=user_create.user_id,
                   user_name=user_create.user_name,
                   password=pwd_context.hash(user_create.password1),
                   email=user_create.email,
                   phone_number=user_create.phone_number,
                   use=True,
                   state=True,
                   attendance_type=True)
    db.add(db_user)
    db.commit()


def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.user_id == user_create.user_id) |
        (User.user_name == user_create.user_name) |
        (User.email == user_create.email) |
        (User.phone_number == user_create.phone_number)
    ).first()
    
    
def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.user_id == user_id).first()


def get_user_state(db: Session):
    user_list = db.query(User).order_by(User.user_id).all()
    return user_list