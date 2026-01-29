from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from database import get_db
from models.User import User
import hashlib

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGOLITHM = os.getenv("ALGOLITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    sha = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return pwd_context.hash(sha)




