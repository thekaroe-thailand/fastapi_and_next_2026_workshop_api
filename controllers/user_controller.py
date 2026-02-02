from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
import logging

from database import get_db
from models.User import User
from libs.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/register")
def register(user: dict, db: Session = Depends(get_db)):
    try: 
        db_user = db.query(User).filter(
            (User.email == user["email"]) | (User.username == user["username"])
        ).first()

        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="username or email exists"
            )
        
        hashed_password = get_password_hash(user["password"])
        
        user = User(
            email=user["email"],
            username=user["username"],
            full_name=user["full_name"],
            hashed_password=hashed_password
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
@router.post('/login')
def login(form_data: dict, db: Session = Depends(get_db)):
    try:
        username = form_data.get("username")
        password = form_data.get("password")

        user = db.query(User).filter(User.username == username).first()
        
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authentication": "Bearer"}
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        access_token = create_access_token(
            data={"sub": user.username, "user_id": user.id},
            expire_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "name": user.username,
                "is_admin": user.is_admin
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
@router.get('/profile')
def profile(request: Request, db: Session = Depends(get_db)):
    try:
        auth_header = request.headers.get('Authorization')
        #check_bearer = auth_header.startsWith('Bearer')

        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_AUTHORIZED,
                detail="Invalid authentication credentials"
            )
    
        # Bearer 23rds9f8sduf8asdfjasdjfsdjfklsjdflkjawoefjsdkfsd
        token = auth_header.split(' ')[1]

        from libs.auth import verify_token

        token_data = verify_token(token)

        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        current_user = db.query(User).filter(User.username == token_data.username).first()

        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        return {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "full_name": current_user.full_name
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
