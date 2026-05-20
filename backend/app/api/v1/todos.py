from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.crud import crud_todo
from app.models.user import User
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse

router = APIRouter()

@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_user_todo(
    obj_in: TodoCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Create a new private todo linked to the authenticated user.
    """
    return crud_todo.create_todo(db=db, obj_in=obj_in, user_id=current_user.id)

@router.get("", response_model=List[TodoResponse], status_code=status.HTTP_200_OK)
def read_user_todos(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get all private todos belonging to the authenticated user.
    """
    return crud_todo.get_user_todos(db=db, user_id=current_user.id)

@router.put("/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def update_user_todo(
    todo_id: int,
    obj_in: TodoUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Update a private todo owned by the authenticated user.
    """
    todo = crud_todo.get_todo_by_id(db=db, todo_id=todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this todo"
        )
    return crud_todo.update_todo(db=db, db_obj=todo, obj_in=obj_in)

@router.delete("/{todo_id}", status_code=status.HTTP_200_OK)
def delete_user_todo(
    todo_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Delete a private todo owned by the authenticated user.
    """
    todo = crud_todo.get_todo_by_id(db=db, todo_id=todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this todo"
        )
    crud_todo.delete_todo(db=db, db_obj=todo)
    return {"status": "success", "message": "Todo deleted successfully"}
