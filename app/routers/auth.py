from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status
from app.models.user import User
from app.schemas.user import CreateUser
from app.backend.db_depends import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy import select, insert


router = APIRouter(prefix='/auth', tags=['auth'])
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
# SECRET_KEY = "a21679097c1ba42e9bd06eea239cdc5bf19b249e87698625cba5e3572f005544"
# ALGORITHM = 'HS256'

security = HTTPBasic()

@router.post('/') # создание пользователя
async def create_user(db: Annotated[AsyncSession, Depends(get_db)], create_user: CreateUser):
    await db.execute(insert(User).values(username=create_user.username,
                                         hashed_password=bcrypt_context.hash(create_user.password)))
    await db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


async def get_current_username(db: Annotated[AsyncSession, Depends(get_db)], credentials: HTTPBasicCredentials = Depends(security)) -> dict:
    user = await db.scalar(select(User).where(User.username == credentials.username))

    if not user or not bcrypt_context.verify(credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user


@router.get('/users/me')
async def read_current_user(user: dict = Depends(get_current_username)):
    return {'User': user}


# @router.post('/token')
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = await authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail='Could not validate user'
#         )
#     access_token_expires = timedelta(minutes=30)
#     access_token = create_access_token(
#         data={"sub": user.username, "id": user.id},
#         expires_delta=access_token_expires,
#     )
#     return {"access_token": access_token, "token_type": "bearer"}
#
#
# async def authenticate_user(username: str, password: str):
#     async with get_db() as db:
#         user = await db.execute(select(User).where(User.username == username))
#         user = user.scalars().first()
#         if user and bcrypt_context.verify(password, user.hashed_password):
#             return user
#     return None
#
#
# def create_access_token(data: dict, expires_delta: timedelta):
#     expire = datetime.utcnow() + expires_delta
#     data.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
#
#
# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get('sub')
#         user_id: int = payload.get('id')
#         expire = payload.get('exp')
#         if username is None or user_id is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail='Could not validate user'
#             )
#         if expire is None:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="No access token supplied"
#             )
#         if datetime.now() > datetime.fromtimestamp(expire):
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Token expired!"
#             )
#
#         return {
#             'username': username,
#             'id': user_id,
#         }
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail='Could not validate user'
#         )