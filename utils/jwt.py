from jose import jwt
from fastapi.security import HTTPBearer

SECRET_KEY = "secretkey"

ALGORITHM = "HS256"

security = HTTPBearer()

def create_access_token(data:dict):

    return jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )