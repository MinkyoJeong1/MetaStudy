from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
import json, os
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))  # 255 길이의 VARCHAR로 변경

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(255))  # 255 길이의 VARCHAR로 변경
    user = relationship("User")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_FILE = os.path.join(BASE_DIR, 'secrets.json')
secrets = json.loads(open(SECRET_FILE).read())
DB = secrets["DB"]

DB_URL = f"mysql+pymysql://{DB['user']}:{DB['password']}@{DB['host']}:{DB['port']}/{DB['database']}?charset-utf8"

engine = create_engine(DB_URL)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# User와 Post를 join하는 쿼리
query = session.query(User, Post).join(Post, User.id == Post.user_id)
for user, post in query.all():
    print(user.name, post.title)
