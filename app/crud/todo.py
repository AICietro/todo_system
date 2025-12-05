from sqlalchemy.orm import Session
from models.todo import Todo
from schemas.todo import TodoCreate


def create_todo(db: Session, todo: TodoCreate, user_id: int):
    # 创建待办事项
    db_todo = Todo(
        id=todo.id,
        title=todo.title,
        user_id=user_id,
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todos(db: Session, user_id: int):
    # 查询待办事项
    return db.query(Todo).filter(Todo.user_id == user_id).all()


def complete_todo(db: Session,todo_id: int):
    # 标记完成待办事项
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo:
        db_todo.completed = True
        db.commit()
        db.refresh(db_todo)
    return db_todo