from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.api import deps
from app.crud import crud_user
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.core.security import verify_password, create_access_token

router = APIRouter()

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(obj_in: UserCreate, db: Session = Depends(deps.get_db)):
    """
    Register a new user. Enforces email uniqueness and minimum password length constraints.
    """
    # Prevent duplicate email registration
    existing_user = crud_user.get_user_by_email(db, email=obj_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this email already exists in the system.",
        )
    
    try:
        user = crud_user.create_user(db, obj_in=obj_in)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to register user: {str(e)}"
        )

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login(login_data: UserLogin, db: Session = Depends(deps.get_db)):
    """
    Authenticate user using email and password, returning a JWT access token.
    """
    user = crud_user.get_user_by_email(db, email=login_data.email)
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    access_token = create_access_token(subject=user.email)
    return Token(
        access_token=access_token,
        token_type="bearer"
    )
