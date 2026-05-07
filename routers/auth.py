from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from jose import jwt

from dependencies import get_db

from models.user import User

from schemas.user import UserCreate

from utils.hashing import (
    hash_password,
    verify_password
)

from utils.jwt import (
    create_access_token,
    security,
    SECRET_KEY,
    ALGORITHM
)

from fastapi.security import (
    HTTPAuthorizationCredentials
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if db_user:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user = User(
        username=user.username,
        hashed_password=hash_password(
            user.password
        ),
        role="user"
    )

    db.add(new_user)

    db.commit()

    return {
        "message":"Registration Successful"
    }

@router.post("/login")
def login(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if not db_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid Username"
        )

    if not verify_password(
        user.password,
        db_user.hashed_password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    access_token = create_access_token(
        {"sub": db_user.username}
    )

    return {
        "message":"Login Successful",
        "access_token":access_token
    }

@router.get("/me")
def get_current_logged_in_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    username = payload.get("sub")

    user = db.query(User).filter(
        User.username == username
    ).first()

    if user.role == "admin":

        return {
            "username": user.username,
            "role":"admin"
        }

    else:

        return {
            "username": user.username,
            "role":"user"
        }