from fastapi import APIRouter
from app.api.v1 import auth, todos, guest

api_router = APIRouter()

# Include versioned sub-routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(todos.router, prefix="/todos", tags=["todos"])
api_router.include_router(guest.router, prefix="/guest", tags=["guest"])
