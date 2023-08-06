from typing import Callable, Dict, Optional
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..exceptions import MissingDependencyError

try:
    import jwt
    from jwt import PyJWTError

    PYJWT_INSTALLED = 1
except ImportError:
    PYJWT_INSTALLED = 0
try:
    from passlib.context import CryptContext

    PASSLIB_INSTALLED = 1
except ImportError:
    PASSLIB_INSTALLED = 0
from pydantic import BaseModel
from starlette.status import HTTP_401_UNAUTHORIZED
from .models import JWTConfig, User


DEFAULT_USERS_DB = {
    "admin": {
        "username": "admin",
        "full_name": "System Administrator",
        "email": "admin@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class UserInDB(User):
    hashed_password: str


def set_oauth2(
    app: FastAPI,
    users_db: Optional[Dict[str, dict]] = None,
    openfaas_enable: bool = False,
    openfaas_function: Optional[str] = None,
) -> Callable:
    """
    Setup oauth2 authentication with password (and hashing).
    Manage bearer with JWT tokens.
    Returns a function that can get current user.
    """
    if PYJWT_INSTALLED == 0:
        raise MissingDependencyError(missing_package="PyJWT", extra="oauth")
    if PASSLIB_INSTALLED == 0:
        raise MissingDependencyError(missing_package="passlib", extra="oauth")
    if users_db is None:
        users_db = DEFAULT_USERS_DB
    if openfaas_enable:
        token_url = f"/function/{openfaas_function}/token"
    else:
        token_url = "/token"
    jwt_config = JWTConfig()

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_url)

    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(password):
        return pwd_context.hash(password)

    def get_user(db, username: str):
        if username in db:
            user_dict = db[username]
            return UserInDB(**user_dict)

    def authenticate_user(fake_db, username: str, password: str):
        user = get_user(fake_db, username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(*, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, jwt_config.secret_key, algorithm=jwt_config.algorithm
        )
        return encoded_jwt

    async def get_current_user(token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, jwt_config.secret_key, algorithms=[jwt_config.algorithm]
            )
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except PyJWTError:
            raise credentials_exception
        user = get_user(users_db, username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    async def get_current_active_user(current_user: User = Depends(get_current_user)):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

    @app.post("/token", response_model=Token)
    async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
        user = authenticate_user(users_db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=jwt_config.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    @app.get("/users/me/", response_model=User)
    async def read_users_me(current_user: User = Depends(get_current_active_user)):
        return current_user

    return get_current_active_user
