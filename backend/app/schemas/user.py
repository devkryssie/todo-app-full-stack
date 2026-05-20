from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
