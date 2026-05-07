from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jose import JWTError, jwt

from sqlalchemy.orm import Session

from database import SessionLocal

import models.user
import utils.jwt

security = HTTPBearer()

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    try:

        payload = jwt.decode(
            token,
            utils.jwt.SECRET_KEY,
            algorithms=[utils.jwt.ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:

            raise credentials_exception

    except JWTError:

        raise credentials_exception

    user = db.query(models.user.User).filter(
        models.user.User.username == username
    ).first()

    if user is None:

        raise credentials_exception

    return user

def admin_required(
    current_user: models.user.User = Depends(get_current_user)
):

    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin privileges required"
        )

    return current_user