# Import all models so they are registered on the Base metadata before Alembic imports them.
from app.db.base_class import Base # noqa
from app.models.user import User # noqa
from app.models.todo import Todo, TodoStatus # noqa
from app.models.guest_todo import GuestTodo # noqa
