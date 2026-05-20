from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.crud import crud_guest
from app.schemas.guest_todo import GuestTodoCreate, GuestTodoResponse

router = APIRouter()

@router.post("/todos", response_model=GuestTodoResponse, status_code=status.HTTP_201_CREATED)
def create_public_todo(
    obj_in: GuestTodoCreate,
    db: Session = Depends(deps.get_db)
):
    """
    Create a guest public todo (no authentication needed).
    """
    return crud_guest.create_guest_todo(db=db, obj_in=obj_in)

@router.get("/todos", response_model=List[GuestTodoResponse], status_code=status.HTTP_200_OK)
def read_public_todos(
    db: Session = Depends(deps.get_db)
):
    """
    View all guest public todos.
    """
    return crud_guest.get_guest_todos(db=db)
