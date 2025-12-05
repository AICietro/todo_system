from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    id: Optional[int] = None
    username: str

class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime
