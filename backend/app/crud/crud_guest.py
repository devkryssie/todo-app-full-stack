from sqlalchemy.orm import Session
from typing import List
from app.models.guest_todo import GuestTodo
from app.schemas.guest_todo import GuestTodoCreate

def get_guest_todos(db: Session) -> List[GuestTodo]:
    return db.query(GuestTodo).all()

def create_guest_todo(db: Session, obj_in: GuestTodoCreate) -> GuestTodo:
    db_obj = GuestTodo(
        title=obj_in.title,
        body=obj_in.body
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
