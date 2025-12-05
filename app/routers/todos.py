from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, Base
from app.deps.db import get_db
from app.schemas.todo import TodoCreate, TodoResponse
import app.crud.todo as crud
from app.core.logger import logger
from app.deps.cache import get_redis
from redis import Redis
import json
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="")

Base.metadata.create_all(bind=engine)


@router.post("/users/{user_id}/todos", response_model=TodoResponse)
# 创建待办事项
def create_todo(
    user_id: int,
    todo: TodoCreate,
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    db_todo = crud.create_todo(db=db, todo=todo, user_id=user_id)
    logger.info(f"user {user_id} 创建待办事项：{db_todo.title}")
    redis.delete(f"todos:user:{user_id}")
    logger.info(f"REDIS CACHE INVALIDATE todos:user:{user_id}")
    return db_todo


@router.get("/users/{user_id}/todos", response_model=list[TodoResponse])
# 查询待办事项
def get_todos(
    user_id: int,
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    key = f"todos:user:{user_id}"
    cached = redis.get(key)
    if cached:
        logger.info(f"REDIS CACHE HIT  todos:user:{user_id}")
        return json.loads(cached)
    logger.info(f"REDIS CACHE MISS  todos:user:{user_id}")
    db_todos = crud.get_todos(db=db, user_id=user_id)
    todos = jsonable_encoder(db_todos)
    redis.setex(key, 60, json.dumps(todos))
    return todos


@router.put("/todos/{todo_id}/complete", response_model=TodoResponse)
# 标记完成待办事项
def complete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    db_todo = crud.complete_todo(db=db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="该待办事项不存在")
    logger.info(f"user {db_todo.user_id} 待办事项：{db_todo.title} 已完成")
    # 清除缓存
    redis.delete(f"todos:user:{db_todo.user_id}")
    logger.info(f"REDIS CACHE INVALIDATE todos:user:{db_todo.user_id}")
    return db_todo
