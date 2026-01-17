from datetime import timedelta, datetime, UTC
from typing import Dict, Any, Optional

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from .config import get_settings


class JWTAuth:
    def __init__(self):
        self.secret_key: str = get_settings().SECRET_KEY
        self.algorithm: str = get_settings().ALGORITHM
        self.access_token_expire_minutes: int = get_settings().ACCESS_TOKEN_EXPIRE_MINUTES
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl=get_settings().TOKEN_URL)

    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=self.access_token_expire_minutes)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload.get("sub") is None:
                raise JWTError("Missing subject")
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )


jwt_auth = JWTAuth()
