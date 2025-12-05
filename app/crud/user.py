from sqlalchemy.orm import Session
from schemas.user import UserCreate
from models.user import User


def get_users(db: Session):
    # 获取所有用户
    return db.query(User).all()


def create_user(db: Session, user: UserCreate):
    # 创建用户
    db_user = User(
        id=user.id,
        username=user.username,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    # 获取单个用户
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    # 用名字获取单个用户
    return db.query(User).filter(User.username == username).first()