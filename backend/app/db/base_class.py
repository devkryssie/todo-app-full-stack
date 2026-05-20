from typing import Any
from sqlalchemy.orm import as_declarative, declared_attr

@as_declarative()
class Base:
    id: Any
    __name__: str

    # We will declare __tablename__ explicitly in each model class to be precise,
    # but we can also provide a default helper here.
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
