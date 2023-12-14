from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json, os


from models import User, Attendance, Base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_FILE = os.path.join(BASE_DIR, 'secrets.json')
secrets = json.loads(open(SECRET_FILE).read())
DB = secrets["DB"]

DB_URL = f"mysql+pymysql://{DB['user']}:{DB['password']}@{DB['host']}:{DB['port']}/{DB['database']}?charset-utf8"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(engine)

session = SessionLocal()

query = session.query(User, Attendance).join(Attendance, User.user_id == Attendance.user_id)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
