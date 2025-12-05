from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, Base
from app.deps.db import get_db
from app.schemas.user import UserCreate, UserResponse
import app.crud.user as crud
from app.deps.cache import get_local_cache
from cachetools import TTLCache
from app.core.logger import logger

router = APIRouter(prefix="/users")
Base.metadata.create_all(bind=engine)


@router.post("/", response_model=UserResponse)
# 创建用户
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    return crud.create_user(db=db, user=user)


@router.get("/", response_model=list[UserResponse])
# 查询所有用户
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db=db)


@router.get("/{user_id}", response_model=UserResponse)
# 查询单个用户
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    cache: TTLCache = Depends(get_local_cache),
):
    key = f"user:{user_id}"
    if key in cache:
        logger.info(f"USER CACHE HIT  user:{user_id}")
        return cache[key]
    logger.info(f"USER CACHE MISS  user:{user_id}")
    db_user = crud.get_user_by_id(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="该用户id不存在")
    cache[key] = db_user
    return db_user
