from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate

def get_todo_by_id(db: Session, todo_id: int) -> Optional[Todo]:
    return db.query(Todo).filter(Todo.id == todo_id).first()

def get_user_todos(db: Session, user_id: int) -> List[Todo]:
    return db.query(Todo).filter(Todo.user_id == user_id).all()

def create_todo(db: Session, obj_in: TodoCreate, user_id: int) -> Todo:
    db_obj = Todo(
        title=obj_in.title,
        body=obj_in.body,
        user_id=user_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_todo(db: Session, db_obj: Todo, obj_in: TodoUpdate) -> Todo:
    # Use Pydantic v2 model_dump
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_todo(db: Session, db_obj: Todo) -> None:
    db.delete(db_obj)
    db.commit()
