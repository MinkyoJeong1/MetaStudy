from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_create: UserCreate):
    db_user = User(username=user_create.username,
                   password=pwd_context.hash(user_create.password1),
                   email=user_create.email,
                   phone_number=user_create.phone_number,
                   state=True)
    db.add(db_user)
    db.commit()


def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.username == user_create.username) |
        (User.email == user_create.email) |
        (User.phone_number == user_create.phone_number)
    ).first()
    
    
def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_state(db: Session):
    user_list = db.query(User).order_by(User.id).all()
    return user_list