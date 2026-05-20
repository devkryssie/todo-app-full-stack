from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models.todo import TodoStatus

class TodoBase(BaseModel):
    title: str = Field(..., min_length=1)
    body: Optional[str] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    body: Optional[str] = None
    status: Optional[TodoStatus] = None

class TodoResponse(TodoBase):
    id: int
    status: TodoStatus
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
