from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class GuestTodoBase(BaseModel):
    title: str = Field(..., min_length=1)
    body: Optional[str] = None

class GuestTodoCreate(GuestTodoBase):
    pass

class GuestTodoResponse(GuestTodoBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
