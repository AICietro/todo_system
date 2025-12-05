from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TodoCreate(BaseModel):
    id: Optional[int] = None
    title: str


class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool
    user_id: int
    created_at: datetime
